#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Created on Sun Jun 14 10:19:59 2020

Opens many pdb files in a trajectory, calculates distances for each pdb between two particular residues, and produces a histogram.

This script is currently configured to determine the distances between ctFCP1 residue 927 and rap74 residue 483.

@author: Victor Prieto

"""

import time
import numpy as np
import os
import os.path

# starts program runtime
start_time = time.time()
print('start time: %s Eastern Time' % time.ctime())

# define construct name

# construct = input('enter the name of the construct here: ')
construct = 'WT_02'

# fcp1 residue 920 corresponds to the 113 residue in the .pdb file
# fcp1 residue 927 corresponds to the 120 residue in the .pdb file
# fcp1 residue 935 corresponds to the 128 residue in the .pdb file
# fcp1 residue 955 corresponds to the 148 residue in the .pdb file
# rap74 residue 461 corresponds to the 11 residue in the .pdb file
fcp1_residue = 128
rap74_residue = 148


print('---------- %s: %s-%s ' % (construct, fcp1_residue, rap74_residue),
      'HISTOGRAM (DISTANCES) CALCULATOR ----------')

# need this in order to do the folderpath stuff

#######
# make a folder for trajectory analysis files

new_path = '/sas_syn/Data_VP/trajectory_calc_outputs/' + construct + '%s-%s_distances/' % (fcp1_residue, rap74_residue)
try:
    os.mkdir(new_path)
except:
    None

##########

# identify the number of pdb files in each directory to be analyzed (i.e. frames in trajectory)
DIR = '/sas_syn/Data_VP/split_trajectories/rap74_fcp1_%s/split_CA_N_000_campari_traj/' % construct
number_of_files = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])

# =============================================================================
# section that defines PDB filenames to be opened later
# =============================================================================

directories = []
filenames = []
output_files = []

#for i in range(0, 20):
for i in range(7, 10):
    dir_path = '/sas_syn/Data_VP/split_trajectories/rap74_fcp1_' + construct + '/split_CA_N_' + "{:03d}".format(i) + '_campari_traj/{:02d}'.format(i) + '_'
    directories.append(dir_path)

    temperature = str(230 + 10*i)
    output_files.append(construct + '_distances_' + temperature + 'K.txt')

for j in range(0,number_of_files):
    file_number = str(j + 1).zfill(6)
    file_name = file_number + '.pdb'
    filenames.append(file_name)

distance_array = []
processed_models = 0
output_file_count = 0

# =============================================================================
# section for opening and reading files
# =============================================================================

processed_models = 0

for directory in directories:
    output_file_name = new_path + output_files[output_file_count]
    output_file_count += 1
    output_file = open(output_file_name, 'w')

    dist_array = [] # creates a new dist_array for each directory/temperature (it's actually a list, despite the name)

    filename_list = [directory + file for file in filenames]

    for file in filename_list:
        try:
            pdb_file = open(file, 'r')
        except:
            print('wrong filename = ', file)
            continue

        fcp1_model = []
        rap74_model = []

            # identifies the lines in the PDB file corresponding to atoms in ctFCP1 and appends the xyz coordinates to the array labeled 'fcp1_model'

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
                if count_i == fcp1_residue and count_j == rap74_residue:
                    distance = np.sqrt(((i[0]-j[0])**2)+((i[1]-j[1])**2)+((i[2]-j[2])**2))
                    dist_array.append(distance)

        #a nice status update that reports every 1000 processed models
        processed_models += 1
        if processed_models % number_of_files/10 == 0:
            print('number of processed models: %d' % processed_models)

    count_i = 0
    for i in dist_array:
        output_file.write(str(dist_array[count_i]) + '\n')
        count_i += 1

    output_file.close()
    print("--- %s minutes ---" % '%.3f'%(time.time()/60 - start_time/60))
    print('--- next temperature directory ---')

print('total number of processed models: %d' % processed_models)

#prints runtime
print("--- %s seconds ---" % '%.3f'%(time.time() - start_time))
print("--- %s minutes ---" % '%.3f'%(time.time()/60 - start_time/60))