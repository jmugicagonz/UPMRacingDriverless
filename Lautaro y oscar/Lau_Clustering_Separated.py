#!/usr/bin/env python
# coding: utf-8

# In[1]:

import Lau_GroundPF as D3D


# In[2]:


import numpy as np
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler
import pptk

point = D3D.point
D3d = D3D.GPFV()  #Hacemos que D3d sea un objecto de la clase GPFV
pg,png = D3d.main()


# In[5]:


X = png
# Compute DBSCAN
# You can adapt you r distance norm clustering with "eps" maximum distance.

# Primero, se usa la librería DBSCAN que, según los parámetros de entrada,nos saca un 
# array llamado "labels" que contiene el índice del cluster al que pertenece cada punto.
# Si a un punto se le pone la etiqueta (también llamado "label" o "índice") de "-1", significa
# que no pertenecerá a ningún cluster.
db = DBSCAN(eps=0.1, min_samples=9).fit(X[:,:3])
labels = db.labels_
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
z = 0
conjunto = [[]for i in np.arange(n_clusters_)]

# Con este bucle agrupamos los puntos etiquetados por conjuntos --> "conjunto[i]"
for i in labels:
    if i!=-1:
        conjunto[i].append(X[z])
    z = z+1

# Una vez ya tenemos 
attrib = []
for i in np.arange(len(conjunto)):
    prov=pptk.rand(1,3)
    prov2 = np.asarray(prov)
    prov3 = np.ones((len(conjunto[i]),3))
    prov4 = np.multiply(prov2,prov3)
    prov4 = np.asarray(prov4)
    attrib.extend(prov4)

attrib = np.asarray(attrib)


# In[ ]:


cono = conjunto[7]


# In[ ]:


print("Lautaro afirma que se ha importado correctamente la librería Lau_Clustering_Separated")

