import os
from stringcolor import cs
from readwrite import read, readall

def caclulateavg(list, line):
    avg = []
    list 
    for game in list:
            readx = read(line, f'{game}/meta.txt')
            if readx == 'None' or readx == '':
                #If no players, assume its 12
                readx = 12
            if line == 6 or line ==7:
                readx = readx[:-1]
            try: 
                float(readx)
            except ValueError:
                readx = 12
            avg.append(float(readx))
    try:
        if line == 6 or line == 7:
                return f'{sum(avg)/len(avg)}s'
        else:
            return sum(avg)/len(avg)
    except ZeroDivisionError:
        return 'ZeroDivisionError!'



def underscore():
    print(cs('____________________________________________', '#24abb3'))
readlookup = {0: 'Course: ', 1: 'Players: ',  2: 'Final Rank Entry: ', 3: 'Averege Rank: ', 4: 'Lowest Place: ',  5: 'Highest Place: ',
              6: 'Total Time: ', 7: 'Averege Time For 3 Laps: ', 8: 'Starting Bet: ', 9: 'Ending Bet: ', 10: 'Origin Path: ', 11: 'Image Path: '}
def printoptions(O = 0):

    if O == 0:
        return '''
                1.Avg End Rank
                2.Total Avg Rank
                3.Avg players?
                4.Avg lows/highs per game
                5.Avg time total'''
    elif O != 0:
        return'''
                1.Avg End Rank
                2.Total Avg Rank
                3.Avg players?
                4.Avg lows
                5.highs per game
                6.Avg time total'''
def printavglist(y):
    temp = []
    temp2 = []
    for x in avglist:
        temp.append((x[0], str(x[1][y])))
    for x in temp:
        temp2.append(', '.join(x))
    return temp2

def copypasta(str1, str2, y):
        if y == 5:
            avglist.sort(key=lambda x: x[1][y][:-1])
        else:
            avglist.sort(key=lambda x: x[1][y])
        underscore()
        print(
            avglist[-1][0]+f"has the {str1} on averege at "+str(avglist[-1][1][y]))
        print(
            avglist[0][0]+f"has the {str2} on averege at "+str(avglist[0][1][y]))
        print('a to get the full output')
        t = input()
        if t == 'a':
            underscore()
            for x in printavglist(y):
                print(x)
            input()
        else:
            return
      #  if t != 'a':
state = 1
redo = 0
death = True
listofchannels = []
temp = os.listdir("archive/")
load = 0

for x in temp:
    print(x)
    listofchannels.append(x)

#While you are in limbo; i suppose....
while death == True:
    while state == 1:
        if redo != 1:
            underscore()
            temp =[]
            print(cs(str(len(listofchannels))+' channel found', '#21db65c'))
            if len(listofchannels) == 0:
                print('no channels detected.')
                death = False
                state = 0
                continue
            for x in range(0, len(listofchannels)):
                print(cs(str(x), '#21db65c')+': '+listofchannels[x])
            #channel is the input, reads the input...   
            channel = input('please give channel, you can use the digits above to select <3\nx to quit\n' )
        #input branch.

        if channel == 'x':
            death = False
            state = 0
            continue
        elif channel.isdigit() == True:
            #cleaver me.
            try:
                channel = listofchannels[int(channel)]
                print(channel)
            except LookupError:
                print('index out of range, please try again')
                continue

        elif os.path.exists(f'archive/{channel}') == False:
            print('invalid channel, please try again')
            continue        

        redo = 0
        dirx = []
        for date in os.listdir(f'archive/{channel}/'):
            for game in os.listdir(f'archive/{channel}/{date}'):
                dirx.append(f'archive/{channel}/{date}/{game}')

        underscore()
        print(cs(f'{len(dirx)} ', '#21db65c')+f'''folders found\nwhat would you like to look at?
        {printoptions()}
        6. Go by course
        ? to print this again
        x to back to channel select''')

        state = 2
    while state == 2:
        z = input()
        if z == '?':
            redo = 1
            state = 1
        elif z == 'x':
            redo = 0
            state = 1
        elif z.isdigit() == False:
            print('please enter a digit')
        elif int(z) > 6 or int(z) < 1:
            print('please enter a digit please 1 and 6')
        elif z == "1":
            print(caclulateavg(dirx, 2))
        elif z == "2":
            print(caclulateavg(dirx, 3))
        elif z == '3':
            print(caclulateavg(dirx, 1))
        elif z == '4':
            print('lows: '+str(caclulateavg(dirx, 4)))
            print('highs: '+str(caclulateavg(dirx, 5)))
        elif z == '5':
            print(caclulateavg(dirx, 6))
            print('assuming 3 laps, average time per lap: '+caclulateavg(dirx, 7))
        elif z == '6':
            dictcourse = {}
            for x in dirx:
                course = read(0, f'{x}/meta.txt')
                if course == '' or course == "File or line doesn't exist":
                    continue
                if course not in dictcourse:
                    dictcourse[course] = [x]
                else:
                    dictcourse[course].append(x)
                dictcourselist =[]
                for x in dictcourse:
                    dictcourselist.append((x, (dictcourse[x])))
                state = 3
                load = 1
    while state == 3:
        if load == 1:
            del(dictcourse)
            load = 0
        if load ==0:
            underscore()
            print(cs(str(len(dictcourselist)), '#21db65c')+' unique courses found')
            temp = []
            dictcourselist.sort(key=lambda x: len(x[1]))
            for x in range(-abs(len(dictcourselist))+1, 1):
                x = abs(x)
                y = x - len(dictcourselist)+1
                temp.append(str(abs(y))+' '+dictcourselist[x][0])
            print(', '.join(temp))
            print('type the digit for the course you want to see')
            print('type r to sort corses by best-least')
            print('? to display this again')
            print('x to return up')
            load = 2
        sf = input()
        if sf == 'x':
            redo = 1
            state = 1
        elif sf == '?':
            load = 0
        elif sf == 'r':
            avglist = []
            load = 1
            state = 6
            while state == 6:
                if load == 1:
                    for x in range(0, len(dictcourselist)):
                        avglist.append((dictcourselist[x][0], []))  
                        for xz in range(1, 8):
                            if caclulateavg(
                                    channel, dictcourselist[x][1], xz) == 'error':
                                continue
                            else:
                                avglist[x][1].append(caclulateavg(
                                channel, dictcourselist[x][1], xz))
                    load = 0
                  #  avglist.sort(key=lambda x: x[1][0])
                if load == 0:
                    underscore()
                    print('display courses by highest to least')
                    print('avalible options are:')
                    print(printoptions('zx'))
                    print('? to display this again')
                    print('x to go back up to course selection')
                    load = 2
                sf = input()
                if sf == 'x':
                    load = 0
                    state = 3   
                    break
                elif sf == '?':
                    load = 0
                    continue
                elif sf.isdigit() == False:
                    print('please enter digit')
                elif int(sf) > 6 or int(sf) < 1:
                    print('please enter a digit less than between 1 and 5.')   
                    load = 0    
                elif sf == "1":
                    copypasta('highest rank', 'lowest rank', 1)
                    load = 0
                elif sf == "2":
                    copypasta('highest rank avg rank', 'lowest rank', 2)
                    load = 0
                elif sf == "3":
                    copypasta('most players', 'least players', 0)
                    load = 0
                elif sf == "4":
                    copypasta('highest low', 'lowest low', 3)
                    load = 0
                elif sf == "5":
                    copypasta('highest high', 'highest low', 4)
                    load = 0
                elif sf == "6":
                    copypasta('most players', 'least players', 5)
                    load = 0
        elif sf.isdigit() == False:
            print('please enter a digit')
        elif int(sf) > len(dictcourselist):
            print('number you entered too large. Pick a smaller number.')
        else:
            sf = int(sf) - len(dictcourselist)+1
            sf = abs(sf)
            select = dictcourselist[int(sf)]
            state = 4
            load = 1
            while state == 4:
                if load == 1:
                    underscore()
                    print(f'''select actions:
                                0. select specific match and print all details
                                {printoptions()}
                                ? to print this again
                                x to back to channel select''')
                    print(select[0])
                    print(select[1])
                    load = 0
                sf = input()
                if sf == '?':
                    load = 1
                    continue
                elif sf == 'x':
                    state = 3
                    break
                elif sf.isdigit() == False:
                    print('please enter a digit')
                    continue
                elif sf == "1":
                    underscore()
                    print(caclulateavg(select[1], 2))
                    underscore()
                elif sf == "2":
                    underscore()
                    print(caclulateavg(select[1], 3))
                    underscore()
                elif sf == '3':
                    underscore()
                    print(caclulateavg(select[1], 1))
                    underscore()
                elif sf == '4':
                    underscore()
                    print('lows: '+str(caclulateavg(select[1], 4)))
                    print('highs: '+str(caclulateavg(select[1], 5)))
                    underscore()
                elif sf == '5':
                    underscore()
                    print(caclulateavg(select[1], 6))
                    print('assuming 3 laps, average time per lap: ' +
                          caclulateavg(select[1], 7))
                    underscore()
                elif int(sf) > 5 or int(sf) > 0 :
                    print('please pick a number between 0 and 5')
                elif sf == '0':
                    underscore()
                    for x in range(0, len(select[1])):
                        print(str(x)+'. '+select[1][x])
                    print('x to return up')
                    state = 5
                    while state == 5:
                        sf = input()
                        if sf == 'x':
                            load = 1
                            state = 4
                            break
                        elif sf.isdigit() == False:
                            print('please enter a digit')
                        elif int(sf) > len(select[1])-1:
                            print('number you entered too large. Pick a smaller number.')
                            continue
                        else:
                            temp = readall(f'{channel}/out/{select[1][int(sf)]}/meta.txt')
                            underscore()
                            for x in range(0, 12):
                                if x == 8 or x == 9:
                                    continue
                                print(readlookup[x]+''+temp[x])
                            underscore()
if death == False:
    underscore()
    print('V2, Dec-Jan 2021') 
    
