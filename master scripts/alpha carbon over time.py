# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 13:59:46 2017

This script plots the x-coordinate of an alpha carbon as a function of time.
@author: Victor Prieto
"""

''# -*- coding: utf-8 -*-

from tkinter import filedialog
import tkinter   

import sys

import numpy as np

import matplotlib.pyplot as plt

#file =open("N_000_campari_traj.pdb", "r")
#this tells the OS to open a window to find the directory containing the files
root = tkinter.Tk()
root.withdraw()

files = filedialog.askopenfilenames()

model_x = []
model_y = []
model_z = []

timepoint = range (1, 10001)

for file in files:
    
    specificfile = open(file, 'r')
    
    m = 0
    
#identifies the line in the PDB file which corresponds to the alpha carbon for a cysteine mutant
#and appends the xyz coordinates to the array
    for line in specificfile:
    
        if 'ATOM' and 'CA' and 'CYS' in line:
            
            coordinate_x = [float((str(line)[30:38]).strip())]
            model_x.append(coordinate_x)
            
            coordinate_y = [float((str(line)[39:46]).strip())]
            model_y.append(coordinate_y)
            
            coordinate_z = [float((str(line)[46:54]).strip())]
            model_z.append(coordinate_z)
                                    
        else: 
            None
            
print(timepoint)
print(type(timepoint))


print(model_x)
print(type(model_x))

plt.plot(timepoint, model_x)
plt.xlabel('frame')
plt.ylabel('x-coordinate position')
plt.show()

sys.exit()


