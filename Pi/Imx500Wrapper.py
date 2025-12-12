from picamera2.devices.imx500 import IMX500
import cv2
from picamera2.devices.imx500 import (NetworkIntrinsics,
                                      postprocess_nanodet_detection)
import sys
from Detection import Detection
import numpy as np
from functools import lru_cache
from picamera2 import MappedArray

class IMX500Wrapper:

    model = "assets/imx500_network_yolov8n_pp.rpk"
    threshold = 0.01
    iou = 0.65
    max_detections = 10

    
    def __init__(self):
        self.lastDetections = []
        self.imx500 = IMX500(self.model)
        self.last_results = None
        self.createIntrinsics()
        self.checkIfLabelsAreNone()
        self.labels = self.getLabels()
        print("=== MODEL INFO ===")
        print("Task:", self.intrinsics.task)
        print("Postprocess:", self.intrinsics.postprocess)
        print("Labels:", self.intrinsics.labels)
        print("Input size:", self.imx500.get_input_size())
        print("BBox normalization:", self.intrinsics.bbox_normalization)
        print(f"IMX500 camera_num: {self.imx500.camera_num}")  # ADD THIS
        print(f"IMX500 device: {self.imx500}")

    
    def createIntrinsics(self):
        intrinsics = self.imx500.network_intrinsics
        if not intrinsics:
            intrinsics = NetworkIntrinsics()
            intrinsics.task = "object detection"
        intrinsics.postprocess = "yolo"
        intrinsics.bbox_normalization = False
        intrinsics.update_with_defaults()
        self.intrinsics = intrinsics

    def checkIfLabelsAreNone(self):
        if self.intrinsics.labels is None:
            clean_labels = []
            with open("assets/coco_labels.txt", "r") as f:
                for line in f:
                    self.intrinsics.labels = f.read().splitlines()
                    #clean_labels.append(line.strip().split(",")[-1])

            #self.intrinsics.labels = clean_labels
            self.intrinsics.update_with_defaults()
            

    def parseDetections(self, metadata: dict, piCamera):
        """Parse the output tensor into a number of detected objects, scaled to the ISP out."""
        bbox_normalization = self.intrinsics.bbox_normalization

        np_outputs = self.imx500.get_outputs(metadata, add_batch=True)
        input_w, input_h = self.imx500.get_input_size()
        if np_outputs is None:
            return self.lastDetections
        if self.intrinsics.postprocess == "nanodet":
            boxes, scores, classes = \
                postprocess_nanodet_detection(outputs=np_outputs[0], conf=self.threshold, iou_thres=self.iou,
                                            max_out_dets=self.max_detections)[0]
            from picamera2.devices.imx500.postprocess import scale_boxes
            boxes = scale_boxes(boxes, 1, 1, input_h, input_w, False, False)
        else:
            boxes, scores, classes = np_outputs[0][0], np_outputs[1][0], np_outputs[2][0]
            if bbox_normalization:
                boxes = boxes / input_h

            boxes = np.array_split(boxes, 4, axis=1)
            boxes = zip(*boxes)

        self.lastDetections = [
            Detection(box, category, score, metadata,self.imx500, piCamera)
            for box, score, category in zip(boxes, scores, classes)
            if score > self.threshold
        ]
        self.last_results = self.lastDetections
        return self.lastDetections

    @lru_cache
    def getLabels(self):
        labels = self.intrinsics.labels
        if self.intrinsics.ignore_dash_labels:
            labels = [label for label in labels if label and label != "-"]
        return labels


    def draw_detections(self, request, stream="main"):
        """Draw the detections for this request onto the ISP output."""
        detections = self.last_results
        if detections is None:
            return
        labels = self.getLabels()
        with MappedArray(request, stream) as m:
            for detection in detections:
                x, y, w, h = detection.box
                print("DEBUG:", labels, detection, detection.category, detection.conf)
                label = f"{labels[int(detection.category)]} ({detection.conf:.2f})"

                # Calculate text size and position
                (text_width, text_height), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
                text_x = x + 5
                text_y = y + 15

                # Create a copy of the array to draw the background with opacity
                overlay = m.array.copy()

                # Draw the background rectangle on the overlay
                cv2.rectangle(overlay,
                            (text_x, text_y - text_height),
                            (text_x + text_width, text_y + baseline),
                            (255, 255, 255),  # Background color (white)
                            cv2.FILLED)

                alpha = 0.30
                cv2.addWeighted(overlay, alpha, m.array, 1 - alpha, 0, m.array)

                # Draw text on top of the background
                cv2.putText(m.array, label, (text_x, text_y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

                # Draw detection box
                cv2.rectangle(m.array, (x, y), (x + w, y + h), (0, 255, 0, 0), thickness=2)

            if self.intrinsics.preserve_aspect_ratio:
                b_x, b_y, b_w, b_h = self.imx500.get_roi_scaled(request)
                color = (255, 0, 0)  # red
                cv2.putText(m.array, "ROI", (b_x + 5, b_y + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
                cv2.rectangle(m.array, (b_x, b_y), (b_x + b_w, b_y + b_h), (255, 0, 0, 0))
    
    def getImX500Instance(self):
        return self.imx500
    
    def shutDown(self):
        self.imx500.stop()
        self.imx500.close()