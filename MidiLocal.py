#Run this program NOT on the Pi, but on another computer hooked up to a midi device

import sys, pygame, pygame.midi
from BlinkyHTTPServer import handleManualCommand

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

        note = input[0][0][1]
        volume = input[0][0][2]
        on = volume == 75

        beginPixel = (note - lowNote) * 2 #2 pixels per note
        if beginPixel > 148:
            beginPixel = 148 #This shouldn't happen...

        #print onLights
        print "Pixel: " + str(beginPixel)

        color = "000000"
        if on:
            color = "ff0000"

        handleManualCommand(beginPixel,color)
        handleManualCommand(beginPixel+1,color)

        print "HERE"


    # wait 1ms - this is arbitrary, but wait(0) still resulted
    # in 100% cpu utilization
    pygame.time.wait(1)
