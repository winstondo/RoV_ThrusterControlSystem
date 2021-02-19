import ArduCamInit
import controllerInit
import CameraControlling
import swapCamera
#def main():
joy = controllerInit.ControllerInit()
ArduCamInit.ArducamInit()

while(1):
    if CameraControlling.CamController(joy):
        swapCamera.SwapCamera(CameraControlling.camera, CameraControlling.permit)
