import cv2
import numpy as np
from robot import Robot, MoveType
from camera import Camera
import time
from model import Model
from vector import Vector
from cluster import find_clusters
from config import *


class Pollinator:
    # Offset of the camera from the TCP
    CAMERA_OFFSET = Vector(*CAMERA_OFFSET)

    def __init__(self):
        self.camera = Camera()
        self.robot = Robot(CONTROL_IP, RECEIVE_IP)
        self.model = Model('best.pt')

        # self.robot.home()
        
    def pollinate(self):
        # take a picture of the flowers
        self.robot.picture_pose()

        # find targets
        targets = self.find_targets()

        if len(targets) == 0:
            print('No targets found')
            return
        
        self.robot.home()

        
        for point in targets:
            self.move_to_point(point)

            time.sleep(1)

            # TODO: make a path to avoid obstacles while moving to the target instead of moving home
            self.robot.home()

    def display(self, color_image, depth_image, targets):
        if not DISPLAY:
            return
        
        # TODO: put the displays in the same window

        # left half of the screen is the color image with the bounding boxes, center, and confidence
        # right half of the screen is the depth image
        for target in targets:
            x1, y1, x2, y2 = target.xyxy
            cv2.rectangle(color_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(color_image, f'{target.confidence:.2f} | {target.position}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (36,255,12), 2)

        cv2.imshow('Color Image', color_image)

        # display the depth image
        # cv2.imshow('Depth Image', depth_image)

        cv2.waitKey(1)

    def find_targets(self):

        targets = []
        # while len(targets) < TARGET_COUNT:
        for pic_num in range(PICTURE_COUNT):
            # TODO: move/rotate camera between pictures to have more coverage and opportunities to find targets
            
            color_image, depth_image = self.camera.take_picture()
            new_targets = self.model.find_targets(color_image)

            print(f'Picture {pic_num} - Targets Found: {len(new_targets)} (unfiltered)', end=' | ')

            # calculate the 3D positions of the targets relative to the camera
            # print('Calculating 3D positions')
            new_targets = self.calculate_3d_positions(new_targets, depth_image)

            self.display(color_image, depth_image, new_targets)

            # filter out targets that are not reachable by the robot
            # print('Filtering out far targets')
            new_targets = self.filter_far_targets(new_targets)

            print(f'{len(new_targets)} (filtered)')

            targets.extend(new_targets)


        # TODO: move order based on confidence
        # cluster the targets
        print(f'Found {len(targets)} targets, clustering...')
        clusters = find_clusters([target.position.to_list() for target in targets], CLUSTER_DISTANCE)
        print(f'Found {len(clusters)} clusters')

        # TODO: use an algorithm to order the targets
        target_order = self.order_targets(clusters)

        return target_order
    
    def order_targets(self, clusters):
        # temp return it in the same order
        return clusters

    def calculate_3d_positions(self, targets, depth_image):
        current_pose = self.robot.get_pose()
        rotation_vector = Vector(*current_pose[3:6])
        current_pose = Vector(*current_pose[0:3])
        new_targets = []
        for target in targets:
            center = target.center  

            # get the median of the depth values within a radius of the center
            depths = depth_image[center[1] - 3: center[1] + 3, center[0] - 3: center[0] + 3]
            depth = np.median(depths)

            if depth == 0:
                continue

            # vector from the camera to the target
            target_vec = self.camera.pixel_to_point(center, depth)
            
            # vector from the tcp to the target
            target_vec -= self.CAMERA_OFFSET

            # rotate the vector to the robot's frame of reference
            target_vec = target_vec.rotate(rotation_vector)

            # add the current position of the robot to get the 3D position of the target
            target_point = target_vec + current_pose

            target.set_3d_position(target_point)

            new_targets.append(target)

        return new_targets
    
    def filter_far_targets(self, targets):
        reachable_targets = []

        for target in targets:
            point = target.position.to_list()
            if self.robot.is_pose_safe(point):
                reachable_targets.append(target)

        return reachable_targets

    def move_to_point(self, point):
        # TODO: go right before the target and take a picture to do fine adjustments 
        print(f'Moving to target: {point}')
        self.robot.move_tcp(point, MoveType.SYNCHRONOUS)           

    def run(self):
        print('Pollinator started')

        try:
            self.pollinate()
        finally:
            self.robot.stop()

        self.camera.stop()

def main():
    pollinator = Pollinator()
    pollinator.run()

if __name__ == '__main__':
    main()