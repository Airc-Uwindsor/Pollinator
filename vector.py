import numpy as np

class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

        self.length = np.linalg.norm([x, y, z])

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def rotate(self, rotation):
        # rotation is a Vector with the rotation vector (rx, ry, rz)
        theta = rotation.length  # Angle of rotation
        if theta > 0:
            k = np.array(rotation.to_list()) / theta  # Normalized axis of rotation
            K = np.array([
                [0, -k[2], k[1]],
                [k[2], 0, -k[0]],
                [-k[1], k[0], 0]
            ])
            rotation_matrix = np.eye(3) + np.sin(theta) * K + (1 - np.cos(theta)) * (K @ K)
            rotated_vector = rotation_matrix.dot(np.array(self.to_list()))
            return Vector(*rotated_vector)
        else:
            return Vector(self.x, self.y, self.z)
        
    def undo_rotate(self, rotation):
        inverse_rotation = Vector(-rotation.x, -rotation.y, -rotation.z)
        return self.rotate(inverse_rotation)
    
    def rotate_rpy(self, roll, pitch, yaw):
        rotation_vector = rpy_to_rotation_vector(roll, pitch, yaw)
        return self.rotate(rotation_vector) 
    
    def to_list(self):
        return [self.x, self.y, self.z]
    
    def __repr__(self):
        return f"Vector(x={self.x}, y={self.y}, z={self.z})"
    
    def __str__(self):
        return f"({self.x:.3f}, {self.y:.3f}, {self.z:.3f})"
    
def rpy_to_rotation_vector(roll, pitch, yaw):
    # Roll rotation matrix (x-axis)
    Rx = np.array([
        [1, 0, 0],
        [0, np.cos(roll), -np.sin(roll)],
        [0, np.sin(roll), np.cos(roll)]
    ])
    
    # Pitch rotation matrix (y-axis)
    Ry = np.array([
        [np.cos(pitch), 0, np.sin(pitch)],
        [0, 1, 0],
        [-np.sin(pitch), 0, np.cos(pitch)]
    ])
    
    # Yaw rotation matrix (z-axis)
    Rz = np.array([
        [np.cos(yaw), -np.sin(yaw), 0],
        [np.sin(yaw), np.cos(yaw), 0],
        [0, 0, 1]
    ])
    
    # Combined rotation matrix (Rz * Ry * Rx)
    R = Rz.dot(Ry).dot(Rx)
    
    # Extract the rotation vector from the rotation matrix
    theta = np.arccos((np.trace(R) - 1) / 2)
    if theta > 0:
        r = np.array([
            R[2, 1] - R[1, 2],
            R[0, 2] - R[2, 0],
            R[1, 0] - R[0, 1]
        ]) / (2 * np.sin(theta))
        rotation_vector = r * theta
        return Vector(*rotation_vector)
    else:
        return Vector(0, 0, 0) # No rotation