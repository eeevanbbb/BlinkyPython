#Run this program NOT on the Pi, but on another computer hooked up to a midi device

import sys, pygame, pygame.midi
import grequests

# set up pygame
pygame.init()
pygame.midi.init()

# list all midi devices
for x in range( 0, pygame.midi.get_count() ):
    print pygame.midi.get_device_info(x)

# open a specific midi device
inp = pygame.midi.Input(0)

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

            color = "000000"
            if on:
                color = "ff0000"

            #Send the request to turn on or off each light (on = red, off = black)
            grequests.get("http://192.168.0.138:9001/manual/"+str(beginPixel)+"/"+color)
            grequests.get("http://192.168.0.138:9001/manual/"+str(beginPixel+1)+"/"+color)

            print "HERE"
