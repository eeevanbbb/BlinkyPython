import time
import BaseHTTPServer

import threading
import subprocess

from BlinkyTape import BlinkyTape

import GlobalSettings

import flash_example
import RoundAndRound
import DynamicColor
import Music
import OutsideInRemix
import Beauty
import Dance

#Blinky Code
bb = BlinkyTape('/dev/ttyACM0',ledCount=150)
p = None

def stop():
    if GlobalSettings.inProgress == True:
        GlobalSettings.keepGoing = False

def startRoutine(routine,name="routine"):
    print("Stopping...")
    stop()
    print("Starting "+name+"...")
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

"""
#This is yet to be supported in the HTTP server 
onLights = {}
for x in range(0,150):
    onLights[x] = False
def showPixels(theOnLights):
    for x in theOnLights:
        onLights[int(x)] = theOnLights[x]
    for x in onLights:
        if onLights[x]:
            bb.sendPixel(GlobalSettings.color[0],GlobalSettings.color[1],GlobalSettings.color[2])
        else:
            bb.sendPixel(0,0,0)
    bb.show()
"""

#Note: Commands should come in as GET requests with the URL pattern:
#192.168.0.137/command/start
#Colors should be sent as hex strings:
#192.168.0.137/color/ffffff
#Speed should be sent as a stringified double:
#192.168.0.137/speed/30.521


#Color conversion code
_NUMERALS = '0123456789abcdefABCDEF'
_HEXDEC = {v: int(v, 16) for v in (x+y for x in _NUMERALS for y in _NUMERALS)}

def rgb(triplet):
    return _HEXDEC[triplet[0:2]], _HEXDEC[triplet[2:4]], _HEXDEC[triplet[4:6]]


#Validate Input
command_list = ["Flash","Stop","Clear","RoundAndRound","Snake","OutsideIn","Random","Solid","Rainbow","DCStart","DCStop","OutsideInRemix","Beauty","FourOnTheFloor","AlternatePush"]

def validateCommand(command):
    if command in command_list:
        return True
    else:
        return False

def validateColor(color):
    if len(color) != 6:
        return False
    for c in color:
        if c not in _NUMERALS:
            return False
    return True

def validateSpeed(speed):
    try:
        theSpeed = float(speed)
    except:
        return False
    if not theSpeed or theSpeed <= 0 or theSpeed > 60:
        return False
    else:
        return True

def validateBPM(bpm):
	try:
		theBPM = int(bpm)
	except:
		return False
	if not theBPM or theBPM <= 0 or theBPM > 600:
		return False
	else:
		return True

#Handle Input
def handleCommand(command):
    if command == "Flash":
        startRoutine(flash_example.flash,name="Flash")
    elif command == "Stop":
        stop()
        GlobalSettings.inProgress = False
    elif command == "Clear":
        startRoutine(flash_example.clear,name="Clear")
    elif command == "RoundAndRound":
        startRoutine(RoundAndRound.start,name="RoundAndRound")
    elif command == "Snake":
        startRoutine(RoundAndRound.startSnake,name="Snake")
    elif command == "OutsideIn":
        startRoutine(RoundAndRound.outsideIn,name="OutsideIn")
    elif command == "Random":
        startRoutine(flash_example.random,name="Random")
    elif command == "Solid":
        startRoutine(flash_example.solid,name="Solid")
    elif command == "Rainbow":
        startRoutine(flash_example.rainbow,name="Rainbow")
    elif command == "Beauty":
        startRoutine(Beauty.start,name="Beauty")
    elif command == "FourOnTheFloor":
        startRoutine(Dance.fourOnTheFloor,name="Four on the Floor")
	elif command == "AlternatePush":
		startRoutine(Dance.alernatePush,name="Alternate Push")
    elif command == "DCStart":
        startDC();
    elif command == "DCStop":
        stopDC();
    elif command == "OutsideInRemix":
        startRoutine(OutsideInRemix.start,name="OutsideInRemix")
    else:
        print("Unrecognized Command")
    print(command)
    
def handleColor(color):
    red, green, blue = rgb(color)
    GlobalSettings.setColor([red,green,blue])
    print("Red: "+str(red)+" Green: "+str(green)+" Blue: "+str(blue))
    
def handleSpeed(speed):
    theSpeed = float(speed)
    GlobalSettings.setSpeed(speed)
    print("Speed: "+str(theSpeed))

def handleBPM(bpm):
	theBPM = int(bpm)
	GlobalSettings.setBPM(bpm)
	print("BPM: "+str(bpm))



#HTTP Server Code, from https://wiki.python.org/moin/BaseHttpServer
HOST_NAME = '192.168.0.137'
#HOST_NAME = 'localhost'
PORT_NUMBER = 9001

class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type","text/html")
        s.end_headers()
    def do_GET(s):
        s.send_response(200)
        s.send_header("Content-type","text/html")
        s.end_headers()
        s.wfile.write("<html><head><title>Blinky Server Response</title></head><body>")
        if s.path == "/request/hello":
            s.wfile.write("<p>Hello! The server is running.</p>")
        elif s.path == "/request/validcommands":
            string = "<ul>"
            for validCommand in command_list:
                string += "<li>" + validCommand + "</li>"
            string+="</ul>"
            s.wfile.write(string)
        else:
            if s.path.startswith("/command/"):
                command = s.path.split("/command/")[1]
                s.wfile.write("<p>Received Command: "+command+"</p>")
                if validateCommand(command) == False:
                    s.wfile.write("<p>Unrecognized Command</p>")
                else:
                    handleCommand(command)
            elif s.path.startswith("/color/"):
                color = s.path.split("/color/")[1]
                s.wfile.write("<p>Received Color: "+color+"</p>")
                if validateColor(color) == False:
                    s.wfile.write("<p>Invalid Color</p>")
                else:
                    handleColor(color)
            elif s.path.startswith("/speed/"):
                speed = s.path.split("/speed/")[1]
                s.wfile.write("<p>Received Speed: "+speed+"</p>")
                if validateSpeed(speed) == False:
                    s.wfile.write("<p>Invalid Speed</p>")
                else:
                    handleSpeed(speed)
			elif s.path.startswith("/bpm/"):
				bpm = s.path.split("/bpm/")[1]
				s.wfile.write("<p>Received BPM: "+bpm+"</p>")
				if validateBPM(bpm) == False:
					s.wfile.write("<p>Invalid BPM</p>")
				else:
					handleBPM(bpm)
            else:
                s.wfile.write("<p>Invalid Route</p>")
            
        
        s.wfile.write("</body></html>")
        
if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), RequestHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
