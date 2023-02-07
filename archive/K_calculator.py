#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 17:19:09 2018

k calculator

@author: Victor Prieto
"""

from math import pi

H1omega = 600000000*2*pi
C13omega = 150890000*2*pi

K = 1.23e-32 
t = 0.009
H1R2 = 0.0001
C13R2 = 0.00009
t = 0.0125
H1R2 = 0.0002
C13R2 = 0.00009 


#my constants for calculating K

#gyromagnetic ratios for 1H and 13C, in rad per seconds per tesla
H1gamma = 267.513
C13gamma = 67.2828

#spin values, unitless
S = 0.5

#electron g factor, unitless
g = 2.002319

#bohr magneton
beta = 9.27e-21

def K_calculator(S, gamma, g, beta):
    a = (1/15)
    b = gamma**2*g**2*beta**2
    return a * S * (S+1) * b 

K_proton = K_calculator(S, H1gamma, g, beta)
K_carbon = K_calculator(S, C13gamma, g, beta)

print(K_proton)
print(K_carbon)

print(K_proton/K_carbon)