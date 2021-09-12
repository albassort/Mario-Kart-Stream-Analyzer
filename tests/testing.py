import sys
from init import readall
import os
#STOLEN FROM STACKOVERFLOW...
#Theres just not much reason to do anything else...
def get_size(starting):
    total_size = 0
    for dir, unused, files in os.walk(starting):
        for f in files:
            fp = os.path.join(dir, f)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return ((total_size/1024)/1024)
testcount = []

folder = "streamers/testoutput"
originalfolder = "tests/rankcheck"
sizenew = get_size(f'{folder}/out')
sizeold = get_size(originalfolder)

if sizenew == sizeold:
    print("Sizes are identical")
    testcount.append(True)
else:
    print("sizes are not identical")
    #checks if its sizenew 98% and 102%.
    testcount.append(((sizeold/100)*98) <= sizenew <= ((sizeold/100)*102))
    if testcount[-1] == True:
        print("They're not identical but they fall within 2% range!")
print(sizenew, 'MB')
print(sizeold, "MB")
incorrect = 0
for x in range(0,5):
    reference = readall(f"tests/rankcheck/{x}/rank.txt")
    x = f"{folder}/out/{x}"
    tobechecked = readall(f'{x}/rank.txt')
    if not reference:
        print(str(x)+" IS BLANK!!!!!!")
        testcount.append(False)
        continue
    #compares the size of folders. If its not the same length it just say "No"
    #Because its really difficult to compare lists of different sizes.
    if len(reference) != len(tobechecked):
        print("incorrect amount of frames")
        print(f'Refence ammount: {len(reference)} New Amount: {len(tobechecked)}')
        print(f'{len(reference)-len(tobechecked)} difference or {len(tobechecked)/len(reference)}%')
        testcount.append(False)
    else:    
        #runs through the lists and compares each one.
        #we could do if x = x but i would like to give it a small 
        #tolerance
        print(str(len(reference))+" total frames, their lengths match!")
        for i in range(0, len(tobechecked)):
            if reference[i] != tobechecked[i]:
                incorrect+= 1
    print(f'{incorrect/len(reference)}% incorrect')      
    if incorrect < 6:
        testcount.append(True)     
#prints output
print(len(testcount))
print("False: "+str(testcount.count(False)), "Correct: "+ str(testcount.count(True)))
print(str((testcount.count(True)/len(testcount))*100)+"% Correct!")
