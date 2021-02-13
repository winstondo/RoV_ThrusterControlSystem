import ArduCamInit
import controllerInit
import CameraControlling
import swapCamera
#def main():
controllerInit.controllerInit()
ArduCamInit.ArducamInit()

while(1):
    if CameraControlling(CameraControlling.joy):
        swapCamera(CameraControlling.camera, CameraControlling.permit)
