import csv
import numpy as np
##FUNCTION TO USE WHEN READING POINTS ON A CSV
def preProcesamientoCsv(name):
    coordinates = []
    with open(name, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)     
        for row in csv_reader:
            temp=[row["Points_m_XYZ:0"],row["Points_m_XYZ:1"],row["Points_m_XYZ:2"],row["laser_id"],row["distance_m"],row["azimuth"]]
            coordinates.append(temp)
    point = np.asarray(coordinates).astype(np.float)
    return point