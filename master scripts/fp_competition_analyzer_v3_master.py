#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  7 15:50:17 2018

@author: graceusher
"""

#imports relevant modules

import numpy as np

import matplotlib.pyplot as plt

from scipy import optimize

#indicate the text file containing data
tempArray = np.loadtxt('run1.txt')

#create separate arrays for the X and Y data points
Xarray = tempArray[:,0]

#SPOP represents the total concentration of macromolecule in uM assuming it is unchanging over the duration of the experiment
SPOP = 6.0
#Puc is the concentration of fluorophore-labeled probe, which is unchanged over the course of the experiment
Puc = 0.040
#Kd1 is the measured dissociation constant from direct binding assays between SPOP and probe in uM
Kd1 = 2.55

#convert polarization (mP) in tempArray[:,1] to mA
Pol = tempArray[:,1] / 1000

mA = 1000 * (2 * Pol) / (3 - Pol)               

I = mA
pep = Xarray
Af = np.min(tempArray[:,1])
Ab = np.max(tempArray[:,1])
Q = 1.15

#normalizes FP values from 0 to 1

#Inorm = (tempArray[:,1] - 180)/(max(tempArray[:,1])-180)
#Inorm = tempArray[:,1]
#pep = Xarray

#fitting function 'kdfit' is defined with four parameters:
    #SPOP = Total concentration of SPOP in uM
    #Kd = dissociation constant based on midpoint of fit (in uM)


def kd2fit(pep, Kd2, G):
    d = Kd1 + Kd2 + Puc + pep - SPOP
    e = ((pep - SPOP) * Kd1) + ((Puc - SPOP) * Kd2) + (Kd1 * Kd2)
    f =  -1 * Kd1 * Kd2 * SPOP
    
    theta_top = (-2* d**3) + (9 * d * e) - (27 * f)
    theta_bottom = 2 * np.sqrt(((d**2)-3*e)**3)
    th = np.arccos(theta_top/theta_bottom)

    top = (2 * np.sqrt(d**2 - 3 * e) * np.cos(th / 3)) - d
    bottom = (3 * Kd1) + (2 * np.sqrt((d**2 - 3 * e)) * np.cos(th / 3)) - d
             
    FB = (top/bottom)
     
    Aobs = ((Q * FB * Ab) + ((Af *(1 - FB))/ (1 - (FB * (1 - Q)))))
         
    return G * Aobs



#user-inputted guesses for Kd2 and A

guess1 = [8, 1]


#p1 is where the fit is stored
p1, pcov1 = optimize.curve_fit(kd2fit, pep, I, guess1)

#allows fit extrapolation beyond data range for completeness
#xval = np.arange(0,10000) 
fit1 = np.array(kd2fit(pep, p1[0], p1[1]))


Kd2round = round(p1[0], 2)

plt.figure(figsize = (4,4))

#plotting
plt.ylabel('anisotropy (mA)')
plt.xlabel('peptide concentration (uM)')
plt.xlim(0.01, 10000)
plt.ylim(90, 160)

plt.xscale('log')
plt.title('fcp1')
plt.scatter(pep, I, s = 48, facecolors='none', edgecolors='b', marker = 'X' ) 
plt.annotate('Kd2 = ' +str(Kd2round)+ ' uM', xy = (10, 100))

#plt.plot(pep, fit1 , 'k')
plt.savefig('rep1.ps',  format = 'ps', dpi = 600)


