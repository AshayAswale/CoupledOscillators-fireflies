import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random 
import copy

fig = plt.figure()
first = True

R = 20
size = 20
probabs = np.full((size,size), 0.001)
petri_dish= np.zeros([size,size])
resets = np.zeros([size,size])
size_preds = np.zeros([size,size])

i = 0
thr = 2
k=0.5

def isProbable(probability):
    if random.random()<=probability:
        return True
    else:
        return False

def neighborFlashed(x,y):
    east = petri_dish[max(x-1,0),y]  == 1
    west = petri_dish[min(x+1,size-1),y]  == 1
    south = petri_dish[x,max(y-1,0)]  == 1
    north = petri_dish[x,min(y+1,size-1)]  == 1
    return east or west or south or north

def getPetriDish():
    global petri_dish
    global size_preds

    for row in range(size):
        for col in range(size):
            if (resets[row,col]<=0):
                petri_dish[row,col] = 0.0
            else:
                if(petri_dish[row,col] == 0.0):
                    size_preds[row,col] += 1
                petri_dish[row,col] = 1.0

    # print(size_preds)
    # print()
    return petri_dish

def updateBoard(size):
    global resets
    global petri_dish
    global i, thr
    
    if i<thr:
        temp_ = np.zeros([size,size])
        i += 1
        temp_[0,0] = 1
        return temp_
    
    for row in range(size):
        for col in range(size):
            if (petri_dish[row,col] == 0):
                if(neighborFlashed(row,col)):
                    resets[row,col] = R
                if (isProbable(probabs[row,col])):
                    resets[row,col] = R
            else:
                resets[row,col] -= 1

    return getPetriDish()


im = plt.imshow(updateBoard(size), animated=True)

def updatefig(*args):
    im.set_array(updateBoard(size))
    return im,

ani = animation.FuncAnimation(fig, updatefig, interval=50, blit=True)
plt.show()