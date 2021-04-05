import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random 

fig = plt.figure()
first = True
T = 10
size = 10
counters = np.random.rand(size,size)
counters *= T
k=0.5

def neighborFlashed(x,y):
    east = counters[max(x-1,0),y]  >= T
    west = counters[min(x+1,size-1),y]  >= T
    south = counters[x,max(y-1,0)]  >= T
    north = counters[x,min(y+1,size-1)]  >= T
    return east or west or south or north

def getFireflies():
    global first
    fireflies = np.zeros([size,size])
    # Code Snippet
    if first:
        fireflies[0,0] = 1.0
        first = False
    ###

    for row in range(size):
        for col in range(size):
            if counters[row,col] >= T:
                fireflies[row,col] = 1.0
    return fireflies

def updateBoard(size):
    global counters
    new_counter = np.zeros((size,size))
    for row in range(size):
        for col in range(size):
            val = counters[row,col]
            new_counter[row,col] = val+1

            if(neighborFlashed(row,col)):
                new_counter[row,col] = val + k*val
            
            if val >= T:
                new_counter[row,col] = 0.0
    counters = new_counter
    return getFireflies()


im = plt.imshow(updateBoard(size), animated=True)

def updatefig(*args):
    im.set_array(updateBoard(size))
    return im,

ani = animation.FuncAnimation(fig, updatefig, interval=90, blit=True)
plt.show()