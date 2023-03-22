#ROV Team K
#Winston Do

#program disc: this should be on the host computer with the same directory as the camera control script. It does NOT need to be run directly, unless for testing.
#It interprets input from the xbox controller and controls the ROV through the ethernet cable
#UI partially based on https://www.pygame.org/docs/ref/joystick.html

import pygame 
import time
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
from multiprocessing import Process #for simultaneous thruster arming

from threading import Thread #not true parralism but the application is I/O bound so concurrancy sho

#class definitions

# This is a simple class that will help us print to the screen.
# It has nothing to do with the joysticks, just outputting the
# information.
class TextPrint(object):
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def tprint(self, screen, textString, FONT_COLOR):
        textBitmap = self.font.render(textString, True, FONT_COLOR)
        screen.blit(textBitmap, (self.x, self.y))
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10


#helper functions

#desc: rescales values between an arbitary set of values [a,b] given the min_val and max_val
#input: (x) value to be rescaled, (a,b) new range values, min and max values of original 
#output: rescaled value
def MinMaxNormalization(x, a, b, min_val, max_val):
    return a + (((x - min_val) * (b-a))/(max_val - min_val))

#desc: clamps a value between the min_val and max_val
#input: (x) value to be rescaled, min and max values  
#output: clamped value
def clamp(x, min_val, max_val):
    return(max(min_val, min(x, max_val)))

#desc: sleeps for the argument time and outputs a countdown
#input: interger
#output:none 
def CountSleep(seconds):
  for i in range(seconds):
    time.sleep(1)
    print(seconds-i)


#device functions

#desc: Arms each thruster on the craft and outputs diagnostic message. First sets throttle to zero then to max and finnally at the neutral value. Sequence given by ESC documentation.
#input:(arming_interval) time the arming function waits between oscillating between the thrusters neutral and max pulse width for ESC calibration
#input: (thrusters) dictionary of all thruster objects of the Servo class, each identified by keys ("Front","Left", etc)
#output: none
def armSerial(arming_interval, thrusters):
    for thruster in thrusters.values():    
        print("initilizing:{} at MAX_PW".format(thruster))
        #thruster.max()
        thruster.value = 1
        print("PULSE WIDTH At:", thruster.pulse_width)
        print(arming_interval, " to turn on power now:")
        CountSleep(arming_interval)
        print("initilizing:{} at NEUTRAL".format(thruster))
        #thruster.mid()
        thruster.value = 0
        print("PULSE WIDTH At:", thruster.pulse_width)
        CountSleep(int(arming_interval/2))
        thruster.value = 0
    print("Initilization process completed")

#desc: Shuts down all thrusters.
#input: (thrusters) dictionary of all thruster objects of the Servo class, each identified by keys ("Front","Left", etc)
#output: none
def ShutDown(thrusters):
    print("Thruster shutdown sequence initiating...")
    for thruster in thrusters.values():    
        print("shutting off: {}".format(thruster))
        thruster.mid()
        time.sleep(0.5)


#desc: Arms the given thruster and outputs a diagnostic message
#input:(arming_interval) time the arming function waits between oscillating between the thrusters neutral and max pulse width for ESC calibration
#input: (thruster) thruster to be armed
#output: none
def armThruster(arming_interval, thruster):
    print("initialilzing: {} at {}".format(thruster, thruster.pulse_width))
    thruster.max()
    print(arming_interval, " to turn on power now:")
    CountSleep(arming_interval)
    print("throttling out: {} at {}".format(thruster, thruster.pulse_width))
    thruster.mid()

#desc: Arms each thruster on the craft simultaneously. Depends on the multiprocessing module
#input:(arming_interval) time the arming function waits between oscillating between the thrusters neutral and max pulse width for ESC calibration
#input: (thrusters) dictionary of all thruster objects of the Servo class, each identified by keys ("Front","Left", etc)
#output: none
def armMultiProcess(arming_interval, thrusters):
    #for thruster in thrusters.values():    
    ProcessArmF = Process(target=armThruster, args=(arming_interval, thrusters['Front']))
    ProcessArmF.start()
    ProcessArmB = Process(target=armThruster, args=(arming_interval, thrusters['Back']))
    ProcessArmB.start()
    ProcessArmL = Process(target=armThruster, args=(arming_interval, thrusters['Left']))
    ProcessArmL.start()
    ProcessArmR = Process(target=armThruster, args=(arming_interval, thrusters['Right']))
    ProcessArmR.start()

    ProcessArmF.join()
    ProcessArmB.join()
    ProcessArmL.join()
    ProcessArmR.join()
    print("Multi Process initilization process completed")

#desc: Arms each thruster on the craft simultaneously. Depends on the multiprocessing module
#input:(arming_interval) time the arming function waits between oscillating between the thrusters neutral and max pulse width for ESC calibration
#input: (thrusters) dictionary of all thruster objects of the Servo class, each identified by keys ("Front","Left", etc)
#output: none
def armMultiThreaded(arming_interval, thrusters):
    #for thruster in thrusters.values():    
    ThreadArmF = Thread(target=armThruster, args=(arming_interval, thrusters['Front']))
    ThreadArmF.start()
    ThreadArmB = Thread(target=armThruster, args=(arming_interval, thrusters['Back']))
    ThreadArmB.start()
    ThreadArmL = Thread(target=armThruster, args=(arming_interval, thrusters['Left']))
    ThreadArmL.start()
    ThreadArmR = Thread(target=armThruster, args=(arming_interval, thrusters['Right']))
    ThreadArmR.start()

    ThreadArmF.join()
    ThreadArmB.join()
    ThreadArmL.join()
    ThreadArmR.join()
    print("Multithreaded initilization process completed")


# -------- Main Program Loop -----------
#desc: This is the main program loop that polls the controller for input as well as creates the UI window. Automatically exits if the user exits the UI window.
#input: (UPS) an int value that tells the program how many times a second to poll the controller and update the UI window
#input: (WINDOW_HEIGHT, WINDOW_WIDTH) two interger values that tells the main program how large to draw the window
#input: (thrusters) (thrusters) dictionary of all thruster objects of the Servo class, each identified by keys ("Front","Left", etc)
#output:none 
def MainControlLoop(UPS, WINDOW_HEIGHT, WINDOW_WIDTH, thrusters, SCREEN_BACKGROUND_COLOR, FONT_COLOR):
    
    pygame.init()

    # Set the width and height of the screen (width, height).
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    pygame.display.set_caption("ROV Controller Diagnostic")

    # Loop until the user clicks the close button.
    bDone = False

    # Used to manage how fast the screen updates.
    clock = pygame.time.Clock()

    # Initialize the joysticks.
    pygame.joystick.init()

    # Get ready to print.
    textPrint = TextPrint()

    while not bDone:
        #
        # EVENT PROCESSING STEP
        #
        # Possible joystick actions: JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN,
        # JOYBUTTONUP, JOYHATMOTION
        for event in pygame.event.get(): # User did something.
            if event.type == pygame.QUIT: # Triggered if window is closed
                bDone = True # Flag that we are done so we exit this loop.
            elif event.type == pygame.JOYBUTTONDOWN:
                print("Joystick button pressed.")
            elif event.type == pygame.JOYBUTTONUP:
                print("Joystick button released.")

        #
        # DRAWING STEP
        #
        # First, clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.
        screen.fill(SCREEN_BACKGROUND_COLOR)
        textPrint.reset()

        # Get count of joysticks.
        joystick_count = pygame.joystick.get_count()

        textPrint.tprint(screen, "Number of joysticks: {}".format(joystick_count), FONT_COLOR)
        textPrint.indent()

        # For each joystick:
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()

            try:
                jid = joystick.get_instance_id()
            except AttributeError:
                # get_instance_id() is an SDL2 method
                jid = joystick.get_id()
            textPrint.tprint(screen, "Joystick {}".format(jid), FONT_COLOR)
            textPrint.indent()

            # Get the name from the OS for the controller/joystick.
            name = joystick.get_name()
            textPrint.tprint(screen, "Joystick name: {}".format(name), FONT_COLOR)

            try:
                guid = joystick.get_guid()
            except AttributeError:
                # get_guid() is an SDL2 method
                pass
            else:
                textPrint.tprint(screen, "GUID: {}".format(guid), FONT_COLOR)

            # Usually axis run in pairs, up/down for one, and left/right for
            # the other.
            axes = joystick.get_numaxes()
            textPrint.tprint(screen, "Number of axes: {}".format(axes), FONT_COLOR)
            textPrint.indent()

            #for i in range(axes):
                #axis = joystick.get_axis(i)
                #textPrint.tprint(screen, "Axis {} value: {:>6.3f}".format(i, axis,), FONT_COLOR)
            
            trigger_coeff = 1.0
            #axis designation block
            flJoyLeftX = -1*joystick.get_axis(0)
            flJoyLeftY =  joystick.get_axis(1) #pygames returns the Y axis on the joysticks as inverted for a stupid reason
            flJoyRightX = joystick.get_axis(2)
            flJoyRightY = -1*joystick.get_axis(3) #pygames returns the Y axis on the joysticks as inverted because stupid 
            flLeftTrigger = MinMaxNormalization(joystick.get_axis(4)*trigger_coeff, 0.0, 1.0, -1.0, 1.0) #pygames has the triggers between [-1,1] with the 0 outputing only if the trigger is squeezed half way.
            flRightTrigger = MinMaxNormalization(joystick.get_axis(5)* trigger_coeff, 0.0, 1.0, -1.0, 1.0) #should correct trigger values to ranges [0,1] unless a button is pressed then the thing over normalizes
            

            textPrint.tprint(screen, "JoyLeftX is value: {:>6.3f}".format(flJoyLeftX), FONT_COLOR)
            textPrint.tprint(screen, "JoyLeftY is value: {:>6.3f}".format(flJoyLeftY), FONT_COLOR)
            textPrint.tprint(screen, "JoyRightX is value: {:>6.3f}".format(flJoyRightX), FONT_COLOR)
            textPrint.tprint(screen, "JoyRightY is value: {:>6.3f}".format(flJoyRightY), FONT_COLOR)
            textPrint.tprint(screen, "LeftTrigger is value: {:>6.3f}".format(flLeftTrigger), FONT_COLOR)
            textPrint.tprint(screen, "RightTrigger is value: {:>6.3f}".format(flRightTrigger), FONT_COLOR)
            textPrint.unindent()
            textPrint.indent()
            #somewhat inelegant, can be improved
            lThrust_val = clamp(flJoyLeftX + flJoyLeftY, -1, 1)
            rThrust_val = clamp(-1*flJoyLeftX + flJoyLeftY, -1, 1)
            #lThrust_val = flJoyLeftX
            #rThrust_val = flJoyLeftX

            #thruster control logic for left analog stick and diagnostic display

            thrusters["Left"].value = lThrust_val
            thrusters["Right"].value = -1*rThrust_val

            textPrint.tprint(screen, "{:>6.3f} input -> LeftThruster with PULSE WIDTH: {:>6.5f}".format(-1*lThrust_val, thrusters["Left"].pulse_width), FONT_COLOR)
            textPrint.tprint(screen, "{:>6.3f} input -> RightThruster with PULSE WIDTH: {:>6.5f}".format(rThrust_val, thrusters["Right"].pulse_width), FONT_COLOR)

            
            fwrd_val = flRightTrigger
            bck_val = flLeftTrigger 
            

            #compensates for the wiring
            thrusters["Front"].value = -1 * fwrd_val
            thrusters["Back"].value = fwrd_val
            thrusters["Front"].value = bck_val
            thrusters["Back"].value = -1 * bck_val

            textPrint.tprint(screen, "{:>6.3f} -> FrontThruster with PULSE WIDTH: {:>6.3f}".format(fwrd_val, thrusters["Front"].pulse_width), FONT_COLOR)
            textPrint.tprint(screen, "{:>6.3f} -> BackThruster with PULSE WIDTH: {:>6.3f}".format(bck_val, thrusters["Back"].pulse_width), FONT_COLOR)

            textPrint.unindent()

            buttons = joystick.get_numbuttons()
            textPrint.tprint(screen, "Number of buttons: {}".format(buttons), FONT_COLOR)
            textPrint.indent()

            for i in range(buttons):
                button = joystick.get_button(i)
                textPrint.tprint(screen,
                                 "Button {:>2} value: {}".format(i, button), FONT_COLOR)
            textPrint.unindent()

            hats = joystick.get_numhats()
            textPrint.tprint(screen, "Number of hats: {}".format(hats), FONT_COLOR)
            textPrint.indent()

            # Hat position. All or nothing for direction, not a float like
            # get_axis(). Position is a tuple of int values (x, y).
            for i in range(hats):
                hat = joystick.get_hat(i)
                textPrint.tprint(screen, "Hat {} value: {}".format(i, str(hat)), FONT_COLOR)
            textPrint.unindent()

            textPrint.unindent()

        #
        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
        #

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # How often the loop updates or polls the controller
        clock.tick(UPS)

    # Close the window and quit.
    # If you forget this line, the program will 'hang'
    # on exit if running from IDLE.
    pygame.quit()


#desc: This function connects the thrusters with the RPs GPIO Remotely
#input: (hostname) This is the RPi's hostname but can also be an IP address. Ensure that remoteGPIO is configured on on the RPi
#input: (min_pw, max_pw) range of pulse width modulation variables in seconds
#input: (i...TPin) int values that the thrusters are connected to. thrusters are always in FBLR order and ins are in GP.BCM mode
#output: a dictionary of thruster objects. call the thruster objects by their key ["Front"], etc
def ConnectToNetworkGPIO(hostname, MIN_PW, MAX_PW, iFrontTPin, iBackTPin, iLeftTPin, iRightPin):
    #sets the pinfactory which enables networking features. This class can take IP addresses, but host names are more constant.
    remote_host = PiGPIOFactory(host=hostname) 

    #pulse width units for the Servo class are in seconds, below are the default values
    #Servo(pin, *, initial_value=0, min_pulse_width=1/1000, max_pulse_width=2/1000, frame_width=20/1000, pin_factory=None)

    objFrontThruster = Servo(iFrontTPin, min_pulse_width=MIN_PW, max_pulse_width=MAX_PW, pin_factory=remote_host)
    objBackThruster = Servo(iBackTPin, min_pulse_width=MIN_PW, max_pulse_width=MAX_PW, pin_factory=remote_host)
    objLeftThruster = Servo(iLeftTPin, min_pulse_width=MIN_PW, max_pulse_width=MAX_PW, pin_factory=remote_host)
    objRightThruster = Servo(iRightPin, min_pulse_width=MIN_PW, max_pulse_width=MAX_PW, pin_factory=remote_host)

    #dictionary of thruster servo objects
    thrusters = {
        "Front": objFrontThruster,
        "Back": objBackThruster,
        "Left": objLeftThruster,
        "Right": objRightThruster    
    }
    return thrusters


#used to test different arming fucntions that use concurrency
def debugArm(ARMING_INTERVAL, THRUSTERS):
    x = 0
    x = input("Enter which arming mode to use\n 0 - serial arming \n 1 - multithreaded arming\n 2 - multiprocess arming " )
    x = int(x)
    if (x == 0):
        armSerial(ARMING_INTERVAL, THRUSTERS)
    elif (x == 1):
        armMultiThreaded(ARMING_INTERVAL, THRUSTERS)
    elif (x == 2):
        armMultiProcess(ARMING_INTERVAL, THRUSTERS)
    else:
        armSerial(ARMING_INTERVAL, THRUSTERS)

def main(config):

    #config variables
    UPDATE_SPEED = config.getint('MAIN','UPDATE_SPEED', fallback=60)
    USE_MULTITHREADED_ARM = config.getboolean('MAIN', 'USE_MULTITHREADED_ARM', fallback=False)
    USE_DEBUG_MODE = config.getboolean('MAIN', 'USE_DEBUG_MODE', fallback=True)
  
    #host
    CLIENT_NAME = config.get('NETWORKING', 'CLIENT_NAME', fallback='raspberrypi')

    #ui

    SCREEN_BACKGROUND_COLOR = pygame.Color(config.get('UI', 'SCREEN_BACKGROUND_COLOR', fallback='black'))
    FONT_COLOR = pygame.Color(config.get('UI', 'FONT_COLOR', fallback='white'))
    WINDOW_HEIGHT = config.getint('UI', 'WINDOW_HEIGHT', fallback=600)
    WINDOW_WIDTH = config.getint('UI', 'WINDOW_WIDTH', fallback=600)

    #Pulse Width (units in s)
    MAX_PW = config.getfloat('THRUSTERCONFIG','MAX_PW', fallback=2E-3)

    MIN_PW = config.getfloat('THRUSTERCONFIG','MIN_PW', fallback=1E-3)
    ARMING_INTERVAL = config.getint('THRUSTERCONFIG','ARMING_INTERVAL', fallback=2)
    #thruster pins
    FRONT_THRUSTER_PIN = config.getint('THRUSTERCONFIG','FRONT_THRUSTER_PIN', fallback=17)
    BACK_THRUSTER_PIN = config.getint('THRUSTERCONFIG','BACK_THRUSTER_PIN', fallback=27)
    LEFT_THRUSTER_PIN = config.getint('THRUSTERCONFIG','LEFT_THRUSTER_PIN', fallback=22)
    RIGHT_THRUSTER_PIN = config.getint('THRUSTERCONFIG','RIGHT_THRUSTER_PIN', fallback=23)

    #SCREEN_BACKGROUND_COLOR = pygame.Color('black')
    #FONT_COLOR = pygame.Color('white')
    #UI window dimentions in pixels
    #WINDOW_HEIGHT = 600
    #WINDOW_WIDTH = 600
    #Pulse Width (units in s)
    #MAX_PW = 2E-3
    #MIN_PW = 1E-3 
    #FRAME_WIDTH = 20E-3   #The length of time between servo control pulses measured in seconds. Using defaults of 20ms which is a common value for servos.
    #NEUTRAL_THROTTLE = 1500 #pulse widths lower than this value will have the thruster fire in reverse
    #ARMING_INTERVAL = 2 #minimum ammount of time the arming function waits between oscillating the throttles to arm the ESCs


    #=======================================================
    #THRUSTERS = ConnectToNetworkGPIO("raspberrypi", MIN_PW, MAX_PW, FRONT_THRUSTER_PIN, BACK_THRUSTER_PIN, LEFT_THRUSTER_PIN, RIGHT_THRUSTER_PIN) 
    THRUSTERS = ConnectToNetworkGPIO(CLIENT_NAME, MIN_PW, MAX_PW, FRONT_THRUSTER_PIN, BACK_THRUSTER_PIN, LEFT_THRUSTER_PIN, RIGHT_THRUSTER_PIN) 
    
    try:
        print("Starting Control Program")
        if(not USE_DEBUG_MODE):
            if (USE_MULTITHREADED_ARM):       
                armMultiThreaded(ARMING_INTERVAL, THRUSTERS)
            else:
                armSerial(ARMING_INTERVAL, THRUSTERS)
        else:
            debugArm(ARMING_INTERVAL, THRUSTERS)
        MainControlLoop(UPDATE_SPEED, WINDOW_HEIGHT, WINDOW_WIDTH, THRUSTERS, SCREEN_BACKGROUND_COLOR, FONT_COLOR)
        ShutDown(THRUSTERS)

    except KeyboardInterrupt:
        print("program inturrupted... exiting")
        ShutDown(THRUSTERS)
   

if __name__ == "__main__":
    main()