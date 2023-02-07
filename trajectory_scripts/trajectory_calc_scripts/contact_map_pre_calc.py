#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

This script analyzes frames of a trajectory that has been split up into many PDB files and exports a list of population-weighted PRE values between ALL alpha carbons of chain A and chain B (both intramolecular and intermolecular contacts).

This script has been specifically adapted for producing a contact map between alpha carbons of FCP1 and RAP74 to process the trajectories run by Scott in March/April 2020.

Note that residues 1-67 correspond to RAP74 452-520, 68-71 corresponds to the GPGW cloning artifact + exogenous tryptophan installed on ctFCP1, and 72-153 correspond to ctFCP1 879-960.

Created on Thu Apr 30 09:00:31 2020

@author: Victor Prieto

"""

#starts program runtime
import time
start_time = time.time()

import numpy as np
from math import e
from math import pi

######
#PRE calculation section, references Battiste and Wagner, Biochemistry 2000 and Sjott and Clubb, Bio Protoc 2016

#outputs the intensity ratio given nucleus and distance r
def pre_calculator(nucleus, r):

    #correlation time for the electron nuclear interaction
    tau = 0.0000000207 #20.7 ns

    t = 0.0125   #the total evolution time of the transverse proton magnetization during the NMR experiment, per Sjott and Clubb, or total INEPT evolution time of the HSQC (∼9 ms), per Battiste and Wagner.

    #Larmor frequency of the nuclear spin (proton, carbon, etc.) For proton, omega = 500,000,000Hz. For carbon, omega = 125,700,000Hz.
    if nucleus == '13C':
        omega = 150890000*2*pi # 13C Larmor frequency for NEO600
        K = 7.778e-34   #equation for K defined in Battiste and Wagner
        R2 = 8.1    #R2 has been defined by Erik as 8.1 for 13C - not sure why.
    if nucleus == '1H':
        omega = 600000000*2*pi # 1H Larmor frequency for NEO600
        K = 1.23e-32
        R2 = 13   #R2 has been defined by Erik as 13 for 1H - not sure why.

    r = r*1e-8   #note: this may be the wrong conversion factor for angstroms to centimeters, but it seems to fit the experimental data better. Not sure why, there may be another error in the calculation.

    #equation 5 from Battiste and Wagner
    b = 4*tau+((3*tau)/(1+(omega**2)*(tau**2)))
    R2S = (K * b)/(r**6)

    #equation 4 from Battiste and Wagner
    return (R2*e**(-R2S*t))/(R2 + R2S)

distance = []
pre_values = []

## this section produces a nice figure that shows how the PRE Iratio varies as a function of distance in angstroms, used as a sanity check that the PRE calculator is modelling PRE from distances correctly.

# Removed this section for running from terminal window, since plt breaks the script?
#
#for i in range(1, 50):
#    pre = pre_calculator('1H', i)
#    if i % 5 == 0:
#        print('PRE at distance ' + str(i) + ' angstroms ----- ' + str(pre))
#    distance.append(i)
#    pre_values.append(pre)
#
#import matplotlib.pyplot as plt
#plt.plot(distance, pre_values, 'r:')
#plt.ylabel('$I_{para}/I_{dia}$', fontsize = 10)
#plt.xlabel('distance (angstroms)', fontsize = 10)
#plt.show()

#######
# make a folder for trajectory analysis files

import os
import os.path

new_path = r'/sas_syn/Data_VP/trajectory_scripts/KRK_calc_output/'
try:
    os.mkdir(new_path)
except:
    None

##########

# identify the number of pdb files in each directory to be analyzed (i.e. frames in trajectory)
number_of_files = 20000

# defining split directory paths

directories = []
filenames = []

for i in range(0, 20):
    dir_path = 'split_CA_N_' + "{:03d}".format(i) + '_campari_traj/'
    directories.append(dir_path)

# section that defines PDB filenames to be opened later

    for j in range(0,number_of_files):
        dir_number = '{:02d}'.format(i) + '_'
        file_number = str(j + 1).zfill(6)
        file_name = '/sas_syn/CAMPARI_TRAJ/rap74_fcp1_KRK_restrained/' + dir_path + dir_number + file_number + '.pdb'
        filenames.append(file_name)

#open file for writing
output_file_name = new_path + 'KRK_pre_values.txt'
output_file = open(output_file_name, 'w')

##########
# section that opens each PDB, analyzes for distance, converts to PRE, and saves the value

processed_models = 0

for file in filenames:
    try:
        pdb_file = open(file, 'r')
    except FileNotFoundError:
        print('wrong filename = ', file)
        continue

    fcp1_model = []
    rap74_model = []
    pre_array = []

        #identifies the lines in the PDB file corresponding to atoms in ctFCP1 and appends the xyz coordinates to the array labeled 'fcp1_model'

    for line in pdb_file:
        if 'ATOM' in line:
            appendage = [float((str(line)[30:38]).strip()), float((str(line)[38:46]).strip()), float((str(line)[46:54]).strip())]
            fcp1_model.append(appendage)
        #same thing as above, but finds the xyz coordinates for the residue of interest in RAP74 and appends them to array labeled 'rap74_model'
        if 'ATOM' in line:
            appendage = [float((str(line)[30:38]).strip()), float((str(line)[38:46]).strip()), float((str(line)[46:54]).strip())]
            rap74_model.append(appendage)

    #calculates the distance between each xyz coordinate in fcp1_model and rap74_model (i1 and j1, i1 and j2... i1 and jn, i2 and j1, i2 and j2... in and jn).
    count_i = 0
    for i in fcp1_model:
        count_j = 0
        #please note that i = j = 1 for the first element, not zero
        count_i +=1
        pre_list = []
        for j in rap74_model:
            count_j += 1
            distance = np.sqrt(((i[0]-j[0])**2)+((i[1]-j[1])**2)+((i[2]-j[2])**2))
            pre_value = pre_calculator('1H', distance)
            pre_list.append(pre_value)
        pre_array.append(pre_list)

    if processed_models == 0:
        average_pre = np.array(pre_array)

    else:
        pre_array = np.array(pre_array)
        try:
            average_distance = np.add(average_distance, distance_array)
        except ValueError:
            print('ValueError on file: ', file)
            continue

    # nice status update that reports every 100 processed models
    processed_models += 1
    if processed_models % 100 == 0:
        print ('\nnumber of processed models: ', processed_models, '\n')

# divides pre value sums up to this point by the number of models processed
average_pre = average_pre/processed_models

#print('\ntotal number of processed models: ', f'{processed_models:,}')
print('\ntotal number of processed models: ', processed_models)

count_i = 0
for i in average_pre:
    count_i += 1
    count_j = 0
    for j in average_pre[count_i-1]:
        count_j += 1
        output_file.write(str(count_i) + '\t', )
        output_file.write(str(count_j) + '\t', )
        output_file.write(str(j) + '\n')

output_file.close()

#prints runtime
print("--- %s seconds ---" % (time.time() - start_time))
