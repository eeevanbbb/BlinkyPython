import socket
import json
import threading
import subprocess
import time

from BlinkyTape import BlinkyTape

import GlobalSettings

import flash_example
import RoundAndRound

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
            if 'command' in dataDict:
                command = dataDict['command']
                if command == 'Flash':
                    startRoutine(flash_example.flash,name="Flash")
                elif command == 'Stop':
                    write("Stopping\n")
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
                    startRoutine(flash_example.rainbox,name="Rainbox")
                else:
                    write('Unrecognized Command\n')
            if 'color' in dataDict:
                color = dataDict['color']
                GlobalSettings.setColor(color)
            if 'speed' in dataDict:
                speed = dataDict['speed']
                GlobalSettings.setSpeed(speed)
                

def beginServer():
    while True:
        listen()
            
beginServer()
