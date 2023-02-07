"""

This script plots a heatmap with the output of contact_map_distances.py, which analyzes frames of a trajectory that has been split up into many PDB files and exports distances between ALL alpha carbons of chain A and chain B (both intramolecular and intermolecular contacts).

This script has been specifically adapted for producing a contact map between alpha carbons of FCP1 and RAP74 to process the trajectories run by Scott in April/May 2020.

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
import matplotlib as mpl

#####
#opens file. Make sure filename and extension are correct, and it is in the same folder. 
filename = 'wt_distances.txt'
distance_file = open(filename, 'r')

distance_array = []
distance_list = []
count = 0

for line in distance_file:
    line = line.split() #this line makes line[0] through line[2] = residue i, residue j, distance
#    print('i = ', line[0])
#    print('j = ', line[1])
    if line[1] == '1' and line[0] != '1': #this activates when j restarts to 1 and it's not the first line. It would be simpler to ask if line[1] == total number of residues, but this is written to run regardless of the number of residues. 
        distance_array.append(distance_list) #appends list of distances described above to array
        distance_list = []
    distance_list.append(float(line[2])) #creates list of distances from residue i to all residues j
    count += 1

distance_array.append(distance_list) #this makes sure the last distance list is included in the array, since the loop above doesn't catch the last distance

distance_array = np.array(distance_array)


###########             
#heatmap plotting section starts here

#defining the number of residues, which is necessary for the axis lengths
fcp1_residues = np.arange(879, 960, 1)
rap74_residues = np.arange(452, 520, 1)
fcp1_residue_number = len(fcp1_residues)
rap74_residue_number = len(rap74_residues)

#this defines the colormap used.
cmap = 'coolwarm_r' #the cmap color scheme was reversed by adding '_r'

#colormap defined here. The second argument = number of color tiers (256 is usually enough for gradient)
colormap = cm.get_cmap(cmap, 256)

#function to generate heatmaps
def heatmap(colormaps):
    data = distance_array
    n = len(colormaps)
    fig, axs = plt.subplots(1, n, figsize=(6,6), constrained_layout=True, squeeze=False)
    for [ax, cmap] in zip(axs.flat, colormaps):

        #the color bar lower and upper bounds are set here in vmin and vmax
        psm = ax.pcolormesh(data, cmap=cmap, rasterized=True, vmin=0, vmax=40)
        
        #colorbar defined here. Label defined here. Change third argument of np.linspace to adjust tick number.
        fig.colorbar(psm, ax=ax, label = 'average interresidue distance\nangstroms', ticks=np.linspace(0, 40, 5))
                
heatmap([colormap])

#axis, figure titles
plt.title('contact map')
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
