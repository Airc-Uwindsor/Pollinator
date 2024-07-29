from robot import Robot, MoveType, TCP
from camera import Camera
import time

PICTURE_COUNT = 5
CAMERA_FRAMERATE = 2 # /s


class Pollinator:
    # Offset of the camera from the TCP
    OFFSET = (
        0.12,
        -0.0325,
        -0.05
    )

    def __init__(self):
        control_ip = '192.168.0.100'
        receive_ip = '192.168.0.100'
        self.camera = Camera()
        self.robot = Robot(control_ip, receive_ip)
        
    def pollinate(self):
        # home position
        self.robot.home()

        # take pictures
        self.camera.reset_target()

        # find target
        target = self.find_target()

        pixel = target[0:2]
        depth = target[2]
        
        point = self.camera.pixel_to_point(pixel, depth)

        self.move_to_target(point)

    def find_target(self):
        target_found = False
        target = None
        pose = self.robot.get_pose()
        while not target_found:
            time.sleep(1/CAMERA_FRAMERATE)
            self.camera.display()
            targets = self.camera.get_targets()
            print(f'Found {len(targets)} targets')

            if len(targets) == 0:
                continue

            for t in targets:
                if self.is_target_valid(t, pose):
                    target = t
                    target_found = True
                    break
        return target

    def is_target_valid(self, target, pose):
        pixel = target[0:2]
        depth = target[2]

        if depth == 0:
            return False
        
        # calculate the x, y, z coordinates of the target relative to the camera
        point = self.camera.pixel_to_point(pixel, depth)
        m_point = [p/1000 for p in point]

        # print(f'Point: {point}')
        
        # offset the point with the camera offset
        offset = [m_point[i] - self.OFFSET[i] for i in range(3)]

        # check if the target is within the reachable area of the robot
        safe = self.robot.is_offset_safe(offset, current_pose=pose)
        # print(f'Offset: {offset}, Safe: {safe}')
        return safe

    def move_to_target(self, point):
        m_point = [p/1000 for p in point]
        target = [m_point[i] - self.OFFSET[i] for i in range(3)]
        self.offset_with_display(target)

    def offset_with_display(self, offset):
        print(f'Moving to offset: {offset}')
        self.robot.move_offset(offset, MoveType.SYNCHRONOUS)
        # while not self.robot.is_operation_done():
        #     self.camera.display()
        #     time.sleep(0.2)

                

    def run(self):
        print('Pollinator started')
        for _ in range(PICTURE_COUNT):
            self.camera.take_picture()
            time.sleep(1/CAMERA_FRAMERATE)

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