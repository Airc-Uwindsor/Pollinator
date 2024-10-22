from ultralytics import YOLO
import cv2
from target import Target

class Model:
    def __init__(self, model_file):
        self.model = YOLO(model_file, verbose=False)
        print(f'Model loaded: {model_file}')

    def find_targets(self, frame):
        result = self.model(frame, verbose=False)[0]

        # get the confidence and bounding box for the detections
        targets = []
        for box in result.boxes:
            targets.append(Target(box.xyxy, box.conf))

        return targets