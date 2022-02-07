import numpy as np
import numpy.linalg as la
from svd_solve import svd, svd_solve
import csv
import math

##FUNCTION TO USE WHEN READING POINTS ON A CSV
def preProcesamientoCsv(name):
    coordinates = []
    with open(name, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)     
        for row in csv_reader:
            temp=[row["Points_m_XYZ:0"],row["Points_m_XYZ:1"],row["Points_m_XYZ:2"]]
            coordinates.append(temp)
    point = np.asarray(coordinates).astype(np.float)
    return point
def initial_filter(distBoard, points, distance=4):
    # points: Nxm homogeneous 3d points
    
#    prer = np.multiply(points[:,:2],points[:,:2]);
#    r =np.sqrt(prer[:,0]+prer[:,1])
    '''FUNCION MODIFICADA PARA METER LA R EN LA QUINTA COLUMNTA'''
    r = points[:,4]
    tmp_filtered_list = np.where((r < distBoard+0.5)&(r > distBoard-0.5))[0]   
    filtered = points[tmp_filtered_list, :]
    return filtered

def fit_plane_LSE(points):
    # points: Nx4 homogeneous 3d points
    # return: 1d array of four elements [a, b, c, d] of
    # ax+by+cz+d = 0
    assert points.shape[0] >= 3 # at least 3 points needed
    U, S, Vt = svd(points)
    null_space = Vt[-1, :]
    return null_space

def get_point_dist(points, plane):
    # return: 1d array of size N (number of points)
    dists = []
    dists.extend(np.abs(np.sum(points[i]*plane)) / np.sqrt(plane[0]*plane[0] + plane[1]*plane[1] + plane[2]*plane[2]) for i in range(len(points)))
    #dists = np.abs(np.sum(points*plane)) / np.sqrt(plane[0]*plane[0] + plane[1]*plane[1] + plane[2]*plane[2])
    dists = np.asarray(dists)
    return dists

def angle_planes(plane1,plane2):
    d = (plane1[0]*plane2[0]+plane1[1]*plane2[1]+plane1[2]*plane2[2])
    e1 = math.sqrt(plane1[0]*plane1[0] + plane1[1]*plane1[1] + plane1[2]*plane1[2]) 
    e2 = math.sqrt(plane2[0]*plane2[0] + plane2[1]*plane2[1] + plane2[2]*plane2[2]) 
    d = d / (e1 * e2) 
    A = math.degrees(math.acos(d))
    return A

def fit_plane_LSE_RANSAC(points, iters=2000, inlier_thresh=0.15, return_outlier_list=False):
    # points: Nx4 homogeneous 3d points
    # return: 
    #   plane: 1d array of four elements [a, b, c, d] of ax+by+cz+d = 0
    #   inlier_list: 1d array of size N of inlier points
    max_inlier_num = -1
    max_inlier_list = None
    
    N = points.shape[0]
    assert N >= 3

    for i in range(iters):
        #We pick 3 random points from N
        chose_id = np.random.choice(N, 3, replace=False)
        chose_points = points[chose_id, :]
        tmp_plane = fit_plane_LSE(chose_points)
        #print(angle_planes(tmp_plane,np.array([0,0,1])))
        
        if angle_planes(tmp_plane,np.array([0,-1,0]))<10 or angle_planes(tmp_plane,np.array([0,-1,0]))>170:
            #print(tmp_plane)
            dists = get_point_dist(points, tmp_plane)
            #print(len(points))
#            print(np.max(dists))
            #We pick the points inside the threshold
            #tmp_inlier_list = np.where(dists < inlier_thresh)[0]
            cond = dists<inlier_thresh
            #print(len(tmp_inlier_list))
            #tmp_inliers = points[tmp_inlier_list, :]
            tmp_inliers = points[cond]
            num_inliers = tmp_inliers.shape[0]
            #print(num_inliers)
            if num_inliers > max_inlier_num:
                max_inlier_num = num_inliers
                #max_inlier_list = tmp_inlier_list
                max_inlier_list = cond
                #print(angle_planes(tmp_plane,np.array([0,0,1])))
                #print(len(max_inlier_list))
                #plane = fit_plane_LSE(points[max_inlier_list,:])
                plane = fit_plane_LSE(points[cond])
            #print('iter %d, %d inliers' % (i, max_inlier_num))

    final_points = points[max_inlier_list, :]
    #print(len(final_points))
    plane = fit_plane_LSE(final_points)
    #print(plane)
    
    fit_variance = np.var(get_point_dist(final_points, plane))
    print('RANSAC fit variance: %f' % fit_variance)
    #print(plane)

    dists = get_point_dist(points, plane)

    select_thresh = inlier_thresh*1
    inlier_list = np.where(dists < select_thresh)[0]
    if not return_outlier_list:
        return plane, inlier_list
    else:
        outlier_list = np.where(dists >= select_thresh)[0]
        return plane, inlier_list, outlier_list
    
#FUNCTION TO DO THE COMPLETE GROUNDFILTERING
def main(name):
    #Change if initial file is not Csv (for ROS)
    point = preProcesamientoCsv(name)
