
# Number of pictures to be taken per position
PICTURE_COUNT = 1

# Cluster distance
EPS = 0.02

# Display the images?
DISPLAY = True

# Offset of the camera from the TCP
CAMERA_OFFSET = (
    0.0325,
    0.05,
    0.14
)

# Offset of the approach point from the target
APPROACH_OFFSET = (
    0,
    0,
    0
)

# Offset of the departure point from the target
DEPARTURE_OFFSET = (
    0,
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
    [-15, 0, -45, -135, 90, 0],
    [-10, 0, -45, -135, 90, 0],
    [-5, 0, -45, -135, 90, 0],
    [0, 0, -45, -135, 90, 0],
    [5, 0, -45, -135, 90, 0],
    [10, 0, -45, -135, 90, 0],
    [15, 0, -45, -135, 90, 0]
]