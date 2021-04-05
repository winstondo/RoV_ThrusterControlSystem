#this should be run on the host computer

from inputs import devices
from inputs import get_gamepad

import os
import time
import RPi.GPIO as GPIO
import pigpio


#desc: function that outputs all connected devices
#dependencies: requires the input module
#i/o: non
def getDevices():
    for device in devices:
        print(device)

class objThruster:
    def __init__(self, name, pin):
        self.name = name
        self.pin = pin

def main():
    #Just print out some event infomation when the gamepad is used.
    while True:
        events = get_gamepad()
        for event in events:
            #print(event.ev_type, event.code, event.state)
            #event state prints out the values for analog inputs
            print(event.state)

if __name__ == "__main__":
    main()

