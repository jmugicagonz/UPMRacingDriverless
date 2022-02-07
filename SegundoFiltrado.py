import numpy as np

th_discont = 0.025
def classify_layer(points,layer_ID=3,azimuth=5):
    #Function to classify points in an ascendent azimuth by layer
    # points: Nxm homogeneous 3d points where layer_ID indicates the position of the layer_ID and azimuth the position of the azimuth
    filtered = [[]for i in np.arange(16)]
    for i in np.arange(len(points)):
        j = int(points[i,layer_ID])
        filtered[j-1].append(points[i])
    
    #Now we remove the subLists whose layers are empty
    Aux = []
    removed = 0;
    for i in np.arange(16):
        if(len(filtered[i])>3):
            filtered[i] = np.asarray(filtered[i])
            Aux.append(filtered[i])
        else:
            removed+=1
    
    Aux = np.asarray(Aux)  
    filtered = Aux
    acumulative = []
    for i in np.arange(16-removed):
        index = np.lexsort(filtered[i][:,:].T)
        p_sort = filtered[i][index]
        acumulative.append(p_sort)
    
    acumulative = np.asarray(acumulative)
    return acumulative

def depth_discontinuity(points,distance=4):
    #Function to retain just those points where there's depth discontinuity
    # points: LxNxm homogeneous 3d points where distance indicated the position of the distance. L is the number of layer_ID not empty
    filtered = [[]for i in np.arange(len(points))]
    for j in np.arange(len(points)):
        length = len(points[j])
        for i in np.arange(length):
            if i<(length-1):
                if not(np.abs(points[j][i,distance]-points[j][i-1,distance])<th_discont and np.abs(points[j][i,distance]-points[j][i+1,distance])<th_discont):
                    filtered[j].append(points[j][i])
            else:
                if not(np.abs(points[j][i,distance]-points[j][i-1,distance])<th_discont):
                    filtered[j].append(points[j][i])
        filtered[j] = np.asarray(filtered[j])
    filtered = np.asarray(filtered)
    return filtered

def azimuth_discontinuity(points,azimuth=5,th_azimuth=100):
    #Function to retain just those points where there's azimuth discontinuity
    # points: LxNxm homogeneous 3d points where distance indicated the position of the distance. L is the number of layer_ID not empty
    filtered = [[]for i in np.arange(len(points))]
    for j in np.arange(len(points)):
        length = len(points[j])
        for i in np.arange(length):
            if i<(length-1):
                aux1 =np.abs(points[j][i,azimuth]-points[j][i-1,azimuth])
                aux2 = np.abs(points[j][i,azimuth]-points[j][i+1,azimuth])
                if not((aux1<th_azimuth or aux1>30000)  and (aux2<th_azimuth or aux2>30000)):
                    filtered[j].append(points[j][i])
            else:
                aux3 = np.abs(points[j][i,azimuth]-points[j][i-1,azimuth])<th_azimuth
                if not(aux3<th_azimuth or aux3>30000):
                    filtered[j].append(points[j][i])
        filtered[j] = np.asarray(filtered[j])
    filtered = np.asarray(filtered)
    return filtered


def GreatVector(layered):
    points = []
    for i in np.arange(len(layered)):
        points.extend(layered[i])
    points = np.asarray(points)
    return points
