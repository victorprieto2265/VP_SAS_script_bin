#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Created on Mon Sep 23 22:03:33 2019

This script outputs the ideal constant concentration of macromolecule (RAP74) in uM for each well of the competition assay.

Definitions for the following variables are provided below:
    macro = RAP74 concentration per well
    fpep = f-FCP1 concentration per well
    

@author: Victor Prieto

"""

#imports relevant modules

import numpy as np

import matplotlib.pyplot as plt

from scipy import optimize

#indicate the text file containing data
tempArray = np.loadtxt('simulated competition data.txt')

#create separate arrays for the X and Y data points
Xarray = tempArray[:,0]

#macromolecule represents the total concentration of macromolecule in uM assuming it is unchanging over the duration of the experiment
macro = 80.0
#Puc is the concentration of fluorophore-labeled probe, which is unchanged over the course of the experiment
fpep = 0.040
#Kd1 is the measured dissociation constant from direct binding assays between SPOP and probe in uM
Kd1 = 2.41

#This section converts polarization (mP) in tempArray[:,1] to anisotropy (mA). It is not needed if the data provided in the text file is already anisotropy.
#Pol = tempArray[:,1] / 1000
#
#mA = 1000 * (2 * Pol) / (3 - Pol)     

mA = tempArray[:,1]       

I = mA
pep = Xarray
Af = np.min(mA)
Ab = np.max(mA)
Q = 1.3

#normalizes FP values from 0 to 1

#Inorm = (tempArray[:,1] - 180)/(max(tempArray[:,1])-180)
#Inorm = tempArray[:,1]
#pep = Xarray

#fitting function 'kdfit' is defined with four parameters:
    #SPOP = Total concentration of SPOP in uM
    #Kd = dissociation constant based on midpoint of fit (in uM)


def kd2fit(pep, Kd2, G):
    d = Kd1 + Kd2 + fpep + pep - macro
    e = ((pep - macro) * Kd1) + ((fpep - macro) * Kd2) + (Kd1 * Kd2)
    f =  -1 * Kd1 * Kd2 * macro
    
    theta_top = (-2* d**3) + (9 * d * e) - (27 * f)
    theta_bottom = 2 * np.sqrt(((d**2)-3*e)**3)
    th = np.arccos(theta_top/theta_bottom)

    top = (2 * np.sqrt(d**2 - 3 * e) * np.cos(th / 3)) - d
    bottom = (3 * Kd1) + (2 * np.sqrt((d**2 - 3 * e)) * np.cos(th / 3)) - d
             
    FB = (top/bottom)
     
    Aobs = ((Q * FB * Ab) + ((Af *(1 - FB))/ (1 - (FB * (1 - Q)))))
         
    return G * Aobs



#user-inputted guesses for Kd2 and A

guess1 = [2, 1]


#p1 is where the fit is stored
p1, pcov1 = optimize.curve_fit(kd2fit, pep, I, guess1)
print('p1:\n', p1)
print(type(p1))

#allows fit extrapolation beyond data range for completeness
#xval = np.arange(0,10000) 
fit1 = np.array(kd2fit(pep, p1[0], p1[1]))

Kd2round = round(p1[0], 2)

plt.figure(figsize = (4,4))

#plotting
plt.ylabel('anisotropy (mA)')
plt.xlabel('RAP74 concentration (uM)')
#plt.xlim(0.01, 10000)
#plt.ylim(110, 170)

plt.xscale('log')
plt.title('placeholder')
plt.scatter(pep, I, s = 48, facecolors='none', edgecolors='b', marker = 'o' ) 
plt.annotate('Kd2 = ' +str(Kd2round)+ ' uM', xy = (0.1, 55))

plt.plot(pep, fit1 , 'k')
print('pep:\n', pep)
print('fit1:\n', fit1)
#plt.savefig('del248-MATH_rep3.ps',  format = 'ps', dpi = 600)


