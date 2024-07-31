from camera import Camera
from ultralytics import YOLO
import cv2
import time
from model import Model


def main():
    # initialize webcam
    # cap = cv2.VideoCapture(0)
    # print("Webcam initialized")

    camera = Camera()
    model = Model('best.pt')

    while True:
        color_image, depth_image = camera.take_picture()
        # ret, color_image = cap.read()

        results = model.model(color_image)
        
        annotated_frame = results[0].plot()

        cv2.imshow('Annotated Frame', annotated_frame)
        cv2.waitKey(1)

if __name__ == '__main__':
    main()