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

def write(x, y, path):
    writemakepath(path)
    with open(path) as f:
        linex = f.readlines()
        linxc = len(linex)
        linxc = int(linxc - 1)
    if int(y) > linxc:
        with open(path, 'a') as f:
            for xy in range(int(linxc), int(y)):
                f.writelines("\n")
                f.close
                f'{xy}'
    with open(path) as f2:
        x = str(x)
        lines = f2.readlines()
        lines[y] = x+'\n'
    with open(path, 'w') as f2:
        f2.writelines(lines)


def writelist(listx, file):
    writemakepath(file)
    with open(file, 'a') as f:
        for xy in listx:
            f.writelines(str(xy)+"\n")
        f.close

def read(line, file):
    #...reads file
    try:
        return open(file).readlines()[line].rstrip()
    except LookupError or FileExistsError:
        return "File or line doesn't exist"
def readall(file):
    baby = []
    for x in range(0, linecount(file)):
        baby.append(read(x, file))
    #reada all by spamming the read function
    return baby
def linecount(file):
    try:
        #opens file
        with open(file) as f:
            linex = f.readlines()
            linxc = len(linex)
        f.close
        #len counts the item properly, but files start at line 0 and not line 1
        if linxc == -1:
            #if an item is sempty it will return 0, and there is no line -1, so return 0
            linxc =+ 1
        return linxc
    except Exception:
        return 0    
def ocr_core(f):
    #uses pytesseract to open an image and output string
    text = pytesseract.image_to_string(Image.open(f)).rstrip()
    text = text.replace('\n', '')
    text = text.lstrip(' ')
    #filters noise
    return text
if __name__ == '__main__':
    exit("This script is not to be ran standalone, and only exists as a module for streamget.py.")
