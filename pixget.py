from PIL import Image
def pix(frame, inx):
    # Reads the image from a parrent script through pipe:0
    img = Image.fromarray(frame)   
    inx = int(inx)
    #inx is the program state
    #these if statements only trigger if a state is given
    #this saves a lot of time
    if int(inx) == 1 or int(inx) == -5:
        #ordered BGR
        btwtul = [img.getpixel((310, 32)), img.getpixel((321, 293   )), img.getpixel((420, 330))]
        z = []
        ib1 = 680 <= sum(btwtul[0]) <= 770
        ib2 = 0 <= sum(btwtul[1]) <= 55
        ib3 = 140 <= btwtul[2][0] <= 230
        ib4 = 140 <= btwtul[2][1] <= 230
        ib5 = 140 <= btwtul[2][2] <= 230
        ibl1 = (ib1, ib2, ib3, ib4, ib5)    #ib1-6 are composite rgb values because innacuracy is unlikely
    #ib7-13 are the 6 RGB values for ending to create a very specific very false positive proof check
    if int(inx) == 2:
        #Go, only triggers while waiting for race start
        #These split the get pixels and checks if they ar within a certain color range
        #If they all correct, the logic below will switch the program state
        gox1 = img.getpixel((260,150)); gox2 = img.getpixel((330,145)); gox3 = img.getpixel((380,145))
        (b0, g0, r0) = gox1; (b1, g1, r1) = gox2; (b2, g2, r2) = gox3
        go1 = 200 <= r0 <= 255
        go2 = 200 <= r1 <= 255
        go3 = 200 <= r2 <= 255
        
        go4 = 180 <= g0 <= 225 
        go5 = 180 <= g1 <= 225 
        go6 = 180 <= g2 <= 225
        
        go7 = 0 <= b0 <= 70 
        go8 = 0 <= b1 <= 70 
        go9 = 0 <= b2 <= 70
        goftul = [go1, go2, go3, go4, go5, go6, go7, go8, go9]
    if int(inx) == 3:
        #End Checuk, only triggers while race in progress
        c7 = img.getpixel((354,133)); c8 = img.getpixel((420,156)); c9 = img.getpixel((220,152))
        (b6, g6, r6) = c7; 
        (b7, g7, r7) = c8; 
        (b8, g8, r8) = c9
        ib7 = 200 <= r6 <= 255
        ib8 = 200 <= r7 <= 255
        ib9 = 200 <= r8 <= 255
        ib10 = 205 <= g6 <= 255
        ib11 = 205 <= g7 <= 255
        ib12 = 205 <= g8 <= 255
        ib13 = 10 <= b6 <= 70 or 180 <= b6 <= 255 
        ib14 = 10 <= b7 <= 70 
        ib15 = 10 <= b8 <= 70
        ibl3 = (ib7, ib8, ib9, ib10, ib11, ib12, ib13, ib14, ib15)
    #startup state, looks for loading
    #returns are used to communicate with upper script
    #It is fed the previous entry ie 1 will be fed 1
    # this is why we have he else statements
    if int(inx) == 1:
           # print(ibl1)
        if all(ibl1) == True:
            return int(-5)
        else:
            return int(1)
    #attempts to gate out false positives with -5
    #it will wait 5 frames, and if it is still reading loading, it will actually  register loading load
    if int(inx) == -5:
        if all(ibl1) == True:
            return int(-1)
        else:
            return int(1)
    #Loading check
    if int(inx) == 2:
        if all(goftul) == True:
            #outputs -3 for upper script to inturpret and route to 3
            return int(-3)
        #outputs -2 to upper script to count untill error out to 1
        else:
            return int(-2)  
    #End Check
    if int(inx) == 3:
        if all(ibl3) == True:
            return int(4)
        #outputs 4 marking start of new loop
        else:
            return int(3) 
               
#MARK THE START OF NEW CYCLE

#for debug in streamex
#print(crgb1, crgb2, crgb3)
#print(crgb4, crgb5, crgb6)
#print(r6, g6, b6)
#print(r7, g7, b7)
#print(r8, g8, b8)
#print(l1(0))
def getplayers(img):
    img = Image.fromarray(img)
    #gets consistant player pixel locations
    placetuples = [img.getpixel((220, 40)), img.getpixel((300, 82)), img.getpixel((300, 127)), img.getpixel((300, 172)), img.getpixel((300, 218)), img.getpixel(
    (300, 270)), img.getpixel((540, 40)), img.getpixel((540, 87)), img.getpixel((540, 130)), img.getpixel((540, 174)), img.getpixel((540, 223)), img.getpixel((540, 260))]

    pixelSums = []
    for place in range(0, len(placetuples)):
       pixelSums.append(sum(placetuples[place]))
    plce = []

    #this seems unreliable.
    for x in range(0, 12):
        pib = 500 <= pixelSums[x] <= 800
        plce.append(pib)
    if all(plce):
        return 12   
    else:
        p = 0
        for x in range(0, 11):
            if plce[x] == False:
                break
            p += 1
        return p

if __name__ == '__main__':
    exit("This script is not to be ran standalone, and only exists as a module for streamget.py.")