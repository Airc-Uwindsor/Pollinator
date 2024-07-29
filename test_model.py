from camera import Camera
from ultralytics import YOLO
import cv2
import time


def main():
    camera = Camera()
    model = YOLO("best.pt")

    while True:
        time.sleep(1/10)
        color_image, target_array, depth_image = camera.take_picture()

        results = model(color_image)

        annotated_frame = results[0].plot()

        cv2.imshow('Annotated Frame', annotated_frame)
        cv2.waitKey(1)


if __name__ == '__main__':
    main()