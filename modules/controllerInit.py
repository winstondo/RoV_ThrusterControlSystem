import os
import xbox
import time
from picamera import PiCamera #

def ControllerInit():
    joy = xbox.Joystick() # joy object for our xbox 360 camera
