#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Biochemistry, Vol. 43, No. 51, 2004

Optimizes RT in equation 5 from the above citation. 

Grace Usher + Victor Prieto
09/27/19

"""

import matplotlib.pyplot as plt

import numpy as np

#fraction of fluorophore bound
Fsb = 0.8

#concentration of fluorophore in micromolar
Lst = 0.040

#generates a random data set of Kd1 values between 1 and 400 micromolar
Kd1 = np.random.randint(low=0.1, high=100, size=100)

num = (-Lst * (Fsb **2)) + ((Kd1 + Lst) * Fsb)

denom = 1 - Fsb

Rt = num / denom

plt.scatter(Rt, Kd1)
plt.ylabel('RT (uM)')
plt.xlabel('Kd1 (uM)')
plt.title('RT/Kd1 plot for fraction bound = '+str(Fsb))
plt.show()

plt.savefig(str(Fsb)+ '_fractionbound.png', format = 'png', dpi = 600)

for i in range(1,100):
    print('Kd1= ', Kd1[i], '\nRT = ', Rt[i])




