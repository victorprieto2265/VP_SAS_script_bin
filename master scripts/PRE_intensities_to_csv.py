#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 14:29:01 2019

short script for extracting intensity values out of .list files exported from
Sparky, calculating PRE for each, and exporting residue numbers and PRE
values to a .csv file?

@author: Victor Prieto
"""

#starts program runtime
import time
start_time = time.time()

import numpy as np
import matplotlib.pyplot as plt
import sys
from math import e

#identifies the names of the .list files exported from Sparky. Must be in the same folder as the script.
paramagnetic_list = input('PARAMAGNETIC: copy and paste the file name (include .list extension if there is one): ')
diamagnetic_list = input('DIAMAGNETIC: copy and paste the file name (include .list extension if there is one): ')

output_filename = input('What do you want the filename to be? ') + '.csv'
print(output_filename)
                       
#opens the files and places text into a list
para_file = open(paramagnetic_list, 'r')
dia_file = open(diamagnetic_list, 'r')

#creates arrays necessary for later
para_residue_number = []
para_peak_intensity = []

dia_residue_number = []
dia_peak_intensity = []

#defines function to identify residue numbers
def residue_number(x):
    return x[6:9]

#goes through each line looking for 'CD1' or 'CO'
for line in para_file:
    
    #CD1 indicates side chain, which we ignore
    if 'CD1' in line:
        None
    
    #CO indicates backbone amide bond, which we want. First, it deposits the residue number into an array,
    #then, splits up the text in the line by whitespace and deposits the peak height (index 3) into an array.    
    elif 'CO' in line:
        para_residue_number.append(int(residue_number(line)))
        line = line.split()
        para_peak_intensity.append(float(line[3]))
        
    else:
        None

#repeats the above code for the diamagnetic file
for line in dia_file:
    
    if 'CD1' in line:
        None
        
    elif 'CO' in line:
        dia_residue_number.append(int(residue_number(line)))
        line = line.split()
        dia_peak_intensity.append(float(line[3]))
        
    else:
        None        

#makes sure there is an equal number of residues in paramagnetic and diamagnetic lists   
if para_residue_number != dia_residue_number:
    print('WARNING: residue numbers do not match up!')
    sys.exit()
else:
    None
    
    

output = open(output_filename, 'wb')

