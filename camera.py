import pyrealsense2 as rs
import numpy as np
import cv2

class Camera:
    RES_X = 640
    RES_Y = 480

    # RGB color of the target
    TARGET_COLOR = [240, 240, 20]

    # Sensitivity of the color detection (0-100)
    COLOR_SENSITIVITY = 25

    # Maximum distance from the target color
    FARTHEST = 3**(1/2) * 255

    def __init__(self):
        self.pixel = None # last detected pixel
        self.depth = None

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
        pixel, depth = self.choose_random_target(old_target=False, target_array=target_array, depth_image=depth_image)
        if pixel is not None and depth is not None:
            self.pixel = pixel
            self.depth = depth

        return color_image, target_array, depth_image
    
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
    
    def choose_random_target(self, old_target=True, target_array=None, depth_image=None):
        if old_target:
            return self.pixel, self.depth
        
        target_indices = np.nonzero(target_array)
        if len(target_indices[0]) == 0:
            return None, None
        
        depth = 0
        while depth == 0:
            
            target_index = np.random.randint(len(target_indices[0]))
            y, x = target_indices[0][target_index], target_indices[1][target_index]

            depth = depth_image[y, x] # TODO: weighted average of the depth values around the target pixel
            
        pixel = (int(x), int(y))
        return pixel, depth
    
    def pixel_to_point(self, pixel, depth):
        x, y = pixel
        z = depth

        # Convert pixel to point
        point = rs.rs2_deproject_pixel_to_point(self.intrinsics, [x, y], z)
        return point
    
    def display(self):
        color_image, target_array, depth_image = self.take_picture()

        # convert target array to displayable image
        target_image = np.zeros_like(color_image)
        target_image[target_array == 1] = [255, 255, 0]

        # convert depth image to displayable image
        depth_visual = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

        if self.pixel is not None:
            # draw a circle around the target pixel for every image
            for image in [color_image, target_image, depth_visual]:
                cv2.circle(image, self.pixel, 10, (0, 0, 255), 2)

        # display images
        images = np.hstack((color_image, target_image, depth_visual))

        cv2.namedWindow('Camera', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('Camera', images)
        cv2.waitKey(1)

    def reset_target(self):
        self.pixel = None
        self.depth = None

    def stop(self):
        self.pipeline.stop()

if __name__ == '__main__':
    import time

    camera = Camera()
    while True:
        camera.display()
        time.sleep(0.3)