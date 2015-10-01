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


#Handle Input
def handleCommand(command):
    if command == 'Flash':
        startRoutine(flash_example.flash,name="Flash")
    elif command == 'Stop':
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
    print(str(theSpeed))



#HTTP Server Code, from https://wiki.python.org/moin/BaseHttpServer
#HOST_NAME = '192.168.0.137'
HOST_NAME = 'localhost'
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
        s.wfile.write("<html><head><title>Blinky Server Response</title></head>")
        if s.path == "/request/hello":
            s.wfile.write("<body><p>Hello! The server is running.</p>")
        else:
            if s.path.startswith("/command/"):
                handleCommand(s.path.split("/command/")[1])
            if s.path.startswith("/color/"):
                handleColor(s.path.split("/color/")[1])
            if s.path.startswith("/speed/"):
                handleSpeed(s.path.split("/speed/")[1])
        
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