from BlinkyTape import BlinkyTape
import time

import GlobalSettings as G

def sendColorPixel(blinky):
    blinky.sendPixel(G.color[0],G.color[1],G.color[2])
    
def sendBlackPixel(blinky):
    blinky.sendPixel(0,0,0)

def start(blinky):
    while G.keepGoing is False:
        continue
    while True:
        for i in range(0,150):
            for x in range(0,i):
                sendBlackPixel(blinky)
            sendColorPixel(blinky)
            if i<149:
                for y in range(i+1,150):
                    sendBlackPixel(blinky)
            blinky.show()
            time.sleep(1/float(G.speed))
            if G.keepGoing is False:
                G.keepGoing = True
                return
    
    
def startSnake(blinky):
    while G.keepGoing is False:
        continue
    length = 10
    while True:
        leftover = 0
        for i in range(0,150):
            if i+length+1 < 150:
                for x in range(0,i):
                    sendBlackPixel(blinky)
                for x in range(i,i+length+1):
                    sendColorPixel(blinky)
                for x in range(i+length+1,150):
                    sendBlackPixel(blinky)
            else:
                leftover = length-(150-i)
                for x in range(0,leftover+1):
                    sendColorPixel(blinky)
                for x in range(leftover+1,i):
                    sendBlackPixel(blinky)
                for x in range(i,150):
                    sendColorPixel(blinky)
            blinky.show()
            time.sleep(1/float(G.speed))
            if G.keepGoing is False:
                G.keepGoing = True
                return
                

def outsideIn(blinky):
    while G.keepGoing is False:
        continue
    while True:
        for i in range(0,150):
            if i < 75:
                for x in range(0,i):
                    sendColorPixel(blinky)
                for x in range(i,150-i):
                    sendBlackPixel(blinky)
                for x in range(150-i,150):
                    sendColorPixel(blinky)
            else:
                for x in range(0,i-75):
                    sendBlackPixel(blinky)
                for x in range(i-75,150-(i-75)):
                    sendColorPixel(blinky)
                for x in range(150-(i-75),150):
                    sendBlackPixel(blinky)
            blinky.show()
            time.sleep(1/float(G.speed))
            if G.keepGoing is False:
                G.keepGoing = True
                return