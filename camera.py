import pyrealsense2 as rs
import numpy as np
import cv2

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
        # (x, y, depth) of each target found
        self.targets = []

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
        aligned_frames = self.align.process(frames)

        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()

        color_image = np.asanyarray(color_frame.get_data())
        target_array = self.find_target(color_image)
        depth_image = np.asanyarray(depth_frame.get_data())

        # TODO: use YOLO image processing to find the target instead of color detection
        # pick a pixel and depth value for the target
        self.compile_targets(target_array, depth_image)

        return color_image, target_array, depth_image
    
    def compile_targets(self, target_array, depth_image):
        self.targets = []
        # for each target in the target array, find the pixel and depth value
        for y, row in enumerate(target_array):
            for x, target in enumerate(row):
                if target == 1:
                    depth = depth_image[y, x]
                    self.targets.append((x, y, depth))

    def get_targets(self):
        return self.targets
    
    def find_target(self, color_image):
        sensitivity = self.COLOR_SENSITIVITY / 100 * self.FARTHEST
        
        # convert color image to RGB
        color_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)

        # calculate the difference between the target color and the image
        diff = np.linalg.norm(color_image - self.TARGET_COLOR, axis=2)

        # create target array with True where the color is close to the target color
        target_array = np.zeros((self.RES_Y, self.RES_X))
        target_array[diff < sensitivity] = 1

        return target_array

    
    def pixel_to_point(self, pixel, depth):
        x, y = pixel
        yaw = (x - self.RES_X / 2) * self.FOV_X / self.RES_X
        pitch = -(y - self.RES_Y / 2) * self.FOV_Y / self.RES_Y

        yaw_rad = np.radians(yaw)
        pitch_rad = np.radians(pitch)

        print(f'Yaw: {yaw_rad}, Pitch: {pitch_rad}')
        # calculate the x, y, z coordinates of the target relative to the camera
        x_offset = depth
        y_offset = depth * np.tan(yaw_rad)
        z_offset = depth * np.tan(pitch_rad)

        return [x_offset, y_offset, z_offset]
    
    def display(self):
        color_image, target_array, depth_image = self.take_picture()

        # convert target array to displayable image
        target_image = np.zeros_like(color_image)
        target_image[target_array == 1] = [255, 255, 0]

        # convert depth image to displayable image
        depth_visual = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)


        # display images
        images = np.hstack((color_image, target_image, depth_visual))

        cv2.namedWindow('Camera', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('Camera', images)
        cv2.waitKey(1)

    def reset_target(self):
        self.targets = []

    def stop(self):
        self.pipeline.stop()

if __name__ == '__main__':
    import time

    camera = Camera()
    pixel = [camera.RES_X // 2, camera.RES_Y // 2]
    depth = 800
    point = camera.pixel_to_point(pixel, depth)
    print(point)