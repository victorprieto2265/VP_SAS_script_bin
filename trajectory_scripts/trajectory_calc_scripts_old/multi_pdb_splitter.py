#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

This script takes the 20 pdb files from a CAMPARI trajectory and
produces 20 directories containing pdb files corresponding to each frame
of the trajectory. The 20 directories corresponds to the 20 temperatures
from 230K to 420K.

Created on Tue Jun  9 09:34:15 2020

@author: Victor Prieto
@editor: Jarod Olson

"""

import time
import os
import os.path

# starts program runtime
start_time = time.time()
print('start time: %s Eastern Time' % time.ctime())

# create list of filenames, WITHOUT .pdb extensions
filename_list = []

for i in range(0, 20):
    filename = 'N_' + "{:03d}".format(i) + '_campari_traj'
    filename_list.append(filename)

model = []

count = 0
processed_model_count = 0

for filename in filename_list:

    # make a folder for the filename
    try:
        new_path = (r'/sas_syn/CAMPARI_TRAJ/rap74_fcp1_WT_restrained/'
                    + 'split_CA_' + filename)
        os.mkdir(new_path)
    except:
        None

    file = open(r'/sas_syn/CAMPARI_TRAJ/rap74_fcp1_WT_restrained/'
                + filename + '.pdb')

    for line in file:

        if line.startswith('CRYST'):
            count += 1
            processed_model_count += 1
            if processed_model_count % 100 == 0:
                print('\nnumber of processed models: ', str(count), '\n')
            count_string = str(count)
            output_file_name = filename[3:6] + count_string.zfill(6) + '.pdb'

            save_path = os.path.join(new_path, output_file_name)

            output_file = open(save_path, 'w')
            output_file.write(line)

        if line.startswith('TITLE'):
            output_file.write(line)
        if line.startswith('MODEL'):
            output_file.write(line)
        if line.startswith('ATOM') and line[13:15] == 'CA':
            output_file.write(line)
        if line.startswith('ENDMDL'):
            output_file.write('ENDMDL\n')
            output_file.close()

    # resets count to zero for next directory
    count = 0

# prints runtime
print("--- %s seconds ---" % '%.3f' % (time.time() - start_time))
print("--- %s minutes ---" % '%.3f' % (time.time()/60 - start_time/60))
