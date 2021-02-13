def controllerInit():
    import os
    import xbox
    import time
    from picamera import PiCamera #

    joy = xbox.Joystick() # joy object for our xbox 360 camera
    camera = 1# O will be cam a and 1 will be cam b
    permit = False #semiphore to prevent setupt on the
