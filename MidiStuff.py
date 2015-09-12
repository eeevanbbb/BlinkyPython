import sys, pygame, pygame.midi

from BlinkyTape import BlinkyTape
import time
import GlobalSettings as G

def sendColorPixel(blinky):
    blinky.sendPixel(G.color[0],G.color[1],G.color[2])
    
def sendBlackPixel(blinky):
    blinky.sendPixel(0,0,0)
 
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

def straightMap(blinky):
    for x in range(0,150):
        onLights[x] = False
    while G.keepGoing is False:
        continue
    while True:
        if inp.poll():
            # no way to find number of messages in queue
            # so we just specify a high max value
            input = inp.read(1000)
            
            note = input[0][0][1]
            volume = input[0][0][2]
            on = volume == 75
            
            beginPixel = (note - lowNote) * 2
            
            onLights[beginPixel] = on
            onLights[beginPixel+1] = on
            
            for x in range(0,150):
                if onLights[x]:
                    sendColorPixel(blinky)
                else:
                    sendBlackPixel(blinky)
            blinky.show()
        
            print note
            print on    
 
        # wait 10ms - this is arbitrary, but wait(0) still resulted
        # in 100% cpu utilization
        pygame.time.wait(10)
        
        if G.keepGoing is False:
            G.keepGoing = True
            return