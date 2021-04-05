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


#run sudo pigpiod in console or uncomment out this line. NO LONGER NEEDED.
#os.system ("sudo pigpiod")
#pi = pigpio.pi()

#throttle globals
MAX_THROTTLE = 2000
MIN_THROTTLE = 1000 
NEUTRAL_THROTTLE = 1500 #pulse widths lower than this value will have the thruster fire in reverse
ARMING_INTERVAL = 4 #minimum ammount of time the arming function waits between oscillating the throttles to arm the ESCs

#ESC Calibration
#function to calibrate and initlize all the thrusters. requires a global list of thruster objects

#desc: Arms each thruster on the craft and outputs diagnostic message. First sets throttle to zero then to max and finnally at the neutral value. Sequence given by ESC documentation.
#input:none
#output: none
def arm():
    for thruster in THRUSTER_LIST:    
        print("initilizing:{} at 0".format(thruster.name))
        pi.set_servo_pulsewidth(thruster.pin, 0)
        
        CountSleep(int(ARMING_INTERVAL/2))
        print("initilizing:{} at {}".format(thruster.name, MAX_THROTTLE))
        pi.set_servo_pulsewidth(thruster.pin, MAX_THROTTLE)
        print("5s to turn on power now:" )
        CountSleep(ARMING_INTERVAL)
        
        print("initilizing:{} at {}".format(thruster.name, NEUTRAL_THROTTLE))
        pi.set_servo_pulsewidth(thruster.pin, NEUTRAL_THROTTLE)
        CountSleep(int(ARMING_INTERVAL/2))
    print("Initilization process completed")


#PWM initilization
#ESC_CONTROL_FREQUENCY = 50 #setting the esc pulse control to 50hz


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
    print("Thruster shutdown sequence initiating...")
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

#main thruster control function logic
#desc: takes the output of the controller fires the appropriate thrusters using control logic to orientate the rov 
#input:joystick object, 4 thruster objects (must be in order:FBLR)
#output: none 
#arguments(joystick object of xbox, thrusters1-4)
def ControlThruster(joy, frontThruster, backThruster, leftThruster, rightThruster):
    FireThruster(leftThruster, joy.leftX() + joy.leftY())
    FireThruster(rightThruster, -1*joy.leftX() + joy.leftY())
    #acent and decent control
    FireThruster(frontThruster, joy.rightTrigger())
    FireThruster(backThruster, joy.rightTrigger())
    #backward logic for left trigger reversing.
    FireThruster(frontThruster, -1*joy.leftTrigger())
    FireThruster(backThruster, -1*joy.leftTrigger())
    

        
     
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
ShutDown()
# Close out when done
joy.close()



