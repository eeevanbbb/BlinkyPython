from BlinkyTape import BlinkyTape
import time

import GlobalSettings as G

def sendBluePixel(blinky):
    blinky.sendPixel(0,0,255)

def sendOrangePixel(blinky):
    blinky.sendPixel(255,165,0)

def sendBlackPixel(blinky):
    blinky.sendPixel(0,0,0)

def celebrate(blinky):
    while G.keepGoing is False:
        continue
    #Flash for one second
    for t in range(30):
        for x in range(150):
            sendBluePixel(blinky)

        blinky.show()

        time.sleep(1/60.0)
        if G.keepGoing is False:
            G.keepGoing = True
            return

        for x in range(150):
            sendBlackPixel(blinky)
        blinky.show()

        time.sleep(1/60.0)
        if G.keepGoing is False:
            G.keepGoing = True
            return

    #Weird streamy thing for a few seconds
    for n in range(0,3):
		#Left to right
		for t in range(0,30):
			for x in range(0,15):
				for i in range(0,10):
					if (t <= 15 and x <= t) or (t >= 15 and x >= t-15):
						if (x % 2 == 0):
							sendBluePixel(blinky)
						else:
							sendOrangePixel(blinky)
					else:
						sendBlackPixel(blinky)
			blinky.show()
			time.sleep(1.0/60)
			if G.keepGoing is False:
				G.keepGoing = True
				return
		#Right to left
		for t in range(0,30):
			for x in range(0,15):
				for i in range(0,10):
					if (t <= 15 and (15 - x) <= t) or (t >= 15 and (15 - x) >= t-15):
						if (x % 2 == 0):
							sendBluePixel(blinky)
						else:
							sendOrangePixel(blinky)
					else:
						sendBlackPixel(blinky)
			blinky.show()
			time.sleep(1.0/60)
			if G.keepGoing is False:
				G.keepGoing = True
				return
    while True:
    	if G.keepGoing is False:
    		G.keepGoing = True
    		return
