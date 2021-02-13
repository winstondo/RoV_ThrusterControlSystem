import ArduCamInit
import controllerInit
import CameraControlling
import swapCamera
#def main():
    ArducamInit.ArducamInit()
    controllerInit.controllerInit()
    while(1):
        if CameraControlling(CameraControlling.joy):
            swapCamera(CameraControlling.camera, CameraControlling.permit)
