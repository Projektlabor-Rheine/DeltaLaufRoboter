import math
import DeltaLaufRoboter as botti
from adafruit_servokit import ServoKit
import time
import RPi.GPIO as gpio

#Max and min values for the servos
minX = -40
maxX = 40
minZ = -120
maxZ = -170

print("Bot is starting")

class Group():
    def __init__(self, address,defaultRot):
        self.defaultRot = defaultRot/360*100
        self.ref = ServoKit(channels=16,address=address)
        for i in range(16):
            self.ref.servo[i].actuation_range = 120
        self.x = 0
        self.y = 0
        self.z = 0

    def moveRot(self,rot,extend,height):
        rot+=self.defaultRot
        rad = math.pi*2*(rot/100)
        x = math.cos(rad)*((maxX-minX)/2)*(extend/100)
        y = math.sin(rad)*((maxX-minX)/2)*(extend/100)
        z = (maxZ-minZ)*(height/100)+minZ

        self.move(x,y,z)

    def move(self,x=None,y=None,z=None):
        if x == None:
            x = self.x

        if y == None:
            y = self.y

        if z == None:
            z = self.z

        #Checks if the group has to move 
        if x != self.x or y != self.y or z != self.z:
            #Calculates the new positions
            botX,botY,botZ = botti.delta_calcInverse(x,y,z)
            r=0
            for i in range(0,10,4):
                self.ref.servo[i].angle = -botX+87
                self.ref.servo[i+1].angle = -botY+87
                self.ref.servo[i+2].angle = -botZ+87
                r+=3

    def angle(self,botX,botY,botZ):
        r=0
        for i in range(0,10,4):
            self.ref.servo[i].angle = botX
            self.ref.servo[i+1].angle = botY
            self.ref.servo[i+2].angle = botZ
            r+=3

groupA = Group(0x40,0)
groupB = Group(0x60,60)

gpio.setup(5,gpio.IN)
gpio.setup(6,gpio.IN)

rotation=0
stopped = True

def walk():
    t = .4
    global rotation

    #A up
    groupA.moveRot(rotation,0,100)
    time.sleep(t)

    #B back
    groupB.moveRot(rotation+50,100,0)
    time.sleep(t)
    #A fordown
    groupA.moveRot(rotation,100,0)
    time.sleep(t)

    #B up
    groupB.moveRot(rotation,0,100)
    time.sleep(t)

    #A back
    groupA.moveRot(rotation+50,100,0)
    time.sleep(t)

    #B forward
    groupB.moveRot(rotation,100,0)
    time.sleep(t)
    
def checkPins():
    #Checks the buttons
    if gpio.input(5) is 1:
       handleUpdate(5)

    if gpio.input(6) is 1:
       handleUpdate(6)
def handleUpdate(pin):
    global rotation
    global stopped

    if pin == 5:
       rotation+=90
       rotation%=360

    if pin == 6:
       stopped = not stopped

while True:
    checkPins()

    if stopped:
       time.sleep(2)
    else:
       walk()
