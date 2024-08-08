# https://sdurobotics.gitlab.io/ur_rtde/api/api.html

import threading
import rtde_control
import rtde_receive

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

DEFAULT_ROTATION_VECTOR = [2.4071581, -2.42914925, 2.41536115]

class Robot:
    def __init__(self, control_ip: str, receive_ip: str, velocity: float = 0.075, acceleration: float = 0.5):
        # Connect to the RTDE interface
        print(f'Connecting to control IP: {control_ip} and receive IP: {receive_ip}')
        self.control_ip = control_ip
        self.receive_ip = receive_ip

        self.velocity = velocity
        self.acceleration = acceleration

        # Initialize the control and receive interfaces
        control_thread = threading.Thread(target=self.init_control)
        receive_thread = threading.Thread(target=self.init_receive)

        control_thread.start()
        receive_thread.start()

        control_thread.join()
        receive_thread.join()

    def init_control(self):
        self.rtde_c = rtde_control.RTDEControlInterface(self.control_ip)
        print('Control interface connected')

    def init_receive(self):
        self.rtde_r = rtde_receive.RTDEReceiveInterface(self.receive_ip)
        print('Receive interface connected')

    def get_pose(self):
        '''Get the current TCP pose of the robot'''
        return self.rtde_r.getActualTCPPose()
    
    def clean_pose(self, pose: list):
        '''Clean the pose by adding the default rotation vector if it is not provided'''
        if len(pose) == 3:
            return pose + DEFAULT_ROTATION_VECTOR
        return pose
    
    def is_pose_safe(self, pose: list):
        '''Check if the pose is within the safety limits'''
        clean_pose = self.clean_pose(pose)
        return self.rtde_c.isPoseWithinSafetyLimits(clean_pose)
    
    def is_joint_safe(self, joints: list):
        '''Check if the joints are within the safety limits'''
        return self.rtde_c.isJointsWithinSafetyLimits(joints)
    
    def is_offset_safe(self, offset: list):
        '''Check if the offset is safe to move'''
        current_pose = self.get_pose()
        new_pose = current_pose.copy()
        for i in range(len(offset)):
            new_pose[i] += offset[i]

        return self.is_pose_safe(new_pose)

    def move_tcp(self, pose: list, move_type: bool):
        '''Move the robot to the given TCP pose'''
        clean_pose = self.clean_pose(pose)

        # Check if the pose is safe
        if not self.is_pose_safe(clean_pose):
            self.stop()
            raise ValueError('Pose is not safe')

        print(f'Moving to pose: {clean_pose}')
        
        self.rtde_c.moveL(clean_pose, self.velocity, self.acceleration, move_type)

    def move_joints(self, joints: list, move_type: bool):
        '''Move the robot to the given joint pose'''

        # Check if the joints are safe
        if not self.is_joint_safe(joints):
            self.stop()
            raise ValueError('Joints are not safe')
        
        self.rtde_c.moveJ(joints, self.velocity*3, self.acceleration, move_type)

    def read_pose(self):
        '''Read the current TCP and joint pose of the robot'''

        TCP_pose = self.get_pose()
        cleaned_pose = [round(i, 3) for i in TCP_pose]

        joint_pose = self.rtde_r.getActualQ()
        cleaned_joint_pose = [round(i, 3) for i in joint_pose]

        print(f'Current TCP Pose: {cleaned_pose}\tCurrent Joint Pose: {cleaned_joint_pose}')

    def get_asynch_status(self):
        '''Get the status of the asynchronous operation'''
        # < 0: Operation done / No operation
        # 0: Operation in progress
        return self.rtde_c.getAsyncOperationProgress()
    
    def is_operation_done(self):
        status = self.get_asynch_status()
        return status < 0
    
    def stop(self):
        self.rtde_c.stopScript()

if __name__ == '__main__':
    control_ip = '192.168.0.100'
    receive_ip = '192.168.0.100'

    # Initialize the robot
    robot = Robot(control_ip, receive_ip)

    # Get the initial TCP pose - [x, y, z, rx, ry, rz]
    init_pose = robot.get_pose()
    print(f'Initial TCP Pose: {init_pose}')

    new_pose = init_pose.copy()
    new_pose[TCP.X] += 0.1 # Move 10 cm in the x direction
    robot.move_tcp(new_pose, MoveType.SYNCHRONOUS)

    # Move back to the initial pose
    robot.move_tcp(init_pose, MoveType.SYNCHRONOUS)

    # Stop the robot
    robot.stop()