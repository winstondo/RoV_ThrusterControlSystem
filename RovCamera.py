#Programmer: Israel Garcia Figueroa
#program: operates the camera on with arducam module
#Team: ROV team
#---------------------------------------------------
import RPi.GPIO as gp 
import os
import xbox
import time
from picamera import PiCamera # 

# gpio being set up for i2c interface
gp.setwarnings(False)
gp.setmode(gp.BOARD)

gp.setup(7, gp.OUT)
gp.setup(11, gp.OUT)
gp.setup(12, gp.OUT)

gp.setup(15, gp.OUT)
gp.setup(16, gp.OUT)
gp.setup(21, gp.OUT)
gp.setup(22, gp.OUT)

gp.output(11, True)
gp.output(12, True)
gp.output(15, True)
gp.output(16, True)
gp.output(21, True)
gp.output(22, True)
#end of i2c setup for camera

joy = xbox.Joystick() # joy object for our xbox 360 camera

camera = 1# O will be cam a and 1 will be cam b 
permit = False #semiphore to prevent setupt on the 
while(1):
    if joy.Y(): # calls on xbox.py to check button press: 0 -> false, 1 -> true
        print("camera button was pressed")
        time.sleep(.4) #rebounding on button press
        if camera == 0:
            camera = 1
            permit = True
            #cmd = "raspistill -t 1"
            os.system(cmd)
            
        elif camera ==1:
            camera =0
            permit =True
    
    if permit == True: # condition will check if to change camera
        print("changing camera to ")
        if camera == 0 :
            permit = False
            i2c = "i2cset -y 1 0x70 0x00 0x04 "
            os.system(i2c)
            gp.output(7, False)
            gp.output(11, False)
            gp.output(12, True)
            print("Camera A")
            cmd = "raspistill -p 0,0,1280,720 -t 1800000  -k" # will time after 30 min
            os.system(cmd)
            
        elif camera == 1:
            permit = False
            i2c = "i2cset -y 1 0x70 0x00 0x06"
            os.system(i2c)
            gp.output(7, False) 
            gp.output(11, True)
            gp.output(12, False)
            print("camera B")
            cmd = "raspistill -p 0,0,1280,720 -t 1800000 -k"
            os.system(cmd)
#                 to end current camera process, press key k then key enter
#                 then press the y button to swap camera