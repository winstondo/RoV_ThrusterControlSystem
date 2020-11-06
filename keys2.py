#!/usr/bin/python

from evdev import InputDevice, categorize, ecodes

dev = InputDevice('/dev/input/event0')

print(dev)



for event in dev.read_loop():

   if event.type == ecodes.EV_KEY:

      print(categorize(event))
      print(event.code)
      print(event.value)
