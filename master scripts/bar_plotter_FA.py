#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Created on Sun Mar 15 19:35:40 2020

@author: Victor Prieto

"""

import numpy as np
import matplotlib.pyplot as plt
#from scipy import stats

# puc_data=np.loadtxt('Puc_reps2.txt')
# s1_data=np.loadtxt('site1_reps.txt')
# s2_data=np.loadtxt('site2_reps.txt')
# pdx1c_data=np.loadtxt('pdx1c_reps.txt')
# e224k_data=np.loadtxt('e224k_reps_temp.txt')
# pdx1cSPOP_data=np.loadtxt('pdx1c_SPOP_reps_temp.txt')
# e224kSPOP_data=np.loadtxt('e224k_SPOP_reps.txt')


# pos = [1, 1.5, 2, 2.5, 3, 3.5, 4]
# x1 = np.random.normal(pos[0], 0.02, len(puc_data))
# x2 = np.random.normal(pos[1], 0.02, len(s1_data))
# x3 = np.random.normal(pos[2], 0.02, len(s2_data))
# x4 = np.random.normal(pos[3], 0.02, len(pdx1c_data))
# x5 = np.random.normal(pos[4], 0.02, len(e224k_data))
# x6 = np.random.normal(pos[5], 0.02, len(pdx1cSPOP_data))
# x7 = np.random.normal(pos[6], 0.02, len(e224kSPOP_data))

# puc = np.mean(puc_data)
# s1 = np.mean(s1_data)
# s2 = np.mean(s2_data)
# pdx1c = np.mean(pdx1c_data)
# e224k = np.mean(e224k_data)
# pdx1c = np.mean(pdx1c_data)
# pdx1cSPOP = np.mean(pdx1cSPOP_data)
# e224kSPOP = np.mean(e224kSPOP_data)

# plt.scatter(x1, puc_data, facecolors = 'none', color = 'navy', s = 40)
# plt.scatter(x2, s1_data, facecolors = 'none', color = 'navy', s = 40)
# plt.scatter(x3, s2_data, facecolors = 'none', color = 'navy', s = 40)
# plt.scatter(x4, pdx1c_data, facecolors = 'none', color = 'navy', s = 40)
# plt.scatter(x5, e224k_data, facecolors = 'none', color = 'navy', s = 40)
# plt.scatter(x6, pdx1cSPOP_data, facecolors = 'none', color = 'navy', s = 40)
# plt.scatter(x7, e224kSPOP_data, facecolors = 'none', color = 'navy', s = 40)

# plt.scatter(pos[0], puc, marker = '_' , color = 'red', s = 500)
# plt.scatter(pos[1], s1, marker = '_' , color = 'red', s = 500)
# plt.scatter(pos[2], s2, marker = '_' , color = 'red', s = 500)
# plt.scatter(pos[3], pdx1c, marker = '_' , color = 'red', s = 500)
# plt.scatter(pos[4], e224k, marker = '_' , color = 'red', s = 500)
# plt.scatter(pos[5], pdx1cSPOP, marker = '_' , color = 'red', s = 500)
# plt.scatter(pos[6], e224kSPOP, marker = '_' , color = 'red', s = 500)
                

plt.title('FCP1 construct binding strengths')
plt.ylim(1, 1000)
plt.xlim(0.5 ,4.5)
plt.ylabel('Kd')
plt.yscale('log')

plt.tight_layout()  
#plt.legend(loc = 'upper right')
#plt.savefig('190919_Kd_viz2.ps', format='ps', dpi=600)

plt.show()
