#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Created on %(date)s

This script identifies models that have a distance between residue 921 of ctFCP1 and residue 483 of rap74 of 25 angstroms or shorter, and saves a copy of the PDB file to a new directory.

@author: Victor Prieto

"""

# starts program runtime
import time
start_time = time.time()
print('start time: %s Eastern Time' % time.ctime())

# allows importing of modules in my modules folder. Must have the biopython (Bio) in the folder!
import sys
sys.path.insert(1, '/Users/victorprieto/opt/anaconda3/lib/python3.7/site-packages/')

from Bio.PDB import PDBParser
parser = PDBParser(PERMISSIVE = 1, QUIET = 1)

# define construct name

construct = '3K'

print('---------- %s short distance calculator ----------' % construct)

# need this in order to do the folderpath stuff
import os
import os.path

#######
# make a folder for trajectory analysis files

new_path = '/sas_syn/Data_VP/split_trajectories/' + construct + '_short_distance_files/'
try:
    os.mkdir(new_path)
except:
    None
    
# identify the number of pdb files in each directory to be analyzed (i.e. frames in trajectory)
# =============================================================================
# DIR = '/sas_syn/Data_VP/split_trajectories/rap74_fcp1_%s_restrained/split_CA_N_000_campari_traj/' % construct
# number_of_files = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
# =============================================================================

# DELETE THIS LATER
number_of_files = 99

# =============================================================================
# section that defines PDB filenames to be opened later
# =============================================================================

directories = []
filenames = []

for i in range(0, 20):
#    dir_path = '/sas_syn/Data_VP/split_trajectories/rap74_fcp1_' + construct + '_restrained/split_CA_N_' + "{:03d}".format(i) + '_campari_traj/{:02d}'.format(i) + '_'
    dir_path = '/Users/victorprieto/Desktop/Research/python/trajectory_training_set/rap74_fcp1_3K_restrained/split_CA_N_' + "{:03d}".format(i) + '_campari_traj/{:02d}'.format(i) + '_'
    directories.append(dir_path)
    
for j in range(0,number_of_files):
    file_number = str(j + 1).zfill(6)
    file_name = file_number + '.pdb'
    filenames.append(file_name)

output_file_count = 0
processed_models = 0

structure_name = 'structure_name'

for directory in directories:

    filename_list = [directory + file for file in filenames]

    for file in filename_list:
        
        
        try:
            structure = parser.get_structure(structure_name, file)
        except:
            print('wrong filename = ', file)
            continue
                
        model = structure[0]
        fcp1_chain = model['B']
        rap74_chain = model['A']

#        # keeping this section around in case I ever want to modify it for helicity        
#        try:
#            dssp = DSSP(model, file, dssp='dssp')
#            dssp_list = list(dssp)
#            print(dssp_list[0][0] + dssp_list[0][2])
#        except:
#            None
            
        # residue 33 in rap74 = G483
        # residue 41 in rap74 = N491
        # residue 114 in fcp1 = K921
        
        G483 = rap74_chain[33]
        K921 = fcp1_chain[114]
        
        if G483['CA'] - K921['CA'] <= 19:
            prefix = int(file[105:107])
            distance = G483['CA'] - K921['CA']
            print('distance = ', str(G483['CA'] - K921['CA']))
                                    
            output_file_name = r'/Users/victorprieto/Desktop/Research/python/trajectory_training_set/short distance files/' + file[121:134]
            output_file = open(output_file_name, 'w')

            file = open(file)
            
            for line in file:     
                output_file.write(line)
            output_file.close()
            output_file_count += 1
        
        processed_models += 1
        if processed_models % number_of_files/1000 == 0:
            print('number of processed models: %d' % processed_models)
            if processed_models % number_of_files/1000 == 0:
                print("--- %s minutes ---" % '%.3f'%(time.time()/60 - start_time/60))
                
print('total number of processed models: %d' % processed_models)
print('total number of saved pdb files: %d' % output_file_count)


#prints runtime
print("--- %s seconds ---" % '%.3f'%(time.time() - start_time))   
print("--- %s minutes ---" % '%.3f'%(time.time()/60 - start_time/60))   
