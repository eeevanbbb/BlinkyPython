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
    while True:
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


def epicSave(blinky):
    while G.keepGoing is False:
        continue
    while True:
        #ball towards goal
        for x in range(0,150-25):
            pos = 149 - x
            for i in range(0,pos):
                sendBlackPixel(blinky)
            sendOrangePixel(blinky)
            for i in range(pos+1,150):
                sendBlackPixel(blinky)
            blinky.show()
            time.sleep(1.0/60)
            if G.keepGoing is False:
    			G.keepGoing = True
    			return

        #soccar comes out of nowhere, but also still move the ball
        for x in range(1,6):
            pos = 25 - x
            carEnd = x * 4
            for i in range(0,carEnd):
                sendBluePixel(blinky)
            for i in range(carEnd+1,pos):
                sendBlackPixel(blinky)
            sendOrangePixel(blinky)
            for i in range(pos+1,150):
                sendBlackPixel(blinky)
            blinky.show()
            time.sleep(1.0/60)
    		if G.keepGoing is False:
    			G.keepGoing = True
    			return

            #collision sends ball flying
            for x in range(pos,150-carEnd):
                for i in range(0,carEnd):
                    sendBluePixel(blinky)
                for i in range(cardEnd+1,pos):
                    sendBlackPixel(blinky)
                sendOrangePixel(blinky)
                for i in range(pos+1,150):
                    sendBlackPixel(blinky)
                blinky.show()
                time.sleep(1.0/60)
        		if G.keepGoing is False:
        			G.keepGoing = True
        			return

            #slink away
            for x in range(150-carEnd,150):
                for i in range(0,150-x):
                    sendBluePixel(blinky)
                for i in range(150-x,x):
                    sendBlackPixel(blinky)
                sendOrangePixel(blinky)
                for i in range(x+1,150):
                    sendBlackPixel(blinky)
                blinky.show()
                time.sleep(1.0/60)
        		if G.keepGoing is False:
        			G.keepGoing = True
        			return

            #sleep for a second then repeat
            time.sleep(1.0)
    		if G.keepGoing is False:
    			G.keepGoing = True
    			return
