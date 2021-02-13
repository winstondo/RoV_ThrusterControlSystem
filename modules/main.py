import ArducamInit
import controllerInit
def main():
    ArducamInit.ArducamInit()
    if CameraControlling():
        swapCamera()
