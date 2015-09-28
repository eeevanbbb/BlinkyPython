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
                for x in range(0,i+1):
                    sendColorPixel(blinky, (i-x))
                for x in range(i+1,149-i):
                    sendBlackPixel(blinky)
                for x in range(149-i,150):
                    sendColorPixel(blinky, (x-(149-i)))
            else:
                for x in range(0,i-75+1):
                    sendBlackPixel(blinky)
                for x in range(i-75+1,75):
                    sendColorPixel(blinky, 74-(x-(i-75+1)))
                for x in range(75,149-(i-75)):
                    sendColorPixel(blinky, 74-((149-(i-75))-1-x))
                for x in range(149-(i-75),150):
                    sendBlackPixel(blinky)
            blinky.show()
            time.sleep(1/float(G.speed))
            if G.keepGoing is False:
                G.keepGoing = True
                return
