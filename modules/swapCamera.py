import os
from picamera import PiCamera #
def SwapCamera(camera, permit):
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
