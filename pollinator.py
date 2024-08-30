import threading
import cv2
import numpy as np
from robot import TCP, Robot
from camera import Camera
import time
from model import Model
from cluster import find_clusters
from path_order import order_path
from frame import Frame
from config import *

class Pollinator:
    # Offset of the camera from the TCP

    def __init__(self):
        self.camera = None
        self.robot = None
        self.model = None
        
        camera_thread = threading.Thread(target=self.init_camera)
        robot_thread = threading.Thread(target=self.init_robot)
        model_thread = threading.Thread(target=self.init_model)
        
        # Start all threads
        camera_thread.start()
        robot_thread.start()
        model_thread.start()
        
        # Wait for all threads to complete
        camera_thread.join()
        robot_thread.join()
        model_thread.join()

        # Wait for the robot to reach the picture pose
        self.wait_for_operation()

    def init_camera(self):
        self.camera = Camera(resolution=(RES_X, RES_Y))

        # Warm up the camera
        for i in range(5):
            self.camera.take_picture()

        # Take an initial picture
        color_image, depth_image = self.camera.take_picture()
        self.frames = [Frame(color_image, depth_image, self.robot.get_pose())]
        
    def init_robot(self):
        self.robot = Robot(CONTROL_IP, RECEIVE_IP, velocity=0.1, acceleration=0.5)

        # Move to picture pose
        self.picture_pose(async_move=True)
        
    def init_model(self):
        self.model = Model('models/1000_32.pt')

    def vibrate(self):
        '''Vibrates the brush to pollinate the flowers'''
        time.sleep(0.25)

    def drive(self):
        '''Drives the robot forward to cover more area'''
        pass

    def wait_for_operation(self):
        '''Waits for the robot to finish the current operation'''
        while not self.robot.is_operation_done():
            time.sleep(0.1)

    def home(self, async_move: bool = False):
        '''Moves the robot to the home position'''
        home_pose = np.deg2rad(HOME_POSE)
        self.robot.move_joints(home_pose, async_move)

    def picture_pose(self, picture_number: int = 0, async_move: bool = False):
        '''Moves the robot to the picture pose'''
        print(f'Moving to picture pose {picture_number}')
        picture_number = picture_number % len(PICTURE_POSES)
        picture_pose = np.deg2rad(PICTURE_POSES[picture_number])
        self.robot.move_joints(picture_pose, async_move)

    def filter_targets(self, targets):
        '''Filter out the targets that are too far away or unsafe'''
        safe_targets = []

        for target in targets:
            if self.robot.is_pose_safe(target):
                safe_targets.append(target)

        return safe_targets

    def display(self, frame):
        '''Displays the images and targets'''
        if not DISPLAY:
            return
        
        color_image = frame.color_image
        
        # Display the color image
        cv2.imshow('Color Image', color_image)

        cv2.waitKey(1)

    def scan(self):
        '''Scans the area and takes pictures of the flowers'''
        self.frames = self.frames[-1:] # Keep the last frame
        
        # Take pictures of the flowers
        for pos_num in range(len(PICTURE_POSES)):
            # Move to the picture position
            self.picture_pose(pos_num)
            current_pose = self.robot.get_pose()

            # Take pictures
            for pic_num in range(PICTURE_COUNT):
                print(f'Taking picture {pic_num + 1} at position {pos_num + 1}')
                color_image, depth_image = self.camera.take_picture()
                frame = Frame(color_image, depth_image, current_pose)

                # Display the images
                self.display(frame)

                self.frames.append(frame)

    def get_latest_frame(self):
        '''Returns the latest frame'''
        color_image = self.frames[-1].color_image
        depth_image = self.frames[-1].depth_image
        return color_image, depth_image

    def pollinate(self):
        '''Runs a cycle of pollination'''

        # Take pictures of the flowers
        self.scan()

        # Home position
        self.home(async_move=True)

        # Find the targets in the pictures taken
        targets = []
        for frame in self.frames[1:]: # Skip the first frame
            targets += frame.find_targets(self.model)

        if len(targets) == 0:
            print('No targets found')
            return

        # Cluster the targets
        clusters = find_clusters(targets, EPS)
        print(f'Found {len(clusters)} clusters')

        points = self.filter_targets(clusters)

        # Order the clusters
        path = order_path(points)

        print(f'Found {len(points)} targets to pollinate')

        # Wait until home position is reached
        self.wait_for_operation()

        for point in path:
            # Back
            back = point.copy()
            back[TCP.X] -= 0.06
            self.robot.move_tcp(back, verbose=False)

            # Move to the point
            self.robot.move_tcp(point, verbose=False)

            # Pollinate
            self.vibrate()

            # Back
            self.robot.move_tcp(back, verbose=False)

    def step_back(self):
        '''Steps back to the previous position'''
        current_pose = self.robot.get_pose()
        new_pose = current_pose.copy()
        new_pose[TCP.X] -= 0.1

        self.robot.move_tcp(new_pose)

    def stop(self):
        '''Stops the robot and camera'''
        self.robot.stop()
        self.camera.stop()

    def run(self):
        '''Runs the pollinator'''
        self.pollinate()
        # self.step_back()
        # self.home()
        self.drive()



def main():
    pollinator = Pollinator()
    for i in range(25):
        pollinator.run()

    pollinator.stop()

if __name__ == '__main__':
    main()