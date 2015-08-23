from BlinkyTape import BlinkyTape
import time

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
    blinky.buf = ""
    blinky.position = 0
    while True:
        for x in range(50):
            blinky.sendPixel(G.color[0],G.color[1],G.color[2])
        for x in range(50):
            blinky.sendPixel(G.color[0],G.color[1],G.color[2])
        for x in range(50):
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