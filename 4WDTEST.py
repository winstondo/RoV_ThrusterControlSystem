#!/usr/bin/python
from evdev import InputDevice , categorize, ecodes
from select import select
from Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor

import atexit
import time
import Robot

dev = InputDevice('/dev/input/event0') 
print(dev)
mh = Raspi_MotorHAT(addr=0x6f)

def stop():
	mh.getMotor(1).run(Raspi_MotorHAT.RELEASE)
	mh.getMotor(2).run(Raspi_MotorHAT.RELEASE)
	mh.getMotor(3).run(Raspi_MotorHAT.RELEASE)
	mh.getMotor(4).run(Raspi_MotorHAT.RELEASE)

atexit.register(stop)

mh.getMotor(1).setSpeed(50)
mh.getMotor(2).setSpeed(50)
mh.getMotor(3).setSpeed(50)
mh.getMotor(4).setSpeed(50)


def forward():
        mh.getMotor(1).run(Raspi_MotorHAT.FORWARD)
        mh.getMotor(2).run(Raspi_MotorHAT.FORWARD)
        mh.getMotor(3).run(Raspi_MotorHAT.FORWARD)
        mh.getMotor(4).run(Raspi_MotorHAT.FORWARD)
def back():
        mh.getMotor(1).run(Raspi_MotorHAT.BACKWARD)
        mh.getMotor(2).run(Raspi_MotorHAT.BACKWARD)
        mh.getMotor(3).run(Raspi_MotorHAT.BACKWARD)
        mh.getMotor(4).run(Raspi_MotorHAT.BACKWARD)
def right():
        mh.getMotor(1).run(Raspi_MotorHAT.FORWARD)
        mh.getMotor(2).run(Raspi_MotorHAT.FORWARD)
        mh.getMotor(3).run(Raspi_MotorHAT.BACKWARD)
        mh.getMotor(4).run(Raspi_MotorHAT.BACKWARD)
def left():
        mh.getMotor(1).run(Raspi_MotorHAT.BACKWARD)
        mh.getMotor(2).run(Raspi_MotorHAT.BACKWARD)
        mh.getMotor(3).run(Raspi_MotorHAT.FORWARD)
        mh.getMotor(4).run(Raspi_MotorHAT.FORWARD)

while (True):

        for event in dev.read_loop():

            if (event.code == 103 and event.value == 1):
                print "Forward"
                print(event.value)
                forward();
	        time.sleep(0.5)
            elif (event.code == 108 and event.value == 1):
                print  "Back"
                print(event.value)
                back();
	        time.sleep(0.5)
            elif (event.code == 106 and event.value == 1) :
                print "right"
                print(event.value)
                right();
                time.sleep(0.5)
            elif (event.code == 105 and event.value == 1) :
                print "left"
                print(event.value)
                left();
                time.sleep(0.5)
            elif (event.code == 28 and event.value == 1) :
                print "Stop"
                stop();

