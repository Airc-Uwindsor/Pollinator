# Robotic Arm Tomato Pollination

## Project Description
This project investigates the automation of tomato flower pollination using a robotic arm. The system combines computer vision, clustering algorithms, and a precise control system to identify and pollinate tomato flowers effectively. By leveraging the Intel RealSense camera for depth and color imagery, the project uses machine learning models to predict flower locations and control a Universal Robotics Cobot Arm to perform the pollination task.

## Installation

### Prerequisites
1. [**Python 3.9.1**](https://www.python.org/downloads/release/python-391/)
2. Intel RealSense Camera (with [pyrealsense2 library](https://pypi.org/project/pyrealsense2/))
3. Universal Robotics Cobot Arm (with [ur_rtde library](https://sdurobotics.gitlab.io/ur_rtde/api/api.html))
4. OpenCV
5. YOLO for object detection (with [ultralytics library](https://github.com/ultralytics/ultralytics))

### Step-by-Step Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Doomsy1/Pollinator
   cd Pollinator
   ```

2. **Install Required Libraries:**
   Install the necessary Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configuring the Universal Robotics Cobot Arm:**
   - Configure the robot’s network settings following the steps in the [Controlling a Universal Robotics Cobot Arm with Python](link) guide.

4. **Setting Up YOLO for Flower Detection:**
   - Download and set up the required YOLO models by following the steps in the [YOLO Setup](link) guide.

## Usage

### Pollination Process
- Run `pollinator.py`. This script integrates the camera input, clustering algorithm, and robot control to execute the pollination.

### Robot Control
- Use `robot.py` for direct control and testing of the robotic arm's movements.

## Authors and Acknowledgment
- Lead Developer: [Ario Barin Ostovary](https://github.com/Doomsy1)
- Contributors: [jblee0310](https://github.com/jblee0310)
