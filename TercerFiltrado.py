import numpy as np
def circle_points(points):
    #Function to obtain just those points corresponding to the four circles (or eliminate boundaries)
    # points:  16xNxM homogeneous 3d points
    circlePoints = []
    layersWithCircle = 0
    for i in np.arange(len(points)):
        if len(points[i])>2:
            circlePoints.extend(points[i])
            layersWithCircle+=1
    if(layersWithCircle*4<len(circlePoints)):
        print("Too many outboundaries when creating circle_points")
    circlePoints = np.asarray(circlePoints)
    return circlePoints