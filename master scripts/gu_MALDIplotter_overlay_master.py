#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 21 13:23:27 2017

@author: graceusher
"""

import numpy as np
import matplotlib.pyplot as plt

from scipy.signal import argrelextrema


tempArray = np.loadtxt('chloro_p53_Me_ctrl_0_B3_1.txt')
temp2 = np.loadtxt('chloro_p53_Me_rxn_0_B4_1.txt')

tempArray[:,1] = tempArray[:,1]/(np.amax(tempArray[:,1]))
temp2[:,1] = temp2[:,1]/(np.amax(temp2[:,1]))

maxima = argrelextrema(tempArray[:,1], np.greater, order = 1000)
max2 = argrelextrema(temp2[:,1], np.greater, order = 200)

plt.plot(tempArray[:,0], tempArray[:,1], color = "k", linewidth = 1.0, label = 'apo')
plt.plot(temp2[:,0], temp2[:,1], color = 'r', linewidth = 1.0, label = 'methyl')


for i in maxima[0]:
    #Conditional statement to calculate maxima of points in a specfic range. An 'X' in added at local maxima.
   if ((tempArray[:,0][i] > 10000) and (tempArray[:,0][i] < 10700)):
       plt.annotate(str(tempArray[:,0][i]), xy=(tempArray[:,0][i], tempArray[:,1][i]+0.1), horizontalalignment = 'center', fontsize = 8, rotation=45)
       
       
for i in max2[0]:
    #Conditional statement to calculate maxima of points in a specfic range. An 'X' in added at local maxima.
    if ((tempArray[:,0][i] > 10000 ) and (tempArray[:,0][i] < 10700)):
       plt.annotate(str(temp2[:,0][i]), xy=(temp2[:,0][i], temp2[:,1][i]+0.1), horizontalalignment = 'center', fontsize = 8, rotation=45)


plt.legend(loc='upper right')
plt.xlabel('m/z')
plt.ylabel('Intensity')
plt.title('p53 methylation by SET7')
plt.xlim(10500, 10800)
plt.ylim([-0.05, 1.2])



plt.tight_layout()
plt.savefig('p53_SET7_Me_ol.ps', format='ps', dpi=600)
plt.show()