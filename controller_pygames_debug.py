import pygame


# Define some colors.
BLACK = pygame.Color('black')
WHITE = pygame.Color('white')


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

pygame.init()

# Set the width and height of the screen (width, height).
screen = pygame.display.set_mode((500, 700))

pygame.display.set_caption("ROV Controller Diagnostic")

# Loop until the user clicks the close button.
bDone = False

# Used to manage how fast the screen updates.
clock = pygame.time.Clock()

# Initialize the joysticks.
pygame.joystick.init()

# Get ready to print.
textPrint = TextPrint()

# -------- Main Program Loop -----------
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
            #textPrint.tprint(screen, "Axis {} value: {:>6.3f}".format(i, axis))

        #axis designation block
        flJoyLeftX = joystick.get_axis(0)
        flJoyLeftY = -1 * joystick.get_axis(1) #pygames returns the Y axis on the joysticks as inverted for a stupid reason
        flJoyRightX = joystick.get_axis(2)
        flJoyRightY = -1 * joystick.get_axis(3) #pygames returns the Y axis on the joysticks as inverted for a stupid reason
        flLeftTrigger = MinMaxNormalization(joystick.get_axis(4), 0, 1, -1, 1) #pygames has the triggers between [-1,1] with the 0 outputing only if the trigger is squeezed half way.
        flRightTrigger = MinMaxNormalization(joystick.get_axis(5), 0, 1, -1, 1) 

        textPrint.tprint(screen, "JoyLeftX is value: {:>6.3f}".format(flJoyLeftX))
        textPrint.tprint(screen, "JoyLeftY is value: {:>6.3f}".format(flJoyLeftY))
        textPrint.tprint(screen, "JoyRightX is value: {:>6.3f}".format(flJoyRightX))
        textPrint.tprint(screen, "JoyRightY is value: {:>6.3f}".format(flJoyRightY))
        textPrint.tprint(screen, "LeftTrigger is value: {:>6.3f}".format(flLeftTrigger))
        textPrint.tprint(screen, "RightTrigger is value: {:>6.3f}".format(flRightTrigger))

        textPrint.unindent()
        textPrint.tprint(screen, "Thruster Output")
        textPrint.indent()
        #lThrust_val = MinMaxNormalization(flJoyLeftX + flJoyLeftY, -1, 1, -2, 2)
        #rThrust_val = MinMaxNormalization(-1*flJoyLeftX + flJoyLeftY, -1, 1, -2, 2)
        
        lThrust_val = clamp(flJoyLeftX + flJoyLeftY, -1 ,1)
        rThrust_val = clamp(-1*flJoyLeftX + flJoyLeftY, -1, 1)

        #thruster control logic for left analog stick and diagnostic display

        textPrint.tprint(screen, "{:>6.3f} input LeftThruster".format(lThrust_val))
        textPrint.tprint(screen, "{:>6.3f} input RightThruster".format(rThrust_val))


                

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

    # Limit to 20 frames per second.
    clock.tick(20)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()