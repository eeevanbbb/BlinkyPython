from BlinkyTape import BlinkyTape
import time

import GlobalSettings as G

def start(blinky):
    while G.keepGoing is False:
        continue
    blinky.buf = ""
    blinky.position = 0
    while True:
        for i in range(0,150):
            for x in range(0,i):
                blinky.sendPixel(0,0,0)
            blinky.sendPixel(G.color[0],G.color[1],G.color[2])
            if i<149:
                for y in range(i+1,150):
                    blinky.sendPixel(0,0,0)
            blinky.show()
            time.sleep(1/float(G.speed))
            if G.keepGoing is False:
                G.keepGoing = True
                return
    
    
def startSnake(blinky):
    while G.keepGoing is False:
        continue
    blinky.buf = ""
    blinky.position = 0
    length = 10
    while True:
        leftover = 0
        for i in range(0,150):
            if i+length+1 < 150:
                for x in range(0,i):
                    blinky.sendPixel(0,0,0)
                for x in range(i,i+length+1):
                    blinky.sendPixel(G.color[0],G.color[1],G.color[2])
                for x in range(i+length+1,150):
                    blinky.sendPixel(0,0,0)
            else:
                leftover = length-(150-i)
                for x in range(0,leftover+1):
                    blinky.sendPixel(G.color[0],G.color[1],G.color[2])
                for x in range(leftover+1,i):
                    blinky.sendPixel(0,0,0)
                for x in range(i,150):
                    blinky.sendPixel(G.color[0],G.color[1],G.color[2])
            blinky.show()
            time.sleep(1/float(G.speed))
            if G.keepGoing is False:
                G.keepGoing = True
                return
                
                