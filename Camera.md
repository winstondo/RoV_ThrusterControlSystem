# ROV Camera Documentation 

Final solution taken was the use of socket communication. Therefore, there exist a server and client program. 

In the case of the server (host computer), make sure all of the items below are installed :
  1. Python 3
  2. opencv --> pip install opencv-python
  3. pillow --> pip install pillow
  4. numpy --> pip install pillow
  
Additionally, on the host computer, remote connection has to be enable, and in my case, ssh on window 10 pro version 20H2. this is done by
  setting -> apps-> apps &features -> optional Features -> search -> Search for Open SSH Client in text field, and choose to install      openSSH client
