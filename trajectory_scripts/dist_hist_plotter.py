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

filenames = filedialog.askopenfilenames()

# request construct name
construct = input('enter the fcp1 construct name (just the code, e.g. 5KR): ')

#creates directory to store new figures
import os
import os.path

new_path = '/Users/victorprieto/Desktop/Research/python/trajectory_scripts/trajectory_calc_outputs/' + construct + '_histograms/'
try:
    os.mkdir(new_path)
except:
    None

temperature = 230
for filename in filenames:
    print('\ntemperature = ', str(temperature))
    print(filename, '\n')

    dist_hist_file = open(filename, 'r')
    
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
    plt.title('number of distances: ' + str(count) + '\nFCP1' + construct + ' - RAP74\n C927 - G483\n%iK distances (angstroms)' % temperature)
        
    # sets number of bins
    n_bins = 20
    
    plt.hist(dist_list, histtype = 'bar', rwidth = 0.8, bins = n_bins, color = 'gray', weights = np.ones(len(dist_list)) / len(dist_list))
    plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
    plt.xlim(0, 100)
    plt.ylim(0, 0.3)

    # save figure
    savefig_title = construct + '_dist_hist_%dK' % temperature
    plt.savefig(new_path + savefig_title + '.svg', format='svg', transparent=True, bbox_inches='tight')
    plt.savefig(new_path + savefig_title + '.jpg', format='jpg', transparent=True, bbox_inches='tight')
    
    temperature += 10

    plt.clf()

#prints runtime
print("--- %s seconds ---" % '%.3f'%(time.time() - start_time))   
print("--- %s minutes ---" % '%.3f'%(time.time()/60 - start_time/60))   
