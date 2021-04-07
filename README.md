## Remote GPIO
This is the key to using a host computer to pass controller data to the RPi. 
Requires using a new libary to detect Xbox controller on the host machine with python:

https://pypi.org/project/inputs/0.5/

This also uses a new GPIOZero module on the host machine to pass pwm signals to the RPi.
Refer to:

https://gpiozero.readthedocs.io/en/stable/api_pins.html#module-gpiozero.pins.pigpio

and 

https://gpiozero.readthedocs.io/en/stable/api_output.html#phaseenablemotor

for a PWM ESC motor. 

If the above doesn't work, then try GPIOZero's servo motor class.

## Patch 1:

New software logic should iron out left analog stick issues. 

Added analog trigger control over thrusters. RT should fire both dorsal thrusters forward to have the RoV accend. LT should cause the craft to decend. 

Once the Patch 1 is tested with the ROV throughly, merge patch 1 with the main branch.


# RoV_ThrusterControlSystem

main file is now rov_control_GPIO. 

Software uses pigpio libary for more accurate pulse width modulation (PWM) to control the ESC and brushless motors.

## Initialization:

### Host Computer
Need to install pigpio, gpiozero and pygames modules.
Also ensure that python is installed on the host computer.

#### Python on Windows CMD
Its also easier to use the Windows CMD to use pip. 
To do this when installing python on the windows machine, ensure that set PATH environment variable changes are checked. 

If python is already installed:
1. Locate the python.exe on the host machine. Copy the path.
2. Go to Control Panel and edit the system environment variables: System -> Advanced Tab -> Environmental Variables.
3. In the System Variables or Account Variables, find the PATH Variable. If there is no PATH variable add one.
4. When editing the PATH variable add the python.exe directory and another one with \Scripts appended to the directory path.
5. Check if pip works in the command line by typing in pip list or python to start the python interpreter. 

#### pigpio, pygames and gpiozero modules
Install it on the host computer by using the command:
```
pip instal pigpio pygames gpiozero modules
```
Check all the installed python modules on the machine by using:
```
pip list
```

### Raspberry PI:
Enable I2C, Remote GPIO in the settings.

Ensure the pigpio library is installed:
```
sudo apt-get install pigpio python-pigpio python3-pigpio
```
Check the version with:
```
pigpiod -v
```
The pigpio daemon is a piece of software that needs to be running in the back ground for it to work

To manually start the pigpio daemon use:
```
sudo pigpiod
```
or adding this line in the code in the python script:
```python
os.system ("sudo pigpiod")
```
The command to check when the pigpio daemon starts running is:
```
ps  -ef | grep gpio
```

To have the pigpio daemon start everytime the RPi boots use:
```
sudo systemctl enable pigpiod
```
and
```
sudo systemctl start pigpiod
```
This has already been enabled on one of the test RPis.

Refer to http://abyz.me.uk/rpi/pigpio/index.html for further instructions.

### ESC Calibration:
ESCs are manufactured in china and have spotty documentation.
To calibrate the ESCs for forward and reverse, the instructions that came with the ESC say to
1. Connect everything to the ESC 
2. Pulse for the highest frequency
3. Power on the thrusters and wait for 2 seconds. The thrusters should beep twice.
4. Pulse at the neutral frequency. The thrusters will beep twice.

The arm() function in the python code should take care of all the ESC calibrations for all four thrusters. 

Refer to the manufacture's website for specifications: http://www.ztwshop.com/product/shark-brushless-esc-for-rc-boat/ztw-shark-40A-bec-for-rc-boat.html

## Current Issues:
  
~~The analog stick is too sensitive and does not adequetly send out a consistant signal to the ESC, which causes the thrusters to stop firing if the analog stick is not in the ~~ appropriate dead zone. Some interpolation is needed to smooth this out.~~
Initilization takes forever and can be shortend.

Further testing with all four thrusters.

## Deprecated
Functions or drivers that are no longer used but kept for completeness or troubleshooting.
### Xbox Driver:

No longer used. The driver is only for interfacing a USB controller with a linux machine. All the controller interpretation is done on the host machine which is most likely a windows machine this no longer works. 

To initilize first ensure the xbox controller driver is installed:

```
sudo apt-get install xboxdrv
```

To test the driver use:
```
sudo xboxdrv --detach-kernel-driver
```

Refer to https://github.com/FRC4564/Xbox for more info on the xbox driver

# Connection to Raspberry Pi via Ethernet

## Static IP address on the Host Computer

First establish a static IPv4 address on the host computer via the network configuration on the Control Panel.
Make the IP address something memorable but the default is **192.168.1.1**.

## DHCP Server
Install the DHCP server software:
http://www.dhcpserver.de/cms/download/
DHCP will automatically assign IP addressesses to your PI: default is **192.168.1.2-4**

Do not have the IP adresses range collide with the currently set static IP address.

Configure the DHCP server software by giving it the range of IP adresses. Ensure the range should be small considering only one pi is connected at a time. 

## Connection:
Now use PuTTY SSH or Remote Desktop to connect to the pi directly. Its easier to connect using the default host name: **raspberrypi**, rather than the IP address. If for whatever reason the raspberry PI's hostname is unknown, then connect to it directly and use the following to get the host name.
```
sudo hostname
```
