#!/usr/bin/env python
# coding: utf-8

# In[1]:

import numpy as np
import math
import pptk
import Lau_Clustering_Separated as clus
import Lau_EncloseCircle as encl
import Lau_ObtainClusterGround as obtain
import Lau_GroundPF as D3D
from math import pi

point = D3D.point
D3d = D3D.GPFV()  #Hacemos que D3d sea un objecto de la clase GPFV
pg,png = D3d.main()


# In[2]:


# DEFINIMOS las funciones:
def Zground(point):
    Xmin, Ymin, Zmin = np.amin(point, 0)
    return Zmin

def EncloseCluster(conjunto):
    conjunto_projected = np.delete(conjunto, 2, 1)
    Xcircle, Ycircle, Rcircle = encl.make_circle(conjunto_projected)
    return Xcircle, Ycircle, Rcircle

def DistanceToLidar(Xcircle, Ycircle, Zmin):
    Xdist_2 = Xcircle * Xcircle
    Ydist_2 = Ycircle * Ycircle
    Zdist_2 = Zmin * Zmin
    Dist = math.sqrt(Xdist_2 + Ydist_2 + Zdist_2)
    return Dist

def expectedconepoints(Dist):
    hc=0.325
    wc=0.228
    rv=2*pi/180
    rh=0.2*pi/180
    tan1=np.tan(rv/2)
    tan2=np.tan(rh/2)
    d = (0.5*(hc/(2*Dist*tan1))*(wc/(2*Dist*tan2)))
    return(d)


# In[3]:


# INICIALIZAMOS parámetros.
conjunto = clus.conjunto
ClusterWithGround = obtain.ClusterWithGround
TH = 0.05
pg = np.asarray(pg)
Zmin = Zground(pg)
Clusterwithcone = []


# Este primer bucle es para saber cuántos conos tenemos, y guardar la cantidad en la variable ncluster.
ncluster=0
for i in np.arange(len(ClusterWithGround)):
    Xcircle, Ycircle, Rcircle = EncloseCluster(ClusterWithGround[i])
    Dist = DistanceToLidar(Xcircle, Ycircle, Zmin)
    d = expectedconepoints(Dist) # "d" es el número de puntos que tendría un cono a la distancia Dist
    if ((d + d*TH)>len(ClusterWithGround[i])):
        if((d - d*TH)<len(ClusterWithGround[i])):
            ncluster=ncluster+1
    

# CREAMOS "Clusterwithcone" de tamaño "ncluster"
Clusterwithcone = [[]for i in np.arange(ncluster)]
print(f'Tenemos {len(Clusterwithcone)} cono(s).')  
 
# VOLVEMOS a mirar los clusters. Los que sean conos se meten en el array "Clusterwithcone".
z=0
for i in np.arange(len(ClusterWithGround)):
    Xcircle, Ycircle, Rcircle = EncloseCluster(ClusterWithGround[i])
    Dist = DistanceToLidar(Xcircle, Ycircle, Zmin)
    d=expectedconepoints(Dist)
    if ((d + d*TH)>len(ClusterWithGround[i])):
        if((d - d*TH)<len(ClusterWithGround[i])):
            Clusterwithcone [z] = ClusterWithGround[i]        
            z=z+1
            
attrib = []
for i in np.arange(len(Clusterwithcone)):
    prov=pptk.rand(1,3)
    prov2 = np.asarray(prov)
    prov3 = np.ones((len(Clusterwithcone[i]),3))
    prov4 = np.multiply(prov2,prov3)
    prov4 = np.asarray(prov4)
    attrib.extend(prov4)

attrib = np.asarray(attrib)

# CUARTO, representamos el ArrayCompleto de clusters con su suelo.
ArrayCompleto=[]
for i in np.arange(len(Clusterwithcone)):
    Clusterwithcone[i]=np.asarray(Clusterwithcone[i])
    ArrayCompleto.extend(Clusterwithcone[i])
ArrayCompleto=np.asarray(ArrayCompleto)
v = pptk.viewer(ArrayCompleto[:,:3])
v.set(point_size=0.005)
v.attributes(attrib)

