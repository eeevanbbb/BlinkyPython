import socket
import json
import threading
import subprocess
import time

from BlinkyTape import BlinkyTape

import GlobalSettings

import flash_example
import RoundAndRound
import DynamicColor
import Music

bb = BlinkyTape('/dev/ttyACM0',ledCount=150)
p = None
client_socket = 'None'

def write(message):
    print("Writing message to client: "+message)
    try:
        client_socket.send(message)
    except socket.error:
        print("Cannot write to client")

def stop():
    if GlobalSettings.inProgress == True:
        GlobalSettings.keepGoing = False

def startRoutine(routine,name="routine"):
    print("Stopping...")
    stop()
    print("Starting "+name+"...")
    write("Starting "+name)
    thread = threading.Thread(target=routine,args=(bb, ))
    thread.daemon = True
    thread.start()
    GlobalSettings.inProgress = True

def startDC():
    print("Starting Dynamic Color thread")
    GlobalSettings.dynaColor = True
    dcThread = threading.Thread(target=DynamicColor.dynamicColor)
    dcThread.daemon = True
    dcThread.start()
    GlobalSettings.GDCThread = dcThread

def stopDC():
    print("Stopping Dynamic Color thread")
    GlobalSettings.dynaColor = False
    
def showPixels(onLights):
    for x in range(0,150):
        if onLights[x]:
            bb.sendPixel(G.color[0],G.color[1],G.color[2])
        else:
            bb.sendPixel(0,0,0)
    bb.show()

def listen():
    print("Listening...")
    global bb
    global p
    global client_socket
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('',4329))
    server.listen(4)
    client_socket, client_address = server.accept()
    while True:
        try:
            received_data = client_socket.recv(128)
            if not received_data:
                print("Received empty packet from client")
                return
        except socket.error:
            print("Cannot receive data from client")
            return
        #print(received_data)
        jsonData = received_data
        try:
            dataDict = json.loads(jsonData)
        except ValueError:
            write('Malformed Data')
        else:
            left = 0 #Music
            right = 0 #Music
            if 'color' in dataDict:
                color = dataDict['color']
                GlobalSettings.setColor(color)
            if 'speed' in dataDict:
                speed = dataDict['speed']
                GlobalSettings.setSpeed(speed)
            if 'Music' in dataDict:
                left = dataDict['Music'][0]
                right = dataDict['Music'][1]
            if 'command' in dataDict:
                command = dataDict['command']
                if command == 'Flash':
                    startRoutine(flash_example.flash,name="Flash")
                elif command == 'Stop':
                    write("Stopping...")
                    print("Stopping...")
                    stop()
                    GlobalSettings.inProgress = False
                elif command == 'Clear':
                    startRoutine(flash_example.clear,name="Clear")
                elif command == 'RoundAndRound':
                    startRoutine(RoundAndRound.start,name="RoundAndRound")
                elif command == 'Snake':
                    startRoutine(RoundAndRound.startSnake,name="Snake")
                elif command == 'OutsideIn':
                    startRoutine(RoundAndRound.outsideIn,name="OutsideIn")
                elif command == 'Random':
                    startRoutine(flash_example.random,name="Random")
                elif command == "Solid":
                    startRoutine(flash_example.solid,name="Solid")
                elif command == "Rainbow":
                    startRoutine(flash_example.rainbow,name="Rainbow")
                elif command == "DCStart":
                    startDC();
                elif command == "DCStop":
                    stopDC();
                elif command == "Music":
                    write("Stopping...")
                    print("Stopping...")
                    stop()
                    write("Showing volume...")
                    print("Showing volume; left: "+str(left)+", right: "+str(right))
                    Music.showVolume(left,right,bb)
                elif command == "Show":
                    onLights = dataDict["onLights"]
                    showPixels(onLights)
                else:
                    write('Unrecognized Command\n')


def beginServer():
    while True:
        listen()

beginServer()
