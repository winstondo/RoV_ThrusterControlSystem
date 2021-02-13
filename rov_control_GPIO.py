from __future__ import print_function
import xbox

import time
#import atexit
import RPi.GPIO as GPIO
import pigpio


#Set GPIO numbering mode
#sets the pin numbering to match the boards numbering
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#motor GPIO designation block
FRONT_THRUSTER_PIN = 17
BACK_THRUSTER_PIN = 22
LEFT_THRUSTER_PIN = 23
RIGHT_THRUSTER_PIN = 27
THRUSTER_PIN_LIST = [FRONT_THRUSTER_PIN, BACK_THRUSTER_PIN, LEFT_THRUSTER_PIN, RIGHT_THRUSTER_PIN]

#GPIO initilization as output
GPIO.setup(FRONT_THRUSTER_PIN, GPIO.OUT)
GPIO.setup(BACK_THRUSTER_PIN, GPIO.OUT)
GPIO.setup(LEFT_THRUSTER_PIN, GPIO.OUT)
GPIO.setup(RIGHT_THRUSTER_PIN, GPIO.OUT)


pi = pigpio.pi()
#ESC Calibration
MAX_THROTTLE = 2000
MIN_THROTTLE = 1000
for thruster_pin in THRUSTER_PIN_LIST:
    pi.set_servo_pulsewidth(thruster_pin, MAX_THROTTLE)
    sleep(2)
    pi.set_servo_pulsewidth(thruster_pin, MIN_THROTTLE)
    sleep(2)



#PWM initilization
ESC_CONTROL_FREQUENCY = 50 #setting the esc pulse control to 50hz

frontThruster = GPIO.PWM(FRONT_THRUSTER_PIN, ESC_CONTROL_FREQUENCY)
backThruster = GPIO.PWM(BACK_THRUSTER_PIN, ESC_CONTROL_FREQUENCY)
leftThruster = GPIO.PWM(LEFT_THRUSTER_PIN, ESC_CONTROL_FREQUENCY)
rightThruster = GPIO.PWM(RIGHT_THRUSTER_PIN, ESC_CONTROL_FREQUENCY)

frontThruster.start(0)
backThruster.start(0)
leftThruster.start(0)
rightThruster.start(0)




#helper functions


#bounding function
#desc: takes a float value between 1 to -1 and outputs a value between 0 and r
#input:float between 1 to -1
#output int value 0-r
def bounding(x,r):
    if (x<0):
        return int(x/-1*r)
    return int(x*r)


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


def FireThrusterForward(thruster, throttle): #already uses boudning function to 
    thruster.ChangeDutyCycle(bounding(throttle,12))


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


