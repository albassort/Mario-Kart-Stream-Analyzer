from PIL import Image
import pytesseract
import os
from os import path
#i have no clue how this works.
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
if __name__ == '__main__':
    exit("This script is not to be ran standalone, and only exists as a module for streamget.py.")
