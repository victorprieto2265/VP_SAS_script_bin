#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 15:30:17 2019

This script reads two .list files from a paramagnetic and diamagnetic spectrum,
and exports a .txt file than can be used for defining an attribute in Chimera.

The .list files should have residue name in the first column and intensity
in the fourth column.

This script has been optimized for .list files exported from an HSQC spectrum 
of RAP74. Adapting this script for other proteins will require a code change.

@author: Victor Prieto
"""

#starts program runtime
import time
start_time = time.time()

import sys
import numpy as np

#identifies the names of the .list files exported from Sparky. Must be in the same folder as the script.
paramagnetic_list = input('PARAMAGNETIC: copy and paste the file name (do not include .list extension if there is one): \n') + '.list'
diamagnetic_list = input('DIAMAGNETIC: copy and paste the file name (do not include .list extension if there is one): \n') + '.list'

atrribute_name = input('ATTRIBUTE NAME: what should the attribute be named in Chimera? \n')               
filename = input('FILENAME: type the desired name of file (do not include extension): \n') + '.txt'

                         
#opens the files and places text into a list
para_file = open(paramagnetic_list, 'r')
dia_file = open(diamagnetic_list, 'r')

#creates arrays necessary for later
para_residue_number = []
para_peak_intensity = []

dia_residue_number = []
dia_peak_intensity = []

#defines function to identify residue numbers (note: may change depending on experiment and .list parameters)
def residue_number(x):
    return x[11:14]

#goes through each line looking for 'CD1' or 'CO'
for line in para_file:
        
    #CD1 indicates side chain, which we ignore
    if 'CD1' in line:
        None
    
    #CO indicates backbone amide bond, which we want. First, it adds the 
    #residue number to the residue array, then, splits up the text in the line  
    #by whitespace, and finally deposits the peak height (index 3) into an array.    
    elif 'N-H' in line:
        para_residue_number.append(int(residue_number(line)))
        line = line.split()
        para_peak_intensity.append(float(line[3]))
        
    else:
        None

#repeats the above code for the diamagnetic file
for line in dia_file:
        
    if 'CD1' in line:
        None
        
    elif 'N-H' in line:
        dia_residue_number.append(int(residue_number(line)))
        line = line.split()
        dia_peak_intensity.append(float(line[3]))
        
    else:
        None

#makes sure there is an equal number of residues in paramagnetic and 
#diamagnetic lists before continuing
if para_residue_number != dia_residue_number:
    print('WARNING: residue numbers do not match up!')
    sys.exit()
else:
    None

#converts peak intensity arrays into NumPy arrays
para_peak_intensity = np.array(para_peak_intensity)
dia_peak_intensity = np.array(dia_peak_intensity)

#creates a nested array with paramagnetic intensities divided by diamagnetic intensitites
PRE_ratio = (para_peak_intensity/dia_peak_intensity)

count = 434
for i in PRE_ratio:
    print(count, '----------', i)
    count +=1

bruker_slip = input('BRUKER SLIP: do the above values appear to be \naccidentally doubled? (type "Y" if yes): ')

if bruker_slip == 'Y' or bruker_slip == 'y':
    PRE_ratio = (0.5*para_peak_intensity/dia_peak_intensity)
else:
    None

output = open(filename, 'w')

output.write('attribute: pre_RAP74_' + attribute_name + '\nmatch mode: 1-to-1\nrecipient: residues\n')


count = 0

for i in para_residue_number:
    output.write('\t:')
    output.write(str(i))
    output.write('\t')
    output.write(str(PRE_ratio[count]) + '\n')
    count += 1

output.close()

#prints runtime
print("--- %s seconds ---" % (time.time() - start_time))       