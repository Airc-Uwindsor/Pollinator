import numpy as np

class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

        self.length = np.sqrt(x**2 + y**2 + z**2)

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

    def to_list(self):
        return [self.x, self.y, self.z]
    
    def __repr__(self):
        return f"Vector(x={self.x}, y={self.y}, z={self.z})"
    
    def __str__(self):
        return f"({self.x:.3f}, {self.y:.3f}, {self.z:.3f})"