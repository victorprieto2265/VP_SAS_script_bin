#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Created on May 6 2021

@author: Victor Prieto

"""

import time
# place additional modules here

# starts program runtime
start_time = time.time()
print('start time: %s Eastern Time' % time.ctime())

import numpy as np
from math import e
from math import pi
import matplotlib.pyplot as plt

######
#PRE calculation section, references Battiste and Wagner, Biochemistry 2000 and Sjott and Clubb, Bio Protoc 2016

#outputs the intensity ratio given nucleus and distance r
def pre_calculator(nucleus, r):

    #correlation time for the electron nuclear interaction
    tau = 0.0000000207 # 20.7 ns
#    tau = 1.2e-9 # Erik's value

    t = 0.0125   #the total evolution time of the transverse proton magnetization during the NMR experiment, per Sjott and Clubb, or total INEPT evolution time of the HSQC (∼9 ms), per Battiste and Wagner.
#    t = 9e-3 # 9 ms, not that different from 12.5 ms and experiment dependent

    #Larmor frequency of the nuclear spin (proton, carbon, etc.) For proton, omega = 500,000,000Hz. For carbon, omega = 125,700,000Hz.
    if nucleus == '13C':
        omega = 150890000*2*pi # 13C Larmor frequency in 600 NEO
#        omega = 2*pi*126e6 # 13C Larmor frequency in 500
        K = 7.778e-34   #equation for K defined in Battiste and Wagner
        R2 = 0.0002    #R2 has been defined by Erik as 8.1 for 13C - not sure why.
        R2 = 8.1
    if nucleus == '1H':
        omega = 600000000*2*pi # 1H Larmor frequency in 600 NEO
#        omega = 500000000*2*pi # 1H Larmor frequency in 500
        K = 1.23e-32
        R2 = 0.00009   #R2 has been defined by Erik as 13 for 1H - not sure why.
        R2 = 13

    r = r*1e-8 # conversion factor from angstroms to centimeters

    #equation 5 from Battiste and Wagner
    b = 4*tau+((3*tau)/(1+(omega**2)*(tau**2)))
    R2S = (K * b)/(r**6)

    #equation 4 from Battiste and Wagner
    return (R2*e**(-R2S*t))/(R2 + R2S)

distance = []
residue_number = []
C13_pre_values = []
H1_pre_values = []

#aveDistance_file = input('DISTANCES: copy and paste the file name (include .txt extension if there is one): ')
aveDistance = np.loadtxt('a927c_avedistances.txt')

for i in range(len(aveDistance)):

    residue_number.append(i+1)
    H1_pre_values.append(pre_calculator('1H', aveDistance[i]))
    C13_pre_values.append(pre_calculator('13C', aveDistance[i]))


plt.figure(figsize=(5,2))
figure = plt.bar(residue_number,
                 H1_pre_values,
                 color = "royalblue",
                 width=0.75)

plt.savefig('PRE_1H_ratio_a927c.svg', format='svg', dpi=600)

plt.close()
#
#plt.figure(figsize=(5,2))
#figure = plt.bar(residue_number,
#                 C13_pre_values,
#                 color = "red",
#                 width=0.75)
#
#plt.savefig('PRE_13C_ratio_a927c.svg', format='svg', dpi=600)

# prints runtime
print("--- %s seconds ---" % '%.3f' % (time.time() - start_time))
print("--- %s minutes ---" % '%.3f' % (time.time()/60 - start_time/60))
