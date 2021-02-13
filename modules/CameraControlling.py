    joy = xbox.Joystick() # joy object for our xbox 360 camera
    camera = 1# O will be cam a and 1 will be cam b
    permit = False #semiphore to prevent setupt on the

def CameraControlling():
        if joy.Y(): # calls on xbox.py to check button press: 0 -> false, 1 -> true
            print("camera button was pressed")
            time.sleep(.4) #rebounding on button press
            if camera == 0:
                camera = 1
                permit = True
                return true
                #cmd = "raspistill -t 1"

            elif camera ==1:
                camera =0
                permit =True
                return true
        else :
            permit = False
            return False
