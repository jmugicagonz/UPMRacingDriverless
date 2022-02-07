# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 09:11:32 2020

@author: Juan Múgica González
"""

class Point(object):
    def __init__(self,x=0, y=0,z=0,laser_ID=0,distance_m=0,azimuth=0, label=-1):
        self.x=x
        self.y=y
        self.z=z
        self.laser_ID=laser_ID
        self.azimuth=azimuth
        self.label=label
        self.distance_m=distance_m
        self.run = -1