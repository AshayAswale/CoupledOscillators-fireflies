import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random 
import copy
import sys

fig = plt.figure()
first = True

input_args = len(sys.argv)
if int(input_args) != 2:
    print("Input board size not found. Size of 5 considered")
    size = 5
else:
    size = int(sys.argv[1])


if size == 5:
    R = 5
    P = 0.005
elif size == 10:
    R = 3
    P = 0.001
elif size == 20:
    R = 2
    P = 0.0001
else:
    print("Only tuned sizes are 5, 10, and 20. This size is not tuned. Still trying.")
    R = 3
    P = 0.001


silent_count_max = 1/P
# silent_count_max = 200
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

    for row in range(size):
        for col in range(size):
            if (resets[row,col]<=0):
                petri_dish[row,col] = 0.0
            else:
                petri_dish[row,col] = 1.0
    return petri_dish

def updateBoard(size):
    global resets
    global petri_dish, signal
    global i, thr
    global size_preds
    
    if i<thr:
        temp_ = np.zeros([size,size])
        i += 1
        temp_[0,0] = 1
        return temp_
    
    temp_signal = copy.deepcopy(signal)
    silent_count = 0
    for row in range(size):
        for col in range(size):
            if resets[row,col] <-1 and isProbable() and fire_once[row,col] == 0:
                temp_signal[row,col] = 1 
                resets[row,col] = R + 1
                fire_once[row,col] = 1
                size_preds[row,col] += 1
                
            if signal[row,col] == 0:
                if neighborFlashed(row,col, signal) and not(resets[row,col]>0):
                    temp_signal[row,col] = 1
                    resets[row,col] = R + 1
                    size_preds[row,col] += 1
                    
            else:
                temp_signal[row,col] -= 1
            resets[row,col] -= 1
            if resets[row,col] < -silent_count_max:
                silent_count += 1
    # print(resets)
    signal = temp_signal
    if silent_count >= size*size:
        print("\nSize estimate of all the agents:")
        print(size_preds)
        exit()
    return getPetriDish()


im = plt.imshow(updateBoard(size), animated=True)

def updatefig(*args):
    im.set_array(updateBoard(size))
    return im,

ani = animation.FuncAnimation(fig, updatefig, interval=2, blit=True)
plt.show()