import math
from collections import defaultdict

class UnionFind:
    def __init__(self):
        self.parent = {}

    def add(self, x):
        if x not in self.parent:
            self.parent[x] = x

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]

    def union(self, x, y):
        rootX = self.find(x)
        rootY = self.find(y)
        if rootX != rootY:
            self.parent[rootX] = rootY

    def count(self):
        clusters = 0
        for key in self.parent:
            if self.parent[key] == key:
                clusters += 1
        return clusters

    def get_clusters(self):
        clusters = defaultdict(list)
        for key in self.parent:
            root = self.find(key)
            clusters[root].append(key)
        return clusters

def find_clusters(coordinates, distance):
    print(coordinates)
    uf = UnionFind()

    # Add each point to the union-find structure
    for i in range(len(coordinates)):
        uf.add(i)

    # Perform union operations for points that are within the specified distance
    for i in range(len(coordinates)):
        for j in range(i + 1, len(coordinates)):
            if is_within_distance(coordinates[i], coordinates[j], distance):
                uf.union(i, j)

    # calculate the cluster means
    means = []
    for root in uf.get_clusters():
        xcoord = 0
        ycoord = 0
        zcoord = 0
        cnt = 0
        for index in uf.get_clusters()[root]:
            point = coordinates[index]
            xcoord += point[0]
            ycoord += point[1]
            zcoord += point[2]
            cnt += 1
        means.append([xcoord / cnt, ycoord / cnt, zcoord / cnt])

    return means

def is_within_distance(point1, point2, distance):
    return (abs(point1[0] - point2[0]) < distance and
            abs(point1[1] - point2[1]) < distance and
            abs(point1[2] - point2[2]) < distance)

def main():
    coordinates = []

    # Read file
    with open("targets.txt", "r") as file:
        lines = file.readlines()

    # Process lines
    for line in lines:
        line = line.strip()
        line = line[1:-1]
        parts = line.split(", ")
        coordinates.append([float(parts[0]), float(parts[1]), float(parts[2])])

    uf = UnionFind()

    # Add each point to the union-find structure
    for i in range(len(coordinates)):
        uf.add(i)

    # Perform union operations for points that are within the specified distance
    for i in range(len(coordinates)):
        for j in range(i + 1, len(coordinates)):
            if is_within_distance(coordinates[i], coordinates[j], 0.02):
                uf.union(i, j)

    # Count the number of distinct clusters
    number_of_clusters = uf.count()
    print("Number of clusters:", number_of_clusters)

    # Get and print clusters
    clusters = uf.get_clusters()

    means = []
    for root in clusters:
        xcoord = 0
        ycoord = 0
        zcoord = 0
        cnt = 0
        print(f"Cluster formed by root {root}: ", end="")
        for index in clusters[root]:
            point = coordinates[index]
            print(f"[{point[0]}, {point[1]}, {point[2]}] ", end="")
            xcoord += point[0]
            ycoord += point[1]
            zcoord += point[2]
            cnt += 1
        print(cnt)
        means.append([xcoord / cnt, ycoord / cnt, zcoord / cnt])
        print(f"Average for Cluster formed by root {root}: ({xcoord / cnt}, {ycoord / cnt}, {zcoord / cnt})")

    print(len(lines))
    for mean in means:
        print(f"[{mean[0]:.3f}, {mean[1]:.3f}, {mean[2]:.3f}]")

if __name__ == "__main__":
    main()
