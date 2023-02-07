#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

This script analyzes frames of a trajectory that has been split up into many PDB files and exports distances between ALL alpha carbons of chain A and chain B (both intramolecular and intermolecular contacts).

This script has been specifically adapted for producing a contact map between alpha carbons of FCP1 and RAP74 to process the trajectories run by Scott in March/April 2020.

Note that residues 1-67 correspond to RAP74 452-520, 68-71 corresponds to the GPGW cloning artifact + exogenous tryptophan installed on ctFCP1, and 72-153 correspond to ctFCP1 879-960.

Created on Thu Apr 30 09:00:31 2020

@author: Victor Prieto

"""

#starts program runtime
import time
start_time = time.time()

#from tkinter import filedialog
import numpy as np

#######
# make a folder for trajectory analysis files

import os
import os.path

new_path = r'/Users/victorprieto/Desktop/Research/python/trajectory_training_set/calc output files/'
try:
    os.mkdir(new_path)
except:
    None

##########

# identify the number of pdb files in each directory to be analyzed (i.e. frames in trajectory)

DIR = '/Users/victorprieto/Desktop/Research/python/trajectory_training_set/trajectory_files'
number_of_files = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
number_of_files = 3

# defining split directory paths

directories = []
filenames = []

for i in range(0, 3):
    dir_path = 'split_CA_N_' + "{:03d}".format(i) + '_campari_traj/'
    directories.append(dir_path)

# section that defines PDB filenames to be opened later

    for j in range(0,number_of_files):
        dir_number = '{:02d}'.format(i) + '_'
        file_number = str(j + 1).zfill(6)
        file_name = '/Users/victorprieto/Desktop/Research/python/trajectory_training_set/' + dir_path + dir_number + file_number + '.pdb'
        filenames.append(file_name)

# open file for writing
output_file_name = new_path + 'wt_distances.txt'
output_file = open(output_file_name, 'w')

distance_array = []
processed_models = 0

for file in filenames:
    pdb_file = open(file, 'r')
    fcp1_model = []
    rap74_model = []
    distance_array = []

        #identifies the lines in the PDB file corresponding to atoms in ctFCP1 and appends the xyz coordinates to the array labeled 'fcp1_model'

    for line in pdb_file:
        if 'ATOM' in line:
            appendage = [float((str(line)[30:38]).strip()), float((str(line)[39:46]).strip()), float((str(line)[46:54]).strip())]
            fcp1_model.append(appendage)

        #same thing as above, but finds the xyz coordinates for the residue of interest in RAP74 and appends them to array labeled 'rap74_model'
        if 'ATOM' in line:
            appendage = [float((str(line)[30:38]).strip()), float((str(line)[39:46]).strip()), float((str(line)[46:54]).strip())]
            rap74_model.append(appendage)

    #calculates the distance between each xyz coordinate in fcp1_model and rap74_model (i1 and j1, i1 and j2... i1 and jn, i2 and j1, i2 and j2... in and jn).
    count_i = 0
    for i in fcp1_model:
        count_j = 0
        #please note that i = j = 1 for the first element, not zero
        count_i +=1
        distance_list = []
        for j in rap74_model:
            count_j += 1
            distance = np.sqrt(((i[0]-j[0])**2)+((i[1]-j[1])**2)+((i[2]-j[2])**2))
            distance_list.append(distance)
        distance_array.append(distance_list)

    if processed_models == 0:
        average_distance = np.array(distance_array)
        print('average distance #', processed_models, '\n', average_distance)
        average_distance.fill(0)
        print('average distance #', processed_models, '\n', average_distance)

    else:
        distance_array = np.array(distance_array)
        average_distance = np.add(average_distance, distance_array)
        print('average distance #', processed_models, '\n', average_distance)


    #a nice status update that reports every 100 processed models
    processed_models += 1
    if processed_models % 1000 == 0:
        print('\nnumber of processed models: ', processed_models, '\n')

average_distance = average_distance/processed_models

print('\ntotal number of processed models: ', f'{processed_models:,}')

count_i = 0
for i in average_distance:
    count_i += 1
    count_j = 0
    for j in average_distance[count_i-1]:
        count_j += 1
        output_file.write(str(count_i) + '\t', )
        output_file.write(str(count_j) + '\t', )
        output_file.write(str(j) + '\n')

output_file.close()



#prints runtime
print("--- %s seconds ---" % (time.time() - start_time))
