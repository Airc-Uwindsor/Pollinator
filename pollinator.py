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
        self.camera = Camera()
        self.robot = Robot(CONTROL_IP, RECEIVE_IP)
        self.model = Model('best.pt')

        self.CAMERA_OFFSET = Vector(*CAMERA_OFFSET)
        
    def rotate(self, roll, pitch, yaw):
        '''Rotates the robot by the given angle'''
        # Get the current pose
        pose = self.robot.get_pose()

        rotation_vector = rpy_to_rotation_vector(roll, pitch, yaw)
        current_rotation = Vector(*pose[3:])
        new_rotation = current_rotation + rotation_vector

        # Move to the new pose
        new_pose = pose[:3] + new_rotation.to_list()
        self.robot.move_tcp(new_pose, MoveType.SYNCHRONOUS)

    def scan_for_targets(self):
        '''Take a picture of the flowers and find the targets'''
        # Get the current pose
        current_pose = self.robot.get_pose()
        current_offset = Vector(*current_pose[:3])
        current_rotation_vector = Vector(*current_pose[3:])
        
        # Take a picture of the flowers
        color_image, depth_image = self.camera.take_picture()

        # Find targets
        targets = self.model.find_targets(color_image)
        print(f'Found {len(targets)} targets')

        target_positions = []
        # Go through the targets and calculate the position in 3D space using the depth image
        for target in targets:
            center = target.center
            depth = depth_image[center[1], center[0]]

            if depth == 0:
                print(f'{target} has depth 0')
                continue

            # Vector from the camera to the target
            cam_vec = self.camera.pixel_to_point(center, depth)

            # Vector from the TCP to the target
            tcp_vec = cam_vec - self.CAMERA_OFFSET

            # Rotate the vector to the robot's orientation
            tcp_vec = tcp_vec.undo_rotate(current_rotation_vector) # TODO: undo or rotate?

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

        print(f'Found {len(safe_targets)} safe targets')
        return safe_targets
    
    def vibrate(self):
        '''Vibrates the robot to pollinate the flowers'''
        # TODO
        pass

    def pollinate(self):
        '''Runs a cycle of pollination'''
        self.robot.picture_pose()

        # TODO: change position between pictures
        targets = []
        # Scan for targets
        for pic in range(PICTURE_COUNT):
            print(f'Picture {pic}')
            targets += self.scan_for_targets()

        # Filter out the targets that are too far away/unsafe
        filtered_targets = self.filter_targets(targets)

        # Cluster the targets
        clusters = find_clusters(filtered_targets, EPS)

        if len(clusters) == 0:
            print('No targets found')
            return

        # Order the clusters
        points = order_path(clusters)

        # Home position
        self.robot.home_pose()

        # Move to the targets
        for point in points:
            # Move before the target
            target = Vector(*point)
            target -= Vector(0.05, 0, 0)
            self.robot.move_tcp(target.to_list(), MoveType.SYNCHRONOUS)

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