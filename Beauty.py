from BlinkyTape import BlinkyTape
import time
import math

import GlobalSettings as G

step = 50

def start(blinky):
	while G.keepGoing is False:
		continue
	while True:
		offset = 0
		for i in range(0,150):
			offset += 1
			if offset == 150:
				offset = 0
			red   = math.sin(i+offset)
			green = math.sin(i+step+offset)
			blue  = math.sin(i+step*2+offset)
			red   = int(((red + 1) / 2) * 255)
			blue  = int(((blue + 1) / 2) * 255)
			green = int(((green + 1) / 2) * 255)
			blinky.sendPixel(red,blue,green)
		blinky.show()
		time.sleep(1/float(G.speed))
		if G.keepGoing is False:
			G.keepGoing = True
			return