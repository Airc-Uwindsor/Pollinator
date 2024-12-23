# robot.py

import time
from xarm.wrapper import XArmAPI

class TCP:
    X = 0
    Y = 1
    Z = 2
    ROLL = 3
    PITCH = 4
    YAW = 5

class Robot:
    def __init__(self, arm_ip: str = '192.168.1.206', speed: float = 100, is_radian: bool = False, home: bool = True):
        """
        Initialize the xArm by connecting to the given IP address
        and setting initial parameters.
        """
        print(f'Connecting to xArm at IP: {arm_ip}')
        self.arm_ip = arm_ip
        self.speed = speed
        self.is_radian = is_radian

        self.arm = XArmAPI(self.arm_ip, is_radian=self.is_radian)
        self.arm.motion_enable(True)
        # 0 = position control mode
        self.arm.set_mode(0)
        # 0 = sport state
        self.arm.set_state(0)

        # Example of setting collision sensitivity (range: 0-5)
        self.arm.set_collision_sensitivity(5)
        print('xArm connected and ready')

        if home:
            self.home()

    def get_pose(self):
        """
        Returns the current [x, y, z, roll, pitch, yaw] of the robot (in degrees if is_radian=False).
        """
        return self.arm.get_position(is_radian=self.is_radian)

    def move_tcp(self, pose, wait=True):
        """
        Move the robot to the given TCP pose: [x, y, z, roll, pitch, yaw].
        Speed is set in constructor or can be overridden per call.
        """
        # For direct substitution, we accept a list of length 6
        # [x, y, z, roll, pitch, yaw]
        if len(pose) != 6:
            raise ValueError("Pose must have 6 elements [x, y, z, roll, pitch, yaw]")
        self.arm.set_position(
            *pose,
            speed=self.speed,
            wait=wait,
            is_radian=self.is_radian
        )

    def move_joints(self, joint_positions, wait=True):
        """
        Move the robot to the given joint positions (list of angles).
        """
        self.arm.set_servo_angle(
            servo_id=None,          # move all joints
            angles=joint_positions,
            speed=self.speed,
            is_radian=self.is_radian,
            wait=wait
        )

    def stop(self):
        """
        Stop the robot. For an emergency stop, you can also use arm.emergency_stop().
        """
        # The xArm approach to stopping can vary; set_state(4) or emergency_stop()
        self.arm.set_state(4)
        # self.arm.emergency_stop()  # For an immediate e-stop

    def read_pose(self):
        """
        Print the current pose and joint angles.
        """
        tcp_pose = self.get_pose()
        joint_pose = self.arm.get_servo_angle(is_radian=self.is_radian)
        print(f"Current TCP Pose: {tcp_pose} | Current Joint Pose: {joint_pose}")

    def home(self, wait=True):
        """
        Moves the robot to the 'home' position using xArm's built-in move_gohome method.
        """
        self.arm.move_gohome(wait=wait)

    def disconnect(self):
        """
        Disconnect from the xArm.
        """
        self.arm.disconnect()
        print("xArm disconnected.")


def main():
    robot = Robot(arm_ip='192.168.1.206', home=False)
    # print pose
    print(robot.get_pose())

    # set pose
    robot.move_tcp([0, 300, 550, 180, -90, 90], wait=True)


    robot.stop()
    robot.disconnect()

if __name__ == '__main__':
    main()
