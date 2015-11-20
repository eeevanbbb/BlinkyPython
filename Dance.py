from BlinkyTape import BlinkyTape
import time
from random import randint

import GlobalSettings as G

flashTime = 1/5.0 #must increase for > 300 BPM

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


def downbeatPeaks(blinky):
    base = 15
    offBeat = 40
    downBeat = 60
    beat = 1
    timeSinceBeat = 0.0
    while G.keepGoing is False:
        continue
    while True:
        theBPM = float(G.bpm)
        timeBetweenBeats = 60.0 / theBPM
        fuzz = randint(-5,5)
        length = base
        if timeSinceBeat >= timeBetweenBeats:
            timeSinceBeat -= timeBetweenBeats
            beat = beat % 4 + 1
            if beat == 1:
                length = downBeat
            else:
                length = offBeat
        for i in range(0,length+fuzz):
            blinky.sendPixel(G.color[0],G.color[1],G.color[2])
        for i in range(length+fuzz,150-(length+fuzz)):
            blinky.sendPixel(0,0,0)
        for i in range(150-(length+fuzz),150):
            blinky.sendPixel(G.color[0],G.color[1],G.color[2])
        blinky.show()
        timeSinceBeat += (1.0/float(G.speed))
        time.sleep(1.0/float(G.speed))
        if G.keepGoing is False:
            G.keepGoing = True
            return


def dart(blinky):
    beat = 1
    dartLeft = 55
    dartRight = 95
    dartDirection = 0
    while G.keepGoing is False:
        continue
    while True:
        downbeatColor = G.color
        offbeatColor  = [255 - G.color[0],255 - G.color[1], 255 - G.color[2]]
        theColor = offbeatColor
        if beat == 1:
            theColor = downbeatColor

        theBPM = float(G.bpm)
        bpmTime = 60.0 / theBPM

        if dartDirection == 0:
            dartDirection = 1
            for x in range(dartLeft,dartRight):
                for i in range(0,x):
                    blinky.sendPixel(0,0,0)
                blinky.sendPixel(theColor[0],theColor[1],theColor[2])
                for i in range(x+1,150):
                    blinky.sendPixel(0,0,0)
                blinky.show()
                time.sleep(bpmTime / (dartRight - dartLeft))
                if G.keepGoing is False:
                    G.keepGoing = True
                    return
        else:
            dartDirection = 0
            for x in range(0,dartRight-dartLeft):
                for i in range(0,dartRight-x):
                    blinky.sendPixel(0,0,0)
                blinky.sendPixel(theColor[0],theColor[1],theColor[2])
                for i in range(dartRight-x+1,150):
                    blinky.sendPixel(0,0,0)
                blinky.show()
                time.sleep(bpmTime / (dartRight - dartLeft))
                if G.keepGoing is False:
                    G.keepGoing = True
                    return
        beat = beat % 4 + 1



