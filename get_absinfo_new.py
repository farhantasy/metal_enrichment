########			Code to obtain EW_r, zabs, logN of each CIV absorbers
########							(in UNIQUES)
########

#Farhanul Hasan: farhasan@nmsu.edu

# import string
import numpy as np
import collections
import sys
import subprocess
import os
from pathlib import Path
from astropy.table import Table
from astropy.io import ascii

# Set log options here:

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,filemode='w')

# Set log file output
handler = logging.FileHandler('get_absinfo_new.log','w')
handler.setLevel(logging.INFO)

# Create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(handler)

cvel = 2.99792458*10.**5. #speed of light in km/s

# def deltav(zqso, zabs):
#     '''calculates the delta v between absorber and galaxy
#     ... or between two redshifts'''

#     deltaz = zabs-zqso

#     deltav = (cvel * deltaz) / (1.0 + zqso)

#     return deltav

#read in QSO sample:
listfile = str(sys.argv[1])
qsolist = np.genfromtxt(listfile,unpack=True,dtype=np.str)

abs_count = 0 #counter for tracking number of absorbers

zabs_list = [] #list of absorber redshifts
ewr_list, ewr_e_list = [], [] #list of absorber EQW_r and sigma
logN_list, logN_l_list, logN_u_list = [], [], []  #list of absorber logN and errors

abs_qso_list = [] #list of absorber qsos

for qso in qsolist: #loop over each qso
	# cat, jname = qso.split('/')
	# qsodir = Path(qso[1]+'/'+qso[0])
	# ct += 1
	# print(ct)
	# qsodir = qso[0]
	# ewlim_path = Path(qsodir+'/CIV_ewlim.data')
	# zdir = Path(qsodir)
	# print(os.getcwd())

	# os.chdir(qsodir)

	zdirs = [f.path for f in os.scandir(qso) if f.is_dir()] #list of z-dirs in this qso

	abs_count += len(zdirs) #add to the absorber tally
	
	# print(zdirs)
	if len(zdirs) == 0:
		logger.info("============= no absorbers found in {}. ============\n".format(qso))
		continue 
	else:
		# print(zdirs)
		logger.info("============= {} absorbers found in {}. ============\n".format(len(zdirs),qso))

		for zdir in zdirs:
			# c,q,zd = zdir.split('/',3)
			# print(zd)
			os.chdir(zdir) #go into redshift directory
			# print(os.getcwd())

			ews_path = Path('sysanal.ews')
			zabs_path = Path('zabs.dat')
			aod_path = Path('sysanal.aod')

			#the following if loop is not needed for the main code:
			if (ews_path.exists() == False) or (zabs_path.exists() == False) or (zabs_path.stat().st_size == 0):
				os.chdir('../..')
				# continue
			else: 
				
				zabs = np.loadtxt('zabs.dat',usecols=(0),unpack=True,dtype='float') #zabs from zabs.dat
				# zab = ascii.read('zabs.dat',format='basic',data_start=0) #zabs from zabs.dat
				# print(zabs)

				aod = np.loadtxt('sysanal.aod',skiprows=1, usecols=(4,5,6),unpack=True)

				ews = np.loadtxt('sysanal.ews',skiprows=1, usecols=(3,4),unpack=True)
				
				# for k in zabs:
				zabs_list.append(float(zabs))
				ewr_list.append(float(ews[0][0])), ewr_e_list.append(float(ews[1][0]))
				logN_list.append(float(aod[0][0]))
				logN_l_list.append(float(aod[1][0])), logN_u_list.append(float(aod[2][0]))

				# print(ewr[0][0])
				abs_qso_list.append(qso)
				os.chdir('../..')

logger.info("===== data obtained from {} absorbers found in total =====\n".format(abs_count))


t = Table([abs_qso_list, zabs_list, ewr_list, ewr_e_list, logN_list, logN_l_list, logN_u_list],
	names=('QSO', 'z_abs', 'EW_r','EW_r_e','logN','logN_l','logN_u'))

ascii.write(t,'abs_info_new.txt', overwrite=True)
# t = np.array([zabs_list, ewr_list, ewr_e_list])
# np.savetxt('abs_info.txt',t,fmt = '%1.4f')