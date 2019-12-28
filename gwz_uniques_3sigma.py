################ Code to calculate g(W,z) from ewlim spectra ################ 
################ detection limit at 3 sigma
################ ################ ################ 
################ ################ ################

import string
import numpy as np
import sys
import itertools
import os
from subprocess import call
import logging
# import scipy.integrate as integ
# import scipy.stats
# import scipy.optimize as op
# import matplotlib.pyplot as plt
# from matplotlib import rc
# import numpy.random as npr
# import pylab
# import scipy.odr as odr
# from scipy.optimize import curve_fit
# from matplotlib.patches import Ellipse
# from stat_funcs import *


# Set log options here:

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,filemode='w')

# Set log file output
handler = logging.FileHandler('gwz_uniques_3sigma.log','w')
handler.setLevel(logging.INFO)

# Create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(handler)


#sigma detection limit:
N_sigma = 3.

#define a function to find nearest redshift:
def find_nearest(array,value):
    idx = (np.abs(array-value)).argmin()
    return array[idx]


#read in QSO sample:
listfile = str(sys.argv[1])
jnames = np.loadtxt(listfile,unpack=True,dtype=np.str)

# jnames = np.transpose(jnames)

redshift = [] #array of redshifst
EW_limit = [] #array of EWlims

# counter = 0

for qso in jnames:

    os.chdir(qso)
#     print(os.getcwd())

    
    # Check if CIV_ewlim.mask exists
    if (os.path.isfile('CIV_ewlim.mask') == False):
        logger.info("============= CIV_ewlim.mask NOT found in {}. ============\n".format(qso))  
        os.chdir("..")
        continue

    else:        
    # Read in CIV_ewlim.mask and store redshift and corr. EWlim in arrays:

        f = np.loadtxt('CIV_ewlim.mask',unpack=True)
        logger.info("============= Reading in CIV_ewlim.mask for {}. ============\n".format(qso))  
        z_arr, ewl_arr = [], []

        for j in range(len(f[0])):

            z,ewlim,mask = f[0][j],f[1][j],f[2][j]

            if mask == 1.:
                z_arr.append(float(z)), ewl_arr.append(float(ewlim)/ (1.+float(z)))
            # else:
            #     continue
            
        redshift.append(z_arr)
        EW_limit.append(ewl_arr)


    os.chdir("..")   
    
logger.info("============= Done reading in CIV_ewlim.mask files ============\n")  

# print(redshift,EW_limit)

#define the grid range and spacing:

min_ewl, max_ewl, ewl_spacing = 0.005, 0.405, 0.005
min_CIV_z, max_CIV_z, z_spacing = 1.00, 5.00, 0.005

w_grid = np.arange(min_ewl, max_ewl, ewl_spacing) 

z_grid = np.arange(min_CIV_z,max_CIV_z,z_spacing)


#make and populate g(W,z) grid:

gwz_CIV = np.zeros((len(w_grid),len(z_grid))) #make an array of zeros


for i in range(len(w_grid)):
    
    # CIV z path length
    for j in range(len(z_grid)):
#         gwz_CIV[i][j] = 0
        w, z = w_grid[i], z_grid[j]
        w = round(w,4)
        z = round(z,4)

        logger.info("============= At grid point ({},{}) ============\n".format(w,z))  

        
        for k in range(len(redshift)):
            # redshift[k] = np.array(redshift[qso])
            # print(jnames[k])

            #Make sure that QSO has CIV coverage:

            if len(redshift[k]) == 0:
#                 print(qso)
                continue

            else:
            #Check if z in z grid is within the search range of the JNAME spectrum
                if ((z >= min(redshift[k])) and (z <= max(redshift[k]))):

                    z_val = find_nearest(redshift[k],z)

                    # print(z_val)
                    # z_index = np.where(redshift[k] == z_val)[0]
                    z_index = [i for i, e in enumerate(redshift[k]) if e == z_val][0]
                    
                    #     print(z, z_val, z_index)
                    # print((EW_limit[k][z_index]))
                    if (N_sigma * (EW_limit[k][z_index]) <= w):
                        # print(w_grid[i],z_grid[j])
                        # z_val_grid = find_nearest(z_grid,z_val) #find where z_val is closest on the grid
                        # z_index_grid = [i for i, e in enumerate(z_grid) if e == z_val_grid][0]
                        
                        # if (3.4290 < z < 3.4976) or (3.8977 < z < 3.9728):
                        #     print(z_val,abs(z-z_val))

                        if abs(z-z_val) <= z_spacing:

                            gwz_CIV[i][j] += 1 #add to the grid


np.savetxt('gwz_uniques_3sigma.grid',gwz_CIV,fmt='%i')
