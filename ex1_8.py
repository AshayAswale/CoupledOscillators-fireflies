import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random 
import copy

fig = plt.figure()
first = True

R = 3
size = 20
P = 0.001
petri_dish= np.zeros([size,size])
resets = np.zeros([size,size])
size_preds = np.zeros([size,size])
signal = np.zeros([size,size])
history = np.zeros([size,size])

signal[10,10] = 1
resets[10,10] = R
history[10,10] = 1


i = 0
thr = 3
k=0.5

def isProbable():
    return random.random()<=P


def neighborFlashed(x,y, signal):
    east = signal[max(x-1,0),y]  == 1
    west = signal[min(x+1,size-1),y]  == 1
    south = signal[x,max(y-1,0)]  == 1
    north = signal[x,min(y+1,size-1)]  == 1

    north_east = signal[min(x+1,size-1),max(y-1,0)]  == 1
    north_west = signal[min(x+1,size-1),min(y+1,size-1)]  == 1
    south_east = signal[max(x-1,0),max(y-1,0)]  == 1
    south_west = signal[max(x-1,0),min(y+1,size-1)]  == 1

    four_way = east or west or south or north
    eight_way = four_way or north_east or north_west or south_east or south_west
    return  eight_way

def getPetriDish():
    global petri_dish
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
        return signal
    
    temp_signal = copy.deepcopy(signal)
    for row in range(size):
        for col in range(size):
            if signal[row,col] == 0:
                if neighborFlashed(row,col, signal) and not(history[row,col]==1):
                    temp_signal[row,col] = 1
                    resets[row,col] = R + 1
                    history[row,col] = 1
            else:
                temp_signal[row,col] -= 1
            resets[row,col] -= 1
    signal = temp_signal
    return getPetriDish()


im = plt.imshow(updateBoard(size), animated=True)

def updatefig(*args):
    im.set_array(updateBoard(size))
    return im,

ani = animation.FuncAnimation(fig, updatefig, interval=100, blit=True)
plt.show()