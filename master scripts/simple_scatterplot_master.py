#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Created on Mon Oct 21 09:04:12 2019

@author: Victor Prieto

"""

# Starts program runtime
import time
start_time = time.time()

import numpy as np
import matplotlib.pyplot as plt

filename = 'simulated competition data' + '.txt'
line_number = 1

x_values = []
y_values = []

temp = np.loadtxt(filename)
print(temp)
for line in temp:
    x_values.append(line[0])
    y_values.append(line[1])


plt.plot(x_values, y_values, 'k')
plt.ylabel('x')
plt.xlabel('y')
plt.show()

plt.savefig(filename + '.jpg',  format = 'jpg', dpi = 600)
