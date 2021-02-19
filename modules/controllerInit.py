
import xbox



def ControllerInit():
    joy = xbox.Joystick() # joy object for our xbox 360 camera
    print("Initializing joy controller")
    return joy 