from BlinkyTape import BlinkyTape
import time
from random import randint

import GlobalSettings as G

#bb = BlinkyTape('/dev/tty.usbmodemfa131')
#bb = BlinkyTape('COM8')
'''
bb = BlinkyTape('/dev/tty.usbmodemfd121',ledCount=150)


while True:

    for x in range(50):
        bb.sendPixel(255, 0, 0)
    for x in range(50):
        bb.sendPixel(0, 255, 0)
    for x in range(50):
        bb.sendPixel(0, 0, 255)
                
    bb.show()

    time.sleep(.5)

    for x in range(150):
        bb.sendPixel(0, 0, 0)
    bb.show()

    time.sleep(.5)
'''


def flash(blinky):
    while G.keepGoing is False:
        continue
    while True:
        for x in range(150):
            blinky.sendPixel(G.color[0],G.color[1],G.color[2])
    
        blinky.show()

        time.sleep(1/float(G.speed))
        if G.keepGoing is False:
            G.keepGoing = True
            return
    
        for x in range(150):
            blinky.sendPixel(0,0,0)
        blinky.show()
        
        time.sleep(1/float(G.speed))
        if G.keepGoing is False:
            G.keepGoing = True
            return
            
def clear(blinky):
    while G.keepGoing is False:
        continue
    for x in range(150):
        blinky.sendPixel(0,0,0)
    blinky.show()
    while True:
        if G.keepGoing is False:
            G.keepGoing = True
            return
            
            
def random(blinky):
    while G.keepGoing is False:
        continue
    while True:
        chosen = randint(0,149)
        for x in range(0,chosen):
            blinky.sendPixel(0,0,0)
        blinky.sendPixel(randint(0,255),randint(0,255),randint(0,255))
        for x in range(chosen+1,150):
            blinky.sendPixel(0,0,0)
        blinky.show()
        
        time.sleep(1/float(G.speed))
        if G.keepGoing is False:
            G.keepGoing = True
            return
            
            
def solid(blinky):
    while G.keepGoing is False:
        continue
    while True:
        for x in range(150):
            blinky.sendPixel(G.color[0],G.color[1],G.color[2])
        blinky.show()
        
        time.sleep(1/float(G.speed))
        if G.keepGoing is False:
            G.keepGoing = True
            return
            

def rainbow(blinky):
    while G.keepGoing is False:
        continue
    r = 0
    g = 0
    b = 0
    while True:
        rNew = randint(0,255)
        gNew = randint(0,255)
        bNew = randint(0,255)
        
        transitionTime = 3.0
        numberOfSteps = float(G.speed) * transitionTime
        
        rDelta = (rNew - r) / numberOfSteps
        gDelta = (gNew - g) / numberOfSteps
        bDelta = (bNew - b) / numberOfSteps
        
        while transitionTime > 0:
            transitionTime -= 1/float(G.speed)

            r += rDelta
            g += gDelta
            b += bDelta
            print(str(int(r))+","+str(int(g))+","+str(int(b)))
            for x in range(150):
                blinky.sendPixel(int(r),int(g),int(b))
            blinky.show()
        
            time.sleep(1/float(G.speed))
            if G.keepGoing is False:
                G.keepGoing = True
                return