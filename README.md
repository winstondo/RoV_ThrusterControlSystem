## Patch 1:

New software logic should iron out left analog stick issues. 

Added analog trigger control over thrusters. RT should fire both dorsal thrusters forward to have the RoV accend. LT should cause the craft to decend. 

Once the Patch 1 is tested with the ROV throughly, merge patch 1 with the main branch.


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
