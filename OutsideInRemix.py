from BlinkyTape import BlinkyTape
import time

import GlobalSettings as G

# OutsideIn (benmckibben's "Faded" Remix)
# Samples from RoundAndRound.py appear courtesy of HVTCH MONEY Records
# soundcloud.com/axonicmusic

def sendColorPixel(blinky, offset):
    blinky.sendPixel(int(round(G.color[0]-(3.4*offset))),int(round(G.color[1]-(3.4*offset))),int(round(G.color[2]-(3.4*offset))))

def sendBlackPixel(blinky):
    blinky.sendPixel(0,0,0)

def start(blinky):
    while G.keepGoing is False:
        continue
    while True:
        for i in range(0,150):
            if i < 75:
                for x in range(0,i):
                    sendColorPixel(blinky, (i-x))
                for x in range(i,150-i):
                    sendBlackPixel(blinky)
                for x in range(150-i,150):
                    sendColorPixel(blinky, (x-i))
            else:
                for x in range(0,i-75):
                    sendBlackPixel(blinky)
                for x in range(i-75,75):
                    sendColorPixel(blinky, (74-(x-(i-75))))
                for x in range(75,150-(i-75)):
                    sendColorPixel(blinky, (74-((150-(i-75))-x)))
                for x in range(150-(i-75),150):
                    sendBlackPixel(blinky)
            blinky.show()
            time.sleep(1/float(G.speed))
            if G.keepGoing is False:
                G.keepGoing = True
                return
