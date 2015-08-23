from BlinkyTape import BlinkyTape
import time

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

keepGoing = True

def flash(blinky,color,speed):
    global keepGoing
    while keepGoing is False:
        continue
    blinky.buf = ""
    blinky.position = 0
    while True:
        for x in range(50):
            blinky.sendPixel(color[0],color[1],color[2])
        for x in range(50):
            blinky.sendPixel(color[0],color[1],color[2])
        for x in range(50):
            blinky.sendPixel(color[0],color[1],color[2])
    
        blinky.show()
        
        time.sleep(1/float(speed))
        if keepGoing is False:
            keepGoing = True
            return
    
        for x in range(150):
            blinky.sendPixel(0,0,0)
        blinky.show()
        
        time.sleep(1/float(speed))
        if keepGoing is False:
            keepGoing = True
            return
        
def stopFlash():
    global keepGoing
    keepGoing = False