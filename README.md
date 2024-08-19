# Pollinator
## Goal
The goal of the pollinator is to pollinate the flowers in a precise and optimized manner. 

## Running the Pollinator with Python
1. Configure the robot’s network settings by changing the IP address
2. Configure the computer's network setting corresponding to the robot's netwrok 
3. Ensure the required version (3.9.1) of Python is installed
4. Download and extract the ZIP file and run the program

## Features
- Used the process of test, train, valid for training the robot to detect flowers
- Used realsense and opencv to calculate depth of the target flowers
- The robot took multiple pictures in various locations to enhance the accuracy of the detection
- Used vectors and field of view (FOV) of the sensors to calculate offset between the camera, tcp, and the robot base 
- Used clustering algorithm to increase the accuracy of the target flower location
- Used rotations (rx, ry, rz) to optimize pathways between each target flower

## Challenges
