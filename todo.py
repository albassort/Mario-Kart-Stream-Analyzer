from init import read, write, linecount, ocr_core, writelist  # type: ignore
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


def penme(todo):
    print('testt')
    cc = []
    v1 = len(os.listdir(todo))-3
    v1 = (int(v1/4), int(v1) % 4)
    #counts the amount of files in todo and creates 1/4 slices for
    state = []
    print(v)
    if v != 0:
        print('test')
        #detects if the images are already genered
        for x in range(0, int(v)):
            #reads ID from all of processed/
            match = read(0, f'processed/{x}/id.txt')
            if match == todo:
                state.append(1)
                globals()['v'] = x
                break
            else:
                state.append(0)
        print(state)
        print(x)
    else:
        state.append(0)
    if state[-1] == 0:
        #ugly ugly subprocess code
        print(state[-1])
        os.makedirs(f'processed/{v}/rank')
        if os.path.exists('cache.txt') == False:
            with open('cache.txt', 'w') as temp:
                temp.close
            write("0", 3, 'cache.txt')
        #does some basic math to allocate the 4 subprocess range
        #to perfectly split up 'todo ls \ wc -l'
        p = subprocess.Popen(['bash', 'ascii.sh', 'convert',
                          str(1), str(v1[0]), todo, str(v), str(1)])
        p1 = subprocess.Popen(['bash', 'ascii.sh', 'convert',  str(
            v1[0]), str(v1[0]*2), todo, str(v), str(2)])
        p2 = subprocess.Popen(['bash', 'ascii.sh', 'convert',  str(
            v1[0]*2), str(v1[0]*3), todo, str(v), str(3)])
        p3 = subprocess.Popen(['bash', 'ascii.sh', 'convert',  str(
            v1[0]*3), str((v1[0]*4)+v1[1]), todo, str(v), str(4)])
        x = len(cc)
        p1.wait(); p2.wait(); p3.wait(); p.wait()
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
        time.sleep(1)
        shutil.rmtree(f'processed/{v}/rank/')
        #writes todo, to id, to complete the loop :)
        write(todo, 0, f'processed/{v}/id.txt')
        print('beep')
    #generates ascii rank-detection.
  #  writelist(os.listdir(f'processed/{v}/id'), 0, f'{exdir}/source.txt')
    os.makedirs(f'{exdir}/html')
    print(f'processed/{v}')
    gen('gen', exdir, f'processed/{v}')
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
    elif os.path.exists(todo) == False:
        write(f'done, {todo}//path doesn"t exist', xz, 'todo.txt')
        continue
    else:
        s = stopwatch()
      #  if os.path.exists(f'{todo}/temp/temp50.jpg') == False:
        #write(f'done, {todo}//ERROR MISSING temp50.jpg', xz, 'todo.txt')
        #print('ERROR MISSING TEMP50')
        #f continue
        #this is pretty self explanitory
        #this just takes stuff from around the files and gleans all the data it can from it
        channel = todo.partition('/')[0]
        if not channel:
            continue
        if os.path.exists(f'{channel}/out/') == False:
            os.makedirs(f'{channel}/out/')
        z = len(os.listdir(f'{channel}/out'))
        if not z:
            z = 0
        exdir = f'{channel}/out/{z}'
        print('test pp')
        penme(todo)
        subprocess.Popen(
            ['convert', f'{todo}/temp/temp50.jpg', '-crop', '640x360+210+315', '-crop', '-200-20', '-type', 'Grayscale', '-sharpen', '0x12', f'{exdir}/boop.jpg'])
        shutil.copy(f'{todo}/temp/temp50.jpg', exdir)
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
            write('some really stupid shit bug happened',
                  7, f'{exdir}/meta.txt')
        bet1 = read(0, f'{todo}/meta.txt')
        bet2 = read(1, f'{todo}/meta.txt')
        write(bet1, 8, f'{exdir}/meta.txt')
        write(bet2, 9, f'{exdir}/meta.txt')
        write(todo, 10, f'{exdir}/meta.txt')
        write(f'processed/{v}', 11, f'{exdir}/meta.txt')
        time.sleep(1)
        write(f'done, {todo}', xz, 'todo.txt')
        print(s.stop())
        ai = ocr_core(f'{exdir}/boop.jpg')
        write(ai, 0, f'{exdir}/meta.txt')

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
