import time
import subprocess
from PiCameraWrapper import PiCameraWrapper
from FfmpegWrapper import FfmpegWrapper
from Imx500Wrapper import IMX500Wrapper
from picamera2.outputs import FfmpegOutput
from picamera2.encoders import H264Encoder


RTMP_URL = "rtmp://192.168.50.232:1935/live/testStream"

def initImx500() -> IMX500Wrapper:
    imx500 = IMX500Wrapper()
    time.sleep(10)
    return imx500


def initCamera(imx500) -> PiCameraWrapper:
    #Give camera time to boot up
    time.sleep(1)
    count = 0
    piCam = None
    #Repeatadly attempt to init camera, restarting pi if too many attempts without success
    while (piCam == None):
        if (count >= 5):
            subprocess.run(["sudo", "reboot"])
        try:
            piCam = PiCameraWrapper(imx500.getImX500Instance())
        except Exception as e:
            #Log error
            print("Failed to init Camera") 
            print(e)
            
            count += 1
            #Sleep and increment error count
            time.sleep(4)
    piCam.setVideoConfigDetails((640,640), 30, "YUV420")
    print("Camera init successful")
    return piCam

def initFfmpeg() -> FfmpegWrapper:
    ffmpeg = FfmpegWrapper()
    ffmpeg.setDetails(640,640,30)
    ffmpeg.openSocket()
    
    return ffmpeg


def record(imx500, piCamera, ffmpeg):
    piCamera.setPreCallback(imx500.draw_detections)
    # Keep the script running
    while True:
        [frame, metadata] = piCamera.getFrameDetails()
        outputs = imx500.imx500.get_outputs(metadata, add_batch=True)
        #print("Outputs ", outputs)
        #print("\n")
        #print(metadata.keys())


        

        detections = imx500.parseDetections(metadata, piCamera.piCamera)
        for detection in detections:
            print("DETECTION")
        ffmpeg.writeToPipe(frame)  


        

def shutDownProtocol(piCamera, ffmpeg, imx500):
    piCamera.shutDownCamera()
    ffmpeg.shutDown()
    imx500.shutDown()


def main():
    try:
        imx500 = initImx500()
        piCamera = initCamera(imx500)
        ffmpeg = initFfmpeg()
        record(imx500,piCamera, ffmpeg)
    except Exception as e:
        print("Shutting down...")
        if isinstance(e ,KeyboardInterrupt):
            print("Natural shutdown")
        else:
            print("ERROR:" + str(e))
        shutDownProtocol(piCamera, ffmpeg, imx500)




main()