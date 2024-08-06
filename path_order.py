import numpy as np

def order_path(points):
    '''Orders 3d points Traveling Salesman Problem'''
    # use the nearest neighbor algorithm
    # https://en.wikipedia.org/wiki/Nearest_neighbour_algorithm

    # Start at the first point - points are [x, y, z]
    start = points[0]
    ordered_points = [start]
    points = points[1:]

    while len(points) > 0:
        # Find the nearest point
        nearest = None
        nearest_distance = None
        for point in points:
            distance = np.sqrt((point[0] - start[0])**2 + (point[1] - start[1])**2 + (point[2] - start[2])**2)
            if nearest is None or distance < nearest_distance:
                nearest = point
                nearest_distance = distance

        # Add the nearest point to the ordered list
        ordered_points.append(nearest)
        points.remove(nearest)
        start = nearest


    return ordered_points