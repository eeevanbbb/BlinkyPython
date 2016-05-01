#Run this program WITHOUT the server running

from BlinkyTape import BlinkyTape
import sys, pygame, pygame.midi

#set up blinky
bb = BlinkyTape('/dev/ttyACM0',ledCount=150)

colors = []
for i in range(0,150):
    colors.append([0,0,0])
def changeLight(lightIndex,color):
    colors[lightIndex] = color
    for c in colors:
        bb.sendPixel(c[0],c[1],c[2])
    bb.show()

# set up pygame
pygame.init()
pygame.midi.init()

# list all midi devices
for x in range( 0, pygame.midi.get_count() ):
    print pygame.midi.get_device_info(x)

# open a specific midi device
inp = pygame.midi.Input(3)

lowNote = 36
highNote = 96

while True:
    if inp.poll():
        # no way to find number of messages in queue
        # so we just specify a high max value
        input = inp.read(1000)

        for message in input:
            note = message[0][1]
            volume = message[0][2]
            on = volume == 75

            beginPixel = (note - lowNote) + 45 #middle of the tape
            if beginPixel > 149:
                beginPixel = 149 #This shouldn't happen...

            print input
            print "Pixel: " + str(beginPixel)

            color = [0,0,0]
            if on:
                color = [255,0,0]

            changeLight(beginPixel,color)
