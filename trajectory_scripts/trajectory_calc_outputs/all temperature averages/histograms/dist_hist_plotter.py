#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Created on %(date)s

This script takes the output of distance_hist_calc and plots a histogram.

@author: Victor Prieto

"""

#starts program runtime
import time
start_time = time.time()
statement = 'start time: ' + str(time.ctime())
print(statement)

from tkinter import filedialog
import tkinter

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import PercentFormatter

#####

#tells tkinter to search for the filename and open the filedialog window
root = tkinter.Tk()
root.withdraw()

filename = filedialog.askopenfilename()
dist_hist_file = open(filename, 'r')

construct = input('enter the fcp1 construct name (just the code, e.g. 5KR): ')

dist_list = []
count = 0

for line in dist_hist_file:
    dist_list.append(float(line))
    count += 1

#####
# this section checks for anomalies in the data, specifically, if a particular distance is repeated five or more times.

def checkKey(dict, key): 
      
    if key in dict: 
        return True
    else: 
        return False

big_dist_dict = {}
for i in dist_list:
    if checkKey(big_dist_dict, i) == False:
        big_dist_dict[i] = 0        
        continue
    if checkKey(big_dist_dict, i) == True:
        big_dist_dict[i] += 1

for i in big_dist_dict:
    
    if big_dist_dict.get(i) >= 5:
        print('WARNING: repeated value found.')
        print(i, ' - ', big_dist_dict[i])

dist_list = np.array(dist_list)

#####
# Formatting choices for histogram. 

# plot title
plt.title('FCP1' + construct + ' - RAP74\n C927 - G483\ndistances (angstroms)')

# creates a normalized list of distances
norm_dist_list = dist_list / np.amax(dist_list)

# sets number of bins
n_bins = 20

plt.hist(dist_list, histtype = 'bar', rwidth = 0.8, bins = n_bins, color = 'gray', weights = np.ones(len(dist_list)) / len(dist_list))
plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
plt.xlim(0, 100)

# save figure
savefig_title = construct + '_dist_hist'
plt.savefig(savefig_title + '.svg', format='svg', transparent=True, bbox_inches='tight')
plt.savefig(savefig_title + '.jpg', format='jpg', transparent=True, bbox_inches='tight')

plt.tight_layout()
plt.show()

#prints runtime
print("--- %s seconds ---" % '%.3f'%(time.time() - start_time))   
print("--- %s minutes ---" % '%.3f'%(time.time()/60 - start_time/60))   
