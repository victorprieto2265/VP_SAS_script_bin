# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 09:36:57 2020

This script splits a .pdb file containing many structures, giving each structure its own .pdb file. Only alpha carbons are carried over.

@author: Victor Prieto

"""

''# -*- coding: utf-8 -*-


#starts program runtime
import time
start_time = time.time()

import tkinter
root = tkinter.Tk()
root.withdraw()

#create list of filenames
filename_list = []

for i in range(1, 20):
    filename = 'N_' + "{:03d}".format(i) + '_campari_traj.pdb'
    filename_list.append(filename)
    
#Place the file requested into an array.
file = open('N_001_campari_traj.pdb')

model = []

count = 0

for filename in filename_list:
    file = open(filename)
    for line in file:
        if line.startswith('CRYST'):
            count += 1
            if count % 100 == 0:
                print ('\nnumber of processed models: ', str(count), '\n')    
            count_string = str(count)
            output_file_name = filename[3:6] + count_string.zfill(6) + '.pdb'
            output_file = open(output_file_name, 'w')
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
        if count == 10000:
            break
        else:
            None

#prints runtime
print("--- %s seconds ---" % (time.time() - start_time))   