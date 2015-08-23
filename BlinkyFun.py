import socket
import json
import threading
import subprocess
import time

from BlinkyTape import BlinkyTape

import GlobalSettings

import flash_example
import RoundAndRound

bb = BlinkyTape('/dev/tty.usbmodemfa131',ledCount=150)
p = None
client_socket = 'None'

def write(message):
    try:
        client_socket.send(message)
    except socket.error:
        print("Socket error\n")

def stop():
    if GlobalSettings.inProgress == True:
        GlobalSettings.keepGoing = False

def beginServer():   
    global bb
    global p
    global client_socket
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    server.bind(('192.168.0.196',4329))
    server.listen(4)
    client_socket, client_address = server.accept()
    while True:
        try:
            received_data = client_socket.recv(128)
        except socket.error:
            beginServer()
            break
        print(received_data)
        jsonData = received_data
        try:
            dataDict = json.loads(jsonData)
        except ValueError:
            write('Malformed Data\n')
        else:
            if 'command' in dataDict:
                command = dataDict['command']
                if command == 'Flash':
                    stop()
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
                else:
                    write('Unrecognized Command\n')
            if 'color' in dataDict:
                color = dataDict['color']
                GlobalSettings.setColor(color)
            if 'speed' in dataDict:
                speed = dataDict['speed']
                GlobalSettings.setSpeed(speed)
                
                
beginServer()