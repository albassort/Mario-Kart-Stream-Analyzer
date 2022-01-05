from pixget import pix 
import cv2
import os
import sys
from readwrite import write 
import time
import shutil
from compile import compile
from multiprocessing import Process
from stringcolor import cs 
from pytube import YouTube, Playlist
import datetime

total = 0
date = str(datetime.datetime.now()).split(" ")[0]
resetswitch = False
load = 0
count = 0
framefail = 0
state = 1
frames = 0
arg1 = sys.argv[1]
youtube = False
channel = None

help = "Argument 1: Should be a valid youtube URL. If you wish to capture a twitch stream use ./streamget.sh, arg1 should be https://twitch.tv/channelname"

threads = []
#twitch shouldn't be passed into arg1
if "twitch.tv/" in arg1:
    print(help)
    exit()
elif "youtube.com/" in arg1:
    #hopefully a big improvement over the bash code of beforetimes.
    youtube = True
    if "&list" in arg1:
        for video in Playlist(arg1):
            individual = YouTube(video)
            try:
                individual.streams.get_by_itag(134).download("vodtemp/", f'{str(video.author)}\{str(video.publish_date).split(" ")[0]}\{total}')
            except:
                exit(f'{individual.title} cannot be downloaded. Be sure that all videos can be downloaded at 360p')
        total+=1
    else:
        video = YouTube(arg1)
        try:
            video.streams.get_by_itag(134).download("vodtemp/", f'{str(video.author)}\{str(video.publish_date).split(" ")[0]}')
        except:
            exit(f'{video.title} cannot be downloaded. Be sure that all videos can be downloaded at 360p')
else:
    arg2 = sys.argv[2]
    twichsplit = arg2.split("/")
    if twichsplit[1] == "popout":
        channel = twichsplit[2]
    else:   
        channel = twichsplit[1]
    if not channel:
        print(help)
        exit()
#a custom generator to make code better.
def returnCaptures(youtube : bool):
    files = None
    if youtube:
        files = os.listdir("vodtemp/")
                            #actually just 1 \
        files = list(map(lambda file: (f'vodtemp/{file}', file.split("\\")), files))
        #returns a tuple of the file path, and its publisher, release date, and write order
        #cast to list because it returns a (data array)? otherwise its unreadable.
    else:
        yield (arg1, channel, date)
        return
    for file in files:  
        yield (file[0], file[1][0], file[1][1])
    return

def process(img): 
    #saves time by manipulating less data.
    img = img[280:360, 530:640]
    #we crop, then convert the input to a black and white image, then convert it to a binary
    bw = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    processed = cv2.threshold(bw, 140, 255, cv2.THRESH_BINARY)[1]
    return processed

def getOutDir(channel, date):
    #this just looks better than f strings for paths.
    baseout = "archive/"+channel+"/"+date
    total = "0"
    if os.path.isdir(baseout):
        total = str(len(os.listdir(baseout)))
    else:
        os.makedirs(baseout)
    #ordered like this
    #archive=>channel=>date=>total amount of games
    #ie. archive/joel/2020-25-8/0
    return baseout+"/"+total+"/"
for video, channel, date in returnCaptures(youtube):
    #Allows for the recapture of video to reduce delay.
    outdir = None
    reading = True
    resetswitch = True
    outStream = None
    while reading:
        if resetswitch:
            print('capture!\n')
            print(video)
            cap = cv2.VideoCapture(video)
            resetswitch = False
            fps = cap.get(cv2.CAP_PROP_FPS)
            if fps != 30:
                print("ONLY 30FPS FOOTAGE IS ALLOWED")
                reading = False
        captured, frame = cap.read()
        if not captured:
            reading = False
            break
        #attempts to gate out false positives
        #it will wait 25 frames, and if it is still reading loading, it will actually  register loading load
        if state == -5:
            if count < 25:
                count += 1
                continue
            else:
                state = -5
                count = 0
        #on detection of a newly black screen
        if state == -1:
            #clears count from other uses of the var.
            if count > 200:
                count = 0
            #skips 110 frames.
            if count < 110:
                count += 1
                continue
            else:
                #this is the outstream, where all frames will be written to.
                #(outpath, fourcc, fps, (width, height))
                #written in avi because it honestly doesn't matter.
                outdir = getOutDir(channel, date)
                outStream = cv2.VideoWriter("video.avi", cv2.VideoWriter_fourcc(*'DIVX'), 200, (110, 80), 0)
                cv2.imwrite("players.jpg", frame)
                state = 2
                count = 0
                
        if state == -2:
            count+=1
            state = 2
            #this is a timeout gate, if go does not happen in 1300 frames or
            #~a minute, it will cancel out and not write anything 
            #longer ones are more dangerous, but with better go protections i decided to boost
            #from 900 to 1300
            if count > 1300:
                state = 1
                count = 0

        #happens when a race first starts. Basically useless after this was reprogrammed
        if state == -3:
            state = 3

        #happens for every frame that a race is in progress
        if state == 3: 
            outStream.write(process(frame))
            count += 1
            print(f'{outdir}, {count} frames', end='\r')

            #this is a timeout. If a race is longer than 5400 frames, exit.
            if count >= 5400:
                state = 1

        #upon reading the end.
        #writes out the video and moves players.jpg to the outdir.
        if state == 4:
            state = 1
            outStream.release()
            #weeds out any unsuccessful readings issue-thingies.
            os.makedirs(outdir)
            shutil.move("players.jpg", outdir)
            shutil.move("video.avi", outdir)
            #this adds a compile and then starts it.
            #we add it encase the application exists before the last 1 or 2 finish.
            threads.append(Process(target=compile, args=(outdir,)))
            threads[-1].start()
            print('\n')

            if not youtube: resetswitch = True        
        state = pix(frame, state)

#cleanup
shutil.rmtree("vodtemp")
#NO COMPILE LEFT BEHIND!
for compile in threads:
    compile.join()