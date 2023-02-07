#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Created on Sun Jun 14 10:19:59 2020

Opens many pdb files in a trajectory, calculates distances for each pdb between two particular residues, and produces a histogram.

This script is currently configured to determine the distances between ctFCP1 residue 927 and rap74 residue 483.

@author: Victor Prieto

"""

#starts program runtime
import time
start_time = time.time()
print('start time: %s Eastern Time' % time.ctime())

import numpy as np

# need this in order to do the folderpath stuff
import os
import os.path

#######
# make a folder for trajectory analysis files

new_path = r'/Users/victorprieto/Desktop/Research/python/trajectory_training_set/calc output files/'
try:
    os.mkdir(new_path)
except:
    None

##########

# identify the number of pdb files in each directory to be analyzed (i.e. frames in trajectory)
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
output_file_name = new_path + 'wt_dist_hist_values.txt'
output_file = open(output_file_name, 'w')

# using the number of files inputted above, prepares a string for each file name and deposits it into files


##########

# section that opens each PDB, analyzes for distance, and saves the value
    
processed_models = 0
dist_array = [] # note: dist_array is actually a list

for file in filenames:
    pdb_file = open(file, 'r')
    fcp1_model = []
    rap74_model = []
    
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
        for j in rap74_model:
            count_j += 1
            # count_i indicates fcp1 residue 927, count_j indicates rap74 residue 483 (predicted as having greatest PRE)
            if count_i == 116 and count_j == 33:
                distance = np.sqrt(((i[0]-j[0])**2)+((i[1]-j[1])**2)+((i[2]-j[2])**2))
                dist_array.append(distance)            
    
        
    #a nice status update that reports every 100 processed models
    processed_models += 1
    if processed_models % 100 == 0:
        print ('\nnumber of processed models: ', processed_models, '\n')    

print('\ntotal number of processed models: ', processed_models)
print('total number of processed models: %d' % processed_models)

count_i = 0
for i in dist_array:
    output_file.write(str(dist_array[count_i]) + '\n')
    count_i += 1
        
output_file.close()

#prints runtime
print("--- %s seconds ---" % (time.time() - start_time))   
