#!/usr/bin/env python
# coding: utf-8

# In[1]:
import Lau_DelphiMejorado as DM


# In[2]:


import numpy as np
import pptk
import csv
######THE OBJECTIVE OF THIS CODE IS TO APPLY THE GROUND FILTERING ALGORITHM DELPHI IN A PROPER WAY, WITH ITS PROPER SEGMENTATION
class GPFV(object):
  def __init__(self,th_z=2, n_iter=2, n_lpr=20, th_seeds=0.05, th_dist=0.05,n_divisions=12,a_max=(2*np.pi),d_max=7):
      self.n_iter = n_iter
      self.n_lpr = n_lpr
      self.th_seeds = th_seeds
      self.th_dist = th_dist
      self.th_z = th_z
      self.coordinates = []
      self.n_divisions = n_divisions
      self.a_max = a_max
      self.d_max = d_max
      'self.name = name'

  def segmentation(self,point):
      sectorized = []
      zGround = np.min(point[:,2])
      condz=point[:,2]<self.th_z+zGround
      point=point[condz]
      prer = np.multiply(point[:,:2],point[:,:2]);
      r =np.sqrt(prer[:,0]+prer[:,1])
      condr = r < self.d_max
      point=point[condr]
      r = r[condr]
      o = np.arctan2(point[:,1],point[:,0])
      intAngle = self.a_max/self.n_divisions
      pointsToSectorize = point
      finAngle = -self.a_max/2
      for p in np.arange(self.n_divisions):
          finAngle = finAngle + intAngle
          pointsInInterval = (o<finAngle)
          pointsToKeep = (o>finAngle)
          sectorized.append(pointsToSectorize[pointsInInterval])
          pointsToSectorize = pointsToSectorize[pointsToKeep]
          o = o[pointsToKeep]
      #sectorized = np.asarray(sectorized).astype(np.float)
      return sectorized

  def display3d(self):
      ground,nonGround = self.main()
      coordinatesIn = []
      coordinatesIn.extend(ground)
      coordinatesIn.extend(nonGround)
      coordinatesIn = np.asarray(coordinatesIn)
      v = pptk.viewer(coordinatesIn[:,:3])
      v.set(point_size=0.005)
      v = pptk.viewer(nonGround[:,:3])
      v.set(point_size=0.005)   

  def main(self):
    #Change if initial file is not Csv (for ROS)
    'point = CustomCSV.preProcesamientoCsv(self.name);'
    sectorized = self.segmentation(point)
    sectorized = np.asarray(sectorized)
    ground = []
    nonGround = []
    for i in np.arange(self.n_divisions-1):
        if len(sectorized[i])>10:
            GPF = DM.GPF(self.n_iter,self.n_lpr,self.th_seeds,self.th_dist)
            seeds = GPF.ExtractInitialSeeds(sectorized[i])
            pg,png = GPF.main(seeds,sectorized[i])
            if len(ground)>1:
                ground = np.concatenate((ground, pg))
            else:
                ground = GPF.main(seeds,sectorized[i])[0]
            if len(nonGround)>1:
                nonGround = np.concatenate((nonGround, png))
            else:
                nonGround = GPF.main(seeds,sectorized[i])[1]
            
    ground = np.asarray(ground).astype(np.float)
    nonGround = np.asarray(nonGround).astype(np.float)
    return ground, nonGround


# In[3]:


my_gpfv = GPFV()


# In[4]:


point = DM.point


# In[10]:


print("Lautaro afirma que se ha importado correctamente la librería Lau_GroundPF.")
