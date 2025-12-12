from picamera2.devices import imx500

class Detection:
    def __init__(self, coords, category, conf, metadata, imx500, piCamera):
        """Create a Detection object, recording the bounding box, category and confidence."""
        self.category = category
        self.conf = conf
        self.box = imx500.convert_inference_coords(coords, metadata, piCamera)