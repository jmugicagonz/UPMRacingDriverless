import numpy as np
from numpy import linalg as la 
class GPF(object):
    def __init__(self, n_iter=2, n_lpr=20, th_seeds=0.4, th_dist=0.2):
        self.n_iter = n_iter
        self.n_lpr = n_lpr
        self.th_seeds = th_seeds
        self.th_dist = th_dist

    def ExtractInitialSeeds(self, point):
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



'''if __name__ =='__main__':
    n_segs = 3
    n_iter = 2
    n_lpr = 20
    th_seeds = 0.05#0.4
    th_dist = 0.05#0.5
    gpf = GPF(n_iter,n_lpr,th_seeds,th_dist)'''

