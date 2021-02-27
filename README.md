# RoV_ThrusterControlSystem

main file is now rov_control_GPIO. 

Software uses pigpio libary for more accurate pulse width modulation (PWM) to control the ESC and brushless motors.

## Initialization:
 
### Xbox Driver:
 
To initilize first ensure the xbox controller driver is installed: 

```
sudo apt-get install xboxdrv
```

To test the driver use:
```
sudo xboxdrv --detach-kernel-driver
```

Refer to https://github.com/FRC4564/Xbox for more info on the xbox driver

### PWM GPIO driver:
  
Ensure the pigpio library is installed:
```
sudo apt-get install pigpio python-pigpio python3-pigpio
```
Check the version with:
```
pigpiod -v
```
Refer to http://abyz.me.uk/rpi/pigpio/index.html for instructions.

## Current Issues:
  
The analog stick is too sensitive and does not adequetly send out a consistant signal to the ESC, which causes the thrusters to stop firing if the analog stick is not in the appropriate dead zone. Some interpolation is needed to smooth this out.

Initilization takes forever and can be shortend.

Further testing with all four thrusters.
