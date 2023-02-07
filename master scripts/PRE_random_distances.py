#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Created on Sat Mar 6 08:37:32 2021

This script examines PRE values of two sets of distances: one set
randomly clustered around an average value, and the other with all
distances fixed at the same average value.

@author: Victor Prieto

"""

import time
import random
from math import pi
from math import e

# starts program runtime
start_time = time.time()
print('start time: %s Eastern Time' % time.ctime())

# =============================================================================
# creation of two distance data sets
# =============================================================================

distances_1 = []  # the list with distances scattered between 1 and 30
list_length = 10000
for i in range(0, list_length):
    n = random.randint(5, 45)
#    n = 15
    distances_1.append(n)

average_distance = sum(distances_1)/list_length
print('average distance = ', average_distance)

"""
If average distance is less than about 14.5, the 1H PRE for the fixed
distances is greater. If average distance is greater than 14.5, the 1H PRE
for the variable distances is greater. Note: 15 is the distance at which
Battiste-Wagner equation predicts 1H PRE ratio = 0.5.
"""

distances_2 = []
for i in range(0, list_length):
    distances_2.append(average_distance)

######
# PRE calculation section, references:
# Battiste and Wagner, Biochemistry 2000
# Sjott and Clubb, Bio Protoc 2016


def pre_calculator(nucleus, r):
    # outputs the intensity ratio given nucleus and distance r

    # correlation time for the electron nuclear interaction
    tau = 0.0000000207  # 20.7 ns
    tau = 1.2e-9  # Erik's value

    t = 0.0125
    # the total evolution time of the transverse proton magnetization
    # during the NMR experiment, per Sjott and Clubb, or total INEPT
    # evolution time of the HSQC (∼9 ms), per Battiste and Wagner.

    # Larmor frequency of the nuclear spin (proton, carbon, etc.)
    # For proton, omega = 500,000,000Hz.
    # For carbon, omega = 125,700,000Hz.
    if nucleus == '13C':
        omega = 150890000*2*pi
        K = 7.778e-34
        # equation for K defined in Battiste and Wagner
        R2 = 8.1
        # R2 has been defined by Erik as 8.1 for 13C - not sure why.
    if nucleus == '1H':
        omega = 600000000*2*pi
        K = 1.23e-32
        R2 = 13
        # R2 has been defined by Erik as 13 for 1H - not sure why.

    r = r*1e-8   # note: this may be the wrong conversion factor for
    # angstroms to centimeters, but it seems to fit the experimental
    # data better. Not sure why, there may be another error in the
    # calculation.

    # equation 5 from Battiste and Wagner
    b = 4*tau+((3*tau)/(1+(omega**2)*(tau**2)))
    R2S = (K * b)/(r**6)

    # equation 4 from Battiste and Wagner
    return (R2*e**(-R2S*t))/(R2 + R2S)


pre_list_1 = []
for i in distances_1:
    pre_value = pre_calculator('1H', i)
    pre_list_1.append(pre_value)

average_pre_1 = sum(pre_list_1)/list_length
print('average_pre_1 = ', average_pre_1)

pre_list_2 = []
for i in distances_2:
    pre_value = pre_calculator('1H', i)
    pre_list_2.append(pre_value)

average_pre_2 = sum(pre_list_2)/list_length
print('average_pre_2 = ', average_pre_2)

# prints runtime
print("--- %s seconds ---" % '%.3f' % (time.time() - start_time))
print("--- %s minutes ---" % '%.3f' % (time.time()/60 - start_time/60))
