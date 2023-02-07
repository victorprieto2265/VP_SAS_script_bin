#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Created on REPLACE WITH TIME AFTER RUNNING THE FOLLOWING CODE:

import time
time.ctime()

@author: Victor Prieto

"""

#starts program runtime
import time
import numpy as np
from math import e
from math import pi

start_time = time.time()


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
C13_pre_values = []
H1_pre_values = []

## this section produces a nice figure that shows how the PRE Iratio varies as a function of distance in angstroms, used as a sanity check that the PRE calculator is modelling PRE from distances correctly.

for i in range(1, 40):
    pre = pre_calculator('13C', i)
    if i % 3 == 0 and pre > 0.02 and pre < 0.98:
        print('13C PRE at distance ' + str(i) + ' angstroms ----- ' + str(pre))
    distance.append(i)
    C13_pre_values.append(pre)

    pre = pre_calculator('1H', i)
    if i % 3 == 0 and pre > 0.02 and pre < 0.98:
        print('1H PRE at distance ' + str(i) + ' angstroms ----- ' + str(pre))
    H1_pre_values.append(pre)

# plt breaks a script in a terminal window, don't forget.

import matplotlib.pyplot as plt
plt.plot(distance, H1_pre_values, 'r:')
plt.plot(distance, C13_pre_values, 'b:')
plt.ylabel('$I_{para}/I_{dia}$', fontsize = 10)
plt.xlabel('distance (angstroms)', fontsize = 10)
#plt.show()

#plt.savefig('PRE_ratio_plot.svg', format='svg', dpi=600)


#######

# prints runtime
print("--- %s seconds ---" % '%.3f' % (time.time() - start_time))
print("--- %s minutes ---" % '%.3f' % (time.time()/60 - start_time/60))
