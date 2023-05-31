import numpy as np
import pandas as pd
from numpy import pi
from pyDOE import *   


    
#latin hypercube sampling-maximize the minimum distance between points, but place the point in a randomized location within its interval
def lhc_samples_maximin(dim,n,ranges): 
    samples=lhs(dim, samples=n, criterion='maximin')
    for i in range(dim): 
       samples[:,i]=samples[:,i]*(ranges[(2*i+1)]-ranges[2*i]) + ranges[2*i]
    return samples

#latin hypercube sampling-minimize the maximum correlation coefficient
def lhc_samples_corr(dim,n,ranges): 
    samples=lhs(dim, samples=n, criterion='corr')
    for i in range(dim): 
       samples[:,i]=samples[:,i]*(ranges[(2*i+1)]-ranges[2*i]) + ranges[2*i]
    return samples

# monte carlo sampling
def random_sampling(dim,n,ranges):
    samples=np.random.rand(n,dim)
    for i in range(dim): 
       samples[:,i]=samples[:,i]*(ranges[(2*i+1)]-ranges[2*i]) + ranges[2*i]
    return samples
    



