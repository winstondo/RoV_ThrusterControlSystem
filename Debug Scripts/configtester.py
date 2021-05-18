import configparser
import figme


def printType(obj):
  print(type(obj))

def read_ini(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    #return config
    
    for section in config.sections():
        for key in config[section]:
            print((key, config[section][key]))
    



def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    figme.main(config)

    #put this in the rovControlHost
    #config variables



if __name__ == "__main__":
    main()
   