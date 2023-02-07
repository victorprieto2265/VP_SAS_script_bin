#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Created on Sun Jun 14 10:36:08 2020

This script takes the output of distance_hist_calc and plots a histogram.

@author: Victor Prieto

"""

#starts program runtime
import time
start_time = time.time()


import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import PercentFormatter

#####
# Opens file, reads values, and sets up histogram plot. Make sure filename and extension are correct, and it is in the same folder. 
filename = 'wt_dist_hist_values.txt'
dist_hist_file = open(filename, 'r')

dist_list = []
count = 0

for line in dist_hist_file:
    dist_list.append(float(line))
    count += 1

#####
# this section checks for anomalies in the data, specifically, if a particular value is repeated five or more times.

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
plt.title('FCP1 wild type - RAP74\n C927 - G483\ndistances (angstroms)')

# creates a normalized list of distances
norm_dist_list = dist_list / np.amax(dist_list)

# sets number of bins
n_bins = 20

plt.hist(dist_list, histtype = 'bar', rwidth = 0.8, bins = n_bins, color = 'gray', weights = np.ones(len(dist_list)) / len(dist_list))
plt.gca().yaxis.set_major_formatter(PercentFormatter(1))

# save figure
plt.savefig('wt_dist_hist.svg', format='svg', transparent=True)
plt.savefig('wt_dist_hist.jpg', format='jpg', transparent=True)

plt.show()



#prints runtime
print("--- %s seconds ---" % (time.time() - start_time))   
