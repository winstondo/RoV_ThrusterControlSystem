import RPi.GPIO as gp
import os
from picamera import PiCamera
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

def main():
    #print("Start testing the camera A")
    a = 0; #this will be for the input form the xbox controller which is initialized to 0
    while(1):
        #read input from the xbox controller which will button Y
        if (a == 0): 
            i2c = "i2cset -y 1 0x70 0x00 0x04"
            os.system(i2c)
            gp.output(7, False)
            gp.output(11, False)
            gp.output(12, True)
            capture(1)

    #rint("Start testing the camera C")
        elif (a == 1): # 
            i2c = "i2cset -y 1 0x70 0x00 0x06"
            os.system(i2c)
            gp.output(7, False)
            gp.output(11, True)
            gp.output(12, False)
            start_preview(); 
            capture(3)


def capture(cam):
    cmd = "raspistill -t 0 "
    os.system(cmd)

if __name__ == "__main__":
    main()

    gp.output(7, False)
    gp.output(11, False)
    gp.output(12, True)