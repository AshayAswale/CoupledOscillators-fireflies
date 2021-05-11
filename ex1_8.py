import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random 
import copy

fig = plt.figure()
first = True

R = 3
size = 5
P = 0.001
# petri_dish= np.zeros([size,size])
resets = np.zeros([size,size])
size_preds = np.zeros([size,size])
signal = np.zeros([size,size])
# history = np.zeros([size,size])
fire_once = np.zeros([size,size])



i = 0
thr = 3
k=0.5

def isProbable():
    return random.random()<=P


def neighborFlashed(x,y, signal):
    i = 0
    east = False
    west = False
    south = False
    north = False
    north_east = False
    north_west = False
    south_east = False
    south_west = False
    
    if(signal[max(x-1,0),y]  == 1):
        east = True
        i += 1
    if(signal[min(x+1,size-1),y]  == 1):
        west = True
        i += 1
    if(signal[x,max(y-1,0)]  == 1):
        south = True
        i += 1
    if(signal[x,min(y+1,size-1)]  == 1):
        north = True
        i += 1

    if(signal[min(x+1,size-1),max(y-1,0)]  == 1):
        north_east = True
        i += 1
    if(signal[min(x+1,size-1),min(y+1,size-1)]  == 1):
        north_west = True
        i += 1
    if(signal[max(x-1,0),max(y-1,0)]  == 1):
        south_east = True
        i += 1
    if(signal[max(x-1,0),min(y+1,size-1)]  == 1):
        south_west = True
        i += 1

    four_way = east or west or south or north
    eight_way = four_way or north_east or north_west or south_east or south_west
    return  eight_way

def getPetriDish():
    petri_dish= np.zeros([size,size])
    global size_preds

    for row in range(size):
        for col in range(size):
            if (resets[row,col]<=0):
                petri_dish[row,col] = 0.0
            else:
                petri_dish[row,col] = 1.0
    return petri_dish

def changeSignal():
    east = petri_dish[max(x-1,0),y]  == 1
    west = petri_dish[min(x+1,size-1),y]  == 1
    south = petri_dish[x,max(y-1,0)]  == 1
    north = petri_dish[x,min(y+1,size-1)]  == 1

def updateBoard(size):
    global resets
    global petri_dish, signal
    global i, thr
    
    if i<thr:
        temp_ = np.zeros([size,size])
        i += 1
        temp_[0,0] = 1
        return temp_
    
    temp_signal = copy.deepcopy(signal)
    for row in range(size):
        for col in range(size):
            if isProbable():
                temp_signal[row,col] = 1 
                resets[row,col] = R + 1
                # history[row,col] = 1
            if signal[row,col] == 0:
                if neighborFlashed(row,col, signal) and not(resets[row,col]>0):
                    temp_signal[row,col] = 1
                    resets[row,col] = R + 1
            # else:

                    # history[row,col] = 1
            else:
                temp_signal[row,col] -= 1
            resets[row,col] -= 1
    # print(resets)
    signal = temp_signal
    return getPetriDish()


im = plt.imshow(updateBoard(size), animated=True)

def updatefig(*args):
    im.set_array(updateBoard(size))
    return im,

ani = animation.FuncAnimation(fig, updatefig, interval=100, blit=True)
plt.show()