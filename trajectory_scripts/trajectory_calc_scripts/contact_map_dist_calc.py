#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

This script analyzes frames of a trajectory that has been split up into
many PDB files and exports distances between ALL alpha carbons of chain
A and chain B (both intramolecular and intermolecular contacts).

This script has been specifically adapted for producing data for 20
contact maps (corresponding to 20 temperatures) between alpha carbons of
FCP1 and RAP74 to process the trajectories run by Scott in March/April
2020.

Note that residues 1-67 correspond to RAP74 452-520, 68-71 corresponds to the GPGW cloning artifact + exogenous tryptophan installed on ctFCP1, and 72-153 correspond to ctFCP1 879-960.

Created on Thu Apr 30 09:00:31 2020

@author: Victor Prieto

"""

#starts program runtime
import time
start_time = time.time()
statement = 'start time: ' + str(time.ctime()) + ' Eastern Time' # this just prints Eastern time, it's not reflective of the actual time zone
print(statement)

import numpy as np

#######
# define construct name

construct = input('enter the name of the construct here: ')

statement = '---------- ' + construct + ' CONTACT MAP DIST CALC ----------'
print(statement)

#######
# make a folder for trajectory analysis files

import os
import os.path

new_path = '/sas_syn/Data_VP/trajectory_calc_outputs/' + construct + '_distances/'
try:
    os.mkdir(new_path)
except:
    None

##########

# identify the number of pdb files in each directory to be analyzed (i.e. frames in trajectory)
DIR = '/sas_syn/Data_VP/split_trajectories/rap74_fcp1_' + construct + '/split_CA_N_000_campari_traj/'
number_of_files = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])

# =============================================================================
# section that defines PDB filenames to be opened later
# =============================================================================

directories = []
filenames = []
output_files = []

for i in range(0, 20):
    dir_path = '/sas_syn/Data_VP/split_trajectories/rap74_fcp1_' + construct + '/split_CA_N_' + "{:03d}".format(i) + '_campari_traj/{:02d}'.format(i) + '_'
    directories.append(dir_path)

    temperature = str(230 + 10*i)
    output_files.append(construct + '_distances_' + temperature + 'K.txt')

for j in range(0, number_of_files):
    file_number = str(j + 1).zfill(6)
    file_name = file_number + '.pdb'
    filenames.append(file_name)

distance_array = []
processed_models = 0  # for keeping track of overall count of files
temperature_count = 0  # for keeping track of which directory is being processed

# =============================================================================
# section for opening and reading files
# =============================================================================

for directory in directories:
    output_file_name = new_path + output_files[0]  # fix the 0
    temperature_count += 1
    temperature = str(230 + 10*temperature_count)
    output_file = open(output_file_name, 'w')

    filename_list = [directory + file for file in filenames]

    for file in filename_list:
        try:
            pdb_file = open(file, 'r')
        except:
            print('wrong filename = ', file)
            continue

#######

    # note: fcp1_model and rap74_model are misnomers for this script, as the two arrays will have coordinates of both chains

        fcp1_model = []
        rap74_model = []
        distance_array = []

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
            distance_list = []
            for j in rap74_model:
                count_j += 1
                distance = np.sqrt(((i[0]-j[0])**2)+((i[1]-j[1])**2)+((i[2]-j[2])**2))
                distance_list.append(distance)
            distance_array.append(distance_list)

        if processed_models == 0:
            average_distance = np.array(distance_array)

        else:
            distance_array = np.array(distance_array)
            try:
                average_distance = np.add(average_distance, distance_array)
            except:
                print('ValueError on file: ', file)
                continue


        #a nice status update that reports each time the directory changes
        processed_models += 1
        if processed_models % number_of_files/10 == 0:
            statement = 'number of processed models: ' + str(processed_models)
            print(statement)
            print("--- %s minutes ---" % '%.3f'%(time.time()/60 - start_time/60))

    average_distance = average_distance/(number_of_files)

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
    print('number of processed models, next temperature: '
          + str(temperature_count))

    # empties the average distance array for the next temperature iteration
    average_distance.fill(0)

#prints runtime
print("--- %s seconds ---" % '%.3f'%(time.time() - start_time))
print("--- %s minutes ---" % '%.3f'%(time.time()/60 - start_time/60))