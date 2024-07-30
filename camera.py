import pyrealsense2 as rs
import numpy as np
from vector import Vector

class Camera:
    RES_X = 640
    RES_Y = 480

    # Field of view of the camera
    FOV_X = 61.6
    FOV_Y = 43.3

    # RGB color of the target
    TARGET_COLOR = [240, 240, 20]

    # Sensitivity of the color detection (0-100)
    COLOR_SENSITIVITY = 25

    # Maximum distance from the target color
    FARTHEST = 3**(1/2) * 255

    def __init__(self):
        self.pipeline = rs.pipeline()
        self.config = rs.config()

        self.config.enable_stream(rs.stream.depth, self.RES_X, self.RES_Y, rs.format.z16, 30)
        self.config.enable_stream(rs.stream.color, self.RES_X, self.RES_Y, rs.format.bgr8, 30)

        print('Starting camera pipeline')
        self.pipeline.start(self.config)
        print('Pipeline started')

        # Get active profile
        self.profile = self.pipeline.get_active_profile()

        # Get depth scale
        depth_sensor = self.profile.get_device().first_depth_sensor()
        self.depth_scale = depth_sensor.get_depth_scale()

        # Create align object
        align_to = rs.stream.color
        self.align = rs.align(align_to)

        # Get camera intrinsics
        self.intrinsics = self.profile.get_stream(rs.stream.color).as_video_stream_profile().get_intrinsics()

        # Create pointcloud object
        self.pc = rs.pointcloud()

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
        yaw = (x - self.RES_X / 2) * self.FOV_X / self.RES_X
        pitch = -(y - self.RES_Y / 2) * self.FOV_Y / self.RES_Y

        yaw_rad = np.radians(yaw)
        pitch_rad = np.radians(pitch)

        # print(f'Yaw: {yaw_rad}, Pitch: {pitch_rad}, depth: {depth}')
        # calculate the x, y, z coordinates of the target relative to the camera
        x_offset = depth
        y_offset = -depth * np.tan(yaw_rad)
        z_offset = depth * np.tan(pitch_rad)

        return Vector(x_offset, y_offset, z_offset)


    def stop(self):
        self.pipeline.stop()

if __name__ == '__main__':
    import time

    camera = Camera()
    pixel = [camera.RES_X // 2, camera.RES_Y // 2]
    depth = 800
    point = camera.pixel_to_point(pixel, depth)
    print(point)