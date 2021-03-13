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
ensure that the pigpio daemon is running by running:
```
sudo pigpiod
```
or by uncommenting out this line in the code:
```python
os.system ("sudo pigpiod")
```
Refer to http://abyz.me.uk/rpi/pigpio/index.html for further instructions.

## MISC
### ESC Calibration.
ESCs are manufactured in china and have spotty documentation.
To calibrate the ESCs for forward and reverse, the instructions that came with the ESC say to
1. Connect everything to the ESC 
2. Pulse for the highest frequency
3. Power on the thrusters and wait for 2 seconds. The thrusters should beep twice.
4. Pulse at the neutral frequency. The thrusters will beep twice.

The arm() function in the python code should take care of all the ESC calibrations for all four thrusters. 

Refer to the manufacture's website for specifications: http://www.ztwshop.com/product/shark-brushless-esc-for-rc-boat/ztw-shark-40A-bec-for-rc-boat.html


## Current Issues:
  
The analog stick is too sensitive and does not adequetly send out a consistant signal to the ESC, which causes the thrusters to stop firing if the analog stick is not in the appropriate dead zone. Some interpolation is needed to smooth this out.

Initilization takes forever and can be shortend.

Further testing with all four thrusters.
