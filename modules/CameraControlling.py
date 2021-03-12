#joy = xbox.Joystick() # joy object for our xbox 360 camera
import time
global camera  # O will be cam a and 1 will be cam b
camera = 1 
global permit  #semiphore to prevent setupt on the
permit = True

def CamController(arg1):
    global camera
    global permit
    if arg1.Y(): # calls on xbox.py to check button press: 0 -> false, 1 -> true
        print("camera button was pressed")
        time.sleep(.4) #rebounding on button press
        if camera == 0:
            camera = 1
            permit = True
            return True
            #cmd = "raspistill -t 1"
        elif camera == 1:
            camera = 0
            permit = True
            return True
    else :
        permit = False
        return False
