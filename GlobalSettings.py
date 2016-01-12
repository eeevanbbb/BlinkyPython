color = [0,0,255]
speed = 1.0
keepGoing = True
inProgress = False
dynaColor = False
bpm = 120
command = "None"

def setColor(_color):
    if dynaColor is False:
        global color
        color = _color

def setSpeed(_speed):
    global speed
    speed = _speed

def setBPM(_bpm):
	global bpm
	bpm = _bpm

def setCommand(_command):
	global command
	command = _command