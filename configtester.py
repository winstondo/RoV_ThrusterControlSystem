import configparser


def printType(obj):
  print(type(obj))

def read_ini(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    #return config
    
    for section in config.sections():
        for key in config[section]:
            print((key, config[section][key]))
    


def tttype():
   while True:
       x = input("enter: ")
       printType(x)
       printType(MAX_PW)
       printType(WINDOW_HEIGHT)
       # x =

def main():
    config = configparser.ConfigParser()
    config.read('config.ini')


    #put this in the rovControlHost
    #config variables



    UPDATE_SPEED = config.getint('MAIN','UPDATE_SPEED', fallback=60)
    USE_MULTITHREADED_ARM = config.getboolean('MAIN', 'USE_MULTITHREADED_ARM', fallback=False)
  
    #host
    HOST = config.get('RASPBERRYPI', 'HOST', fallback='raspberrypi')

    #ui
    SCREEN_BACKGROUND_COLOR = config.get('UI', 'SCREEN_BACKGROUND_COLOR', fallback='black')
    FONT_COLOR = config.get('UI', 'FONT_COLOR', fallback='white')
    WINDOW_HEIGHT = config.getint('UI', 'WINDOW_HEIGHT', fallback=600)
    WINDOW_WIDTH = config.getint('UI', 'WINDOW_WIDTH', fallback=600)

    #Pulse Width (units in s)
    MAX_PW = config.getfloat('THRUSTERCONFIG','MAX_PW', fallback=2E-3)

    MIN_PW = config.getfloat('THRUSTERCONFIG','MIN_PW', fallback=1E-3)
    ARMING_INTERVAL = config.getint('THRUSTERCONFIG','ARMING_INTERVAL', fallback=2)
    #thruster pins
    FRONT_THRUSTER_PIN = config.getint('THRUSTERCONFIG','FRONT_THRUSTER_PIN', fallback=17)
    BACK_THRUSTER_PIN = config.getint('THRUSTERCONFIG','BACK_THRUSTER_PIN', fallback=27)
    LEFT_THRUSTER_PIN = config.getint('THRUSTERCONFIG','LEFT_THRUSTER_PIN', fallback=22)
    RIGHT_THRUSTER_PIN = config.getint('THRUSTERCONFIG','RIGHT_THRUSTER_PIN', fallback=23)

    printType(SCREEN_BACKGROUND_COLOR)


if __name__ == "__main__":
    main()
   