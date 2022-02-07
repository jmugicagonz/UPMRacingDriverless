#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
df3 = pd.read_csv('Prueba.csv')
# Dataset is now stored in a Pandas Dataframe


# In[2]:


points_x = df3['Points_m_XYZ:0']
points_y = df3['Points_m_XYZ:1']
points_z = df3['Points_m_XYZ:2']


# In[3]:


puntos_importantes = pd.concat([points_x, points_y, points_z], axis=1, join='inner')


# In[4]:


point = puntos_importantes.values


# In[5]:


print("Lautaro afirma que se ha importado correctamente la librería Lau_ImportCSV")

point