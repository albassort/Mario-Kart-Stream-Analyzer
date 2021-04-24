from init import read, write, linecount, ocr_core  # type: ignore
import os
import sys
import time
from pixget import getplayers  # type: ignore
from multiprocessing import Process
from stopwatch import Stopwatch
import cv2
from PIL import Image
import shutil
import subprocess
from asciidetection import gen, asciimain  # type: ignore
def penme(todo):
    print('testt')
    cc = []
    v1 = len(os.listdir(todo))-2
    v1 = (int(v1/4), int(v1)%4)
    #counts the amount of files in todo and creates 1/4 slices for
    state = []
    if v != 0:
        print('test')
        #detects if the images are already genered
        for x in range(0, int(v)):
            #reads ID from all of processed/
            match = read(0, f'processed/{x}/id.txt')
            if match == "File or line doesn't exist":
            #if an error occurs, we delete it
                shutil.rmtree(f'processed/{x}')
            if match == todo:
                state.append(1)
                match = x
                break
            else:
                state.append(0)
        print(state)
        print(x)
    if state[-1] == 0:
        #ugly ugly subprocess code
        print(state[-1])
        os.makedirs(f'processed/{v}/rank')
        #does some basic math to allocate the 4 subprocess range
        #to perfectly split up 'todo ls \ wc -l'
        subprocess.Popen(['bash', 'ascii.sh', 'convert',  str(1), str(v1[0]), todo, str(v), str(1)])
        subprocess.Popen(['bash', 'ascii.sh', 'convert',  str(v1[0]), str(v1[0]*2), todo, str(v), str(2)])
        subprocess.Popen(['bash', 'ascii.sh', 'convert',  str(v1[0]*2), str(v1[0]*3), todo, str(v), str(3)])
        subprocess.Popen(['bash', 'ascii.sh', 'convert',  str(v1[0]*3), str((v1[0]*4)+v1[1]), todo, str(v), str(4)])
        x = len(cc)
        time.sleep(1)
        #the weird check for completion of subprocess.
        #reads cache.txt and awaits for the day that the subprocces's are finished.
        while len(cc) != 4:
            for x in range(1, 4):
                time.sleep(1)
                #stop the read from breaking my disk's iowait lol.
                cc1 = read(x, 'cache.txt')
                if cc1 != "1":
                    continue
                else:
                    cc.append(1)
        #Converts images to binary black and white images
        for x in range(1, (v1[0]*3+sum(v1))):
            print(x)
            if os.path.exists(f'processed/{v}/rank/rank{x}.jpg') == False:
                print('error')
                continue
            img = cv2.imread(f'processed/{v}/rank/rank{x}.jpg', 2)
                #magic numbers. First ones i tried, that just kinda work
            ret, bw_img = cv2.threshold(img, 140, 255, cv2.THRESH_BINARY)
            im = Image.fromarray(bw_img)
            #saves the image
            im.save(f'processed/{v}/binrank{x}.jpg')
        shutil.rmtree(f'processed/{v}/rank/')
        #writes todo, to id, to complete the loop :)
        write(todo, 0, f'processed/{v}/id.txt')
        print('beep')
    #generates ascii rank-detection.
  #  writelist(os.listdir(f'processed/{v}/id'), 0, f'{exdir}/source.txt')
    gen('regen', exdir)
    asciimain(exdir)

count = linecount('todo.txt')
for xz in range(0, count):
    todo = read(xz, 'todo.txt')
    if os.path.exists("processed/") == False:
        os.mkdir('processed/')
    v = len(os.listdir('processed/'))
    #filters out done todos.
    #uses quit for specific processing
    if todo.partition(',')[0] == 'done':
        continue
    elif todo == 'quit':
        quit()
    else:
        if os.path.exists(f'{todo}/temp/temp50.jpg') == False:
            write(f'done, {todo}//ERROR MISSING temp50.jpg', xz, 'todo.txt')
            print('ERROR MISSING TEMP50')
            continue
        #this is pretty self explanitory
        #this just takes stuff from around the files and gleans all the data it can from it
        channel = todo.partition('/')[0]
        z = len(os.listdir(f'{channel}/out'))
        exdir = f'{channel}/out/{z}'
        print('test pp')
        penme(todo)
        subprocess.Popen(
            ['convert', f'{todo}/temp/temp50.jpg', '-crop 640x360+210+315', '-crop', '-200-20', '-type Grayscale', '-sharpen 0x12', f'{exdir}/boop.jpg'])

        shutil.move(f'  {todo}/temp/temp50.jpg', exdir)
        ai = ocr_core(f'{exdir}/boop.jpg')
        print(ai)
        write(ai, 0, f'{exdir}/meta.txt')
        players = getplayers(f'{todo}/temp/temp50.jpg')
        write(players, 1, f'{exdir}/meta.txt')
        zf = linecount(f'{exdir}/rank.txt')
        finalrank = read(int(zf-1), f'{exdir}/rank.txt')
        avg = []
        timze = read(3, f'{todo}/meta.txt')[:-1]
        write(f'{timze}s', 6, f'{exdir}/meta.txt')
        try: 
            write(f'{float(timze)/3}s', 7, f'{exdir}/meta.txt')
        except:
            write('some really stupid shit bug happened', 7, f'{exdir}/meta.txt')
        bet1=read(0, f'{todo}/meta.txt')
        bet2=read(1, f'{todo}/meta.txt')
        write(bet1, 8, f'{exdir}/meta.txt')
        write(bet2, 9, f'{exdir}/meta.txt')
        write(todo, 10, f'{exdir}/meta.txt')
        write(f'processed/{v}', 11, f'{exdir}/meta.txt')
        time.sleep(1)
        write(f'done, {todo}', xz, 'todo.txt')
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
