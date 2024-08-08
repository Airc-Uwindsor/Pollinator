import threading
import numpy as np
from robot import Robot
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

    def init_camera(self):
        self.camera = Camera()
        
    def init_robot(self):
        self.robot = Robot(CONTROL_IP, RECEIVE_IP)
        
    def init_model(self):
        self.model = Model('models/best.pt')
    
    def vibrate(self):
        '''Vibrates the robot to pollinate the flowers'''
        # TODO async
        time.sleep(1)

    def drive(self):
        '''Drives the robot forward to cover more area'''
        # TODO
        pass

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

    def scan(self):
        '''Scans the area and takes pictures of the flowers'''
        self.frames = []
        
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

                self.frames.append(frame)

    def pollinate(self):
        '''Runs a cycle of pollination'''

        # Take pictures of the flowers
        self.scan()

        # Home position
        self.home(async_move=True)

        # Find the targets in the pictures taken
        targets = []
        for frame in self.frames: # TODO: run target finding in parallel?
            targets += frame.find_targets(self.model)

        filtered_targets = self.filter_targets(targets)

        if len(filtered_targets) == 0:
            print('No targets found')
            return

        # Cluster the targets
        clusters = find_clusters(filtered_targets)
        print(f'Found {len(clusters)} clusters')

        points = self.filter_targets(clusters)

        # Order the clusters
        path = order_path(points)

        print(f'Found {len(points)} targets to pollinate')

        # Wait until home position is reached
        while not self.robot.is_operation_done():
            time.sleep(0.1)

        for point in path:
            print(f'Moving to {point}')

            # Move to the point
            self.robot.move_tcp(point)

    def stop(self):
        '''Stops the robot and camera'''
        self.robot.stop()
        self.camera.stop()

    def run(self):
        '''Runs the pollinator'''
        self.pollinate()
        self.home()
        self.drive()





if __name__ == '__main__':
    pollinator = Pollinator()
    for i in range(2):
        pollinator.run()
        
    pollinator.stop()