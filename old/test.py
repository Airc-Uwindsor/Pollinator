import time
import numpy as np
from robot import Robot, MoveType, TCP
from camera import Camera

class TODO:
    def focus_pixel(self, pixel, depth):
        x, y = pixel
        # calculate yaw and pitch
        yaw = (x - Camera.RES_X / 2) * Camera.FOV_X / Camera.RES_X
        pitch = -(y - Camera.RES_Y / 2) * Camera.FOV_Y / Camera.RES_Y

        # yaw, pitch = 0, 90

        print(f'Yaw: {yaw}, Pitch: {pitch}')

        yaw_rad = np.radians(yaw)
        pitch_rad = np.radians(pitch)


        # x_offset = Camera.OFFSET[0]
        # y_offset = Camera.OFFSET[1]
        # z_offset = Camera.OFFSET[2]

        x_offset = depth * np.cos(pitch_rad) * np.cos(yaw_rad)
        y_offset = -depth * np.cos(pitch_rad) * np.sin(yaw_rad)
        z_offset = depth * np.sin(pitch_rad)

        print(f'Offsets: {x_offset}, {y_offset}, {z_offset}')

        # apply camera offset
        x_offset -= Camera.OFFSET[0]
        y_offset -= Camera.OFFSET[1]
        z_offset -= Camera.OFFSET[2]

        self.move_offset([x_offset, y_offset, z_offset, 0, 0, 0], MoveType.SYNCHRONOUS)

def touch_color(robot: Robot, camera: Camera):
    for i in range(6):
        camera.display()
        time.sleep(0.2)

    pixel, depth = camera.choose_random_target()
    print(f'Pixel: {pixel}, Depth: {depth}')

    if pixel is None or depth is None:
        print('No target found')
    else:
        robot.focus_pixel(pixel, depth/1000)



def main():
    control_ip = '192.168.0.100'
    receive_ip = '192.168.0.100'

    camera = Camera()
    camera.display()

    robot = Robot(control_ip, receive_ip)

    touch_color(robot, camera)

    camera.stop()
    robot.home()
    robot.stop()

if __name__ == "__main__":
    main()