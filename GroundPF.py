import numpy as np
import pptk
import csv
import DelphiMejorado as DM
import CustomCSV

######THE OBJECTIVE OF THIS CODE IS TO APPLY THE GROUND FILTERING ALGORITHM DELPHI IN A PROPER WAY, WITH ITS PROPER SEGMENTATION
class GPFV(object):
    def __init__(self,th_z=2, n_iter=2, n_lpr=20, th_seeds=0.05, th_dist=0.05,n_divisions=12,a_max=(2*np.pi),d_max=7,name='Pruebas_Csv\Prueba3.csv'):
        self.n_iter = n_iter
        self.n_lpr = n_lpr
        self.th_seeds = th_seeds
        self.th_dist = th_dist
        self.th_z = th_z
        self.coordinates = []
        self.n_divisions = n_divisions
        self.a_max = a_max
        self.d_max = d_max
        self.name = name
###FUNCTION TO USE WHEN READING POINTS ON A CSV
#    def preProcesamientoCsv(self,name):
#        with open(name, mode='r') as csv_file:
#            csv_reader = csv.DictReader(csv_file)     
#            for row in csv_reader:
#                temp=[row["Points_m_XYZ:0"],row["Points_m_XYZ:1"],row["Points_m_XYZ:2"]]
#                self.coordinates.append(temp)
#        point = np.asarray(self.coordinates).astype(np.float)
#        return point
##FUNCTION TO USE WHEN READING POINTS FROM ROS   
    def preProcesamientoROS(self, vector):
        point = np.reshape(vector, (len(vector)/3, 3))
        return point
##SEGMENTATION IN A NODIVISIONS NUMBER OF SEGMENTS (WITH THETA), INSIDE THE ANGLE MAXANGLE. IT ALSO FILTERS POINTS FURTHER THAN MAXDISTANCE AND HIGHER THAN ZGROUND+TH_Z       
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
    #FUNCTION TO USE ONLY IN PYTHON >3.5
    def display3d(self):
        ground,nonGround = self.main()
        coordinatesIn = []
        coordinatesIn.extend(ground)
        coordinatesIn.extend(nonGround)
        coordinatesIn = np.asarray(coordinatesIn)
        v = pptk.viewer(coordinatesIn[:,:3])
        v.set(point_size=0.01)
        v = pptk.viewer(nonGround[:,:3])
        v.set(point_size=0.01)   
    #FUNCTION TO DO THE COMPLETE GROUNDFILTERING
    def main(self):
        #Change if initial file is not Csv (for ROS)
        point = CustomCSV.preProcesamientoCsv(self.name);
        coordinatesIn = []
        coordinatesIn.extend(point)
        coordinatesIn = np.asarray(coordinatesIn)
        #v = pptk.viewer(coordinatesIn[:,:3])
        #v.set(point_size=0.01)
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
        return ground,nonGround

