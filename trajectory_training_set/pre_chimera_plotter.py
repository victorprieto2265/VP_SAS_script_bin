#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Created on Sun May 24 22:17:45 2020

This script analyzes the output of pre_calc, finds the expected pre on RAP74 if MTSL is attached to residue 927, and exports a chimera-readable file for defining an attribute.

@author: Victor Prieto

"""

#starts program runtime
import time
start_time = time.time()

#opens file. Make sure filename and extension are correct, and it is in the same folder. 
filename = 'wt_pre_values.txt'
pre_file = open(filename, 'r')

pre_list = []
count = 0

for line in pre_file:
    line = line.split() #this line makes line[0] through line[2] = residue i, residue j, PRE
        
    #when line[0] <= 67 and line[1] <= 67, values correspond to intramolecular RAP74 PRE.
    #when line[0] >= 68 and line[1] <= 67, values correspond to intermolecular RAP74 and ctFCP1 PRE.
    #when line[0] <= 68 and line[1] >= 67, values correspond to intermolecular RAP74 and ctFCP1 PRE (reversed axes).
    #when line[0] >= 68 and line[1] >= 68, values correspond to intramolecular ctFCP1 PRE.
    
    #line[0] == 68 corresponds to residue 879 of ctFCP1, and line[0] == 116 corresponds to residue 927 of ctFCP1.
    
    if line[0] == '116' and int(line[1]) <= 67:
        pre_list.append(line[2])
#    pre_list.append(float(line[2])) #creates list of PRE values from residue i to all residues j
    
#opens new file and begins writing
output_filename = 'wt_pre_calc.txt'
output = open(output_filename, 'w')

#first line of chimera attribute file
output.write('attribute: pre_RAP74_' + 'wt_pre_calc' + '\nmatch mode: 1-to-1\nrecipient: residues\n')

rap74_residues = range(454, 521, 1)

print(len(rap74_residues))
print(len(pre_list))

count = 0

for i in rap74_residues:
    print(count, '------', i)
    output.write('\t:')
    output.write(str(i) + '.RAP74')
    output.write('\t')
    output.write(str(pre_list[count]) + '\n')
    count += 1

output.close()

#prints runtime
print("--- %s seconds ---" % (time.time() - start_time))       