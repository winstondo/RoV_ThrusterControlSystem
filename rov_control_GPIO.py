from __future__ import print_function
import xbox
import os
import time
#import atexit
import RPi.GPIO as GPIO
import pigpio

#Set GPIO numbering mode
#sets the pin numbering to match the BCM which uses GPIO channel numbering
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

pi = pigpio.pi()
if not pi.connected:
    exit()

class objThruster:
    def __init__(self, name, pin):
        self.name = name
        self.pin = pin


#motor GPIO designation block
frontThruster = objThruster("FrontDorsalThruster",11)
backThruster = objThruster("BackDorsalThruster",13)
leftThruster = objThruster("LeftThruster",17)
rightThruster = objThruster("RightThruster",27)
THRUSTER_LIST = [frontThruster, backThruster, leftThruster, rightThruster]

#FRONT_THRUSTER_PIN = 11
#BACK_THRUSTER_PIN = 13
#LEFT_THRUSTER_PIN = 17
#RIGHT_THRUSTER_PIN = 16
#THRUSTER_PIN_LIST = [FRONT_THRUSTER_PIN, BACK_THRUSTER_PIN, LEFT_THRUSTER_PIN, RIGHT_THRUSTER_PIN]




#run sudo pigpiod in console or uncomment out this line
os.system ("sudo pigpiod")
pi = pigpio.pi()
#ESC Calibration
#function to calibrate and initlize all the thrusters. requires a global list of thruster objects

MAX_THROTTLE = 2000
MIN_THROTTLE = 1000 
NEUTRAL_THROTTLE = 1500 #pulse widths lower than this value will have the thruster fire in reverse

def arm():
    for thruster in THRUSTER_LIST:    
        print("initilizing:{} at 0".format(thruster.name))
        pi.set_servo_pulsewidth(thruster.pin, 0)
        #time.sleep(2)
        CountSleep(2)
        print("initilizing:{} at {}".format(thruster.name, MAX_THROTTLE))
        pi.set_servo_pulsewidth(thruster.pin, MAX_THROTTLE)
        print("5s to turn on power now:" )
        CountSleep(5)
        #time.sleep(3)
        print("initilizing:{} at {}".format(thruster.name, NEUTRAL_THROTTLE))
        pi.set_servo_pulsewidth(thruster.pin, NEUTRAL_THROTTLE)
        CountSleep(3)
        #time.sleep(3)
    print("Initilization process completed")


#PWM initilization
#ESC_CONTROL_FREQUENCY = 50 #setting the esc pulse control to 50hz

#frontThruster = GPIO.PWM(FRONT_THRUSTER_PIN, ESC_CONTROL_FREQUENCY)
#backThruster = GPIO.PWM(BACK_THRUSTER_PIN, ESC_CONTROL_FREQUENCY)
#leftThruster = GPIO.PWM(LEFT_THRUSTER_PIN, ESC_CONTROL_FREQUENCY)
#rightThruster = GPIO.PWM(RIGHT_THRUSTER_PIN, ESC_CONTROL_FREQUENCY)



#helper functions


#bounding function DEPRECIATED DO NOT USE
#desc: takes a float value between 1 to -1 and outputs an absolute int value between min and max
#input:float between 1 to -1
#output int value 
def bounding(x, min_val, max_val):
    if(x<0):
        return min_val + int(x/-1*(max_val-min_val))
    return min_val + int(x*(max_val-min_val))


#desc: takes a float value between 1 to -1 and outputs an int value between min and max with zero being the mid value. This uses a linear curve to scale the float value. 
#this function removes the use of a forward and backward thruster function infavor of a single function
#input:float between 1 to -1, a min, max and mid value
#output int value
def linearResponseCurve(x, min_val, mid_val, max_val):
  return int((max_val - min_val)/2 * x + mid_val)

#desc: sleeps for the argument time and outputs a countdown
#input: interger
#output:none 
def CountSleep(seconds):
  for i in range(seconds):
    time.sleep(1)
    print(seconds-i)

    

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

#control functions

#thruster shutoff function
#desc: takes a thruster object and a coresponding throttle value and fires the thruster forward
#input:thruster object
#output: none 
def ShutOffThruster(thruster):
    pi.set_servo_pulsewidth(thruster.pin,NEUTRAL_THROTTLE)

def ShutDown():
    for thruster in THRUSTER_LIST:    
        print("shutting off: {}".format(thruster.name))
        pi.set_servo_pulsewidth(thruster.pin, NEUTRAL_THROTTLE)
        time.sleep(2)
        
   

#thruster fire function
#desc: takes a thruster object and a coresponding throttle value and fires the thruster 
#input:thruster object, throttle value
#output: none 
def FireThruster(thruster, throttle): #already uses boudning function to
    pi.set_servo_pulsewidth(thruster.pin, linearResponseCurve(throttle,MIN_THROTTLE, NEUTRAL_THROTTLE,MAX_THROTTLE))

#thruster forward function
#desc: takes a thruster object and a coresponding throttle value and fires the thruster forward
#input:thruster object, throttle value
#output: none 
#def FireThrusterForward(thruster, throttle): #already uses boudning function to
#    pi.set_servo_pulsewidth(thruster.pin, bounding(throttle,NEUTRAL_THROTTLE,MAX_THROTTLE))

#thruster bkwd function
#desc: takes a thruster object and a coresponding throttle value and fires the thruster backwards
#input:thruster object, throttle value
#output: none 
#def FireThrusterBackward(thruster, throttle):
#    pi.set_servo_pulsewidth(thruster.pin, bounding(throttle, MIN_THROTTLE, NEUTRAL_THROTTLE))

#left analog stick control function
#desc: takes the output of the left analog stick fires the appropriate thrusters using control logic to orientate the rov 
#input:joystick object, 4 thruster objects (must be in order:FBLR)
#output: none 
#arguments(joystick object of xbox, thrusters1-4)
def LeftStickThruster(joy, frontThruster, backThruster, leftThruster, rightThruster):
    AxisY = joy.leftY()
    AxisX = joy.leftX()
    if(AxisY > 0):
        
        FireThrusterForward(leftThruster, AxisY)
        FireThrusterForward(rightThruster,AxisY)
        
    elif(AxisY < 0):
        
        FireThrusterBackward(leftThruster, AxisY)
        FireThrusterBackward(rightThruster, AxisY)
    
    if(AxisX < 0): #stick is pushed left
        
        FireThrusterForward(rightThruster, AxisX)
        FireThrusterBackward(leftThruster, AxisX)
    
    elif(AxisX > 0):#stick is pushed right
        
        FireThrusterForward(leftThruster, AxisX)
        FireThrusterBackward(rightThruster, AxisX)
        

#left analog stick control function
#desc: takes the output of the controller fires the appropriate thrusters using control logic to orientate the rov 
#input:joystick object, 4 thruster objects (must be in order:FBLR)
#output: none 
#arguments(joystick object of xbox, thrusters1-4)
def ControlThruster(joy, frontThruster, backThruster, leftThruster, rightThruster):
    FireThruster(leftThruster, joy.leftX() + joy.leftY())
    FireThruster(rightThruster, -1*joy.leftX() + joy.leftY())
    if (joy.righttrigger() > 0) ):
        FireThruster(leftThruster, joy.righttrigger())
        FireThruster(rightThruster, joy.righttrigger())
    #backward logic for left trigger reversing. 
    elif (joy.lefttrigger() > 0):
        FireThruster(leftThruster, -1*joy.lefttrigger())
        FireThruster(rightThruster, -1*joy.lefttrigger())
    

        
     
# Instantiate the controller
joy = xbox.Joystick()

# Show various axis and button states until Back button is pressed
print("ROV control: Press [Back] button to exit")
# Show connection status
show("Connected:")
showIf(joy.connected(), "Y", "N")
arm()
while not joy.Back():
    # Show connection status
    #show("Connected:")
    #showIf(joy.connected(), "Y", "N")
    # Left analog stick
    #show("  Left X/Y:", fmtFloat(joy.leftX()), "/", fmtFloat(joy.leftY()))
    ControlThruster(joy, frontThruster, backThruster, leftThruster, rightThruster)
    
    
    
print("[Back] button pressed...shutting down")
print("Shutting thrusters off")
ShutDown()
# Close out when done
joy.close()



