# Robotic Arm Tomato Pollination

## Project Description
This project investigates the automation of tomato flower pollination using a robotic arm. The system combines computer vision, clustering algorithms, and a precise control system to identify and pollinate tomato flowers effectively. By leveraging the Intel RealSense camera for depth and color imagery, the project uses machine learning models to predict flower locations and control a Universal Robotics Cobot Arm to perform the pollination task.

## Installation

### Prerequisites
1. [**Python 3.9.1**](https://www.python.org/downloads/release/python-391/)
2. [**Git**](https://git-scm.com/downloads)

### Step-by-Step Setup

1. **Set up the prerequisites:**
   - **Python** ([Guide](https://docs.google.com/document/d/1zFBC_VnUeAMrMF134yYSXPRlvTYTMshQ4id7R0SHFds/edit?usp=sharing))
   - **Git** ([Guide](https://docs.google.com/document/d/1NjS1S9_UF8pZlKE2WCAqn5UzxHE_imNezgLo-BrlS-s/edit?usp=sharing))

2. **Open Command Prompt:**
   Press `Win`, type `cmd` and press `Enter`

4. **Clone the Repository:**
    - Download the repository by pasting the following into the terminal:
   ```bash
   git clone https://github.com/Doomsy1/Pollinator
   cd Pollinator
   ```

5. **Install Required Libraries:**
    - Install the necessary Python packages by pasting the following into the terminal:
   ```bash
   pip install -r requirements.txt
   ```

6. **Configuring the Universal Robotics Cobot Arm:**
   - Configure the robot’s network settings following the steps in the [Configuring a Universal Robotics Cobot Arm](https://docs.google.com/document/d/1CyodpAacuGGx8rIEQoFwfiqiNlRN47e698ffsrlCcqg/edit?usp=sharing) guide.

## Usage

### Pollination Process
Ensure both the camera and the robot are connected to your computer then paste the following into the terminal to start the pollinator:
   ```bash
   python pollinator.py
   ```
- This script integrates the camera input, clustering algorithm, and robot control to execute the pollination.

## Technical Details

### Coordinate System Conversion
The system relies on the Intel RealSense camera to provide both color and depth images. From these inputs, vectors from the camera to the flowers are calculated. These vectors are initially relative to the camera’s coordinate system and must be transformed to align with the robot’s base coordinate system.

1. **Vector Calculation:** Vectors from the camera to the flowers are calculated using the color and depth images provided by the camera.
2. **Offset Adjustment:** These vectors are offset to be relative to the Tool Center Point (TCP) of the robotic arm.
3. **Coordinate System Rotation:** The vectors are then [rotated](https://en.wikipedia.org/wiki/Rodrigues'_rotation_formula) to match the coordinate system of the robot’s base.
4. **Position Summation:** Each vector is summed with the current TCP position to determine the exact position where the robot needs to move its TCP for successful flower pollination.

## Limitations and Future Work

### Controlled Environment Testing
This system has been tested in a controlled environment. Future work could focus on adapting the system for more variable, real-world agricultural settings, which would involve handling different lighting conditions, occlusions, and varying flower densities.

### Scalability
Currently, the system is optimized for small-scale environments. Further development would be required to make it suitable for large-scale commercial operations.

## Authors and Acknowledgment
- Lead Developer: [Ario Barin Ostovary](https://github.com/Doomsy1)
- Contributors: [Jongbin Lee](https://github.com/jblee0310)
