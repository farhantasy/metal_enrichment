################ Code to ewlims from each QSO ################ 
################ ...to make a CDF of them later ################ 
################ ################ ################

import string
import numpy as np
import sys
import itertools
import os
from subprocess import call
import logging


# Set log options here:

# logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.INFO,filemode='w')

# # Set log file output
# handler = logging.FileHandler('gwz_uniques.log','w')
# handler.setLevel(logging.INFO)

# # Create a logging format
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)

# # Add the handlers to the logger
# logger.addHandler(handler)


#sigma detection limit:
N_sigma = 5.

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
        # logger.info("============= CIV_ewlim.mask NOT found in {}. ============\n".format(qso))  
        os.chdir("..")
        continue

    else:        
    # Read in CIV_ewlim.mask and store redshift and corr. EWlim in arrays:
        print(qso)
        f = np.loadtxt('CIV_ewlim.mask',unpack=True)
        # logger.info("============= Reading in CIV_ewlim.mask for {}. ============\n".format(qso))  
        z_arr, ewl_arr = [], []

        for j in range(len(f[0])):

            z,ewlim,mask = f[0][j],f[1][j],f[2][j]

            if mask == 1.:
                # z_arr.append(float(z)), ewl_arr.append(float(ewlim) / (1.+float(z)))
                EW_limit.append(float(ewlim) / (1.+float(z)))
            # else:
            #     continue
            
        # redshift.append(z_arr)
        # EW_limit.append(ewl_arr)

    os.chdir("..")   
 

np.savetxt('ewlims_all.txt',EW_limit,fmt='%1.5f')
