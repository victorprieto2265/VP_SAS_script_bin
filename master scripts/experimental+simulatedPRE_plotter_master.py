#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 15:24:05 2018
Updated on Wed Dec 19 12:36:39 2018

An amalgam of Erik's experimental and simulated PRE plotter and my PRE plotter (which was
originally adapted from his experimental PRE plotter).

Make a copy of this script and move it to the folder containing the following files:
    -Sparky list of peak heights from the diamagnetic spectrum (w1, w2, peak height)
    -Sparky list of peak heights from the paramagnetic spectrum (w1, w2, peak height)
    -list of interresidue distances created via the interresidue_distance script

Make sure each of those files has the same number of residues.

This script will prompt you for the following information:
    -residue number where MTSL is attached
    -type of experiment (HSQC, CON, HACACON)

@author: Victor Prieto
"""

#starts program runtime
import time
start_time = time.time()

import numpy as np
import matplotlib.pyplot as plt
import sys
from math import e

#identifies the names of the .list files exported from Sparky. Must be in the same folder as the script.
paramagnetic_list = input('PARAMAGNETIC: copy and paste the file name (include .list extension if there is one): ')
diamagnetic_list = input('DIAMAGNETIC: copy and paste the file name (include .list extension if there is one): ')

#opens the files and places text into a list
para_file = open(paramagnetic_list, 'r')
dia_file = open(diamagnetic_list, 'r')

#creates arrays necessary for later
para_residue_number = []
para_peak_intensity = []

dia_residue_number = []
dia_peak_intensity = []

#request for cysteine residue number
cysteine_residue_number = input('MTSL LABEL POSITION: input the residue number where MTSL is attached to cysteine: ')

#defines function to identify residue numbers
def residue_number(x):
    return x[6:9]

#goes through each line looking for 'CD1' or 'CO'
for line in para_file:
    
    #CD1 indicates side chain, which we ignore
    if 'CD1' in line:
        None
    
    #CO indicates backbone amide bond, which we want. First, it deposits the residue number into an array,
    #then, splits up the text in the line by whitespace and deposits the peak height (index 3) into an array.    
    elif 'CO' in line:
        para_residue_number.append(int(residue_number(line)))
        line = line.split()
        para_peak_intensity.append(float(line[3]))
        
    else:
        None

#repeats the above code for the diamagnetic file
for line in dia_file:
    
    if 'CD1' in line:
        None
        
    elif 'CO' in line:
        dia_residue_number.append(int(residue_number(line)))
        line = line.split()
        dia_peak_intensity.append(float(line[3]))
        
    else:
        None

#makes sure there is an equal number of residues in paramagnetic and diamagnetic lists   
if para_residue_number != dia_residue_number:
    print('WARNING: residue numbers do not match up!')
    sys.exit()
else:
    None

#converts peak intensity arrays into NumPy arrays
para_peak_intensity = np.array(para_peak_intensity)
dia_peak_intensity = np.array(dia_peak_intensity)

#creates a nested array with paramagnetic intensities divided by diamagnetic intensitites, and
#residue number as the second element
#the 0.5 is added to account for the unusual doubled paramagnetic data heights from experiment 181002
PRE_ratio = (para_peak_intensity/dia_peak_intensity, para_residue_number)

count = 0
for i in PRE_ratio[0]:
    print(count, '----------', i)
    count +=1

bruker_slip = input('BRUKER SLIP: are the above values accidentally doubled? (type "Y" if yes): ')

if bruker_slip == 'Y' or bruker_slip == 'y':
    PRE_ratio = (0.5*para_peak_intensity/dia_peak_intensity, para_residue_number)
else:
    None

experiment_type = input('EXPERIMENT TYPE: was this an HSQC, CON, or HACACON? ')

#See supplemental information from 2018 J. Phys. Chem. B

tau = 1.2e-9
H1omega = 500e6
C13omega = 126e6
t = 0.009
H1R2 = 13
C13R2 = 8.1

#K for 1H and 13C are different (again, refer to SI from 2018 J. Phys. Chem. B)
if experiment_type == 'CON' or experiment_type == 'HACACON':
    K = 7.778e-34

if experiment_type == 'HSQC':
    K = 1.23e-32

def R2SP(tau, omega, K, r):
    r = r*1e-8
    b = 4*tau+((3*tau)/(1+(omega**2)*(tau**2)))
    return (K * b)/(r**6)

def Iratio(R2, R2S, t):
    return (R2*e**(-R2S*t))/(R2 + R2S)
    
def distance(K, tau, omega, R2S):
    a = K/R2S
    b = 4*tau+((3*tau)/(1+omega**2*tau**2))
    return (a*b)**(1/6)

C13R2SP = np.array([])
H1R2SP = np.array([])

aveDistance_file = input('DISTANCES: copy and paste the file name (include .txt extension if there is one): ')
aveDistance = np.loadtxt(aveDistance_file)

H1R2SP = R2SP(tau, H1omega, K, aveDistance)
H1ratio = Iratio(H1R2, H1R2SP, t)
H1ratio = H1ratio - np.min(H1ratio)
H1ratio = H1ratio/np.max(H1ratio)

C13R2SP = R2SP(tau, C13omega, K, aveDistance)
C13ratio = Iratio(C13R2, C13R2SP, t)
C13ratio = C13ratio - np.min(C13ratio)
C13ratio = C13ratio/np.max(C13ratio)

first_residue_input = input('FIRST RESIDUE NUMBER: input the assigned number for the residue at the N-terminus (typically 878): ')
first_residue = int(first_residue_input)
last_residue_input = input('LAST RESIDUE NUMBER: input the assigned number for the residue at the C-terminus (typically 961): ')
last_residue = int(last_residue_input) + 1

residue = np.arange(first_residue, last_residue, 1)

#plots figure as a bar chart
plt.figure(figsize=(10,6))
figure = plt.bar(PRE_ratio[1], PRE_ratio[0], color = "royalblue", edgecolor = "white", width = 1)

#formatting changes for the bar chart
plt.tick_params(axis='both', which='major', labelsize=16)
plt.ylabel('$I_{para}/I_{dia}$', fontsize = 20)
plt.xlabel('Residue Index', fontsize = 20)
plt.xlim(np.min(PRE_ratio[1]), np.max(PRE_ratio[1]))
plt.ylim(0,1.2)

#plots the simulated PRE line on top of the bar chart, depending on HSQC, CON, or HACACON
#also changes title based on inputs
title = "ctFCP1_" + cysteine_residue_number + "C_MTSL_" + experiment_type + "_PRE"

if experiment_type == 'HSQC':
    plt.title(title)
    plt.plot(residue, H1ratio, color = 'black', linewidth = 2.0)
    
if experiment_type == 'CON':
    plt.title(title)
    plt.plot(residue, C13ratio, color = 'black', linewidth = 2.0)

if experiment_type == 'HACACON':
    plt.title(title)
    plt.plot(residue, H1ratio, color = 'black', linewidth = 2.0)
    
#automatically saves the figure as a .ps file
title = title + '.ps'
plt.savefig(title, format = 'ps', dpi = 600)

#prints runtime
print("--- %s seconds ---" % (time.time() - start_time))

#show the bar chart
plt.show()        

#exits program
sys.exit()  
