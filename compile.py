import cv2
import numpy as np
import pickle
from PIL import Image
from readwrite import write, ocr_core, writelist
from pixget import getplayers
import os 
from multiprocessing import Queue, Process
import itertools
from thefuzz import fuzz
def similar(a,b):
    return (fuzz.ratio(a,b))

def processframes(frames, referenceCoords,  Q):
    for image, count in frames:
        correct = []
        #this is a dictonary. So it goes 0 12
        for rank in referenceCoords:
            holder = []
            #for each identifiying coordinates of each number
            for coords in referenceCoords[rank]:
                #it is a binary image, but cv2 treats it as a typical 3 per pixel byte-video.
                #each byte is the same so 0 == 1 and 1 == 2.
                color = image[coords]
                if color[0] == 0:
                    holder.append(0)
                if color[0] == 255:
                    holder.append(1)
            #counts the whites, or the "incorrect" colors.
            #adds its rank and the count, ie [(1, 0), (2, 692), (3, 700)...]
            correct.append((rank, holder.count(0)))
        correct.sort(key=lambda x: x[1])
        Q.put_nowait((correct, count))
    return 
def chunkStr(a,b):
    return [a[i:i+b] for i in range(0, len(a), b)]

def compile(dir):
    frames = []
    #reads the video
    cap = cv2.VideoCapture(dir+"/"+"video.avi")
    framecount = 0
    while True:
        captured, frame = cap.read()
        if not captured:
            break
        #loads each frame into a pixelaccses list.
        frames.append((Image.fromarray(frame).load(), framecount,))
        framecount+=1
    with open('id/uni.p', 'rb') as pickle_file:
        referenceCoords = pickle.load(pickle_file)
    
    #we split the frames into an array of 8 parts, to make threading actually function
    splitframes = np.array_split(frames, 8)
    threads = []
    totalframes = []
    #Queues are python channels. They work fine.
    Q = Queue()
    for x in splitframes:
        threads.append(Process(target=processframes, args=(x, referenceCoords, Q)))
    for x in threads:
        x.start()
    #You might think "WHAT THE HELL DOES SHE NOT KNOW .JOIN() exists"
    #Well, I do. However, python refuses to return the function out of pure spite and pasta code
    #this is a temporary... maybe permanent workaround.
    while len(totalframes) != len(frames):
        try:
            totalframes.append(Q.get())
        except:
            continue
    #paranoid memory management.
    del frames
    #we provide each frame with an order identifier. This prevents race conditions
    totalframes.sort(key=lambda x: x[1]) 
    #its useless in later code so we just purge it
    totalframes = list(map(lambda x: (x[0]), totalframes))

    output = []
    last = -1

    #you might be wondering why im not just dumping the digits in an array like before
    #this allows me to identify the size of groups of digits without keeping two lists
    #you might ask why i dont just keep a un-roll backed list and just go without the padding 
    #to you, I say shush. It calculates better (if a tad less accurate) this way and looks better on graphs.
    for framedata in totalframes:
        #if the image is all white or all black
            if framedata[0][1] == framedata[1][1]:
                if last == -1:
                    continue
                else:
                    output[-1][1]+=1
                    continue
        #if the image isn't greater than 40 wrong
            if framedata[0][1] > 40:
                if last == -1:
                    continue
                else:
                    output[-1][1]+=1
                    continue
        #if the second most likely is within 20 of the first
            if framedata[1][1] - framedata[0][1] < 20:
                if last == -1:
                    continue
                else:
                    output[-1][1]+=1
                    continue
        #1 is the most ambigious. If the answer is 1 and its not CERTAIN its 1, we skip
            if framedata[0][0] == 1 and framedata[0][1] >= 20:
                if last == -1:
                    continue
                else:
                    output[-1][1]+=1
                    continue
            if last == -1:
                last = framedata[0][0]
                output.append([framedata[0][0], 1])
                continue
            
            last = framedata[0][1]
            #if it passes the gauntlent
            if last == output[-1][0]:
                output[-1][1]+=1
                continue
            output.append([framedata[0][0], 1])
    #alright this is a doozy. First we filter out any outputs which have less than 10
    output = list(filter(lambda x:x[1] > 12, output))
    #we convert [1, 2] => 11, we then chunk it by the size of the origin [1,2]=>"11"=>["1","1"]
    #this preserves double digits, [10, 2] => "1010" => ["10","10"]
    def unpack(input):
        return chunkStr(str(input[0])*input[1], len(str(input[0])))
    #we convert output to a list of unpacked, then flatten it with itertools.chain.
    output = ([*itertools.chain(*[*map(lambda x: unpack(x), output)])])
    #we convert it to ints so it can be evaluated.
    output = [*map(lambda x: int(x), output)]
    #HAND WRITTEN LIST OF ALL COURSES!
    #OCR Isn't magic, but there is a finate amount of possibilities, so I decided to do this so that any mutations on a name could be caught
    #and not become separate instances that need manual correction
    courses = ["Mario Kart Stadium", "Water Park", "Sweet Sweet Canyon", "Thwomp Ruins", "Mario Circuit", "Toad Harbor", 
                "Twisted Mansion", "Shy Guy Falls", "Sunshine Airport", "Dolphin Shoals", "Mount Wario",
                "Cloudtop Cruise", "Bone Dry Dunes", "Bowser's Castle", "Rainbow Road", "Moo Moo Meadows", "GBA Mario Circuit",
                "Cheap Cheap Beach", "Toad's Turnpike", "Dry Dry Desert", "Donut Plains 3", "Royal Raceway", "DK Jungle",
                "Wario Stadium", "Sherbert Land", "Music Park", "Yoshi Valley", "Tick-Tock Clock", "Piranha Plant Slide", 
                "Grumble Volcano", "N64 Rainbow Road", "Yoshi Circuit", "Excitebike", "Dragon Driftway", "Mute City",
                "Wario's Gold Mine", "SNES Rainbow Road", "Ice Ice Outpost", "Hyrule Castle", "Baby Park",
                "Cheese Land", "Wild Wood", "Animal Crossing", "Neo Bowser City", "Ribbon Road", "Super Bell Subway", "Big Blue"]
    #So I feel the need to defend myself here.
    #Normally I dont 'like to include extra dependencies, but I didn't want to copy pasta 
    #someone's dice coefficient and this depnd is very small
    close = []
    players = cv2.imread(dir+"/players.jpg")
    ocr = ocr_core(players)
    #We make an index of which course is closest to the ocr output
    for course in courses:
        close.append((course, similar(ocr,course)))
    #We sort, which default returns the lowest number
    close.sort(key=lambda x: x[1])
    #so we grab the last index which is the highest number; the most similar.
    course = close[-1][0]
    
    writelist(output, f"{dir}/rank.txt")
    write(course, 0, f"{dir}/meta.txt")
    write(getplayers(players), 1,f"{dir}/meta.txt")
    write(output[-1], 2, f"{dir}/meta.txt")
    f = float(sum(output)/len(output))
    write(f, 3, f"{dir}/meta.txt")
    write(min(output), 4, f"{dir}/meta.txt")
    write(max(output), 5, f'{dir}/meta.txt')
    write(len(framedata)/30, 6, f'{dir}/meta.txt')