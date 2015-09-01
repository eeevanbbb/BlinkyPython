from BlinkyTape import BlinkyTape
import time

import GlobalSettings as G

def sendColorPixel(blinky):
    blinky.sendPixel(G.color[0],G.color[1],G.color[2])
    
def sendBlackPixel(blinky):
    blinky.sendPixel(0,0,0)
    
def showVolume(left,right,blinky):
    if left < 0:
        left = 0
    if left > 1:
        left = 1
    if right < 0:
        right = 0
    if right > 1:
        right = 1
    
    adjustedLeft = int(left * 75)
    adjustedRight = int(right *75)
    
    for x in range(adjustedLeft):
        sendColorPixel(blinky)
    for x in range(adjustedLeft,75):
        sendBlackPixel(blinky)
    for x in range(75,75+adjustedRight):
        sendColorPixel(blinky)
    for x in range(75+adjustedRight,150):
        sendBlackPixel(blinky)
    
    blinky.show()