from PIL import Image
import pytesseract
import os
from os import path
#i have no clue how this works.
def writemakepath(path):
    if os.path.exists(path) == False:
        makepath = path.rpartition("/")
        #replace vulnerable os.system()...
        #if the file is in the dir, it will make it
        if not makepath[0]:
            with open(path, 'w') as temp:
                temp.close
        else:
            #if not, it will make the folder.
            if os.path.exists(makepath[0]) == False:
                os.makedirs(makepath[0])
            with open(f'{makepath[0]}/{makepath[2]}', 'w') as temp:
                temp.close

def write(input, writeline, path):
    writemakepath(path)
    with open(path, "r") as file:
        lines = file.readlines()
        totatlines = len(lines)-1
        if int(writeline) > totatlines:
            #if there isn't enough space, we add enough lines to fill the space
            lines.append("\n"*(writeline-totatlines-1))
            #then we simply append, it, rather than overwriting it.
            lines.append(str(writeline))
            file.close()
        else:
            #otherwise we just overwrite the line.
            input = str(writeline)
            lines[writeline] = input+'\n'
            file.close()
    #we open it again because otherwise it creates an issue
    #where it will duplicate the  file within itself.
    #its inefficient and I dont like it. Python's STDLIB can be very shameful at times
    with open(path, "w") as file:
        file.writelines(lines)



def writelist(listx, file):
    writemakepath(file)
    with open(file, 'a') as f:
        for xy in listx:
            f.writelines(str(xy)+"\n")
        f.close

def read(line, file):
    #opens a file and seleCts the line, base 0
    return open(file).readlines()[line].rstrip()

def readall(file):
    #readall all by spamming the read function
    return open(file).readlines()
def linecount(file):
    return len(readall(file))
def ocr_core(file):
    #uses pytesseract to open an image and output string
    text = pytesseract.image_to_string(Image.fromarray(file)).rstrip()
    text = text.replace('\n', '')
    text = text.lstrip(' ')
    return text
if __name__ == '__main__':
    exit("This script is not to be ran standalone, and only exists as a module for streamget.py.")
