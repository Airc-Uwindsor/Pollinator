from ultralytics import YOLO
import cv2
from target import Target

class Model:
    def __init__(self):
        self.model = YOLO("best.pt", verbose=False) # TODO: change name of model file
        print("Model loaded")

    def find_targets(self, frame):
        result = self.model(frame, verbose=False)[0]

        # get the confidence and bounding box for the detections
        targets = []
        for box in result.boxes:
            targets.append(Target(box.xyxy, box.conf))

        return targets