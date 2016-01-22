from BlinkyTape import BlinkyTape
import time

import GlobalSettings as G

def sendRedPixel(blinky):
    blinky.sendPixel(255,0,0)
    
def sendGreenPixel(blinky):
    blinky.sendPixel(0,255,0)
    
def christmas1(blinky):
    while G.keepGoing is False:
        continue
    while True:
    	#Left red
    	for i in range(0,75):
    		sendRedPixel(blinky)
		blinky.show()
		time.sleep(0.5)
		if G.keepGoing is False:
			G.keepGoing = True
			return
		#Add right green
		for i in range(0,75):
			sendRedPixel(blinky)
		for i in range(75,150):
			sendGreenPixel(blinky)
		blinky.show()
		time.sleep(0.5)
		if G.keepGoing is False:
			G.keepGoing = True
			return
		#Switch
		for i in range(0,75):
			sendGreenPixel(blinky)
		for i in range(75,150):
			sendRedPixel(blinky)
		blinky.show()
		time.sleep(0.5)
		if G.keepGoing is False:
			G.keepGoing = True
			return
		#Alternate
		for i in range(0,150):
			if i % 2 == 0:
				sendGreenPixel(blinky)
			else:
				sendRedPixel(blinky)
		blinky.show()
		time.sleep(0.5)
		if G.keepGoing is False:
			G.keepGoing = True
			return
		#Switch
		for i in range(0,150):
			if i % 2 == 0:
				sendRedPixel(blinky)
			else:
				sendGreenPixel(blinky)
		blinky.show()
		time.sleep(0.5)
		if G.keepGoing is False:
			G.keepGoing = True
			return
		#Fall away
		for t in range(0,75):
			for i in range(0,150):
				if i <= 75 - t or i >= 75 + t:
					if i % 2 == 0:
						if t % 2 == 0:
							sendRedPixel(blinky)
						else:
							sendGreenPixel(blinky)
					else:
						if t % 2 == 0:
							sendGreenPixel(blinky)
						else:
							sendRedPixel(blinky)
			blinky.show()
            time.sleep(1/float(G.speed))
            if G.keepGoing is False:
                G.keepGoing = True
                return