#Programmer: Israel Garcia Figueroa
#program: operates the camera on with arducam module
#Team: ROV team
#---------------------------------------------------
import pygame
import sys
import time 
import pygame.camera

import RPi.GPIO as gp
import os
#import xbox
import time
from picamera import PiCamera #

import threading
class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
    def run(self):
        camA = Capture()
        
        camA.main()

class Capture(object):
    def __init__(self):
        self.size = (640,480)
        # create a display surface. standard pygame stuff
        self.display = pygame.display.set_mode(self.size, 0)

        # this is the same as what we saw before
        self.clist = pygame.camera.list_cameras()
        if not self.clist:
            raise ValueError("Sorry, no cameras detected.")
        self.cam = pygame.camera.Camera(self.clist[0], self.size)
        self.cam.start()

        # create a surface to capture to.  for performance purposes
        # bit depth is the same as that of the display surface.
        self.snapshot = pygame.surface.Surface(self.size, 0, self.display)

    def get_and_flip(self):
        # if you don't want to tie the framerate to the camera, you can check
        # if the camera has an image ready.  note that while this works
        # on most cameras, some will never return true.
        if self.cam.query_image():
            self.snapshot = self.cam.get_image(self.snapshot)

        # blit it to the display surface.  simple!
        self.display.blit(self.snapshot, (0,0))
        pygame.display.flip()

    def main(self):
        pygame.joystick.init()
        going = True
        print("starting live feed")

        while going:
            #event = pygame.event.get()
            for event in pygame.event.get(): # User did something.
                print("in for loop")
                if event.type == pygame.QUIT or event.type == pygame.JOYBUTTONDOWN: # If user clicked close.
                    print("closing camera")
                    going = False # Flag that we are done so we exit this loop.
                    self.cam.stop()

            if(going):
                self.get_and_flip()
            
            
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

pygame.init()
WINDOW_HEIGHT = 700
WINDOW_WIDTH = 500
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

pygame.joystick.init()
pygame.camera.init()
#joy = xbox.Joystick() # joy object for our xbox 360 camera


camera = 0# O will be cam a and 1 will be cam b
permit = False #semiphore to prevent setupt on the
done  = False
while(not done):
    for event in pygame.event.get(): # User did something.
        if event.type == pygame.QUIT: # If user clicked close.
            print("closing")
            done = True # Flag that we are done so we exit this loop.
        elif event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
        elif event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")    
    joystick_count = pygame.joystick.get_count()
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

        try:
            jid = joystick.get_instance_id()
        except AttributeError:
            # get_instance_id() is an SDL2 method
            jid = joystick.get_id()

        # Get the name from the OS for the controller/joystick.
        name = joystick.get_name()
        #print(name)
        

        try:
            guid = joystick.get_guid()
        except AttributeError:
            # get_guid() is an SDL2 method
            pass
        else:
            print(guid)
    buttons = joystick.get_numbuttons()
    for i in range(buttons):
        button = joystick.get_button(i)
        if(button == True and i == 6):
            done = True
        if(button == True and i ==  3): # button press: 0 -> false, 1 -> true
            print("camera button was pressed")
            time.sleep(.4) #rebounding on button press
            if camera == 0:
                camera = 1
                permit = True
                #cmd = "raspistill -t 1"
                #os.system(cmd)

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
            threadA = myThread(1,"Camera A", 1)
            threadA.start()
            #cmd = "raspistill -p 10,10,852,480 -t 1800000  -k &" # will time after 30 min
            #os.system(cmd)

        elif camera == 1:
            permit = False
            i2c = "i2cset -y 1 0x70 0x00 0x06"
            os.system(i2c)
            gp.output(7, False)
            gp.output(11, True)
            gp.output(12, False)
            print("camera B")
            camB = Capture()
        
            camB.main()
            print("closed camera B")
            #cmd = "raspistill -p 10,10,852,480 -t 1800000 -k &"
            #os.system(cmd)
#                 to end current camera process, press key k then key enter
#                 then press the y button to swap camera
#  NOTE: the keystorks must be within the terminal or else the operation will not work.
