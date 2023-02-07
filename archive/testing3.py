#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 14:12:50 2018

@author: Victor Prieto
"""

import numpy as np
from math import e

def R2SP(tau, omega, K, r):
    r = r*1e-8
    b = 4*tau+((3*tau)/(1+(omega**2)*(tau**2)))
    return (K * b)/(r**6)

def Iratio(R2, R2S, t):    
    x = (R2*e**(-R2S*t))/(R2 + R2S)
    return x

#correlation time for the electron nuclear interaction
tau = 0.0000000207

#Larmor frequency of the nuclear spin (proton, carbon, etc.) For proton, omega = 500,000,000Hz. For carbon, omega = 125,700,000Hz. 
H1omega = 498.186000
C13omega = 125.7
K = 1.23e-32        
t = 0.009
H1R2 = 0.0001
C13R2 = 0.00009

r = 15

x = R2SP(tau, C13omega, K, r)

print(x)

y = Iratio(C13R2, x, t)

print(y)

#R2SP = np.array([9.99E+01, 1.69E+02, 3.17E+02, 6.71E+02, 1.71E+03, 5.63E+03, 3.38E+04, 5.24E+05])
#R2 = 9.00E-05
#t = 0.009
#
#print('R2SP is equal to ', R2SP)
#print('R2 is equal to ', R2)
#
#x = Iratio(R2, R2SP, t)
#print('Iratio is equal to', x)