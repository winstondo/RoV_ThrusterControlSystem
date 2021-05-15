#program descr: Main script to be run. runs the camera software and the thruster control software. Ensure that both camera and thruster control modules are in the same directory.
import configparser


import ROV_Control_Host #control software


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')
    ROV_Control_Host.main(config)


