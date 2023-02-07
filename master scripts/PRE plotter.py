#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
reads two .list files exported from Sparky, diamagnetic and paramagnetic
    NOTE: the .list files must have four entries: assignment, w1 and w2 (chemical shifts), and peak height.
calculates PRE
plots PRE as a function of residue number

Created on Wed Sep 19 14:16:21 2018

@author: Victor Prieto
"""

import sys

import numpy as np

import matplotlib.pyplot as plt

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
PRE_ratio = (para_peak_intensity/dia_peak_intensity, para_residue_number)

#plots figure as a bar chart
plt.figure(figsize=(10,6))
figure = plt.bar(PRE_ratio[1], PRE_ratio[0], color = "royalblue", edgecolor = "white", width = 1)

#formatting changes for the bar chart
plt.title("ctFCP1_M961C_MTSL CON PRE")
plt.tick_params(axis='both', which='major', labelsize=16)
plt.ylabel('$I_{para}/I_{dia}$', fontsize = 20)
plt.xlabel('Residue Index', fontsize = 20)
plt.xlim(np.min(PRE_ratio[1]), np.max(PRE_ratio[1]))

#this section is code copied directly from Erik's PRESimulatedandExperimentalPlotter.py
#for the purposes of plotting a simulated PRE plot overlaid on the experimental data

#correlation time for the electron nuclear interaction
tau = 0.0000000207
#Larmor frequency of the nuclear spin (proton, carbon, etc.) For proton, omega = 500,000,000Hz. For carbon, omega = 125,700,000Hz. 
H1omega = 498.186000
C13omega = 125.7
K = 1.23e-32        
t = 0.009
H1R2 = 0.0001
C13R2 = 0.00009
def R2SP(tau, omega, K, r):
    r = r*10e-8
    b = 4*tau+((3*tau)/(1+omega**2*tau**2))
    return (K * b)/(r**6)

def Iratio(R2, R2S, t):
    return (R2**(-R2S*t))/(R2 + R2S)
    
def distance(K, tau, omega, R2S):
    a = K/R2S
    b = 4*tau+((3*tau)/(1+omega**2*tau**2))
    return (a*b)**(1/6)

aveDistance = np.loadtxt('testing4.txt')

H1R2SP = R2SP(tau, H1omega, K, aveDistance)
H1ratio = Iratio(H1R2, H1R2SP, t)
H1ratio = H1ratio - np.min(H1ratio)
H1ratio = H1ratio/np.max(H1ratio)

C13R2SP = R2SP(tau, C13omega, K, aveDistance)
C13ratio = Iratio(C13R2, C13R2SP, t)
C13ratio = C13ratio - np.min(C13ratio)
C13ratio = C13ratio/np.max(C13ratio)

residue = np.arange(203, 286, 1)

plt.plot(residue, C13ratio, color = 'black', linewidth = '2.5')

#show the bar chart
plt.show()
        
#exits program
sys.exit()