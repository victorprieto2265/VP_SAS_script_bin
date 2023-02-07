#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
for plotting two growth curves on top of one another


Created on Fri Sep 14 21:56:56 2018

@author: Victor Prieto
"""

import numpy as np
import matplotlib.pyplot as plt
from operator import add

#in natural abundance M9 media
hours = [8, 9, 10, 11, 12, 13, 13]
hours_to_minutes = np.array([i * 60 for i in hours])
minutes = np.array([20, 15, 15, 10, 5, 20, 45])
x = hours_to_minutes[0] + minutes[0]
time = list(map(add, hours_to_minutes - x, minutes))

print(hours)
print(hours_to_minutes)
print(minutes)
print(time)

density = [0, 0.076, 0.124, 0.221, 0.324, 0.584, 0.686]

#in isotopically enriched M9 media
hours2 = [11, 14, 15, 16, 16, 17]
hours_to_minutes2 = np.array([i * 60 for i in hours2])
minutes2 = np.array([45, 45, 35, 20, 45, 20])
y = hours_to_minutes2[0] + minutes2[0]
time2 = list(map(add, hours_to_minutes2 - y, minutes2))

density2 = [0, 0.229, 0.326, 0.466, 0.556, 0.736]

plt.plot(time2, density2, 'r:', time, density, 'b:')
plt.ylabel('OD')
plt.xlabel('minutes')
plt.show()
