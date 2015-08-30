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
                    print("Stop\n")
                    stop()
                    print("Start Flash\n")
                    write('Starting Flash\n')
                    thread = threading.Thread(target=flash_example.flash,args=(bb, ))
                    thread.daemon = True
                    thread.start()
                    GlobalSettings.inProgress = True
                elif command == 'Stop':
                    write("Stopping\n")
                    stop()
                    GlobalSettings.inProgress = False
                elif command == 'Clear':
                    stop()
                    write('Clearing\n')
                    thread = threading.Thread(target=flash_example.clear,args=(bb, ))
                    thread.daemon = True
                    thread.start()
                    GlobalSettings.inProgress = True
                elif command == 'RoundAndRound':
                    stop()
                    write('Starting Round and Round\n')
                    thread = threading.Thread(target=RoundAndRound.start,args=(bb, ))
                    thread.daemon = True
                    thread.start()
                    GlobalSettings.inProgress = True
                elif command == 'Snake':
                    stop()
                    write('Starting Snake\n')
                    thread = threading.Thread(target=RoundAndRound.startSnake,args=(bb, ))
                    thread.daemon = True
                    thread.start()
                    GlobalSettings.inProgress = True
                elif command == 'OutsideIn':
                    stop()
                    write('Starting OutsideIn\n')
                    thread = threading.Thread(target=RoundAndRound.outsideIn,args=(bb, ))
                    thread.daemon = True
                    thread.start()
                    GlobalSettings.inProgress = True
                elif command == 'Random':
                    stop()
                    write('Starting Random\n')
                    thread = threading.Thread(target=flash_example.random,args=(bb, ))
                    thread.daemon = True
                    thread.start()
                    GlobalSettings.inProgress = True
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
