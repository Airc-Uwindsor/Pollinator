from robot import Robot, MoveType, TCP
from camera import Camera
import time

PICTURE_COUNT = 10


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
        for _ in range(PICTURE_COUNT):
            self.camera.display()
            time.sleep(0.2)
            pixel = self.camera.pixel
            depth = self.camera.depth
            if pixel is not None:
                print(f'3D coords: {self.camera.pixel_to_point(pixel, depth)}')
            else:
                print('No target found')

        if pixel is None:
            print('No target found, stopping')
            return            
        # move to the target
        pixel = self.camera.pixel
        depth = self.camera.depth
        point = self.camera.pixel_to_point(pixel, depth)

        self.move_to_target(point)

    def move_to_target(self, point):
        # move to the target
        offset = [dim + self.OFFSET[i] for i, dim in enumerate(point)]
        self.offset_with_display(offset)

    def offset_with_display(self, offset):
        print(f'Moving to offset: {offset}')
        self.robot.move_offset(offset, MoveType.ASYNCHRONOUS)
        while not self.robot.is_operation_done():
            self.camera.display()
            self.time.sleep(0.2)

                

    def run(self):
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