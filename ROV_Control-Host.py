#this should be run on the host computer

import pygame 
import time
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory




#class definitions

# This is a simple class that will help us print to the screen.
# It has nothing to do with the joysticks, just outputting the
# information.
class TextPrint(object):
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def tprint(self, screen, textString):
        textBitmap = self.font.render(textString, True, WHITE)
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
def arm(arming_interval, thrusters):
    for thruster in thrusters.values():    
        print("initilizing:{} at MAX_PW".format(thruster))
        thruster.max()
        print(arming_interval, " to turn on power now:")
        CountSleep(arming_interval)
        print("initilizing:{} at NEUTRAL".format(thruster))
        thruster.mid()
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

# -------- Main Program Loop -----------
#desc: This is the main program loop that pools the controller for input as well as creates the UI window. Automatically exits if the user exits the UI window.
#input: (UPS) an int value that tells the program how many times a second to poll the controller and update the UI window
#input: (WINDOW_HEIGHT, WINDOW_WIDTH) two interger values that tells the main program how large to draw the window
#input: (thrusters) (thrusters) dictionary of all thruster objects of the Servo class, each identified by keys ("Front","Left", etc)
#output:none 
def MainControlLoop(UPS, WINDOW_HEIGHT, WINDOW_WIDTH, thrusters):
    
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
        screen.fill(BLACK)
        textPrint.reset()

        # Get count of joysticks.
        joystick_count = pygame.joystick.get_count()

        textPrint.tprint(screen, "Number of joysticks: {}".format(joystick_count))
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
            textPrint.tprint(screen, "Joystick {}".format(jid))
            textPrint.indent()

            # Get the name from the OS for the controller/joystick.
            name = joystick.get_name()
            textPrint.tprint(screen, "Joystick name: {}".format(name))

            try:
                guid = joystick.get_guid()
            except AttributeError:
                # get_guid() is an SDL2 method
                pass
            else:
                textPrint.tprint(screen, "GUID: {}".format(guid))

            # Usually axis run in pairs, up/down for one, and left/right for
            # the other.
            axes = joystick.get_numaxes()
            textPrint.tprint(screen, "Number of axes: {}".format(axes))
            textPrint.indent()

            #for i in range(axes):
                #axis = joystick.get_axis(i)
                #textPrint.tprint(screen, "Axis {} value: {:>6.3f}".format(i, axis,))
            
            #axis designation block
            flJoyLeftX = joystick.get_axis(0)
            flJoyLeftY = -1 * joystick.get_axis(1) #pygames returns the Y axis on the joysticks as inverted for a stupid reason
            flJoyRightX = joystick.get_axis(2)
            flJoyRightY = -1 * joystick.get_axis(3) #pygames returns the Y axis on the joysticks as inverted because stupid 
            flLeftTrigger = MinMaxNormalization(joystick.get_axis(4), 0, 1, -1, 1) #pygames has the triggers between [-1,1] with the 0 outputing only if the trigger is squeezed half way.
            flRightTrigger = MinMaxNormalization(joystick.get_axis(5), 0, 1, -1, 1) 

            textPrint.tprint(screen, "JoyLeftX is value: {:>6.3f}".format(flJoyLeftX))
            textPrint.tprint(screen, "JoyLeftY is value: {:>6.3f}".format(flJoyLeftY))
            textPrint.tprint(screen, "JoyRightX is value: {:>6.3f}".format(flJoyRightX))
            textPrint.tprint(screen, "JoyRightY is value: {:>6.3f}".format(flJoyRightY))
            textPrint.tprint(screen, "LeftTrigger is value: {:>6.3f}".format(flLeftTrigger))
            textPrint.tprint(screen, "RightTrigger is value: {:>6.3f}".format(flRightTrigger))
            textPrint.unindent()
            textPrint.indent()
            #somewhat inelegant, can be improved
            lThrust_val = clamp(flJoyLeftX + flJoyLeftY, -1, 1)
            rThrust_val = clamp(-1*flJoyLeftX + flJoyLeftY, -1, 1)
            

            #thruster control logic for left analog stick and diagnostic display

            thrusters["Left"].value = lThrust_val
            thrusters["Right"].value = rThrust_val

            textPrint.tprint(screen, "{:>6.3f} input LeftThruster with PULSE WIDTH: {:>6.3f}".format(lThrust_val, thrusters["Left"].pulse_width))
            textPrint.tprint(screen, "{:>6.3f} input RightThruster with PULSE WIDTH: {:>6.3f}".format(rThrust_val, thrusters["Right"].pulse_width))

            thrusters["Front"].value = flRightTrigger
            thrusters["Back"].value = flRightTrigger
            thrusters["Front"].value = -1 * flLeftTrigger
            thrusters["Back"].value = -1 * flLeftTrigger

            textPrint.tprint(screen, "FrontThruster with PULSE WIDTH: {:>6.3f}".format(thrusters["Front"].pulse_width))
            textPrint.tprint(screen, "BackThruster with PULSE WIDTH: {:>6.3f}".format(thrusters["Back"].pulse_width))

            textPrint.unindent()

            buttons = joystick.get_numbuttons()
            textPrint.tprint(screen, "Number of buttons: {}".format(buttons))
            textPrint.indent()

            for i in range(buttons):
                button = joystick.get_button(i)
                textPrint.tprint(screen,
                                 "Button {:>2} value: {}".format(i, button))
            textPrint.unindent()

            hats = joystick.get_numhats()
            textPrint.tprint(screen, "Number of hats: {}".format(hats))
            textPrint.indent()

            # Hat position. All or nothing for direction, not a float like
            # get_axis(). Position is a tuple of int values (x, y).
            for i in range(hats):
                hat = joystick.get_hat(i)
                textPrint.tprint(screen, "Hat {} value: {}".format(i, str(hat)))
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




if __name__ == "__main__":
    #global variables

    # Color scheme for UI window
    BLACK = pygame.Color('black')
    WHITE = pygame.Color('white')
    #UI window dimentions in pixels
    WINDOW_HEIGHT = 700
    WINDOW_WIDTH = 500
    #Pulse Width (units in s)
    MAX_PW = 2E-3
    MIN_PW = 1E-3 
    #FRAME_WIDTH = 20E-3   #The length of time between servo control pulses measured in seconds. Using defaults of 20ms which is a common value for servos.
    #NEUTRAL_THROTTLE = 1500 #pulse widths lower than this value will have the thruster fire in reverse
    ARMING_INTERVAL = 4 #minimum ammount of time the arming function waits between oscillating the throttles to arm the ESCs

    remote_host = PiGPIOFactory(host="raspberrypi") #sets the pinfactory which enables networking features. This class can take IP addresses, but host names are more constant.

    #pulse width units for the Servo class are in seconds, below are the default values
    #Servo(pin, *, initial_value=0, min_pulse_width=1/1000, max_pulse_width=2/1000, frame_width=20/1000, pin_factory=None)

    objFrontThruster = Servo(11, min_pulse_width=MIN_PW, max_pulse_width=MAX_PW, pin_factory=remote_host)
    objBackThruster = Servo(13, min_pulse_width=MIN_PW, max_pulse_width=MAX_PW, pin_factory=remote_host)
    objLeftThruster = Servo(17, min_pulse_width=MIN_PW, max_pulse_width=MAX_PW, pin_factory=remote_host)
    objRightThruster = Servo(27, min_pulse_width=MIN_PW, max_pulse_width=MAX_PW, pin_factory=remote_host)

    #dictionary of thruster servo objects
    THRUSTERS = {
        "Front": objFrontThruster,
        "Back": objBackThruster,
        "Left": objLeftThruster,
        "Right": objRightThruster    
    } 


    

    try:
        arm(ARMING_INTERVAL, THRUSTERS)
        MainControlLoop(20, WINDOW_HEIGHT, WINDOW_WIDTH, THRUSTERS)

    except KeyboardInterrupt:
        print("program inturrupted... exiting")
        ShutDown(THRUSTERS)
   
