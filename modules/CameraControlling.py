#joy = xbox.Joystick() # joy object for our xbox 360 camera
import time
camera = 1 # O will be cam a and 1 will be cam b
permit = False #semiphore to prevent setupt on the

def CamController(arg1):
    if arg1.Y(): # calls on xbox.py to check button press: 0 -> false, 1 -> true
        print("camera button was pressed")
        time.sleep(.4) #rebounding on button press
        if CameraControlling.camera == 0:
            CameraControlling.camera = 1
            CameraControlling.permit = True
            return true
            #cmd = "raspistill -t 1"
        elif CameraControlling.camera ==1:
            CameraControlling.camera = 0
            CameraControlling.permit = True
            return True
    else :
        CameraControllingpermit = False
        return False
