# Number of pictures to take per position 
PICTURE_COUNT = 5

# Maximum distance between two points in a cluster
EPS = 0.02

# Display the images?
DISPLAY = True

# Offset of the camera from the TCP
CAMERA_OFFSET = (
    0.0325,
    0.08,
    0.12
)

# IP addresses for the robot
CONTROL_IP = '192.168.0.100'
RECEIVE_IP = '192.168.0.100'


### Camera

# Resolution of the camera
RES_X = 640
RES_Y = 480

# Field of view of the camera
FOV_X = 54.6
FOV_Y = 42.4



### Robot

# Home position of the robot
HOME_POSE = [0, -90, -120, 30, 90, 0]

# Picture position of the robot
PICTURE_POSES = [
    # [-10, 0, -45, -135, 90, 0],
    [-5, 0, -45, -135, 90, 0],
    [0, 0, -45, -135, 90, 0],
    [5, 0, -45, -135, 90, 0],
    # [10, 0, -45, -135, 90, 0],
]