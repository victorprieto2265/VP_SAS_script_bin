#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Created on Sun May 10 00:32:01 2020

This script plots a heatmap with the output of pre_map.py, which analyzes frames of a trajectory that has been split up into many PDB files and exports PRE values between ALL alpha carbons of chain A and chain B (both intramolecular and intermolecular contacts).

This script has been specifically adapted for producing a PRE map between alpha carbons of FCP1 and RAP74 to process the trajectories run by Scott in April/May 2020.

Note that residues 1-67 correspond to RAP74 452-520, 68-71 corresponds to the GPGW cloning artifact + exogenous tryptophan installed on ctFCP1, and 72-153 correspond to ctFCP1 879-960.

@author: Victor Prieto

"""

#starts program runtime
import time
start_time = time.time()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib as mpl

def shiftedColorMap(cmap, start=0, midpoint=0.5, stop=1.0, name='shiftedcmap'):
    cdict = {
        'red': [],
        'green': [],
        'blue': [],
        'alpha': []
    }

    # regular index to compute the colors
    reg_index = np.linspace(start, stop, 257)

    # shifted index to match the data
    shift_index = np.hstack([
        np.linspace(0.0, midpoint, 128, endpoint=False), 
        np.linspace(midpoint, 1.0, 129, endpoint=True)
    ])

    for ri, si in zip(reg_index, shift_index):
        r, g, b, a = cmap(ri)

        cdict['red'].append((si, r, r))
        cdict['green'].append((si, g, g))
        cdict['blue'].append((si, b, b))
        cdict['alpha'].append((si, a, a))

    newcmap = mpl.colors.LinearSegmentedColormap(name, cdict)
    plt.register_cmap(cmap=newcmap)

    return newcmap

#this defines the colormap used.
orig_cmap = mpl.cm.coolwarm_r #the cmap color scheme was reversed by adding '_r'
cmap = shiftedColorMap(orig_cmap, midpoint=0.75, name='shifted') #this uses the 
cmap = 'shifted' 

#####
#opens file. Make sure filename and extension are correct, and it is in the same folder. 
filename = 'wt_pre_values.txt'
pre_file = open(filename, 'r')

pre_array = []
pre_list = []
count = 0

for line in pre_file:
    line = line.split() #this line makes line[0] through line[2] = residue i, residue j, PRE
#    print('i = ', line[0])
#    print('j = ', line[1])
    if line[1] == '1' and line[0] != '1': #this activates when j restarts to 1 and it's not the first line. It would be simpler to ask if line[1] == total number of residues, but this is written to run regardless of the number of residues. 
        pre_array.append(pre_list) #appends list of PRE values described above to array
        pre_list = []
    pre_list.append(float(line[2])) #creates list of PRE values from residue i to all residues j
    count += 1

pre_array.append(pre_list) #this makes sure the last PRE list is included in the array, since the loop above doesn't catch the last PRE

pre_array = np.array(pre_array)

###########             
#heatmap plotting section starts here

#defining the number of residues, which is necessary for the axis lengths
fcp1_residues = np.arange(879, 960, 1)
rap74_residues = np.arange(452, 520, 1)
fcp1_residue_number = len(fcp1_residues)
rap74_residue_number = len(rap74_residues)

#colormap defined here. The second argument = number of color tiers (256 is fine for a gradient)
colormap = cm.get_cmap(cmap, 64)

#function to generate heatmaps
def heatmap(colormaps):
    data = pre_array
    n = len(colormaps)
    fig, axs = plt.subplots(1, n, figsize=(6,6), constrained_layout=True, squeeze=False)
    for [ax, cmap] in zip(axs.flat, colormaps):

        #the color bar lower and upper bounds are set here in vmin and vmax
        psm = ax.pcolormesh(data, cmap=cmap, rasterized=True, vmin=0, vmax=1)
        
        #colorbar defined here. Label defined here. Change third argument of np.linspace to adjust tick number.
        fig.colorbar(psm, ax=ax, label = 'PRE, $I_{para}/I_{dia}$', ticks=np.linspace(0, 1, 5))
                
heatmap([colormap])

#axis, figure titles
plt.title('PRE contact map')
plt.xlabel('rap74 residues, ctfcp1 residues')
plt.ylabel('rap74 residues, ctfcp1 residues')

plt.tick_params(
    axis='both',       # both x and y axes affected
    which='both',      # both major and minor ticks are affected
    bottom=True,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    left=True,
    labelbottom=True, # labels along the bottom edge are off
    labelleft=True)

image_name = 'wt_heatmap'
mpl.rcParams['svg.fonttype'] = 'none'
plt.draw()
plt.savefig(image_name + '.svg', bbox_inches='tight', format='svg', dpi = 600)

plt.show()

#prints runtime
print("--- %s seconds ---" % (time.time() - start_time))   
