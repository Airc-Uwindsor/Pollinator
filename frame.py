import numpy as np
from vector import Vector
from config import *

class Frame:
    def __init__(self, color_image, depth_image, current_pose):
        self.color_image = color_image
        self.depth_image = depth_image
        self.current_pose = current_pose

    def get_depth(self, pixel):
        '''Get the depth at a specific pixel'''
        # TODO: more complex depth calculation to avoid holes
        x = pixel[0]
        y = pixel[1]
        return self.depth_image[y, x]
    
    def pixel_to_point(self, pixel, depth):
        x, y = pixel
        depth = depth/1000
        yaw = (x - RES_X / 2) * FOV_X / RES_X
        pitch = (y - RES_Y / 2) * FOV_Y / RES_Y

        yaw_rad = np.radians(yaw)
        pitch_rad = np.radians(pitch)

        # print(f'Yaw: {yaw_rad}, Pitch: {pitch_rad}, depth: {depth}')
        x_offset = depth * np.tan(yaw_rad)
        y_offset = depth * np.tan(pitch_rad)
        z_offset = depth

        return Vector(x_offset, y_offset, z_offset)

    def find_targets(self, model):
        '''Take a picture of the flowers and find the targets'''
        current_offset = Vector(*self.current_pose[:3])
        current_rotation_vector = Vector(*self.current_pose[3:])

        targets = model.find_targets(self.color_image)

        target_positions = []
        # Go through the targets and calculate the position in 3D space using the depth image
        for target in targets:
            center = target.center
            depth = self.get_depth(center)

            if depth == 0:
                continue

            # Vector from the camera to the target
            cam_vec = self.pixel_to_point(center, depth)

            # Vector from the TCP to the target
            tcp_vec = cam_vec - Vector(*CAMERA_OFFSET)

            # Rotate the vector to the correct position
            rotated_vec = tcp_vec.rotate(current_rotation_vector)

            # Add the offset
            target_position = current_offset + rotated_vec

            target_positions.append(target_position.to_list())

        return target_positions