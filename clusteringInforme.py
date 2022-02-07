import numpy as np
import GroundPFInforme as D3D
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler
import pptk


D3d = D3D.GPFV(n_iter=2,th_dist=0.05,th_seeds=0.2,n_lpr=100,th_z=1)
pg,png = D3d.main()
D3d.display3d()
X = png
# Compute DBSCAN
db = DBSCAN(eps=0.4, min_samples=10).fit(X[:,:3])
labels = db.labels_
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
z = 0
conjunto = [[]for i in np.arange(n_clusters_)]
for i in db.labels_:
    if i!=-1:
        conjunto[i].append(X[z])
    z = z+1


attrib = []
for i in np.arange(len(conjunto)):
    prov=pptk.rand(1,3)
    prov2 = np.asarray(prov)
    prov3 = np.ones((len(conjunto[i]),3))
    prov4=np.multiply(prov2,prov3)
    prov4 = np.asarray(prov4)
    attrib.extend(prov4)

attrib = np.asarray(attrib)
greatArray=[]
for i in np.arange(len(conjunto)):
    conjunto[i]=np.asarray(conjunto[i])
    greatArray.extend(conjunto[i])
greatArray=np.asarray(greatArray)
v = pptk.viewer(greatArray[:,:3])
v.set(point_size=0.01)
v.attributes(attrib)

