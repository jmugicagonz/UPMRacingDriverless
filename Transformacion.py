import FiltradoInicial as FI
import pptk
import numpy as np
import GroundPF
import CustomCSV
import SegundoFiltrado
import TercerFiltrado
import CuartoPasoCentroides

coordinates =FI.preProcesamientoCsv('Pruebas_CSV\Transformacion.csv')
# v = pptk.viewer(coordinates[:,:3])
# v.set(point_size=0.01)
#
##FIRST WE WILL FILTER THE GROUND
GFObject = GroundPF.GPFV(th_z=4,name='Pruebas_CSV\Transformacion.csv');
ground,nonground = GFObject.main()
# v = pptk.viewer(nonground[:,:3])
# v.set(point_size=0.01)
#
##SECOND WE FILTER UNTIL IT REAMINS JUST THE OBJECT
processed = FI.initial_filter(2.5,nonground)
fourD = np.concatenate((processed[:,:3],np.reshape(np.ones(len(processed)), (len(processed), 1))),axis=1)


plane, inlier_list = FI.fit_plane_LSE_RANSAC(fourD)
firstFiltered = processed[inlier_list]
# f = pptk.viewer(firstFiltered[:,:3])
# f.set(point_size=0.01)

# auxVector = []
# auxVector.extend(firstFiltered[:,:3])
# auxVector.extend(centroids)
# auxVector = np.asarray(auxVector)
# f = pptk.viewer(auxVector)
# f.set(point_size=0.01)

##THIRD WE DO THE SECOND FILTER: JUST THE BORDERS
p_sort = SegundoFiltrado.classify_layer(firstFiltered)
secondFiltered = SegundoFiltrado.depth_discontinuity(p_sort)
# greatVector = SegundoFiltrado.GreatVector(secondFiltered)
# f = pptk.viewer(greatVector[:,:3])
# f.set(point_size=0.01)
altsecondFiltered = SegundoFiltrado.azimuth_discontinuity(p_sort)
# altgreatVector = SegundoFiltrado.GreatVector(altsecondFiltered)
# f = pptk.viewer(altgreatVector[:,:3])
# f.set(point_size=0.01)



#FOURTH WE APPLY THE THIRD FILTER: JUST THE CIRCLE BORDERS
circlePoints = TercerFiltrado.circle_points(altsecondFiltered)
# f = pptk.viewer(circlePoints[:,:3])
# f.set(point_size=0.01)


# ##FHIFTH WE APPLY THE FOURTH FILTER: GET THE CENTROIDS
centroids = CuartoPasoCentroides.getCentroids(circlePoints[:,:3])
print(centroids)
f = pptk.viewer(centroids[:,:3])
f.set(point_size=0.01)

#auxVector = []
#auxVector.extend(altgreatVector[:,:3])
#auxVector.extend(centroids)
#auxVector = np.asarray(auxVector)
#f = pptk.viewer(auxVector)
#f.set(point_size=0.01)

#auxVector2 = []
#auxVector2.extend(circlePoints[:,:3])
#auxVector2.extend(centroids)
#auxVector2 = np.asarray(auxVector2)
#f = pptk.viewer(auxVector2)
#f.set(point_size=0.01)

##NOW WE WILL DISPLAY ALL THE POINTS COLORING THOSE CENTROIDS
TotalPoints = []
TotalPoints.extend(coordinates)
TotalPoints.extend(centroids)
TotalPoints = np.asarray(TotalPoints)
f = pptk.viewer(TotalPoints)
f.set(point_size=0.01)


#attrib = []
#prov= np.array([43,255,0])
#prov2 = np.ones((3,3))
#prov3=np.multiply(prov,prov2)
#prov4 = np.asarray(prov4)
#attrib.extend(prov4)
#    prov=  
#    prov2 =  np.array([255,255,255]) 
#    prov3 = np.ones((len(conjunto[i]),3))
#    prov4=np.multiply(prov2,prov3)
#    prov4 = np.asarray(prov4)
#    attrib.extend(prov4)
#
#attrib = np.asarray(attrib)
#greatArray=[]
#for i in np.arange(len(conjunto)):
#    conjunto[i]=np.asarray(conjunto[i])
#    greatArray.extend(conjunto[i])
#greatArray=np.asarray(greatArray)
#v = pptk.viewer(greatArray)
#v.set(point_size=0.01)
#v.attributes(attrib)

