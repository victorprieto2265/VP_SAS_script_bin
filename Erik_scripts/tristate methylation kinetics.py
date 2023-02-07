#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Created on Fri Jul 19 15:32:15 2019

@author: Victor Prieto

"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 10:04:48 2018

This script fits tri-state methylation kinetics. Fitting is global. Three input files are required (one for each methylation state).

@author: ecc25
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy import optimize
from scipy.optimize import minimize
from scipy.optimize import fmin
#Define functions for methylation

#Definitions for single exponential decay and rise-to-maximum.
def singlerise(x, k, C):
    return C*(1-np.exp(-k*x))
def singledecay(x, yIntercept, preexponential, kon):
    return yIntercept + preexponential*np.exp(-kon*x)
def doubledecay(x, yIntercept, preexponential, kon,preexponential2, kon2):
    return yIntercept + preexponential*np.exp(-kon*x) + preexponential2*np.exp(-kon2*x)
def doublerise(x, k, C, k2, C2):
    return C*(1-np.exp(-k*x))+C2*(1-np.exp(-k2*x))
#Defitions for the integral forms of a three step consecutive reaction.
def Me1Fit(x, k1, k2, a1):
    return (((k1/(k1-k2))*(np.exp(-k2*x)-(np.exp(-k1*x))))*a1)
def Me2Fit(x, k1, k2, k3, a1):
    part1 = ((k1*k2)/(k1-k2))
    part2 = (((np.exp(-k1*x))/(k1-k3))+((np.exp(-k2*x))/(k3-k2))-((1/(k1-k3))+(1/(k3-k2)))*(np.exp(-k3*x)))
    return (part1*part2)*a1
def Me3Fit(x, k1, k2, k3, a1):
    numerator = (k1*k3*(k1-k3)*np.exp(-k1*x))-(k1*k3*(k1-k3)*np.exp(-k2*x))+(k1*k2*(k1-k2)*np.exp(-k3*x))
    denominator = (k1-k2)*(k1-k3)*(k2-k3)
    return (1-numerator/denominator)*a1
def PIMe3Fit(x, k1, k2, k3, k4, a1, a2):
    numerator = (k1*k3*(k1-k3)*np.exp(-k1*x))-(k1*k3*(k1-k3)*np.exp(-k2*x))+(k1*k2*(k1-k2)*np.exp(-k3*x))
    denominator = (k1-k2)*(k1-k3)*(k2-k3)
    return (1-numerator/denominator)*a1 + (np.exp(-k4*x)*a2)
def AltMe3Fit(x, k1, k2, a1, k3, a2):
    return (a1*(1+(1/(k1-k2))*(k2*np.exp(-k1*x)-k1*np.exp(-k2*x))))+(x*k3+a2)

def AltMe3Fit1(x, k1, k2, a1, k3):
    return a1*((1+(1/(k1-k2))*(k2*np.exp(-k1*x)-k1*np.exp(-k2*x)))+np.exp(-k3*x))
#Defitions for the integral forms of a three step consecutive reaction without a pre-exponential.
def WMe1Fit(x, k1, k2):
    return (((k1/(k1-k2))*(np.exp(-k2*x)-(np.exp(-k1*x)))))
def WMe2Fit(x, k1, k2, k3):
    part1 = ((k1*k2)/(k1-k2))
    part2 = (((np.exp(-k1*x))/(k1-k3))+((np.exp(-k2*x))/(k3-k2))-((1/(k1-k3))+(1/(k3-k2)))*(np.exp(-k3*x)))
    return (part1*part2)
def WMe3Fit(x, k1, k2, k3):
    numerator = (k1*k3*(k1-k3)*np.exp(-k1*x))-(k1*k3*(k1-k3)*np.exp(-k2*x))+(k1*k2*(k1-k2)*np.exp(-k3*x))
    denominator = (k1-k2)*(k1-k3)*(k2-k3)
    return (1-numerator/denominator)


#Load three inputs files. First column should contain time, and second column should contain intensity.
Me1 = np.loadtxt("Me1xydata.txt")
Me2 = np.loadtxt("Me2xydata.txt")
Me3 = np.loadtxt("Me3xydata.txt")

 

# Normalize the signal intensity with respect to number of methyl groups. Make the decay phase of the monomethyl and dimethyl peak return to zero.
deadtime = 9+43/60
for i in Me2:
    i[1] = (i[1]-Me2[-1][1])/2
    i[0] = i[0] + deadtime
for i in Me3:
    i[1] = (i[1]-Me3[0][1])/10
    i[0] = i[0] + deadtime
for i in Me1:
    i[1] = (i[1]-Me1[-1][1])/2
    i[0] = i[0] + deadtime

Me1[0] = [0,0]
Me2[0] = [0,0]
Me3[0] = [0,0]
  
#Plot raw data
plt.figure(figsize=(6,6))
plt.scatter(Me1[:,0], Me1[:,1], color="royalblue")
plt.scatter(Me2[:,0], Me2[:,1], color='mediumorchid')
plt.scatter(Me3[:,0], Me3[:,1], color='forestgreen')





#Fit each data set individually prior to global fit.
guess1 = [0.5,0.05,1000]
params1, params_covariance1 = optimize.curve_fit(Me1Fit, Me1[:,0][0:-1], Me1[:,1][0:-1], guess1)
guess2 = [0.2,0.02,0.01,3000]
params2, params_covariance2 = optimize.curve_fit(Me2Fit, Me2[:,0][0:-1], Me2[:,1][0:-1], guess2, maxfev=20000)
guess3 = [0.5,0.05,0.011,3000]
params3, params_covariance3 = optimize.curve_fit(Me3Fit, Me3[:,0], Me3[:,1], guess3)

modelX = np.arange(0,1000)
guess4 = [0.5,0.05,3000, 500000, 5000]
params4, params_covariance4 = optimize.curve_fit(AltMe3Fit, Me3[:,0], Me3[:,1], guess4)
#plt.plot(modelX, AltMe3Fit(modelX, params4[0], params4[1], params4[2]), color='pink')

#Returns sum of squares for global data. The idea of the global fitting is to minimize the return on this function.
def MasterEq(params):
    k1, k2, k3, a1, a2, a3, k4, a4 = params
    sum1 = Me1Fit(Me1[:,0],k1, k2, a1) - Me1[:,1]
    ls1 = 0
    for i in sum1:
        ls1 = ls1 + i**2
    sum2 = Me2Fit(Me2[:,0],k1, k2, k3, a2) - Me2[:,1]
    ls2 = 0
    for i in sum2:
        ls2 = ls2 + i**2
    sum3 = AltMe3Fit(Me3[:,0],k2, k3, a3, k4, a4) - Me3[:,1]
    ls3 = 0
    for i in sum3:
        ls3 = ls3 + i**2

    return ls1 + ls2 + ls3

globalFits = [params1[0],params2[1], params3[2], params1[2], params2[3], params3[3], params4[3], params4[4]]

#Global fitting routine
minimized = minimize(MasterEq, globalFits , method = 'Nelder-Mead',options={'maxiter': 10000})

globalFits = minimized['x']

#for i in range(0,1):
#    sos = MasterEq(globalFits[0], globalFits[1], globalFits[2], globalFits[3], globalFits[4], globalFits[5])
#    newfit = MasterEq(globalFits[0] + 0.01, globalFits[1], globalFits[2], globalFits[3], globalFits[4], globalFits[5])
#    print (newfit < sos)


#Plot models
modelX = np.arange(0,1000)
plt.plot(modelX, Me1Fit(modelX, globalFits[0], globalFits[1], globalFits[3]), color = 'royalblue')
plt.plot(modelX, Me2Fit(modelX, globalFits[0], globalFits[1], globalFits[2], globalFits[4]), color='mediumorchid')
#plt.plot(modelX, Me3Fit(modelX, globalFits[0], globalFits[1], globalFits[2], globalFits[5]), color='darkgreen')
plt.plot(modelX, AltMe3Fit(modelX, globalFits[1], globalFits[2], globalFits[5], globalFits[6], globalFits[7]), color='forestgreen')
#plt.plot(modelX, doublerise(modelX, params4[0], params4[1], params4[2], params4[3]), color='pink')
#plt.plot(modelX, Me1Fit(modelX, params1[0], params1[1], params1[2]), color = 'royalblue')
#plt.plot(modelX, Me2Fit(modelX, params2[0], params2[1], params2[2], params2[3]), color='mediumorchid')
#plt.plot(modelX, Me3Fit(modelX, params3[0], params3[1], params3[2], params3[3]), color='darkgreen')
#plt.plot(modelX, AltMe3Fit(modelX, params4[0], params4[1], params4[2], params4[3], params4[4]), color='darkgreen')
plt.xlim(-10,800)
plt.ylim(-500,10000)
plt.xlabel('Time (seconds)', fontsize=20)
plt.xticks(fontsize=15)
plt.ylabel('Intensity', fontsize=20)
plt.yticks(fontsize=0)
plt.savefig('PRDM9.pdf', dpi=300)

plt.figure(figsize=(3,4))
plt.ylabel('Rate min-1')
plt.bar(['K4Me1','K4Me2','K4Me3'],globalFits[0:3])
plt.yscale('log')
plt.savefig('PRDM9_kinetics.pdf', dpi=-300)

plt.figure(figsize=(6,6))
print ('Global fits: k,K4Me1: ' + str(globalFits[0]) + ', k,K4Me2: ' + str(globalFits[1]) + ', k,K4Me3: ' + str(globalFits[2]))