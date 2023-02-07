#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Created on Tue Jun  8 21:34:05 2021

Calculates pairwise distances between a given residue in Rap74 and
every residue in ctFcp1. Outputs data to .txt file for analysis
in downstream script.

Currently configured to compare residues Lys471.RAP74 CA and
Asp457.RAP74 CA in Rap74 to the ctFcp1 residues.

Note that residues 1-67 correspond to RAP74 452-520, 68-71 corresponds to
the GPGW cloning artifact + exogenous tryptophan installed on ctFCP1, and
72-153 correspond to ctFCP1 879-960.

^I think the above is right but not certain.

@author: Victor Prieto

"""

import time
import numpy as np
import os
import os.path
import csv

# starts program runtime
start_time = time.time()
print('start time: %s Eastern Time' % time.ctime())

construct = '3K'

# =============================================================================
# change this section depending on training set vs. synology
# =============================================================================

# make a folder for trajectory analysis files

new_path = (r'/Users/victorprieto/Desktop/research/python/'
            + r'trajectory_training_set/calc output files/')
try:
    os.mkdir(new_path)
except FileExistsError:
    None

# identify the number of pdb files in each directory to be analyzed
# (i.e. frames in trajectory)

DIR = ('/Users/victorprieto/Desktop/research/python/trajectory_training_set'
       + '/rap74_fcp1_3K_restrained/split_CA_N_000_campari_traj')
number_of_files = len([name for name in os.listdir(DIR) if
                       os.path.isfile(os.path.join(DIR, name))])
number_of_files = 15

# defining split directory paths

directories = []
filenames = []

for i in range(0, 20):
    dir_path = ('/Users/victorprieto/Desktop/research/python/'
                + 'trajectory_training_set/rap74_fcp1_'
                + construct + '_restrained/split_CA_N_'
                + "{:03d}".format(i)
                + '_campari_traj/{:02d}'.format(i) + '_')
    directories.append(dir_path)

# section that defines PDB filenames to be opened later

    for j in range(0, number_of_files):
        file_number = str(j + 1).zfill(6)
        file_name = (dir_path + file_number + '.pdb')
        filenames.append(file_name)

# =============================================================================
# calculation section
# =============================================================================

distance_array = []
processed_models = 0


def xyz_coordinate(line):
    location = (float((str(line)[30:38]).strip()),
                float((str(line)[38:46]).strip()),
                float((str(line)[46:54]).strip()))
    return location


def euclid_distance(point_1, point_2):
    distance = np.sqrt(((point_1[0]-point_2[0])**2)
                       + ((point_1[1]-point_2[1])**2)
                       + ((point_1[2]-point_2[2])**2))
    return distance


for file in filenames:
    pdb_file = open(file, 'r')

    fcp1_model = []
    distance1_array = []
    distance2_array = []

    # identifies the lines in the PDB file corresponding to atoms in
    # ctFCP1 and appends the xyz coordinates to the array labeled 'fcp1_model'

    for line in pdb_file:
        if 'ATOM' in line:
            fcp1_model.append(xyz_coordinate(line))

        # same thing as above, but finds the xyz coordinates for the residue
        # of interest in RAP74 and appends them to array labeled 'Lys471'
        if 'LYS A  21' in line:
            Lys471 = xyz_coordinate(line)

        if 'ASP A   7' in line:
            Asp7 = xyz_coordinate(line)

    fcp1_model = fcp1_model[67:154]

    distance1_list = []
    distance2_list = []

    # calculates the distance between each xyz coordinate in fcp1_model
    # and Lys471 (i1 and j1, i1 and j2... i1 and jn, i2
    # and j1, i2 and j2... in and jn). Repeats for Asp457.

    for i in fcp1_model:
        distance1_list.append(euclid_distance(i, Lys471))
        distance2_list.append(euclid_distance(i, Asp7))
    distance1_array.append(distance1_list)
    distance2_array.append(distance2_list)

    if processed_models == 0:
        average_distance1 = np.array(distance1_array)
        average_distance1.fill(0)
        average_distance2 = np.array(distance2_array)
        average_distance2.fill(0)

    else:
        distance1_array = np.array(distance1_array)
        average_distance1 = np.add(average_distance1, distance1_array)
        distance2_array = np.array(distance2_array)
        average_distance2 = np.add(average_distance2, distance2_array)

    # a nice status update that reports every 100 processed models
    processed_models += 1
    if processed_models % 50 == 0:
        print('\nnumber of processed models: ', processed_models, '\n')


average_distance1 = average_distance1/processed_models
average_distance2 = average_distance2/processed_models

# for some reason it is an array within an array, so we're remaking it here

average_distance1 = average_distance1[0]
average_distance2 = average_distance2[0]

print('\ntotal number of processed models: ', f'{processed_models:,}')

# =============================================================================
# export data to .txt files for later plotting
# =============================================================================


def csv_string(rap74_residue, fcp1_residue, distance, temperature):
    string = (rap74_residue, fcp1_residue, distance, temperature)
    return string


list_of_distances = []

for temp in range(0, 20):
    temperature = str(230 + 10*temp)

    fcp1_count = 875
    res = 'Lys471'

    for i in average_distance1:
        list_of_distances.append(csv_string(res, fcp1_count, i, temperature))
        fcp1_count += 1

    fcp1_count = 875
    res = 'Asp7'

    for i in average_distance2:
        list_of_distances.append(csv_string(res, fcp1_count, i, temperature))
        fcp1_count += 1

output_filename = new_path + 'opposite_face_comparison_' + construct + '.csv'
with open(output_filename, 'w') as csv_file:
    # creating a csv writer object
    csvwriter = csv.writer(csv_file)

    for i in list_of_distances:
        csvwriter.writerows([i])

# prints runtime
print("--- %s seconds ---" % '%.3f' % (time.time() - start_time))
print("--- %s minutes ---" % '%.3f' % (time.time()/60 - start_time/60))
