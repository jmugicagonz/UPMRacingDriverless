#!/usr/bin/env python
# coding: utf-8

# In[1]:

import numpy as np
import math
import pptk
import Lau_Clustering_Separated as clus
import Lau_EncloseCircle as encl


# In[2]:


# Vemos el centro y radio del círculo que engloba a la proyección y guardamos los resultados.
def EncloseCluster(conjunto):
    conjunto_projected = np.delete(conjunto, 2, 1)
    Xcircle, Ycircle, Rcircle = encl.make_circle(conjunto_projected)
    return Xcircle, Ycircle, Rcircle

# Función que obtiene la distancia entre dos puntos:
def DistanceToCenter(Xcircle, Ycircle, PointGround):
    Xdist = PointGround[0] - Xcircle
    Ydist = PointGround[1] - Ycircle
    Xdist_2 = Xdist * Xdist
    Ydist_2 = Ydist * Ydist
    Dist = math.sqrt(Xdist_2 + Ydist_2)
    return Dist

# Comparamos la distancia de los puntos del suelo con Rcircle. Si es menor, incluimos el punto en "ClusterGround"
def ValidGround(pg, th, Xcircle, Ycircle, Rcircle):
    DistMax = Rcircle + th*Rcircle
    ClusterGround = []
    for i in np.arange(len(pg)):
        Dist = DistanceToCenter(Xcircle, Ycircle, pg[i])
        if Dist < DistMax:
            ClusterGround.append(pg[i])
    ClusterGround = np.array(ClusterGround)
    return ClusterGround

# En este main, las entradas son el cluster, los puntos de suelo y el threshold (porcentaje extra del radio).
def ObtainGround(conjunto, pg, th = 0.2):
        Xcircle, Ycircle, Rcircle = EncloseCluster(conjunto) # Usamos esta función para encerrar el cluster en un círculo 
        # y obtener el centro "CenterCircle" y la distancia al centro en una variable a parte "Rcircle".
        ClusterGround = ValidGround(pg, th, Xcircle, Ycircle, Rcircle) # Usamos esta función para obtener los puntos de suelo del cluster.
        return ClusterGround

def UnirClusters(conjunto, ClusterGround):
    conjunto = np.asarray(conjunto)
    ClusterWithGround = np.append(conjunto, ClusterGround, 0)
    return ClusterWithGround


# In[3]:


# INICIALIZAMOS los parámetros de entrada, incluído el array de "ClusterWithGround"
conjunto = clus.conjunto
th = 0.2
pg = clus.pg
ClusterWithGround = [[]for i in np.arange(len(conjunto))]

# PRIMERO, hacemos un bucle para aplicar el suelo a cada uno de los conjuntos del array "conjunto"
for i in np.arange(len(conjunto)):
    ClusterGround = ObtainGround(conjunto[i], pg, th) # Función para obtener el suelo del "conjunto[i]"
    if len(ClusterGround)==0:
        ClusterWithGround [i] = conjunto[i]
    else:
        ClusterWithGround [i] = UnirClusters(conjunto[i], ClusterGround) # Función para unir cluster y suelo 


# SEGUIDAMENTE, creamos un array de atributos para los clusters.
attrib = []
for i in np.arange(len(ClusterWithGround)):
    prov=pptk.rand(1,3)
    prov2 = np.asarray(prov)
    prov3 = np.ones((len(ClusterWithGround[i]),3))
    prov4 = np.multiply(prov2,prov3)
    prov4 = np.asarray(prov4)
    attrib.extend(prov4)

attrib = np.asarray(attrib)

# FINALMENTE, representamos el ArrayCompleto de clusters con su suelo.
ArrayCompleto=[]
for i in np.arange(len(ClusterWithGround)):
    ClusterWithGround[i]=np.asarray(ClusterWithGround[i])
    ArrayCompleto.extend(ClusterWithGround[i])
ArrayCompleto=np.asarray(ArrayCompleto)
v = pptk.viewer(ArrayCompleto[:,:3])
v.set(point_size=0.005)
v.attributes(attrib)


# In[4]:


print(len(ArrayCompleto))

