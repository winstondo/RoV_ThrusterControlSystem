# ROV Camera Documentation 

Final solution taken was the use of socket communication. Therefore, there exist a server and client program. 

In the case of the server (host computer), make sure all of the items below are installed :
  1. Python 3
  2. opencv --> pip install opencv-python
  3. pillow --> pip install pillow
  4. numpy --> pip install pillow
  
Additionally, on the host computer, remote connection has to be enable, and in my case, ssh on window 10 pro version 20H2. this is done by: 

  - setting -> apps-> apps &features -> optional Features -> search -> Search for Open SSH Client in text field, and choose to install         openSSH client
  - 
While on the client (raspberryPi), Picamera has to be enable:
  1. in terminal--> sudo raspi-config
  2. select interfacing options
  3. select camera
  4. enable the camera. 

After all requirement are performed, the devices are ready for socket communications:
  1. camera_server.py has to be on host computer --> python camera_server.py 0.0.0.0 PORT_NUMBER
  2. camera_client.py has to be on raspberrypi --> python camera_client.py SERVER_IP_ADDRESS PORT_NUMBER

NOTE: Server side has to be operational first, then client can be luanched. Additionally, in host computer, ip detection is needed, and in our case, ipconfig was used to find the ip address on the network for the SERVER_IP_ADDRESS

### Futher documentation on other programs will be found in Camera_Doc.pdf with issues and possible soluitons to the problems. 
