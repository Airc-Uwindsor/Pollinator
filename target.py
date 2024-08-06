import numpy as np

class Target:
    def __init__(self, xyxy, confidence):
        list_xyxy = xyxy.tolist()[0]

        self.xyxy = [int(x) for x in list_xyxy]
        self.confidence = confidence.item()

        x1, y1, x2, y2 = self.xyxy
        self.center = int((x1 + x2) / 2), int((y1 + y2) / 2)

    def __repr__(self):
        return f"Target(xyxy={self.xyxy}, confidence={self.confidence})"