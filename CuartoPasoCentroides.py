from sklearn.cluster import KMeans
import numpy as np
def getCentroids(points):
    # points:  Nx3 homogeneous 3d points
    kmeans = KMeans(n_clusters=4, n_init=100, random_state=0).fit(points)
    return kmeans.cluster_centers_


