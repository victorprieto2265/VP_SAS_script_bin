# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 09:36:57 2020

This script splits a .pdb file containing many structures, giving each structure its own .pdb file. Only alpha carbons are carried over.

@author: Victor Prieto

"""

''# -*- coding: utf-8 -*-

#import numpy as np

import tkinter
root = tkinter.Tk()
root.withdraw()

#Place the file requested into an array.
#file = open('N_008_campari_traj.pdb')
file = open('SAMPLE pdb text.txt')

model = []

#output = input('Name your output file.\n')
#outFile = open(output + '.pdb', "w")

count = 0

for line in file:
    if line.startswith('CRYST'):
        count += 1
        count_string = str(count)
        output_file_name = count_string.zfill(6) + '.pdb'
        print('CRYST ' + count_string)  
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
    else:
        None


#outFile.close()                 
