from pixget import pix  # type: ignore
import cv2
import os
import sys
from init import write, read, linecount  # type: ignore
from datetime import date
import time
import shutil
from stopwatch import Stopwatch # type: ignore
from stringcolor import cs # type: ignore
today = date.today()
recordate = today.strftime("%b-%recordate-%Y")
resetswitch = 0 
load = 0
count = 0
framefail = 0
state = 1
frames = 0
framez = []
video = sys.argv[1]
v2 = sys.argv[2]
offline = False
channelname = v2.partition('.tv/')[2]
if not channelname:
        print("EROR INVALID TWITCH LINK")
        print(cs('WARNING: ARG2 will now be interpreted as out folder name.', '#F93148'))
        offline = True
        print(video.partition('youtube.com/')[1])
        if not video.partition('youtube.com/')[1]:
            print("")
            print(cs('WARNING: OFFLINE VIDEO MODE. WILL END AT THE END OF PLAYBACK OF A GIVEN VIDEO FILE', '#F93148'))
            youlist = False
else:        
    channelname = channelname.partition('/')[0]

#does link checking and pratitions it
#print(channelname)
channelname = f'streamers/{channelname}'
def convertdate(video):   
    monthconv = {'01': "Jan", '02': 'Feb', '03': 'Mar', '04': 'Apr', 
    '05': 'Jun', '06': 'Jun', '07': 'Jul', '08': 'Aug', '09': 'Sep',
    '10': 'Oct', '11': 'Nov', '12': 'Dec'}
    temp = video.partition('.')[0].partition('/')[2]
    year = temp[:-4]
    month = (monthconv[temp[-4:][:-2]])
    day = temp[-2:]
    recordate = (f'{month}-{day}-{year}') 
    return recordate
if offline:
    import subprocess
    if os.path.exists('vodtemp') == False:
        os.mkdir('vodtemp')
#    else:
   #     shutil.rmtree('vodtemp')
   #     os.mkdir('vodtemp')
    p = subprocess.Popen(['youtube-dl', '-f', '134', video,
                      '-o', 'vodtemp/%(upload_date)s.%(ext)s'])
    p.wait()
    if p.returncode != 0:
        exit(cs(f'ERROR DOWNLOADING: {video}.\nexiting...', '#F93148'))
    #defines youlist --- which is used to select videos to playback
    #if its not a video list, its just one and does not loop.
    if video.partition('list')[1]:
        incr = 0
        youlist = os.listdir("vodtemp")
        video = f'vodtemp/{youlist[0]}'
        print(len(youlist))
        recordate = convertdate(video)
    else:
        video = f'vodtemp/{os.listdir("vodtemp")[0]}'  
        youlist = False
        recordate = convertdate(video)



while True:
    #Allows for the recapture of video to reduce delay.
    if resetswitch != 1:
        print('capture!\n')
        cap = cv2.VideoCapture(video)
        resetswitch = 1
        fps = cap.get(cv2.CAP_PROP_FPS)
        print(youlist)
        #is a reset switched used to recapture twitch streams to reduce latency.
    succ, frame = cap.read()
    #if it fails to load it increments the fail. And if it fails too many time it exists 
    if not succ:
        framefail += 1
    if framefail >= 20:
        if youlist == False:
            exit('File is probably over')
        else:
            if youlist:
                if incr+1 == len(youlist):
                    exit('file over!')
            incr += 1   
            framefail = 0 
            resetswitch = 0       
            frames = 0
            framez = []
            video = f'vodtemp/{youlist[incr]}'            
            recordate = convertdate(video)

    #if it sucessfully reads the frame...        
    if succ:
        frames = sum([frames, 1])
        #if framefail isn't falsy reset the count.
        if framefail:
            framefail = 0
        if state == -1:
            if count < 110:
                count += 1
                print(count)
                continue
            else:
                cv2.imwrite('temp/temp.jpg', frame)
                os.system('jp2a --colors --fill temp/temp.jpg')
                state = 2
                count = 0
#     #Writes temp.jpg, which will be used to generate meta data
        #resets to 1 if -2 is returned count > x times.
        #used to parse false positives
        if state == -2:
            count+=1
            print(f'    {count}', end='\r')
            state = 2
            try:            
                os.makedirs('temp/')
            except FileExistsError:
                pass
            if count < 100:
                cv2.imwrite(f'temp/temp{count}.jpg', frame)
            #this is a timeout gate, if go does not happen in 1300 frames or
            #~a minute, ir will cancel out and not write anything 
            #longer ones are more dangerous, but with better go protections i decided to boost
            #from 900 to 1300
            if count > 1300:
                state = 1
                count = 0
                cv2.imwrite(f'temp/tempx.jpg', frame)
                os.system('jp2a temp/tempx.jpg --colors -fill')
                shutil.rmtree('temp')
                print('GO TIMEOUT, RETURN TO MONKE')
        #creates a file structure for data if the race start is detected
        # channelname/date/number of files in dir           
        if state == -3:
            if count <= 90:
                count += 1
                continue
            print('go detected, doin stuff')
            if os.path.exists(f'{channelname}/{recordate}/') == False:
                os.makedirs(f'{channelname}/{recordate}/')
            number = len(os.listdir(f'{channelname}/{recordate}/'))
            dir = f'{channelname}/{recordate}/{number}/'
            write("", 0, f'{dir}meta.txt')
            shutil.move('temp', dir)
            os.makedirs('temp')
            print("g")
            count = 0
            if not offline:
                stopwatchx = Stopwatch()
            else:
                framez.append(frames)
            state = 3
        if state == 3: 
            cv2.imwrite(f'{dir}noprocess{count}.jpg', frame)
            print(f'                                  {dir}/noprocess{count}', end='\r')
            count += 1
            if count >= 5000:
                shutil.rmtree(dir)
                state = 1
                count = 0
        if state == 4:
            state = 1
            count = 0
            todo = linecount('todo.txt')
            write(f'{channelname}/{recordate}/{number}/', todo, 'todo.txt')                
            if not offline:
                #does an offline check
                write(str(stopwatchx.stop()), 3, f'{dir}meta.txt')
                resetswitch = 0 
                continue
            else:
                framez.append(frames)
                print(framez)
                stoptime = (framez[1] - framez[0])
                stoptime = f'{float(stoptime/30)}s'
                write(stoptime, 3, f'{dir}meta.txt')
                write(video, 4, f'{dir}meta.txt')
                framez = []
        #check if 
        #attempts to gate out false positives with -5
        #it will wait 25 frames, and if it is still reading loading, it will actually  register loading load
        if state == -5:
            if count < 25:
                count += 1
                continue
            else:
                state = -5
                count = 0
        state = pix(frame, int(state))
        print(str(state)+' '+video+f' {framefail}', end = '\r')
