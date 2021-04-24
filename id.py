from init import write, read, readall  # type: ignore
import sys
import os 
import shutil
import subprocess
import time
#This script generates a key to determine the rank from an image
#it works from reading input images, and determining the unique features....
#that is shared in all images

#To generate:
#Plop images in id/{digit}
#this script will regen the ascii on run with -regen:

#Advice:
#Include an all-black and all-white image, and the output will be nearly perfect.
#however, the images the less likely asciidetection is to freakout.
done = 0
try:
    arg1 = sys.argv[1]
except:
    arg1 = 0
if arg1 == '-regen':
    for x in (range(1, 13)):
        if os.path.exists(f'id/{x}html') == True:
            shutil.rmtree(f'id/{x}html')
        os.mkdir(f'id/{x}html')
    write(0, 0, 'cache.txt')
    subprocess.Popen(['bash', 'ascii.sh', 'id'])
    while done == 0:
        if read(0, 'cache.txt') == '1':
            done = 1
        else:
            time.sleep(1)
            continue
for num in range(1, 13):
    #regenerates if arg1 == -regen
    #else it just... spits out the already existing ascii
    todo = os.listdir(f'id/{num}html')
    uni = []
    ascii =[]
    for x in todo:
        #retrofited onto an older system which used color.
        z = readall(f'id/{num}html/{x}')
        find = []
        #reads the ascii file, this is where its generated...
        for x in range(19, 59):
            find.append(z[x])
        find = ''.join(find)
        ascii.append(find)
    hold = []
    #4000 is the number of ascii "pixels"
    #40x100...
    for xy in range(0, 4000):
        for x in range(0, len(ascii)):
        #this means, for every image in ascii, it adds 0-4000 to hold.
        #for example, 13 images, it will cycle through all 13, and add 13 characters to hold
            hold.append(ascii[x][xy])    
#only appends if there is NO 0 in any of the images
#an all black image wont have the white parts of an all-white images
#through phase cancelation; only the ascii pixels of the desired image will be appended to uni
        if ''.join(hold).count('0') == 0:
#uni is the list which holds the unique values to pick the best fit for an iumage
            uni.append(xy)
        hold = []
    build = []
    #builds the ascii repersentation of an image
    for x in range(0, 4000):
        if x in uni:
            build.append('1')
        else:
            build.append('0')
    buildh = []
    #prints build.
    #100 characters for 40 lines :)
    for xy in range(0, 40):
        for x in range(0, 100):
            x = x + (xy*100)
            buildh.append(build[x])
        print(''.join(buildh))
        buildh = []
#note: add write to id/uni.txt to save output.
#This is a rewrite of a script that was accidentally delete
#I know it works the exact same and the output is identical, but to be safe
#not inlcuding write output
