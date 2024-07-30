import numpy as np

class Target:
    def __init__(self, xyxy, confidence):
        list_xyxy = xyxy.tolist()[0]

        self.xyxy = [int(x) for x in list_xyxy]
        self.confidence = confidence.item()

        x1, y1, x2, y2 = self.xyxy
        self.center = int((x1 + x2) / 2), int((y1 + y2) / 2)

        self.position = None
    
    def set_3d_position(self, position):
        self.position = position # vector object

    def get_3d_distance(self, other):
        diffence = self.position - other.position

        return diffence.length

    def __repr__(self):
        return f"Target(xyxy={self.xyxy}, center={self.center} confidence={self.confidence}, position={self.position})"