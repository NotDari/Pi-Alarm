from picamera2 import Picamera2
from picamera2.encoders import H264Encoder, Quality
from picamera2.outputs import FfmpegOutput
from picamera2.devices import IMX500
import time

RTMP_URL = "rtmp://192.168.50.232:1935/live/testStream"
picam2 = Picamera2()
frame_rate = 30
resolution = (640, 640)
video_config = picam2.create_video_configuration(
    main={"size": resolution, "format": "YUV420"},
    controls={'FrameRate': frame_rate}
)
picam2.configure(video_config)

encoder = H264Encoder(bitrate=5000000)


output_args = [
    '-f', 'flv',
    '-c', 'copy',
    '-fflags', 'nobuffer',
    '-flags', 'low_delay',
    '-tune', 'zerolatency', 
    RTMP_URL
]

# Create the FfmpegOutput object
output_string = " ".join(output_args)

# Use the single string when creating the FfmpegOutput object
rtmp_output = FfmpegOutput(output_string)

# 5. Start Recording/Streaming
try:
    picam2.start_recording(encoder, rtmp_output)
    print(f"Starting RTMP stream to {RTMP_URL}")
    
    # Keep the script running
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("Stopping stream.")

finally:
    picam2.stop_recording()
    picam2.stop()