import subprocess
class FfmpegWrapper():
    RTMP_URL = "rtmp://192.168.50.232:1935/live/testStream"
    
    def __init__(self):
        pass

    def setDetails(self, width, height, fps):
        self.width = width
        self.height = height
        self.fps = fps

    def openSocket(self):
        command = ['ffmpeg',
           '-y',
           '-f','rawvideo',
           '-pix_fmt','yuv420p',
           '-s',f'{self.width}x{self.height}',
           '-r',str(self.fps),
           '-i','-',
           '-c:v','h264_v4l2m2m',
           '-b:v','4M',
           '-f','flv',
           self.RTMP_URL]
        self.pipe = subprocess.Popen(command, stdin=subprocess.PIPE)
        self.pipeOpen = True
        
    def writeToPipe(self, frame):
        if self.pipeOpen == False:
            #Raise Error
            print()
        self.pipe.stdin.write(frame.tobytes())


    def shutDown(self):
        if self.pipeOpen:
            self.pipe.stdin.close()
            self.pipe.wait()
