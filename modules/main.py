import ArduCamInit
import controllerInit
import CameraControlling
import swapCamera
#def main():
joy = controllerInit.ControllerInit()
ArduCamInit.ArducamInit()

while(1):
    if CameraControlling(joy):
        swapCamera(CameraControlling.camera, CameraControlling.permit)
