import os 
import pickle
from PIL import Image
#This is a much updated version of the older ID. This one marks the exit from the ascii days of this project
#As did before. you add your images into id/x (1 .. 2 .. 3), and include a bunch. One full black, and one full white at the bare minimum
#this generates a 0 and 1 representation of that data allowing for classifying. the images based upon this data.


#an index of all 1s so we can get an index of which colors to scan to get a guess of what the image is.
ones = {}
for digit in range(1, 13):
    oneholder = []
    images = []
    binary = []
    base = f"id/{digit}"
    files = os.listdir(base)
    im = Image.open(f'{base}/{files[0]}')
    for x in files:
        images.append(Image.open(f"{base}/{x}").load())
        
    #they should all be of uniform height so we use the first image as a reference.
    for y in range(0, im.size[1]):
        #for y in the height
        for x in range(0, im.size[0]):
            #for x in the width
            for image in images:
            #because of the binary image setup, it only returns 1 value.
            #encase it isn't binary
                if type(image[0,0]) != int: 
                    if image[x,y][0] == 0:
                        binary.append(0)
                        break
                if image[x,y] == 0:
                    binary.append(0)
                    break
            #for-elses only execute if the for loop doesn't break 
            else:
                binary.append(1)
                #cv2's pixels are inverted.
                oneholder.append((x,y))

    for x in range(0, im.size[1]):
        holder = []
        for y in range(0, im.size[0]):
            holder.append(str(binary[(x*im.size[0])+y]))
        print("".join(holder))
    ones[digit] = oneholder
pickle.dump(ones, open( "id/uni.p", "wb" ) )    