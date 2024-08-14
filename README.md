# Pollinator
## Goal
The goal of the pollinator is to pollinate the flowers in a precise and optimized manner. 

## Ideation
- Used the process of test, train, valid for training the robot to detect flowers
- Used realsense and opencv to calculate depth of the target flowers
- The robot took multiple pictures in various locations to enhance the accuracy of the detection
- Used vectors and field of view (FOV) of the sensors to calculate offset between the camera, tcp, and the robot base 
- Used clustering algorithm to increase the accuracy of the target flower location
- Used rotations (rx, ry, rz) to optimize pathways between each target flower

## Challenges
