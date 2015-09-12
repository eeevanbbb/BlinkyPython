#Run this program NOT on the Pi, but on another computer hooked up to a midi device

import sys, pygame, pygame.midi
import socket, json

#set up socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.0.137',4329))
 
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
        
        note = input[0][0][1]
        volume = input[0][0][2]
        on = volume == 75
        
        beginPixel = (note - lowNote) * 2
        
        onLights = {}
        onLights[beginPixel] = on
        onLights[beginPixel+1] = on
    
        #print onLights   
        
        message = json.dumps({"command":"Show","onLights":onLights})
        print message
        sent = client_socket.send(message)
        print(sent)

    # wait 10ms - this is arbitrary, but wait(0) still resulted
    # in 100% cpu utilization
    pygame.time.wait(10)