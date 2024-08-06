import threading
import cv2
import numpy as np
from robot import Robot, MoveType
from camera import Camera
import time
from model import Model
from vector import Vector, rpy_to_rotation_vector
from cluster import find_clusters
from path_order import order_path
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

        self.CAMERA_OFFSET = Vector(*CAMERA_OFFSET)
    
    def init_camera(self):
        self.camera = Camera()
        
    def init_robot(self):
        self.robot = Robot(CONTROL_IP, RECEIVE_IP)
        
    def init_model(self):
        self.model = Model('best.pt')


    def find_targets(self, current_pose, color_image, depth_image):
        '''Take a picture of the flowers and find the targets'''
        # Get the current pose
        current_offset = Vector(*current_pose[:3])
        current_rotation_vector = Vector(*current_pose[3:])
        
        # Find targets
        targets = self.model.find_targets(color_image)
        print(f'Found {len(targets)} targets')

        target_positions = []
        # Go through the targets and calculate the position in 3D space using the depth image
        for target in targets:
            center = target.center
            depth = depth_image[center[1], center[0]]

            if depth == 0: # TODO: why
                # print(f'{target} has depth 0')
                continue

            # Vector from the camera to the target
            cam_vec = self.camera.pixel_to_point(center, depth)

            # Vector from the TCP to the target
            tcp_vec = cam_vec - self.CAMERA_OFFSET

            # Rotate the vector to the robot's orientation
            tcp_vec = tcp_vec.rotate(current_rotation_vector)

            # Add the current offset to the vector
            tcp_vec += current_offset

            target_positions.append(tcp_vec.to_list())

        # TODO: display the image

        return target_positions

    def filter_targets(self, targets):
        '''Filter out the targets that are too far away or unsafe'''
        safe_targets = []

        for target in targets:
            if self.robot.is_pose_safe(target):
                safe_targets.append(target)

        return safe_targets
    
    def vibrate(self):
        '''Vibrates the robot to pollinate the flowers'''
        # TODO
        time.sleep(1)

    def scan(self):
        '''Scans the area for targets'''
        self.robot.picture_pose(0, async_move=False)
        print('Scanning the area')

        targets = []
        for pic in range(1, PICTURE_COUNT):
            current_pose = self.robot.get_pose()
            color_image, depth_image = self.camera.take_picture()
            self.robot.picture_pose(pic, async_move=True)
            targets += self.find_targets(current_pose, color_image, depth_image)

            if not self.robot.is_operation_done():
                time.sleep(0.05)

        return targets


    def pollinate(self):
        '''Runs a cycle of pollination'''

        # Take pictures of the flowers
        targets = self.scan()

        return

        # Home position
        self.robot.home(async_move=True)

        # Filter out the targets that are too far away/unsafe
        filtered_targets = self.filter_targets(targets)

        # Cluster the targets
        clusters = find_clusters(filtered_targets)

        if len(clusters) == 0:
            print('No targets found')
            return

        # Order the clusters
        points = order_path(clusters)

        # Filter out the points that are too far away/unsafe
        waypoints = self.filter_targets(points)

        print(f'Found {len(waypoints)} waypoints')

        # Wait until home position is reached
        while not self.robot.is_operation_done():
            time.sleep(0.1)

        # Move to the targets
        for point in waypoints:
            print(point)
            # Move before the target
            target = Vector(*point)
            offset = Vector(0.05, 0, 0.1)
            target -= offset
            # self.robot.move_tcp(target.to_list(), MoveType.SYNCHRONOUS)

            # TODO: take picture and verify the target position

            # Move to the target
            self.robot.move_tcp(point, MoveType.SYNCHRONOUS)

            # TODO: Pollinate
            self.vibrate()

    def drive(self):
        '''Drives the robot forward to cover more area'''
        # TODO
        pass

    def stop(self):
        '''Stops the robot and camera'''
        self.robot.stop()
        self.camera.stop()

    def run(self):
        '''Runs the pollinator'''
        self.pollinate()
        self.drive()

        self.stop()




if __name__ == '__main__':
    pollinator = Pollinator()
    pollinator.run()
    # pollinator.rotate(0.1, 0, 0)