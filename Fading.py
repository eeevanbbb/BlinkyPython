from BlinkyTape import BlinkyTape
import time

import GlobalSettings as G

def fade_red(blinky):
    while G.keepGoing is False:
        continue
    while True:
        #fade up
        for t in range(0,256):
            for x in range(0,150):
                blinky.sendPixel(t,0,0)
            blinky.show()
            time.sleep(1/(float(G.speed) * 8))
            if G.keepGoing is False:
                G.keepGoing = True
                return
        #fade down
        for t in range(0,256):
            for x in range(0,150):
                blinky.sendPixel(256-t,0,0)
            blinky.show()
            time.sleep(1/(float(G.speed) * 8))
            if G.keepGoing is False:
                G.keepGoing = True
                return
