# RoV_ThrusterControlSystem

main file is now rov_control_GPIO. 

I had to rewrite the software to use the rasberry pi's native GPIO. Also it has to use the pi's software driven PWM to control the ESC.
The previous code used a variation of DC control to move control the motors. But the brushless motor thrusters that are being utilized for the ROV utilize an ESC which is controled using a PWM signal, similar to a servo motor.

The software is untested as I dont have access to a compatible power supply. Currently, the thrusters are capable of firing forward. Due to poor docummentation of the ESC I am still in the process of figuring out which PWM signals tell the ESC to fire the thruster backwards. These ESCs are capable of reverse motion as stated by the products Amazon page but there is little to no documentation how to do so.

Will update later.

right now the all it does is fires the main thruster (m3 @full speed) forward once the right bumper is pushed and stops firing once it is released,
left bumper does the same to the main thruster but backwards

These thruster controls depend on two major libaries: the xbox360controller libary which handels input from the xbox controller via usb and the MotorControllerHAT which controls the motor controller output

The majority of these files are redundant, but kept for compatability issues. Ill prune the files once I get the software to an apporpriate level.
