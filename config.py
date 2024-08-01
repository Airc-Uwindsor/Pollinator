
# Number of pictures to be taken before pollination
PICTURE_COUNT = 10

# Number of targets to be found before pollination
TARGET_COUNT = 10

# Cluster distance
CLUSTER_DISTANCE = 0.02

# Display the images?
DISPLAY = True

# Offset of the camera from the TCP
CAMERA_OFFSET = (
    0.12,
    -0.0325,
    -0.08
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
PICTURE_POSE = [0, 0, -45, -135, 90, 0]