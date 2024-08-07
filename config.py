
# Number of pictures to be taken per position
PICTURE_COUNT = 10

# Cluster distance
EPS = 0.02

# Display the images?
DISPLAY = True

# Offset of the camera from the TCP
CAMERA_OFFSET = (
    0.0325,
    0.05,
    0.15
)

# Offset of the approach point from the target
APPROACH_OFFSET = (
    -0.05,
    0,
    0
)

# Offset of the departure point from the target
DEPARTURE_OFFSET = (
    -0.05,
    0,
    0
)

# IP addresses for the robot
CONTROL_IP = '192.168.0.100'
RECEIVE_IP = '192.168.0.100'



### Camera

# Resolution of the camera
RES_X = 640
RES_Y = 480

# Field of view of the camera
FOV_X = 61.6
FOV_Y = 43.3



### Robot

# Home position of the robot
HOME_POSE = [0, -90, -120, 30, 90, 0]

# Picture position of the robot
PICTURE_POSES = [
    [-20, 5, -45, -135, 90, 0],
    [-15, 0, -45, -135, 90, 5],
    [-10, -5, -45, -135, 90, 0],
    [-5, 0, -45, -135, 90, -5],
    [0, 0, -45, -135, 90, 0],
    [5, 5, -45, -135, 90, 0],
    [10, 0, -45, -135, 90, 5],
    [15, -5, -45, -135, 90, 0],
    [20, 0, -45, -135, 90, -5]
]
    

# Default rotation vector
DEFAULT_ROTATION_VECTOR = [2.4071581, -2.42914925, 2.41536115]

# Move parameters
VELOCITY = 0.075
ACCELERATION = 1