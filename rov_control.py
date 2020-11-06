#ROV control software v0.1
#EGCP 470

import time
import atexit

import signal

#import Xbox360Controller
from xbox360controller import Xbox360Controller


#!/usr/bin/python
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



#button definitons

def button_pressed(button):
    print('button {0} was pressed'.format(button.name))
    



def ThrusterStop(thruster, button):
    print('button {0} was pressed'.format(button.name))
    print("stopping thruster")
    thruster.run(Raspi_MotorHAT.RELEASE)

def ForwardThrustFull(thruster, button):
    print('button {0} was pressed'.format(button.name))
    print ("Forward! ")
    thruster.setSpeed(255)
    thruster.run(Raspi_MotorHAT.FORWARD)


def BackwardThrustFull(thruster, button):
    print('button {0} was pressed'.format(button.name))
    print("Backward!")
    thruster.setSpeed(255)
    thruster.run(Raspi_MotorHAT.BACKWARD)


def button_pressedF(button):
    print('button {0} was pressed'.format(button.name))
    print ("Forward! ")
    ThrusterHorizontalLeft.setSpeed(255)
    ThrusterHorizontalLeft.run(Raspi_MotorHAT.FORWARD)

def button_pressedB(button):
    print('button {0} was pressed'.format(button.name))
    print ("Backward! ")
    ThrusterHorizontalLeft.setSpeed(255)
    ThrusterHorizontalLeft.run(Raspi_MotorHAT.BACKWARD)



def button_released(button):
    print('button {0} was released'.format(button.name))
    print("stopping thruster")
    ThrusterHorizontalLeft.run(Raspi_MotorHAT.RELEASE)
    
    
def on_axis_moved(axis):
    while(True):
        if not (axis.y<0):
            break
        print(bounding(axis.y))
         
    
    print('Axis {0} moved to [{1}] | [{2}]'.format(axis.name, axis.x, axis.y))
    #while(axis.y < 0):
        #print ("Forward! ")
    #print(bounding(axis.y))
        #myMotor.run(Raspi_MotorHAT.FORWARD)
        #print ("\tSpeed up...")
        #myMotor.setSpeed(i)
        #time.sleep(0.01)

        #print ("\tSlow down...")
        #for i in reversed(range(255)):
         #   myMotor.setSpeed(i)
          #  time.sleep(0.01)

           # print ("Backward! ")
            #myMotor.run(Raspi_MotorHAT.BACKWARD)
    
#def on_trigger_pulled(axis):
#    print('Trigger {0} moved to {1} {2}'.format(axis.name, axis.x, axis.y
    
    
    
#Xbox360Controller Class (index: which controller to use set to 1, axis: sensitivity// leave for now,     
try:
    with Xbox360Controller(0, axis_threshold=0.2) as controller:
        #button A
        controller.button_a.when_pressed = button_pressed
        controller.button_a.when_released = button_released
        
        #button X
        controller.button_x.when_pressed = button_pressed
        controller.button_x.when_released = button_released
        
        #button B
        controller.button_b.when_pressed = button_pressed
        controller.button_b.when_released = button_released
        
        #button Y
        controller.button_y.when_pressed = button_pressed
        controller.button_y.when_released = button_released
        
        #lft and right analog stick
        
        
        controller.axis_l.when_moved = on_axis_moved
        #controller.axis_r.when_moved = on_axis_moved
        
        #right bumper
        controller.button_trigger_r.when_pressed = button_pressedF
        controller.button_trigger_r.when_released = button_released
        
        #controller.button_trigger_r.when_pressed = ForwardThrustFull(ThrusterHorizontalLeft, controller.button_trigger_r.when_pressed)
        #controller.button_trigger_r.when_released = ThrusterStop(ThrusterHorizontalLeft, controller.button_trigger_r.when_released)
        
        #left bumper
        controller.button_trigger_l.when_pressed = button_pressedB
        controller.button_trigger_l.when_released = button_released
        #controller.button_trigger_l.when_pressed = Backwaw(ThrusterHorizontalLeft)
        #controller.button_trigger_l.when_released = ThrusterStop(ThrusterHorizontalLeft)
        
        
        
        
        
        #right trigger
        #controller.button_axis_l.axis.when_moved
        
        
        
        signal.pause()
except KeyboardInterrupt:
    pass
