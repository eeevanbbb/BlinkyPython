import socket
import json
import threading
import subprocess
import time

from BlinkyTape import BlinkyTape

import flash_example
import RoundAndRound

bb = BlinkyTape('/dev/tty.usbmodemfa131',ledCount=150)
lastCommand = 'None'
p = None
client_socket = 'None'

def write(message):
    try:
        client_socket.send(message)
    except socket.error:
        print("Socket error\n")

def stop(command):
    client_socket.send("Stopping "+command+"\n")
    if command == 'Flash':
        flash_example.stopFlash()
    elif command == 'RoundAndRound' or command == 'Snake':
        RoundAndRound.stop()

def beginServer():   
    global bb
    global lastCommand
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
            if 'command' not in dataDict or 'color' not in dataDict or 'speed' not in dataDict:
                write('Missing command, color, or speed\n')
            else:
                command = dataDict['command']
                color = dataDict['color']
                speed = dataDict['speed']
                if command == 'Flash':
                    stop(lastCommand)
                    write('Starting Flash\n')
                    thread = threading.Thread(target=flash_example.flash,args=(bb,color,speed, ))
                    thread.daemon = True
                    thread.start()
                elif command == 'Stop':
                    stop(lastCommand)
                #elif command == 'DiscoParty':
                #    client_socket.send('Starting DiscoParty\n')
                #    bb = None
                #    p = subprocess.Popen(['processing-java', '--sketch=/Users/Evan/Documents/Processing/libraries/BlinkyTape/examples/DiscoParty', '--run'])
                elif command == 'RoundAndRound':
                    stop(lastCommand)
                    write('Starting Round and Round\n')
                    thread = threading.Thread(target=RoundAndRound.start,args=(bb,color,speed, ))
                    thread.daemon = True
                    thread.start()
                elif command == 'Snake':
                    stop(lastCommand)
                    write('Starting Snake\n')
                    thread = threading.Thread(target=RoundAndRound.startSnake,args=(bb,color,speed, ))
                    thread.daemon = True
                    thread.start()
                else:
                    write('Unrecognized Command\n')
                lastCommand = command
                
                
beginServer()