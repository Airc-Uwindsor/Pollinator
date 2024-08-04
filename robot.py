import rtde_control
import rtde_receive
import time
import numpy as np
from config import *

class MoveType:
    SYNCHRONOUS = False
    ASYNCHRONOUS = True

class TCP:
    X = 0
    Y = 1
    Z = 2
    RX = 3
    RY = 4
    RZ = 5

class Robot:
    def __init__(self, control_ip: str, receive_ip: str):
        # Connect to the RTDE interface
        print(f'Connecting to control IP: {control_ip} and receive IP: {receive_ip}')
        self.rtde_c = rtde_control.RTDEControlInterface(control_ip)
        print('Control interface connected')
        self.rtde_r = rtde_receive.RTDEReceiveInterface(receive_ip)
        print('Receive interface connected')

    def home(self):
        print('Moving to home position')
        home_pose = np.deg2rad(HOME_POSE)
        self.move_joints(home_pose, MoveType.SYNCHRONOUS)

    def picture_pose(self):
        print('Moving to picture position')
        picture_pose = np.deg2rad(PICTURE_POSE)
        self.move_joints(picture_pose, MoveType.SYNCHRONOUS)

    def get_pose(self):
        return self.rtde_r.getActualTCPPose()
    
    def clean_pose(self, pose: list):
        if len(pose) == 3:
            pose += DEFAULT_ROTATION_VECTOR
        return pose
    
    def is_pose_safe(self, pose: list):
        pose = self.clean_pose(pose)
        return self.rtde_c.isPoseWithinSafetyLimits(pose)
    
    def is_joint_safe(self, joints: list):
        return self.rtde_c.isJointsWithinSafetyLimits(joints)
    
    def is_offset_safe(self, offset: list):
        current_pose = self.get_pose()
        new_pose = current_pose.copy()
        for i in range(len(offset)):
            new_pose[i] += offset[i]

        return self.is_pose_safe(new_pose)

    def move_tcp(self, pose: list, move_type: bool):
        pose = self.clean_pose(pose)

        if not self.is_pose_safe(pose):
            self.stop()
            raise ValueError('Pose is not safe')
        
        self.rtde_c.moveL(pose, VELOCITY, ACCELERATION, move_type)

    def move_joints(self, joints: list, move_type: bool):
        if not self.is_joint_safe(joints):
            self.stop()
            raise ValueError('Joints are not safe')
        
        self.rtde_c.moveJ(joints, VELOCITY, ACCELERATION, move_type)

    def read_pose(self):
        TCP_pose = self.get_pose()
        cleaned_pose = [round(i, 3) for i in TCP_pose]

        joint_pose = self.rtde_r.getActualQ()
        cleaned_joint_pose = [round(i, 3) for i in joint_pose]

        print(f'Current TCP Pose: {cleaned_pose}\tCurrent Joint Pose: {cleaned_joint_pose}')

    def get_asynch_status(self):
        return self.rtde_c.getAsyncOperationProgress()
    
    def is_operation_done(self):
        status = self.get_asynch_status()
        return status <= -1 # TODO: Check this value
    
    def stop(self):
        self.rtde_c.stopScript()




if __name__ == '__main__':
    robot = Robot(CONTROL_IP, RECEIVE_IP)

    robot.picture_pose()
    robot.read_pose()
    robot.stop()