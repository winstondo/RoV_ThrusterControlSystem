import ArduCamInit
import controllerInit
import CameraControlling
import swapCamera
#def main():
joy = controllerInit.ControllerInit()
print("Xbox controller ready")
ArduCamInit.ArducamInit()
print("Camera module and components ready")

print("starting main program")
while(1):
    if CameraControlling.CamController(joy):
        swapCamera.SwapCamera(CameraControlling.camera, CameraControlling.permit)
