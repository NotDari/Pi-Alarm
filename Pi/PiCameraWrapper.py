from picamera2 import Picamera2
from typing import Tuple
from picamera2.outputs import FfmpegOutput
from picamera2.encoders import H264Encoder


class PiCameraWrapper:

    def __init__(self, imx500):
        self.piCamera = Picamera2(imx500.camera_num)
        self.resolution = None; self.frameRate = None; self.format = None
        self.recording = False
    

    def setResolution(self,resolution: Tuple[int, int]):
        if (
            not isinstance(resolution, tuple)
            or len(resolution) != 2 
            or not all(isinstance(i, int) for i in resolution)
        ):
            raise ValueError("Resolution must be a tuple of two integers (width, height)")
        self.resolution = resolution

    def setFrameRate(self, frameRate: int):
        if not isinstance(frameRate, int):
            raise ValueError("Frame Rate must be a int")
        self.frameRate = frameRate
    
    def setFormat(self, format: str):
        if not isinstance(format, str):
            raise ValueError("Format must be a string")
        self.format = format
    
    def updateVideoConfigs(self):
        if (self.resolution == None or self.frameRate == None or self.format == None):
            #Raise Exception as guard triggered
            print()
        video_config = self.piCamera.create_video_configuration(
            main={"size": self.resolution, "format": self.format},
            controls={'FrameRate': self.frameRate}
        )
        self.piCamera.configure(video_config)
                
    def setVideoConfigDetails(self, resolution: Tuple[int, int], frameRate: int, format: str):
        self.setResolution(resolution);self.setFrameRate(frameRate);self.setFormat(format)
        self.updateVideoConfigs()
    
    def setPreCallback(self, callback):
        self.piCamera.pre_callback = callback

    def getFrameDetails(self):
        if self.recording == False:
            self.piCamera.start()
            self.recording = True
        return [self.piCamera.capture_array(), self.piCamera.capture_metadata()]

    def shutDownCamera(self):
        self.piCamera.stop()
        
