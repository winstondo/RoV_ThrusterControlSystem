#!/usr/bin/python
from evdev import InputDevice , categorize, ecodes
from select import select
dev = InputDevice('/dev/input/event0') 
print(dev)
for event in dev.read_loop():

    if event.code == 103:
        print "Forward"
        print(event.value)
    elif event.code == 108:
        print  "Back"
        print(event.value)
    elif event.code == 106:
        print "right"
        print(event.value)
    elif event.code == 105:
        print "left"
        print(event.value)
