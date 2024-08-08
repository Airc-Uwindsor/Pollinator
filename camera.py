import pyrealsense2 as rs
import numpy as np
from config import RES_X, RES_Y

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
    
    def stop(self):
        self.pipeline.stop()

if __name__ == '__main__':
    camera = Camera()