#!/usr/bin/env python
# coding: utf-8

# In[2]:
import Lau_ImportCSV as my_csv
import pandas as pd
import pptk


# In[5]:


#FIRST LIBRARY
import numpy as np #Se importa la librería numpy
from numpy import linalg as la #Se importa linalg, que son herramientas de álgebra lineal
class GPF(object):
    def __init__(self, n_iter=2, n_lpr=20, th_seeds=0.4, th_dist=0.2):
        self.n_iter = n_iter
        self.n_lpr = n_lpr
        self.th_seeds = th_seeds
        self.th_dist = th_dist

    def ExtractInitialSeeds(self, point): # Función con entrada: PUNTOS, salida: PUNTOS 
        """
        args:
        `point`:shape[n,3],[x,y,z]
        """
        p_sort = point[np.lexsort(point[:,:3].T)][:self.n_lpr]
        lpr = np.mean(p_sort[:,2])
        cond = point[:,2] <(lpr+self.th_seeds)
        return point[cond]
 
    def main(self, seeds, point):
        pg = seeds
        png = point
        cov = np.cov(pg[:,:3].T)
        for i in range(self.n_iter):
            # estimate plane
            cov = np.cov(pg[:,:3].T)
            s_mean = np.mean(pg[:,:3],axis=0)
            U,sigma,VT=la.svd(cov)
            #The values are ordered in descending order. With -1 we take the last value
            normal = U[:,-1]
            d = -np.dot(normal.T,s_mean)
            # condition
            th=self.th_dist - d
            cond_pg = np.dot(normal,point[:,:3].T)<th
            pg = point[cond_pg]
            png = point[~cond_pg]
        return pg,png


# In[6]:


my_object = GPF()


# In[7]:


point = my_csv.point
seeds = my_object.ExtractInitialSeeds(point)
pg, png = my_object.main(seeds, point)
print("Lautaro afirma que se ha importado correctamente la librería Lau_DelphiMejorado.")

