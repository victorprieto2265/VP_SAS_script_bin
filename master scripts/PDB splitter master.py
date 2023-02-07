# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 09:36:57 2020

This script splits a .pdb file containing many structures, giving each structure its own .pdb file. Solvent atoms (e.g. sulfate and chloride ions) are excluded. Another script exists that only carries over alpha carbons. 

@author: Victor Prieto

"""

''# -*- coding: utf-8 -*-

#import numpy as np

import tkinter   
root = tkinter.Tk()
root.withdraw()

#Place the file requested into an array.
file = open('N_008_campari_traj.pdb')
#file = open('SAMPLE pdb text.txt')

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
    if line.startswith('ATOM'):
        output_file.write(line)
    if line.startswith('ENDMDL'):
        output_file.write('ENDMDL\n')
        output_file.close()
    else:
        None
        
#for file in files: 
#    outFile.write("MODEL" + str(m)+"\n")
#    specificfile =open(file, "r")
#    for line in specificfile:
#      line = line.replace('\n','')
#      line = line.strip()
#      if ("END" in line) or not(line) or len(line)==0 or not(line.rstrip()):
#          continue
#      else:
#          outFile.write(line + "\n")
#    if m % 100 == 0:
#        print ('Models completed: ' + str(m))
#    else:
#        None
#    outFile.write('ENDMDL\n')
#    specificfile.close()      
#    m = m + 1


#outFile.close()                 
