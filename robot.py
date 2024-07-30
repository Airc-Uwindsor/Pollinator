import rtde_control
import rtde_receive
import time
import numpy as np

HOME_POSE = [0, -90, -120, 30, 90, 0]
PICTURE_POSE = [0, 0, -45, -135, 90, 0]

class MoveType:
    SYNCHRONOUS = False
    ASYNCHRONOUS = True

class MoveParams:
    VELOCITY = 0.05
    ACCELERATION = 1

class TCP:
    X = 0
    Y = 1
    Z = 2
    RX = 3
    RY = 4
    RZ = 5

class Robot:
    def __init__(self, control_ip, receive_ip):
        # Connect to the RTDE interface
        print(f'Connecting to control IP: {control_ip} and receive IP: {receive_ip}')
        self.rtde_c = rtde_control.RTDEControlInterface(control_ip)
        print('Control interface connected')
        self.rtde_r = rtde_receive.RTDEReceiveInterface(receive_ip)
        print('Receive interface connected')

        self.pose = self.get_pose()
        # reset to home position
        self.read_pose()
        # self.home()
    
    def home(self):
        print('Moving to home position')
        # convert to radians using np.deg2rad
        home_pose = np.deg2rad(HOME_POSE)
        self.move_joints(home_pose, MoveType.SYNCHRONOUS)
        self.read_pose()
    
    def picture_pose(self):
        print('Moving to picture position')
        # convert to radians using np.deg2rad
        picture_pose = np.deg2rad(PICTURE_POSE)
        self.move_joints(picture_pose, MoveType.SYNCHRONOUS)
        self.read_pose()

    def get_pose(self):
        return self.rtde_r.getActualTCPPose()
    
    def is_pose_safe(self, pose):
        if len(pose) == 3:
            pose = pose + self.get_pose()[3:]
        return self.rtde_c.isPoseWithinSafetyLimits(pose)
    
    def is_joint_safe(self, joints):
        return self.rtde_c.isJointsWithinSafetyLimits(joints)
    
    def is_offset_safe(self, offset):
        current_pose = self.get_pose()
        new_pose = current_pose.copy()
        for i in range(len(offset)):
            new_pose[i] += offset[i]
        
        return self.is_pose_safe(new_pose)
    
    def move_tcp(self, new_pose, move_type):
        if len(new_pose) == 3:
            new_pose = new_pose + self.get_pose()[3:]
        
        if not self.is_pose_safe(new_pose):
            self.stop()
            raise ValueError('New pose is not safe')
        self.rtde_c.moveL(new_pose, MoveParams.VELOCITY, MoveParams.ACCELERATION, move_type)
        # if move_type == MoveType.SYNCHRONOUS:
        #     while not self.is_operation_done():
        #         self.delay()

    def move_offset(self, offset, move_type):
        current_pose = self.get_pose()
        new_pose = current_pose.copy()
        for i in range(len(offset)):
            new_pose[i] += offset[i]
        self.move_tcp(new_pose, move_type)

    def move_joints(self, new_joints, move_type):
        if not self.is_joint_safe(new_joints):
            self.stop()
            raise ValueError('New joints are not safe')
        self.rtde_c.moveJ(new_joints, MoveParams.VELOCITY * 3, MoveParams.ACCELERATION, move_type)
        # if move_type == MoveType.SYNCHRONOUS:
        #     while not self.is_operation_done():
        #         self.delay()

    def read_pose(self):
        TCP_pose = self.get_pose()
        cleaned_tcp_pose = [round(pose, 3) for pose in TCP_pose]
        print(f'Current TCP pose: {cleaned_tcp_pose}', end='\t')

        joint_pose = self.rtde_r.getActualQ()
        cleaned_joint_pose = [round(pose, 3) for pose in joint_pose]
        print(f'Current joint pose: {cleaned_joint_pose}')

    def get_async_status(self):
        return self.rtde_c.getAsyncOperationProgress()
    
    def is_operation_done(self):
        status = self.get_async_status()
        return status <= -1
    
    def stop(self):
        self.rtde_c.stopScript()

if __name__ == '__main__':
    control_ip = '192.168.0.100'
    receive_ip = '192.168.0.100'
    robot = Robot(control_ip, receive_ip)
    robot.home()

    pose = robot.get_pose()
    print(f'Current pose: {pose}')

    robot.move_offset([0, 0, -0.05], MoveType.ASYNCHRONOUS)
    while not robot.is_operation_done():
        robot.read_pose()
        
    robot.stop()