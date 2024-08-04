import numpy as np
from sklearn.cluster import DBSCAN
from collections import defaultdict
from vector import Vector
from config import *

def cluster(points):
    # Run DBSCAN algorithm
    db = DBSCAN(eps=EPS, min_samples=2).fit(points)
    labels = db.labels_

    # Organize points by clusters
    clusters = defaultdict(list)
    for point, label in zip(points, labels):
        if label != -1:  # Ignore noise points
            clusters[label].append(point)

    # Split clusters if they exceed the max points per cluster
    final_clusters = []
    for cluster_points in clusters.values():
        final_clusters.append(cluster_points)

    return final_clusters

def calculate_centroids(clusters):
    centroids = []
    for cluster in clusters:
        centroid = np.mean(cluster, axis=0)
        centroids.append(centroid)
    return centroids

def find_clusters(vectors):
    # Convert list of vectors 
    points = [v.to_list() for v in vectors]
    clusters = cluster(points)
    centroids = calculate_centroids(clusters)
    return [Vector(*centroid) for centroid in centroids]