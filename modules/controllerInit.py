import os
import xbox

from picamera import PiCamera #

def ControllerInit():
    joy = xbox.Joystick() # joy object for our xbox 360 camera
    print("Initializing joy controller")
    return joy 