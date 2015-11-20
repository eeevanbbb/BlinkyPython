from BlinkyTape import BlinkyTape
import time

import GlobalSettings as G

flashTime = 1/5.0

def fourOnTheFloor(blinky):
    beat = 1
    while G.keepGoing is False:
        continue
    while True:
        downbeatColor = G.color
        offbeatColor  = [255 - G.color[0],255 - G.color[1], 255 - G.color[2]]
        for i in range(0,150):
            if beat == 1:
                blinky.sendPixel(downbeatColor[0],downbeatColor[1],downbeatColor[2])
            else:
                blinky.sendPixel(offbeatColor[0],offbeatColor[1],offbeatColor[2])
        blinky.show()
        beat = beat % 4 + 1 #[1,4]
        time.sleep(flashTime)
        if G.keepGoing is False:
            G.keepGoing = True
            return
        for i in range(0,150):
            blinky.sendPixel(0,0,0)
        blinky.show()
        theBPM = float(G.bpm)
        time.sleep(60.0 / theBPM - flashTime)
        if G.keepGoing is False:
            G.keepGoing = True
            return

def alternatePush(blinky):
    position = 0
    count = 0
    threshold = 200
    while G.keepGoing is False:
        continue
    while True:
        primaryColor = G.color
        secondaryColor = [(G.color[0] + 85) % 256,(G.color[1] + 85) % 256,(G.color[2] + 85) % 256]
        #tertiaryColor = [(secondaryColor[0] + 85) % 256,(secondaryColor[1] + 85) % 256,(secondaryColor[2] + 85) % 256]
        tertiaryColor = [G.color[0],(secondaryColor[1] + 85) % 256,secondaryColor[2]]
        colors = [primaryColor,secondaryColor,tertiaryColor]
        for i in range(0,150):
            color = colors[(i + position) % 3]
            blinky.sendPixel(color[0],color[1],color[2])
        blinky.show()
        if count < threshold / 2.0:
            position = (position + 1) % 3
        else:
            position = (position - 1) % 3
        count += 1
        if count > threshold:
            count = 0
        time.sleep(1.0/float(G.speed))
        if G.keepGoing is False:
            G.keepGoing = True
            return