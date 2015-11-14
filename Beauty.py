from BlinkyTape import BlinkyTape
import time
import math

import GlobalSettings as G

step = 50

def start(blinky):
	while G.keepGoing is False:
		continue
	while True:
		for i in range(0,150):
			red   = math.sine(i)
			green = math.sine(i+step)
			blue  = math.sine(i+step*2)
			red   = ((red + 1) / 2) * 255
			blue  = ((blue + 1) / 2) * 255
			green = ((green + 1) / 2) * 255
			blinky.sendPixel(red,blue,green)
		blinky.show()
		time.sleep(1/float(G.speed))
		if G.keepGoing is False:
			G.keepGoing = True
			return