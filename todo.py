from init import read, write, linecount, ocr_core, readall, writelist # type: ignore
import os
import sys
import time
from pixget import getplayers  # type: ignore
from multiprocessing import Process
from stopwatch import Stopwatch as stopwatch
import cv2
from PIL import Image
import shutil
import subprocess
from asciidetection import gen, asciimain  # type: ignore


def penme(todo, pindex):
    v1 = len(os.listdir(todo))-4
    v1 = (int(v1/4), int(v1) % 4)
    holder = False
    #counts the amount of files in todo and creates 1/4 slices for
    state = []
    if pindex != 0:
        #detects if the images are already genered
        for x in range(0, int(pindex)):
            #reads ID from all of processed/
            if not os.path.exists(f"processed/{x}/id.txt"):
                shutil.rmtree(f"processed/{x}")
                pindex = x
                break
            match = read(0, f'processed/{x}/id.txt')
            if match == todo:
                state.append(1)
                break
            else:
                state.append(0)
    else:
        state.append(0)
    if state[-1] == 0:
        #ugly ugly subprocess code
        os.makedirs(f'{processedir}/rank')
        #does some basic math to allocate the 4 subprocess range
        #to perfectly split up 'todo ls \ wc -l'


        p = subprocess.Popen(['bash', 'ascii.sh', 'convert',
                          str(1), str(v1[0]), todo, str(pindex), str(1)])

        p1 = subprocess.Popen(['bash', 'ascii.sh', 'convert', 
         str(v1[0]), str(v1[0]*2), todo, str(pindex), str(2)])

        p2 = subprocess.Popen(['bash', 'ascii.sh', 'convert',  str(
            v1[0]*2), str(v1[0]*3), todo, str(pindex), str(3)])
            
        p3 = subprocess.Popen(['bash', 'ascii.sh', 'convert',  str(
            v1[0]*3), str((v1[0]*4)+v1[1]), todo, str(pindex), str(4)])
            
        p1.wait(); p2.wait(); p3.wait(); p.wait()

        #Converts images to binary black and white images

        for x in range(1, (v1[0]*3+sum(v1))):
            if os.path.exists(f'{processedir}/rank/rank{x}.jpg') == False:
                continue
            img = cv2.imread(f'{processedir}/rank/rank{x}.jpg', 2)

            #magic numbers. 140 is arbitrary but functional :)

            ret, bw_img = cv2.threshold(img, 140, 255, cv2.THRESH_BINARY)
            im = Image.fromarray(bw_img)
            
            #saves the 
            
            im.save(f'{processedir}/binrank{x}.jpg')

        shutil.rmtree(f'{processedir}/rank/')
        #writes todo, to id, to complete the loop :)
        write(todo, 0, f'{processedir}/id.txt')
        print('beep')
    
    #generates ascii rank-detection.
    
    os.makedirs(f'{exdir}/html')
    gen('gen', exdir, f'{processedir}')
    asciimain(exdir)

def writedata():
    subprocess.Popen(
        ['convert', f'{todo}/temp/temp50.jpg', '-crop', '640x360+210+315', '-crop', '-200-20', '-type', 'Grayscale', '-sharpen', '0x12', f'{exdir}/boop.jpg']).wait()
    abonrormalmaps = {"mount wario" : 1, "n64 rainbow road" : 1, "big blue" : 1, "baby park" : 7 }
    timze = read(3, f'{todo}/meta.txt')[:-1]
    bet1 = read(0, meta)
    bet2 = read(1, f'{todo}/meta.txt')
    players = getplayers(f'{exdir}/temp50.jpg')
    #so it turns out, i moved all of the rank functions to bedone in ascii main to keep everything concise and reduce serialization/
    #having to do stupid return things. ALl of the rank writing is done in ascii main, so if you're looking for that
    #please go there
    write(players, 1, meta)
    write(f'{timze} seconds', 6, meta)
    #gets averege lap given 3 laps.
    #replacing with fuzzy search dictonaries with a list of Mario Kart 8... dunno if i should 
    #write the fuzzy myself or use a library. probably writing myself tbh
    write(f'{float(timze)/3} seconds', 7, meta)
    write(bet1, 8, meta)
    write(bet2, 9, meta)
    write(todo, 10, meta)
    write(f'{processedir}', 11, meta)
    ai = ocr_core(f'{exdir}/boop.jpg')
    if ai in abonrormalmaps:
        write(f'{float(timze)/abonrormalmaps[ai]} seconds', 7, meta)
    write(ai, 0, meta)
    with open(f'{todo}/done.loc', 'w') as temp:
        temp.close


for folder in os.listdir("streamers/"):
    for subfolder in os.listdir(f'streamers/{folder}'):
        if subfolder.partition("out")[1]:
            continue

        for todo in os.listdir(f'streamers/{folder}/{subfolder}'):
            if subfolder.partition("out")[1]:
                continue

            outfol = f'streamers/{folder}/'
            todo = f'streamers/{folder}/{subfolder}/{todo}'
            if not os.path.exists(f'{outfol}/out/'):
                os.makedirs(f'{outfol}/out/')
            if os.path.exists(f'{todo}/done.loc'):
                continue
            if os.path.exists("processed/") == False:
                os.mkdir('processed/')  
            if not os.path.exists(f"{outfol}out/"):
                os.makedirs(f"{outfol}out/")
            pindex = len(os.listdir('processed/'))
            timer = stopwatch()
            print(todo)
            exdir = (f'{outfol}out/{len(os.listdir(f"{outfol}out/"))}')
            processedir = f"processed/{pindex}"    
            os.mkdir(exdir)
            shutil.copy(f'{todo}/temp/temp50.jpg', exdir)
            meta = f'{exdir}/meta.txt'
            penme(todo, pindex)
            writedata()
            timer.stop
            print(timer)
#line 1 = Stage
# 2 = players
# 3 = final rank entry
#4 = averege rank
#5 = lowest place
#6 = highest place
#7 = total time
#8 given 3 laps, averege per lap
#9 starting bet scrape
#10 ending bet scrape
#11 path generated from
#12 imagepath
