from __future__ import print_function
import xbox

import time
import atexit

#motor controller
from Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor


# create a default object, no changes to I2C address or frequency
mh = Raspi_MotorHAT(addr=0x6f)

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    mh.getMotor(1).run(Raspi_MotorHAT.RELEASE)
    mh.getMotor(2).run(Raspi_MotorHAT.RELEASE)
    mh.getMotor(3).run(Raspi_MotorHAT.RELEASE)
    mh.getMotor(4).run(Raspi_MotorHAT.RELEASE)

atexit.register(turnOffMotors)


#creates motor objects
################################# DC motor test!
ThrusterVerticalFront = mh.getMotor(1)
ThrusterVerticalBack = mh.getMotor(2)
ThrusterHorizontalLeft = mh.getMotor(3)
ThrusterHorizontalRight = mh.getMotor(4)



#turn motor objects on
ThrusterVerticalFront.run(Raspi_MotorHAT.RELEASE);
ThrusterVerticalBack.run(Raspi_MotorHAT.RELEASE);
ThrusterHorizontalLeft.run(Raspi_MotorHAT.RELEASE);
ThrusterHorizontalRight.run(Raspi_MotorHAT.RELEASE);

#helper functions


#bounding function
#desc: takes a float value between 1 to -1 and outputs a value between 0 and 255
#input:float between 1 to -1
#output int value 0-255
def bounding(x):
    if (x<0):
        return int(x/-1*255)
    return int(x/1*255)


# Format floating point number to string format -x.xxx
def fmtFloat(n):
    return '{:6.3f}'.format(n)

# Print one or more values without a line feed
def show(*args):
    for arg in args:
        print(arg, end="")

# Print true or false value based on a boolean, without linefeed
def showIf(boolean, ifTrue, ifFalse=" "):
    if boolean:
        show(ifTrue)
    else:
        show(ifFalse)


def FireThrusterForward(thruster, throttle):
    thruster.setSpeed(throttle)
    thruster.run(Raspi_MotorHAT.FORWARD)


def FireThrusterBackward(thruster, throttle):
    thruster.setSpeed(throttle)
    thruster.run(Raspi_MotorHAT.BACKWARD)


#arguments(joystick object of xbox, thrusters1-4)
def LeftStickThruster(joy, frontThruster, backThruster, leftThruster, rightThruster):
    AxisY = joy.leftY()
    AxisX = joy.leftX()
    if(AxisY > 0):
        
        FireThrusterForward(leftThruster, bounding(AxisY))
        FireThrusterForward(rightThruster, bounding(AxisY))
        
    elif(AxisY < 0):
        
        FireThrusterBackward(leftThruster, bounding(AxisY))
        FireThrusterBackward(rightThruster, bounding(AxisY))
    
    if(AxisX < 0): #stick is pushed left
        
        FireThrusterForward(rightThruster, bounding(AxisX))
        FireThrusterBackward(leftThruster, bounding(AxisX))
    
    elif(AxisX > 0):#stick is pushed right
        
        FireThrusterForward(leftThruster, bounding(AxisX))
        FireThrusterBackward(rightThruster, bounding(AxisX))
        
# Instantiate the controller
joy = xbox.Joystick()

# Show various axis and button states until Back button is pressed
print("ROV control: Press [Back] button to exit")
# Show connection status
show("Connected:")
showIf(joy.connected(), "Y", "N")
while not joy.Back():
    # Show connection status
    #show("Connected:")
    #showIf(joy.connected(), "Y", "N")
    # Left analog stick
    #show("  Left X/Y:", fmtFloat(joy.leftX()), "/", fmtFloat(joy.leftY()))
    LeftStickThruster(joy, ThrusterVerticalFront, ThrusterVerticalBack, ThrusterHorizontalLeft, ThrusterHorizontalRight)
    
    # Right trigger
    #show("  RightTrg:", fmtFloat(joy.rightTrigger()))
    FireThrusterForward(ThrusterHorizontalLeft,bounding(joy.rightTrigger()))
    
    

# Close out when done
joy.close()
