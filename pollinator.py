import cv2
import numpy as np
from robot import Robot, MoveType
from camera import Camera
import time
from model import Model
from vector import Vector

PICTURE_COUNT = 5
CAMERA_FRAMERATE = 2 # /s

display = True

class Pollinator:
    # Offset of the camera from the TCP
    CAMERA_OFFSET = Vector(
        0.12,
        -0.0325,
        -0.05
    )

    def __init__(self):
        control_ip = '192.168.0.100'
        receive_ip = '192.168.0.100'
        self.camera = Camera()
        self.robot = Robot(control_ip, receive_ip)
        self.model = Model()

        # self.robot.home()
        
    def pollinate(self):
        # take a picture of the flowers
        self.robot.picture_pose()

        # find target
        targets = self.find_targets()
        print(f'Found {len(targets)} targets')

        self.robot.home()
        
        for point in targets:
            self.move_to_target(point)

            # TODO: make a path to avoid obstacles while moving to the target instead of moving home
            self.robot.home()

    def display(self, color_image, depth_image, targets):
        if not display:
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

        while len(targets) < 5:
            color_image, depth_image = self.camera.take_picture()
            targets = self.model.find_targets(color_image)

            # calculate the 3D positions of the targets relative to the camera
            # print('Calculating 3D positions')
            targets = self.calculate_3d_positions(targets, depth_image)

            self.display(color_image, depth_image, targets)

            # filter out targets that are not reachable by the robot
            # print('Filtering out far targets')
            targets = self.filter_far_targets(targets)

            for target in targets:
                print(target)

            # time.sleep(1)

        # start at the target with the highest confidence and then move to the next target based on the 3D position
        target_order = []

        # add the target with the highest confidence to the target order
        target_order.append(max(targets, key=lambda target: target.confidence))
        targets.remove(target_order[0])

        # TODO: use a better algorithm to order the targets
        # add the next target to the target order based on the 3D position
        while len(targets) > 0:
            target_order.append(min(targets, key=lambda target: target.get_3d_distance(target_order[-1])))
            targets.remove(target_order[-1])

        return target_order

    def calculate_3d_positions(self, targets, depth_image):
        current_pose = self.robot.get_pose()
        current_pose = Vector(*current_pose[0:3])
        new_targets = []
        camera_vec = current_pose - self.CAMERA_OFFSET
        for target in targets:
            center = target.center  

            # get the depth within the bounding box
            x1, y1, x2, y2 = target.xyxy
            depths = depth_image[y1:y2, x1:x2]
            depth = np.percentile(depths, 25)

            if depth == 0:
                continue

            # vector from the camera to the target
            target_vec = self.camera.pixel_to_point(center, depth)

            # from robot base to target
            target_point = camera_vec + target_vec

            target.set_3d_position(target_point)

            new_targets.append(target)

        return new_targets
    
    def filter_far_targets(self, targets):
        reachable_targets = []

        for target in targets:
            point = target.position.to_list()
            # print(f'Checking if target is reachable: {point}')
            if self.robot.is_pose_safe(point):
                reachable_targets.append(target)

        return reachable_targets

    def move_to_target(self, target):
        pose = target.position 
        pose = pose.to_list()

        print(f'Moving to target: {target.position}')
        self.robot.move_tcp(pose, MoveType.SYNCHRONOUS)           

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