from pixget import pix  # type: ignore
import cv2
import os
import sys
from init import write, read, linecount  # type: ignore
from datetime import date
import time
import shutil
from stopwatch import Stopwatch
today = date.today(); d = today.strftime("%b-%d-%Y")
#too many counters wtf was i doing.
z = 0
ccc = 0
cc = 0  
vc = 0
cccc = 0 
v = sys.argv[1]
v2 = sys.argv[2]
v3 = sys.argv[3]
#does link checking and pratitions it
cn = v2.partition('.tv/')[2]
if not cn:
    print("EROR INVALID TWITCH LINK")
    print(cn)
    quit()
cn = cn.partition('/')[0]
print(cn)
s = 0
while True:
    #this is stupid and im too afraid to touch it
    while True:
        #Allows for the recapture of video to reduce delay.
        #Happens at the frame interval dictated by c >, ~line 57~z
        if z != 1:
            cap = cv2.VideoCapture(v)
            print("test")
            z = 1
            c = 0
        try:
            succ, frame = cap.read()
        except:
            continue
        if succ:
            if s == 0:
                state = pix(frame, 1)
                s += 1
                print('ci')
                continue
            if state == -1:
                if cc < 220:
                    cc += 1
                    print(cc)
                    continue
                else:
                    cv2.imwrite('temp/temp.jpg', frame)
                  #  os.system('jp2a --colors --fill temp/temp.jpg')
                    state = 2
                    c = 0
                    ct = 3000
    #     #Writes temp.jpg, which will be used to generate meta data
            #resets to 1 if -2 is returned ccc > x times.
            #used to parse false positives
            if state == -2:
                ccc+=1
                print(f'    {ccc}', end = '\r')
                state = 2
                try:            
                    os.makedirs('temp/')
                except FileExistsError:
                    pass
                if cc <= 100:
                    cv2.imwrite(f'temp/temp{ccc}.jpg', frame)
                if ccc > 900:
                    state = 1
                    ccc = 0
                    shutil.rmtree('temp')
                    print('GO TIMEOUT, RETURN TO MONKE')
            #creates a file structure for data if the race start is detected
            # channelname/date/number of files in dir           
            if state == -3:
                if cccc <= 110:
                    cccc += 1
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
                ct = 1000
                cc = 0
                ccc = 0
                stopwatchx = Stopwatch()
                state = 3
            if state == 4:
                state = 1
                cc = 0
                todo = linecount('todo.txt')
                write(f'{cn}/{d}/{number}/', int(todo+1), 'todo.txt')
                write(str(stopwatchx.stop()), 3, f'{dir}meta.txt')
                time.sleep(15)
            if state == 3:
                cv2.imwrite(f'{dir}noprocess{cc}.jpg', frame)
                print(f'   noprocess{cc}', end = '\r')
                cc += 1
            if state == -5:
                if vc < 5:
                    vc+=1
                    continue
                if vc > 5:
                    state = pix(frame, int(-5))
                    vc = 0
            state = pix(frame, int(state))
            print(state, end = '\r')
        else:
            break
    
    # quit()
