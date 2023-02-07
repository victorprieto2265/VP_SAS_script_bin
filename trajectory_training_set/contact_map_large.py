#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

This script analyzes frames of a trajectory that has been split up into many PDB files and produces a contact map between ALL alpha carbons of chain A and chain B (both intramolecular and intermolecular contacts).

This script has been specifically adapted for producing a contact map between alpha carbons of FCP1 and RAP74 to process the trajectories run by Scott in March/April 2020.

Note that residues 1-67 correspond to RAP74 452-520, 68-71 corresponds to the GPGW cloning artifact + exogenous tryptophan installed on ctFCP1, and 72-153 correspond to ctFCP1 879-960.

Created on Thu Apr 30 09:00:31 2020

@author: Victor Prieto

"""

#starts program runtime
import time
start_time = time.time()

#from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

#some arrays and variables necessary for later
files = []

#input the filename that the .ps file of the image will be saved under
#image_name = input('input filename for image (exclude .ps): ')
image_name = 'wt_contact'

#identify the number of pdb files to be analyzed (a.k.a. the number of frames in the trajectory)
number_of_files = 10
number_of_files = number_of_files - 1

#using the number of files inputted above, prepares a string for each file name and deposits it into files

for i in range(0,number_of_files):
    file_number = str(i + 1).zfill(6)
    file_name = file_number + '.pdb'
    files.append(file_name)

distance_array = []
processed_models = 0

for file in files:
    pdb_file = open(file, 'r')
    fcp1_model = []
    rap74_model = []
    distance_array = []
    
        #identifies the lines in the PDB file corresponding to atoms in ctFCP1 and appends the xyz coordinates to the array labeled 'fcp1_model'

    for line in pdb_file:
        if 'ATOM' in line:
            appendage = [float((str(line)[30:38]).strip()), float((str(line)[39:46]).strip()), float((str(line)[46:54]).strip())]
            fcp1_model.append(appendage)
                        
        #same thing as above, but finds the xyz coordinates for the residue of interest in RAP74 and appends them to array labeled 'rap74_model'             
        if 'ATOM' in line:       
            appendage = [float((str(line)[30:38]).strip()), float((str(line)[39:46]).strip()), float((str(line)[46:54]).strip())]    
            rap74_model.append(appendage)

    for i in fcp1_model:
        distance_list = []
        for j in rap74_model:
            distance = np.sqrt(((i[0]-j[0])**2)+((i[1]-j[1])**2)+((i[2]-j[2])**2))
            distance_list.append(distance)
        distance_array.append(distance_list)

    if processed_models == 0:
        average_distance = np.array(distance_array)

    else:
        distance_array = np.array(distance_array)
        average_distance = np.add(average_distance, distance_array)
        
    #a nice status update that reports every 100 processed models
    processed_models += 1
    if processed_models % 10 == 0:
        print ('\nnumber of processed models: ', processed_models, '\n')    

average_distance = average_distance/processed_models

print('\ntotal number of processed models: ', processed_models)

###########             
#starts the plt.subplots part of the script

#defining the number of residues, which is necessary for the axis lengths
fcp1_residues = np.arange(879, 960, 1)
rap74_residues = np.arange(452, 520, 1)
fcp1_residue_number = len(fcp1_residues)
rap74_residue_number = len(rap74_residues)

#this defines the colormap used.
cmap = 'coolwarm_r' #the cmap color scheme was reversed by adding '_r'

#colormap defined here. The second argument = number of color tiers (256 is usually enough for gradient)
colormap = cm.get_cmap(cmap, 256) 

def heatmap(colormaps):
    """
    Helper function to plot data with associated colormap.
    """
    data = distance_array
    n = len(colormaps)
    fig, axs = plt.subplots(1, n, figsize=(8, 8), constrained_layout=True, squeeze=False)
    for [ax, cmap] in zip(axs.flat, colormaps):


        #the color bar lower and upper bounds are set here in vmin and vmax
        psm = ax.pcolormesh(data, cmap=cmap, rasterized=True, vmin=0, vmax=40)
        
        #colorbar defined here. Label defined here. Change third argument of np.linspace to adjust tick number.
        fig.colorbar(psm, ax=ax, label = 'average interresidue distance\nangstroms', ticks=np.linspace(0, 40, 5))
                
heatmap([colormap])

plt.tick_params(
    axis='both',       # both x and y axes affected
    which='both',      # both major and minor ticks are affected
    bottom=True,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    left=False,
    labelbottom=True, # labels along the bottom edge are off
    labelleft=True)


#axis, figure titles
plt.title('contact map')
plt.xlabel('rap74 residues, ctfcp1 residues')
plt.ylabel('rap74 residues, ctfcp1 residues')

#plt.savefig(image_name + '.ps',  format = 'ps', dpi = 600)

plt.show()

#prints runtime
print("--- %s seconds ---" % (time.time() - start_time))   
