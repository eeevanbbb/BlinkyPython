from BlinkyTape import BlinkyTape
import time
import math

import GlobalSettings as G

step = 50
granularity = 50.0

def start(blinky):
	offset = 0
	while G.keepGoing is False:
		continue
	while True:
		for i in range(0,150):
			red   = math.sin((i+offset) / granularity)
			green = math.sin((i+step+offset) / granularity)
			blue  = math.sin((i+step*2+offset) / granularity)
			red   = int(((red + 1) / 2) * 255)
			blue  = int(((blue + 1) / 2) * 255)
			green = int(((green + 1) / 2) * 255)
			blinky.sendPixel(red,blue,green)
		blinky.show()
		offset += 1
		if offset == 150:
			offset = 0
		time.sleep(1/float(G.speed))
		if G.keepGoing is False:
			G.keepGoing = True
			return