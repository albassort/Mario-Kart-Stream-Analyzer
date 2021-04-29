from pixget import pix  # type: ignore
import cv2
import os
import sys
from init import write, read, linecount  # type: ignore
from datetime import date
import time
import shutil
from stopwatch import Stopwatch
from stringcolor import cs
today = date.today()
d = today.strftime("%b-%d-%Y")
z = 0
load = 0
count = 0
succcount = 0
v = sys.argv[1]
v2 = sys.argv[2]
cn = v2.partition('.tv/')[2]
if not cn:
        print("EROR INVALID TWITCH LINK")
        print(cs('WARNING: ARG2 will now be interpreted as out folder name.', '#F93148'))
        cn = v2
else:        
    cn = cn.partition('/')[0]

try:
    v3 = sys.argv[3]
except:
    v3 = True
try:
    v4 = sys.argv[4]
except:
    v4 = None
print(v4)
state = 1
frames = 0
framez =[]
youlist = False
#does link checking and pratitions it
#print(cn)
def convertdate(v):   
    monthconv = {'01': "Jan", '02': 'Feb', '03': 'Mar', '04': 'Apr', 
    '05': 'Jun', '06': 'Jun', '07': 'Jul', '08': 'Aug', '09': 'Sep',
    '10': 'Oct', '11': 'Nov', '12': 'Dec'}
    temp = v.partition('.')[0].partition('/')[2]
    year = temp[:-4]
    month = (monthconv[temp[-4:][:-2]])
    day = temp[-2:]
    d = (f'{month}-{day}-{year}') 
    return d
if v3 != 'offline' or v3 == None:
    import subprocess
    if os.path.exists('vodtemp') == False:
        os.mkdir('vodtemp')
#    else:
   #     shutil.rmtree('vodtemp')
   #     os.mkdir('vodtemp')
    p = subprocess.Popen(['youtube-dl', '-f', '243', v3,
                      '-o', 'vodtemp/%(upload_date)s.%(ext)s'])
    p.wait()
    if v3.partition('list')[1]:
        incr = 0
        youlist = os.listdir("vodtemp")
        v = f'vodtemp/{youlist[0]}'
        print(len(youlist))
        d = convertdate(v)
    else:
        v = f'vodtemp/{os.listdir("vodtemp")[0]}'  
        youlist = False
        d = convertdate(v)
    v4 = 'video'

while True:
    #Allows for the recapture of video to reduce delay.
    if z != 1:
        print('capture!\n')
        cap = cv2.VideoCapture(v)
        z = 1
        fps = cap.get(cv2.CAP_PROP_FPS)
        print(youlist)
    succ, frame = cap.read()
    if not succ:
        load = 0
        succcount += 1
    if succcount >= 20:
        if youlist == False:
            exit('File is probably over')
        else:
            if incr+1 == len(youlist):
                exit('file over!')
            incr += 1   
            succcount = 0 
            z = 0       
            frames = 0
            framez = []
            v = f'vodtemp/{youlist[incr]}'            
            d = convertdate(v)
    if succ:
        frames = sum([frames, 1])
        if load == 0:
            succcount = 0
            load = 1
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
            if os.path.exists(f'{cn}/{d}/') == False:
                os.makedirs(f'{cn}/{d}/')
            number = len(os.listdir(f'{cn}/{d}/'))
            dir = f'{cn}/{d}/{number}/'
            write("", 0, f'{dir}meta.txt')
            shutil.move('temp', dir)
            os.makedirs('temp')
            print("g")
            count = 0
            if v4 != 'video':
                stopwatchx = Stopwatch()
            else:
                framez.append(frames)
            state = 3
        if state == 4:
            state = 1
            count = 0
            todo = linecount('todo.txt')
            write(f'{cn}/{d}/{number}/', todo, 'todo.txt')                
            if v4 != 'video':
                write(str(stopwatchx.stop()), 3, f'{dir}meta.txt')
                time.sleep(5)
                z =0 
                continue
            else:
                framez.append(frames)
                print(framez)
                stoptime = (framez[1] - framez[0])
                stoptime = f'{float(stoptime/30)}s'
                write(stoptime, 3, f'{dir}meta.txt')
                write(v, 4, f'{dir}meta.txt')
                framez = []
        if state == 3:
            cv2.imwrite(f'{dir}noprocess{count}.jpg', frame)
            print(f'                        {dir}/noprocess{count}', end='\r')
            count += 1
            if count >= 5400:
                shutil.rmtree(dir)
                state = 1
                count = 0
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
        print(str(state)+' '+v, end = '\r')
