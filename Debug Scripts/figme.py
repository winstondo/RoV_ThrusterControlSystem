def main(config):
    configs = []
    #host
    CLIENT_NAME = config.get('NETWORKING', 'CLIENT_NAME', fallback='fail')
    configs.append(CLIENT_NAME)

    #thruster pins
    FRONT_THRUSTER_PIN = config.getint('THRUSTERCONFIG','FRONT_THRUSTER_PIN', fallback=17)
    BACK_THRUSTER_PIN = config.getint('THRUSTERCONFIG','BACK_THRUSTER_PIN', fallback=27)
    configs.append(FRONT_THRUSTER_PIN)
    configs.append(BACK_THRUSTER_PIN)

    for cf in configs:
        print(cf)


if __name__ == "__main__":
    main()
