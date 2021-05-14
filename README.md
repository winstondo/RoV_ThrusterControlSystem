## Patch 2.1.1:
- ~~Corrected ASCEND and DESCEND control issues: thursters will correctly fire at full when triggers are fully depressed~~ 
- Reverted: controller corrects deadzone once a random button has been preseed. Right trigger still does not function correctly. Adjust the minmax bounds.


## Patch 2.1:
- Corrected thruster control logic
- Remote GPIO connection scheme to its own function


## Patch 2.0:
- Implemented new controller API: pygames. Allows Windows host computer to interpret controller input as well as drawing a diagnostic UI.
- Implemented GPIOZero for remote GPIO. Allows the host computer to control the RPis GPIO remotely. 
- Improved thruster software logic should iron out dead zone issues.

## Patch 1.0:
- Added analog trigger control over thrusters. RT should fire both dorsal thrusters forward to have the ROV accend. LT should cause the craft to decend.

## To Do:

 - Fix UI. 
 - Fix triggers.


# RoV_ThrusterControlSystem

~~main file is now rov_control_GPIO.~~ 

main file is rov_control-Host which should be run on the host computer. Instructions to prepare the RPi and the host computer are detailed below. 

Software uses pigpio libary for more accurate pulse width modulation (PWM) to control the ESC and brushless motors.

## Initialization:

### Host Computer
Need to install pigpio, gpiozero and pygames modules.
Also ensure that python is installed on the host computer.

#### Python on Windows CMD
Its also easier to use the Windows CMD to use pip. 
To do this when installing python on the windows machine, ensure that ```set PATH environment variable``` is checked. 

If python is already installed:
1. Locate the python.exe on the host machine. Copy the path.
2. Go to Control Panel and edit the system environment variables: System -> Advanced Tab -> Environmental Variables.
3. In the System Variables or Account Variables, find the PATH Variable. If there is no PATH variable add one.
4. When editing the PATH variable add the python.exe directory and another one with \Scripts appended to the directory path.
5. Check if pip works in the command line by typing in ``` pip list``` or ```python``` to start the python interpreter. 

#### pigpio, pygames and gpiozero modules
Install it on the host computer by using the command:
```
pip install pigpio pygame gpiozero modules
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

## Running the Python Script:
Once the host computer and the RPi have been initialized, the next step to running the control software is to run the python script.
Ensure that python has been properly installed on the host computer by running ```pip list ``` and checking that the ***gpiozero, pigpio, pygame*** modules have been installed. 

The important script is the ```ROV_control-host.py``` so download that into your desired directory. Take note of the path of this directory.

Open the windows power shell by right clicking the start menu. The CMD terminal can also work but the power shell is more powerful and easier to use.

![image](https://user-images.githubusercontent.com/31364456/118205380-1421bb80-b415-11eb-9fce-3b3506655a74.png)

Navigate to the ```ROV_control-host.py``` script directory using ``cd``. So for example if you downloaded the script file into the documents folder of Windows, navigating to the directory would be: ``` cd c:\users\username\documents ```

Run the script using: ```py ROV_control-host.py```

Stop the script by either exiting the pygames window or pressing Ctrl+C on the terminal. Please allow the program to run its termination function when shut down has started. 




## Deprecated
Functions or drivers that are no longer used but kept for completeness or troubleshooting.
### ~~Xbox Driver:~~

No longer used. The driver is only for interfacing a USB controller with a linux machine. All the controller interpretation is done on the host machine which is most likely a windows machine this no longer works. 

~~To initilize first ensure the xbox controller driver is installed:~~

```
sudo apt-get install xboxdrv
```

~~To test the driver use:~~
```
sudo xboxdrv --detach-kernel-driver
```

Refer to https://github.com/FRC4564/Xbox for more info on the xbox driver



### ~~Static IP address on the Host Computer~~
Static IP addresses seem to give remote and ssh connection errors as well as prevents the RPi from sharing internet when directly connected to the host computer. 
Its better to just use dynamic IP addressing and connect through normal means.

~~First establish a static IPv4 address on the host computer via the network configuration on the Control Panel.
Make the IP address something memorable but the default is **192.168.1.1**.~~


## DHCP Server

~~Install the DHCP server software:
http://www.dhcpserver.de/cms/download/~~

~~DHCP will automatically assign IP addressesses to your PI: default is **192.168.1.2-4**~~

~~Do not have the IP adresses range collide with the currently set static IP address.~~

~~Configure the DHCP server software by giving it the range of IP adresses. Ensure the range should be small considering only one pi is connected at a time. 
DHCP will automatically assign IP addressesses to your PI: default is 192.168.1.2-4
Do not have the IP adress range collide with the currently set static IP address
Configure the DHCP server software by giving it the range of IP adresses. Ensure the range of small considering only one pi is connected at a time.~~ 


## Connection:
Now use PuTTY SSH or Remote Desktop to connect to the pi directly. Its easier to connect using the default host name: **raspberrypi**, rather than the IP address. If for whatever reason the raspberry PI's hostname is unknown, then connect to it directly and use the following to get the host name.
```
sudo hostname
```

