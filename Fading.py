from BlinkyTape import BlinkyTape
import time

import GlobalSettings as G

def fade_channel(channel,blinky):
    while G.keepGoing is False:
        continue
    while True:
        #fade up
        for t in xrange(0,256,8):
            for x in range(0,150):
                if channel == 0:
                    blinky.sendPixel(t,0,0)
                elif channel == 1:
                    blinky.sendPixel(0,t,0)
                elif channel == 2:
                    blinky.sendPixel(0,0,t)
            blinky.show()
            time.sleep(1/(float(G.speed) * 8))
            if G.keepGoing is False:
                G.keepGoing = True
                return
        #fade down
        for t in xrange(0,256,8):
            for x in range(0,150):
                if channel == 0:
                    blinky.sendPixel(256-,0,0)
                elif channel == 1:
                    blinky.sendPixel(0,256-t,0)
                elif channel == 2:
                    blinky.sendPixel(0,0,256-t)
            blinky.show()
            time.sleep(1/(float(G.speed) * 8))
            if G.keepGoing is False:
                G.keepGoing = True
                return

def fade_red(blinky):
    fade_channel(0,blinky)

def fade_green(blinky):
    fade_channel(1,blinky)

def fade_blue(blinky):
    fade_channel(2,blinky)
