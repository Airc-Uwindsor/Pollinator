# Pollinator
## Goal
- The goal of the pollinator is to pollinate the flowers in a precise and optimized manner. 

## Running the Pollinator with Python
1. Configure the robot’s network settings by changing the IP address
2. Configure the computer's network setting corresponding to the robot's netwrok 
3. Ensure the required version (3.9.1) of Python is installed
4. Download and extract the ZIP file and run the program

## Features
- Fine-tuned a YOLOv8 model using a [dataset](https://app.roboflow.com/pollinator-2wbdx/pollinator-rjhfp/2) from roboflow to detect tomato flowers
- Captutured images of the flowers from multiple angles using a D435i camera using the [pyrealsense2](https://pypi.org/project/pyrealsense2/) library
- Created a point cloud of the flowers using the camera's intrinsics
- Used a clustering algorithm to identify the flowers in the point cloud
- Found an optimal path to pollinate the flowers using the nearest neighbor algorithm and 2-opt algorithm
- Created a travel path for the pollinator to follow using the optimal path
- Used the [ur_rtde](https://sdurobotics.gitlab.io/ur_rtde/api/api.html) library to travel to the flowers and pollinated them with the robot's end effector

## Challenges
