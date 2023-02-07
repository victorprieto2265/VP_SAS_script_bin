#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 12:38:46 2018

For calculating chemical shift change per residue in 1M salt and 0.05M salt. 

@author: Victor Prieto
"""

#starts program runtime
import time
start_time = time.time()

import sys
import numpy as np
import matplotlib.pyplot as plt

#throughout this script, LS and HS stand for "low salt" and "high salt," respectively.

#identifies the names of the .list files exported from Sparky. 
#must be in the same folder as the script.
LS_list = '50_mM_NaCl_a927c.list'
HS_list = '1000_mM_NaCl_a927c.list'

#opens the files and places text into a list
LS_file = open(LS_list, 'r')
HS_file = open(HS_list, 'r')

#creates arrays necessary for later
LS_residue_number = []
LS_CO_shift = []
LS_HN_shift = []

HS_residue_number = []
HS_CO_shift = []
HS_HN_shift = []

#Defines function to slice out residue numbers.
def residue_number(x):
    return x[6:9]

#Now, we go through LS_file line by line looking for the information we want.
for line in LS_file:
    
    #CD1 indicates side chain, which we ignore.
    if 'CD1' in line:
        None
    
    #CO will be in lines we want - this will incorporate residue number, CO shift and HN
    #shift into the appropriate arrays. 
    elif 'CO' in line:
        LS_residue_number.append(int(residue_number(line)))
        line = line.split()
        LS_CO_shift.append(float(line[2]))
        LS_HN_shift.append(float(line[1]))
        
    else:
        None
        
#repeats the above code for the high salt list.
for line in HS_file:

    if 'CD1' in line:
        None
    
    elif 'CO' in line:
        HS_residue_number.append(int(residue_number(line)))
        line = line.split()
        HS_CO_shift.append(float(line[2]))
        HS_HN_shift.append(float(line[1]))
        
    else:
        None
        
#If the two residue number lists do not line up, this section will halt the script.
if LS_residue_number != HS_residue_number:
    print('WARNING: residue numbers do not match up!')
    sys.exit()

else:
    None

#converts  arrays into NumPy arrays
LS_CO_shift = np.array(LS_CO_shift)
LS_HN_shift = np.array(LS_HN_shift)
HS_CO_shift = np.array(HS_CO_shift)
LS_HN_shift = np.array(LS_HN_shift)

#Creates three nested arrays: one with the difference in CO shift, one with the difference in
#HN shift, and one with the Euclidean distance. All three have the residue number as second element.
CO_deltadelta = (LS_CO_shift - HS_CO_shift, LS_residue_number)
HN_deltadelta = (LS_HN_shift - HS_HN_shift, LS_residue_number)
Euclidean_distance = ((((LS_CO_shift - HS_CO_shift)**2+(LS_HN_shift - HS_HN_shift)**2)**0.5), LS_residue_number)

print('CO_deltadelta ----------', CO_deltadelta)
print('HN_deltadelta ----------', HN_deltadelta)
print('Euclidean_distance -----', Euclidean_distance)

#plots figure as a bar chart
plt.figure(figsize=(10,6))
figure = plt.bar(Euclidean_distance[1], Euclidean_distance[0], color = "royalblue", edgecolor = "white", width = 1)

#formatting changes for the bar chart
plt.tick_params(axis='both', which='major', labelsize=16)
plt.ylabel('chemical shift change', fontsize = 20)
plt.xlabel('residue index', fontsize = 20)
plt.xlim(np.min(Euclidean_distance[1]), np.max(Euclidean_distance[1]))
plt.ylim(0,0.6)


#show the bar chart
plt.show()        





#prints runtime
print("--- %s seconds ---" % (time.time() - start_time))   

#exits program
sys.exit()  