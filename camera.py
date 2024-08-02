import pyrealsense2 as rs
import numpy as np
from vector import Vector
from config import *

class Camera:
    def __init__(self):
        self.pipeline = rs.pipeline()
        self.config = rs.config()

        self.config.enable_stream(rs.stream.depth, RES_X, RES_Y, rs.format.z16, 30)
        self.config.enable_stream(rs.stream.color, RES_X, RES_Y, rs.format.bgr8, 30)

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
    
    def pixel_to_point(self, pixel, depth):
        x, y = pixel
        depth = depth/1000
        yaw = (x - RES_X / 2) * FOV_X / RES_X
        pitch = -(y - RES_Y / 2) * FOV_Y / RES_Y

        yaw_rad = np.radians(yaw)
        pitch_rad = np.radians(pitch)

        # print(f'Yaw: {yaw_rad}, Pitch: {pitch_rad}, depth: {depth}')
        # calculate the x, y, z coordinates of the target relative to the camera
        x_offset = depth * np.tan(yaw_rad)
        y_offset = depth * np.tan(pitch_rad)
        z_offset = depth

        print(f'x: {x_offset}, y: {y_offset}, z: {z_offset}')

        return Vector(x_offset, y_offset, z_offset)

    def stop(self):
        self.pipeline.stop()

if __name__ == '__main__':
    import time

    camera = Camera()
    pixel = [0, 0]
    depth = 800
    point = camera.pixel_to_point(pixel, depth)
    print(point)