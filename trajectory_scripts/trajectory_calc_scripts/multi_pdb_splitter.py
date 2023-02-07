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

# construct = 'WT_restLowT'
construct = input('enter the name of the construct here: ')
print('---------- %s PDB SPLITTER ----------' % construct)

# create list of filenames, WITHOUT .pdb extensions
filename_list = []

for i in range(0, 20):
    filename = 'N_' + "{:03d}".format(i) + '_campari_traj'
    filename_list.append(filename)

model = []
count = 0
error_count = 0
processed_models = 0

# creates top level directory for new split pdb files
try:
    new_path = ('/sas_syn/Data_VP/split_trajectories/rap74_fcp1_'
                + construct
                + '/') # centfcp1_phospho_charmm_02
    os.mkdir(new_path)
except:
    print('no top level directory created')
    None

for filename in filename_list:

    # make a folder for the filename (for a given temperature)
    try:
        new_path = ('/sas_syn/Data_VP/split_trajectories/rap74_fcp1_'
                    + construct
                    + '/split_CA_'
                    + filename)
        os.mkdir(new_path)
    except:
        print('no subdirectory created')
        None

    # opens large pdb file to be split
    print(f'\nopening {filename}.pdb to be split')
    try:
        file = open('/sas_syn/CAMPARI_TRAJ/rap74_fcp1_'
                    + construct
                    + '/'
                    + filename
                    + '.pdb')
    except:
        print(f'bad file: {filename}.pdb')
        continue

    for line in file:

        if line.startswith('CRYST'):
            count += 1
            processed_models += 1
            if processed_models % 1000 == 0:
                statement = 'number of processed models: %s' % processed_models
                print(statement)
                if processed_models % 10000 == 0:
                    print("--- %s minutes ---"
                          % '%.3f'
                          % (time.time()/60 - start_time/60))
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
            except TypeError:
                print(f'TypeError, bad line: {line}')
            except OSError:
                print('OSError, a file was not found?')
            except:
                error_count += 1
                if error_count == 30:
                    print('error count has reached 30!')
                    break

        if line.startswith('ATOM') and line[13:15] == 'CA':
#        if line.startswith('ATOM'):
            output_file.write(line)
        if line.startswith('ENDMDL'):
            output_file.write('ENDMDL\n')
            output_file.close()

    # resets count to zero for next directory, do not reset processed_models!
    count = 0

# prints runtime
print("--- %s seconds ---" % '%.3f' % (time.time() - start_time))
print("--- %s minutes ---" % '%.3f' % (time.time()/60 - start_time/60))
