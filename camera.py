import pyrealsense2 as rs
import numpy as np
import cv2
# https://pyrealsense.readthedocs.io/en/master/

class Camera:
    def __init__(self, resolution=(640, 480)):
        self.resolution = resolution
        self.res_x, self.res_y = resolution

        self.pipeline = rs.pipeline()
        self.config = rs.config()

        self.config.enable_stream(rs.stream.depth, self.res_x, self.res_y, rs.format.z16, 30)
        self.config.enable_stream(rs.stream.color, self.res_x, self.res_y, rs.format.bgr8, 30)

        print('Starting camera pipeline')
        self.pipeline.start(self.config)
        print('Pipeline started')

    def take_picture(self):
        frames = self.pipeline.wait_for_frames()

        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()

        color_image = np.asanyarray(color_frame.get_data())
        depth_image = np.asanyarray(depth_frame.get_data())

        return color_image, depth_image
    
    def stop(self):
        self.pipeline.stop()

def main():
    camera = Camera()

    while True:
        color_image, depth_image = camera.take_picture()

        cv2.imshow('Color', color_image)
        cv2.imshow('Depth', depth_image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == '__main__':
    main()