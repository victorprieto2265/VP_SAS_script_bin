#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Created on Tue Jun  9 09:34:15 2020

@author: Victor Prieto
@editor: Jarod Olson

"""
# need this in order to do the folderpath stuff
import os
import os.path

# starts program runtime
import time
start_time = time.time()
print('start time: %s Eastern Time' % time.ctime())

construct = '3K'
print('---------- %s PDB SPLITTER ----------' % construct)

# create path for python directory
python_dir_path = '/Users/victorprieto/Desktop/Research/python'

# create list of filenames, WITHOUT .pdb extensions
filename_list = []

for i in range(0, 20):
    filename = 'N_' + "{:03d}".format(i) + '_campari_traj'
    filename_list.append(filename)

model = []
count = 0
processed_model_count = 0

try:
    new_path = (python_dir_path +
                '/split_trajectories/split_full_rap74_fcp1_' +
                construct +
                '_restrained/')
    os.mkdir(new_path)
except:
    print('no top level directory created')
    None

for filename in filename_list:

    # make a new directory for directories 000-019
    try:
        new_path = (python_dir_path +
                    '/split_trajectories/split_full_rap74_fcp1_' +
                    construct +
                    '_restrained/split_full_' +
                    filename)
        os.mkdir(new_path)
    except:
        print('no subdirectories created')
        None

    try:
        file = open(python_dir_path +
                    '/full_trajectories/rap74_fcp1_' +
                    construct +
                    '_restrained/' +
                    filename +
                    '.pdb')
    except:
        print('bad file = %s') % file

    for line in file:

        if line.startswith('CRYST'):
            count += 1
            processed_model_count += 1
            if processed_model_count % 1000 == 0:
                statement = 'number of processed models: ' + str(processed_model_count)
                print (statement)
                if processed_model_count % 10000 == 0:
                    print("--- %s minutes ---" % '%.3f'%(time.time()/60 - start_time/60))
            count_string = str(count)
            output_file_name = filename[3:6] + count_string.zfill(6) + '.pdb'

            save_path = os.path.join(new_path, output_file_name)

            output_file = open(save_path, 'w')
            output_file.write(line)

        if line.startswith('TITLE'):
            output_file.write(line)
        if line.startswith('MODEL'):
            try:
                output_file.write(line)
            except:
                print('bad file = %s') % file
#        if line.startswith('ATOM') and line[13:15] == 'CA':
        if line.startswith('ATOM'):
            output_file.write(line)
        if line.startswith('ENDMDL'):
            output_file.write('ENDMDL\n')
            output_file.close()

    # resets count to zero for next directory
    count = 0

# prints runtime
print("--- %s seconds ---" % '%.3f'%(time.time() - start_time))
print("--- %s minutes ---" % '%.3f'%(time.time()/60 - start_time/60))