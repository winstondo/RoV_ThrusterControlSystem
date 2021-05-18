#program descr: Main script to be run. runs the camera software and the thruster control software. Ensure that both camera and thruster control modules are in the same directory.
import configparser #only needed in main file


import ROV_Control_Host #control software
import camera_server #camera software

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')
    ROV_Control_Host.main(config)
    camera_server.main(config)


