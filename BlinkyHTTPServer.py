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
import Christmas
import Fading

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

#Note: Commands should come in as GET requests with the URL pattern:
#192.168.0.138/command/start
#Colors should be sent as hex strings:
#192.168.0.138/color/ffffff
#Speed should be sent as a stringified double:
#192.168.0.138/speed/30.521
#Manual commands should be sent as follows:
#192.168.0.138/manual/149/ffffff


#Color conversion code
_NUMERALS = '0123456789abcdefABCDEF'
_HEXDEC = {v: int(v, 16) for v in (x+y for x in _NUMERALS for y in _NUMERALS)}

def rgb(triplet):
    return _HEXDEC[triplet[0:2]], _HEXDEC[triplet[2:4]], _HEXDEC[triplet[4:6]]


#Validate Input
command_list = ["Clear","Stop","RoundAndRound","Flash","Snake","OutsideIn","Random","Solid","Rainbow","DCStart","DCStop","OutsideInRemix","Beauty","FourOnTheFloor","AlternatePush","DownbeatPeaks","Dart","Swarm","BrightDark","Christmas1","Christmas2","Christmas3","ChristmasDance","Christmas4","FadeRed","FadeGreen","FadeBlue"]

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

def validateIndex(index):
    try:
        theIndex = int(index)
    except:
        return False
    if not theIndex or theIndex < 0 or theIndex >= 150:
        return False
    else:
        return True

#Handle Input
def handleCommand(command):
    valid = True
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
        startRoutine(Dance.alternatePush,name="Alternate Push")
    elif command == "DownbeatPeaks":
        startRoutine(Dance.downbeatPeaks,name="Downbeat Peaks")
    elif command == "Dart":
        startRoutine(Dance.dart,name="Dart in Four")
    elif command == "Swarm":
        startRoutine(Dance.swarm,name="Swarm")
    elif command == "BrightDark":
        startRoutine(Dance.brightDark,name="Bright-Dark")
    elif command == "Christmas1":
    	startRoutine(Christmas.christmas1,name="Christmas1")
    elif command == "Christmas2":
    	startRoutine(Christmas.christmas2,name="Christmas2")
    elif command == "Christmas3":
    	startRoutine(Christmas.christmas3,name="Christmas3")
    elif command == "ChristmasDance":
    	startRoutine(Christmas.christmasDance,name="ChristmasDance")
    elif command == "Christmas4":
    	startRoutine(Christmas.christmas4,name="Christmas4")
    elif command == "FadeRed":
        startRoutine(Fading.fade_red,name="FadeRed")
    elif command == "FadeGreen":
        startRoutine(Fading.fade_green,name="FadeGreen")
    elif command == "FadeBlue":
        startRoutine(Fading.fade_blue,name="FadeBlue")
    elif command == "DCStart":
        startDC();
    elif command == "DCStop":
        stopDC();
    elif command == "OutsideInRemix":
        startRoutine(OutsideInRemix.start,name="OutsideInRemix")
    else:
        print("Unrecognized Command")
        valid = False
    if valid:
    	if command != "DCStart" and command != "DCStop":
			GlobalSettings.setCommand(command)
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

def handleManualCommand(index,color):
    theIndex = int(index)
    red, green, blue = rgb(color)
    if GlobalSettings.command != "Clear":
        handleCommand("Clear")
    changeLight(theIndex,[red,green,blue])
    print("Light #"+str(theIndex)+": ("+str(red)+","+str(green)+","+str(blue)+")")

colors = {}
for i in range(0,150):
    colors[i] = [0,0,0]
def changeLight(lightIndex,color):
    colors[lightIndex] = color
    for c in colors:
        bb.sendPixel(color[0],color[1],color[2])
    bb.show()


#HTTP Server Code, from https://wiki.python.org/moin/BaseHttpServer
HOST_NAME = '192.168.0.138'
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
        if s.path != "/request/stateJSON" and s.path != "/request/commandsJSON":
            s.wfile.write("<html><head><title>Blinky Server Response</title></head><body>")
        if s.path == "/request/hello":
            s.wfile.write("<p>Hello! The server is running.</p>")
        elif s.path == "/request/validcommands":
            string = "<ul>"
            for validCommand in command_list:
                string += "<li>" + validCommand + "</li>"
            string+="</ul>"
            s.wfile.write(string)
        elif s.path == "/request/commandsJSON":
            string = '{commands:['
            for i in range(0, len(command_list)):
                string += '"' + command_list[i] + '"'
                if i != len(command_list) - 1:
                    string += ','
            string += ']}'
            s.wfile.write(string)
        elif s.path == "/request/state":
        	string = "<p><h1>Command\n</h1>"
        	string += GlobalSettings.command
        	string += "</p><p><h1>Color\n</h1>"
        	color = GlobalSettings.color
        	colorString = "(" + str(color[0]) + "," + str(color[1]) + "," + str(color[2]) + ")"
        	string += colorString
        	string += "</p><p><h1>Speed\n</h1>"
        	string += str(GlobalSettings.speed)
        	string += "</p><p><h1>BPM\n</h1>"
        	string += str(GlobalSettings.bpm)
        	string += "</p><p><h1>DynaColor\n</h1>"
        	string += str(GlobalSettings.dynaColor)
        	string += "</p>"
        	s.wfile.write(string)
        elif s.path == "/request/stateJSON":
            color = GlobalSettings.color
            string = '{'
            string += '"command":"'
            string += GlobalSettings.command + '",'
            string += '"colorR":'
            string += str(color[0]) + ','
            string += '"colorG":'
            string += str(color[1]) + ','
            string += '"colorB":'
            string += str(color[2]) + ','
            string += '"speed":'
            string += str(GlobalSettings.speed) + ','
            string += '"bpm":'
            string += str(GlobalSettings.bpm) + ','
            string += '"dynaColor":'
            string += str(GlobalSettings.dynaColor).lower()
            string += '}'
            s.wfile.write(string)
        else:
            if s.path.startswith("/command/"):
                command = s.path.split("/command/")[1]
                s.wfile.write("<h1>Received Command: "+command+"</h1>")
                if validateCommand(command) == False:
                    s.wfile.write("<h1>Unrecognized Command</h1>")
                else:
                    handleCommand(command)
            elif s.path.startswith("/color/"):
                color = s.path.split("/color/")[1]
                s.wfile.write("<h1>Received Color: "+color+"</h1>")
                if validateColor(color) == False:
                    s.wfile.write("<h1>Invalid Color</h1>")
                else:
                    handleColor(color)
            elif s.path.startswith("/speed/"):
                speed = s.path.split("/speed/")[1]
                s.wfile.write("<h1>Received Speed: "+speed+"</h1>")
                if validateSpeed(speed) == False:
                    s.wfile.write("<h1>Invalid Speed</h1>")
                else:
                    handleSpeed(speed)
            elif s.path.startswith("/bpm/"):
                bpm = s.path.split("/bpm/")[1]
                s.wfile.write("<h1>Received BPM: "+bpm+"</h1>")
                if validateBPM(bpm) == False:
                    s.wfile.write("<h1>Invalid BPM</h1>")
                else:
                    handleBPM(bpm)
            elif s.path.startswith("/manual/"):
                #Expect URLs of the form .../manual/light#/hexColor
                manual_command = s.path.split("/manual/")[1]
                components = manual_command.split("/")
                index = components[0]
                color = components[1]
                if validateIndex(index) == False:
                    s.wfile.write("<h1>Invalid Index</h1>")
                elif validateColor(color) == False:
                    s.wfile.write("<h1>Invalid Color</h1>")
                else:
                    handleManualCommand(index,color)
            else:
                s.wfile.write("<h1>Invalid Route</h1>")

        if s.path != "/request/stateJSON" and s.path != "/request/commandsJSON":
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
