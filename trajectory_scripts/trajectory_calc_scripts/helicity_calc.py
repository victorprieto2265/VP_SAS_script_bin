#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Created on %(date)s

@author: Victor Prieto

"""

import time
from Bio.PDB import PDBParser
from Bio.PDB.DSSP import DSSP
import os

# starts program runtime
start_time = time.time()
print('start time: %s Eastern Time' % time.ctime())

parser = PDBParser(PERMISSIVE=1, QUIET=1)

construct = '3K'

python_dir_path = '/Users/victorprieto/Desktop/Research/python'

try:
    output_path = (python_dir_path +
                   '/trajectory_scripts/trajectory_calc_outputs/' +
                   construct +
                   '_helicity_values/')
    os.mkdir(output_path)
except:
    print('no top level directory created')
    None

#####
# opening files, parsing PDBs

filenames = []
directories = []
number_of_files = 10000

split_traj_path = (python_dir_path +
                   '/split_trajectories/split_full_rap74_fcp1_' +
                   construct +
                   '_restrained')

for i in range(0, 20):
    dir_path = (split_traj_path + '/split_full_N_' + "{:03d}".format(i) +
                '_campari_traj/{:02d}'.format(i) + '_')
    directories.append(dir_path)

for j in range(0, number_of_files):
    file_number = str(j + 1).zfill(6)
    file_name = file_number + '.pdb'
    filenames.append(file_name)

# create a dictionary, which later will be updated with each helicity count
structure_name = 'fcp1'
structure = parser.get_structure(structure_name,
                                 split_traj_path +
                                 '/split_full_N_000_campari_traj/00_000001.pdb'
                                 )
model = structure[0]
helical_dict = {}

aa_dict = {}

chainB = model['B']

for residueB in chainB.get_list():
    B_res_id = residueB.get_id()[1]  # added 807 to align numbering scheme?
    helical_dict[B_res_id] = 0
    aa_dict[B_res_id] = residueB.get_resname()

print('amino acid dictionary:')
print(aa_dict)
processed_models = 0

#####
# creates dssp lists for the open PDB structure
for directory in directories:

    file_paths = [directory + filename for filename in filenames]

    helical_dict = dict.fromkeys(helical_dict, 0)

    for file in file_paths:

        try:
            structure = parser.get_structure(structure_name, file)
        except FileNotFoundError:
            print('file not found!')
            print(file)
            continue

        model = structure[0]

        dssp = DSSP(model, file, dssp='dssp')
        dssp_list = list(dssp)

        # model A is rap74, model B is ctFCP1
        chainB = model['B']

        for residueB in chainB.get_list():
            B_res_id = residueB.get_id()[1]
            try:
                if dssp_list[B_res_id][2] == 'H':
                    helical_dict[B_res_id] += 1
            except IndexError:
                None

        processed_models += 1
        if processed_models % 1000 == 0:
            statement = 'number of processed models: ' + str(processed_models)
            print(statement)
            if processed_models % 10000 == 0:
                print("--- %s minutes ---"
                      % '%.3f'
                      % (time.time()/60 - start_time/60))

    # directory[113:115] are values from 00 to 19
    temperature = str(int(directory[113:115]) * 10 + 230)
    output_file_name = (construct +
                        '_helicity_values_' +
                        temperature +
                        'K.txt')
    save_path = os.path.join(output_path, output_file_name)
    output_file = open(save_path, 'w')

    print(temperature)
    print(helical_dict)

    helicity_list = list(helical_dict.items())
    for aa in range(0, len(helical_dict)):
        output_file.write(str(helicity_list[aa][0]) +
                          '\t' +
                          str(helicity_list[aa][1]) +
                          '\n')
    output_file.close()


# prints runtime
print("--- %s seconds ---" % '%.3f' % (time.time() - start_time))
print("--- %s minutes ---" % '%.3f' % (time.time()/60 - start_time/60))
