# Pollinator
## Goal
- The goal of the pollinator is to pollinate the flowers in a precise and optimized manner. 

## Ideation
- Fine-tuned a YOLOv8 model using a [dataset](https://app.roboflow.com/pollinator-2wbdx/pollinator-rjhfp/2) from roboflow to detect tomato flowers
- Captutured images of the flowers from multiple angles using a D435i camera using the [pyrealsense2](https://pypi.org/project/pyrealsense2/) library
- Created a point cloud of the flowers using the camera's intrinsics
- Used a clustering algorithm to identify the flowers in the point cloud
- Found an optimal path to pollinate the flowers using the nearest neighbor algorithm and 2-opt algorithm
- Created a travel path for the pollinator to follow using the optimal path

## Challenges
