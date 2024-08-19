import numpy as np

def calculate_total_distance(points):
    '''Calculates the total distance of the given path'''
    total_distance = 0
    for i in range(len(points) - 1):
        total_distance += np.linalg.norm(np.array(points[i]) - np.array(points[i + 1]))
    total_distance += np.linalg.norm(np.array(points[-1]) - np.array(points[0]))  # close the loop
    return total_distance

def two_opt_algorithm(points):
    '''Improves the path using the 2-opt algorithm'''
    best_distance = calculate_total_distance(points)
    improvement = True

    while improvement:
        improvement = False
        for i in range(1, len(points) - 1):
            for j in range(i + 1, len(points)):
                if j - i == 1:  # adjacent nodes, no need to swap
                    continue
                new_path = points[:i] + points[i:j][::-1] + points[j:]
                new_distance = calculate_total_distance(new_path)
                if new_distance < best_distance:
                    points = new_path
                    best_distance = new_distance
                    improvement = True
        if not improvement:
            break

    return points

def order_path(points):
    '''Orders 3D points using a 2-opt algorithm to solve the Traveling Salesman Problem'''
    # Start with the nearest neighbor algorithm as an initial solution
    start = points[0]
    ordered_points = [start]
    points = points[1:]

    while len(points) > 0:
        nearest = None
        nearest_distance = None
        for point in points:
            distance = np.linalg.norm(np.array(point) - np.array(start))
            if nearest is None or distance < nearest_distance:
                nearest = point
                nearest_distance = distance

        ordered_points.append(nearest)
        points.remove(nearest)
        start = nearest

    # Apply the 2-opt algorithm to improve the initial solution
    ordered_points = two_opt_algorithm(ordered_points)

    return ordered_points
