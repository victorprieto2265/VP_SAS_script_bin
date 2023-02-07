#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

This script uses Biopython and DSSP to calculate the helical
    content per residue of a set of PDB files. The PDB files must have all
    atoms, and not just alpha carbons.

Make sure to edit the "opening files, parsing PDBs" section properly to target
    the local trajectory files.

Biopython must be enabled within Anaconda before running this script.
    Make sure to cite Biopython properly, see the online documentation.

IMPORTANT: enter "conda install -c salilab dssp" in the console window
    before running script to download DSSP. This was necessary for me before
    the script worked. Make sure to cite DSSP properly, see the online
    documentation.

While running in terminal window, execute with "python3 [script name]".
    Additional steps need to be taken in order to recognize Biopython module
    and access DSSP, have not figured this out yet.

Created on Tue Jun  9 19:43:18 2020

@author: Victor Prieto

"""

# starts program runtime
import time
import sys
import subprocess
start_time = time.time()

# add biopython module to path
sys.path.insert(
        1,
        '/Users/victorprieto/Desktop/Research/python/modules')

from Bio.PDB import PDBParser
from Bio.PDB.DSSP import DSSP

parser = PDBParser(PERMISSIVE=1, QUIET=1)

#####
# add anaconda bin to path
cmd = 'PATH=/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin:/Users/victorprieto/opt/anaconda3/condabin'
try:
    subprocess.call(cmd, shell=True)
    print('cmd executed')
except:
    print('did not work')

#####
# opening files, parsing PDBs

filepaths = []
number_of_files = 10

new_path = r'/Users/victorprieto/Desktop/Research/python/trajectory_training_set/calc output files/'

for i in range(0,number_of_files):
    file_number = str(i + 1).zfill(6)
    filepath = '/Users/victorprieto/Desktop/Research/python/trajectory_training_set/all_atom_files/08_' + file_number + '.pdb'
    filepaths.append(filepath)

# create a dictionary, which later will be updated with each helicity count
structure_name = 'fcp1'
structure = parser.get_structure(structure_name, '/Users/victorprieto/Desktop/Research/python//trajectory_training_set/all_atom_files/08_000001.pdb')
model = structure[0]
helical_dict = {}

aa_dict = {}

chainB = model['B']

for residueB in chainB.get_list():
    B_res_id = residueB.get_id()[1] # added 807 to align with ctfcp1 numbering scheme 
    helical_dict[B_res_id] = 0
    aa_dict[B_res_id] = residueB.get_resname()
    
print(aa_dict)

#####
# creates dssp lists for the open PDB structure
for filepath in filepaths:
    structure = parser.get_structure(structure_name, filepath)

    model = structure[0]

    dssp = DSSP(model, filepath, dssp='mkdssp')
    dssp_list = list(dssp)
        
    #model A is rap74, model B is ctFCP1
    chainB = model['B']
    
    for residueB in chainB.get_list():
        B_res_id = residueB.get_id()[1] # added 807 to align with ctfcp1 numbering scheme
        try:   
            if dssp_list[B_res_id][2] == 'H':            
                helical_dict[B_res_id] += 1
        except IndexError:
            None
        
print(helical_dict)

#####
# testing section, includes distance calculation and an attempt at phi/psi angle calculation using DSSP

#for residueA in chainA.get_list():
#
#    A_res_id = residueA.get_id()[1]
#    print('\ndssp_list for A ', A_res_id, ':', dssp_list[A_res_id-1])
#    
#    for residueB in chainB.get_list():
#
#        B_res_id = residueB.get_id()[1]
#        print('dssp_list for B ', B_res_id, ':', dssp_list[B_res_id-1])
#
#        if B_res_id % 17 == 0: # operates betwee every residue of rap74 and every 17 residues of fcp1, picked 17 so it would hit the last residue
#            print('\nresidues: ', A_res_id, '-', B_res_id) # prints 
#            
#            print('distance = ', residueA['CA'] - residueB['CA']) 
      
#            print('psi = ', residueB.internal_coord.get_angle("psi"), ', phi = ', residueB.internal_coord.get_angle('phi'))
            
#            print('i-1 to i peptide bond = ', residueB.internal_coord.get_length("-1C:0N")

#prints runtime
print("--- %s seconds ---" % (time.time() - start_time))   