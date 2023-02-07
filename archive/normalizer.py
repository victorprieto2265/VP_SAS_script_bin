#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 12:20:15 2018

test script for locating max of a .list file, then creating a new numpy array
normalized to that max value

@author: Victor Prieto
"""

import tkinter
import sys
import numpy as np

root = tkinter.Tk()
root.withdraw()

#select the two .list files from the same experiment
diamagnetic_list = ('/Users/Wasabi/Desktop/Work/pre/181101_ctfcp1_g892c/diamagnetic_hacacon_g891c.list')
paramagnetic_list = ('/Users/Wasabi/Desktop/Work/pre/181101_ctfcp1_g892c/paramagnetic_hacacon_g891c.list')
         
para_file = open(paramagnetic_list, 'r')
dia_file = open(diamagnetic_list, 'r')

fileNumber = 0
processedmodels = 0

dia_peak_intensities = []
para_peak_intensities = []

for line in dia_file:
    
    if 'CO' in line:
        line = line.split()
        dia_peak_intensities.append(float(line[3]))
    
    else:
        None

for line in para_file:
    
    if 'CO' in line:
        line = line.split()
        para_peak_intensities.append(float(line[3]))
    
    else:
        None

print('para_peak_intensities maximum: ', np.max(para_peak_intensities))
print('dia_peak_intensities maximum: ', np.max(dia_peak_intensities))



sys.exit()  
