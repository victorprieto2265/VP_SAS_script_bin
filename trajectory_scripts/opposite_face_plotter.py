#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import csv
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm


header = """

plotter script for output .csv file from opposite face calc.

Note: "Asp7" was a typo when generating the data. It is actually
Asp457 of Rap74.

Asp457 is on the back side, Lys471 is in the cleft.

Created on Thu Jun 10 08:09:14 2021

@author: Victor Prieto

"""

# starts program runtime
start_time = time.time()
print('start time: %s Eastern Time' % time.ctime())
print('\n', header)

constructs = ['EDE_restrained',
              'WT_02',
              'KRK_restrained',
              '3K_restrained',
              '4QAN_restrained',
              '5KR_restrained']

distance_list_A = []
distance_list_L = []

for construct in constructs:

    file_dir = ('/Users/victorprieto/Desktop/research/python/'
                + 'trajectory_scripts/trajectory_calc_outputs/'
                + 'opposite_face_'
                + construct
                + '_distances/')
    filename = file_dir + ('opposite_face_comparison_'
                           + construct)

    with open((filename + ".csv"), encoding='utf8') as csv_file:
        csv_reader = csv.reader(csv_file)

        residues = []
        # for comparing two distances in the same construct
        distanceA = []
        distanceL = []

        for row in csv_reader:

            if row[3] == '300' and row[0] == 'Asp7':
                distanceA.append(round(float(row[2]), 3))
                residues.append(int(row[1]))

            if row[3] == '300' and row[0] == 'Lys471':
                distanceL.append(round(float(row[2]), 3))

    distance_list_A.append(distanceA)
    distance_list_L.append(distanceL)

# =============================================================================
# this section plots two points in one construct/trajectory
# =============================================================================

    plt.plot(residues, distanceA, 'b', label='back side')
    plt.plot(residues, distanceL, 'r', label='cleft side')
    plt.legend()
    plt.ylim([0, 120])
    plt.title(construct)

    savefig_title = construct + '_opposite_face_comparison'
    file_dir = ('/Users/victorprieto/Desktop/research/python/'
                + 'trajectory_scripts/plot_outputs/opposite face comparison/')
    plt.savefig(file_dir
                + savefig_title
                + '.svg',
                dpi=600,
                format='svg', transparent=True, bbox_inches='tight')

    plt.show()

    # necessary to clear figure between loops
    plt.clf()

# =============================================================================
# this section is for comparing one point across all constructs/trajectories
# =============================================================================

evenly_spaced_interval = np.linspace(0, 1, len(constructs))
cmap = cm.get_cmap("plasma_r")
colors = [cmap(x) for x in evenly_spaced_interval]

for i, color in enumerate(colors):
    plt.plot(distance_list_A[i], color=color, label=constructs[i])
plt.legend()
plt.title('Asp457 (cleft side) comparison across constructs')
plt.savefig(file_dir
            + 'Asp457_comparison'
            + '.svg',
            dpi=600,
            format='svg', transparent=True, bbox_inches='tight')


plt.show()

plt.clf()

for i, color in enumerate(colors):
    plt.plot(distance_list_L[i], color=color, label=constructs[i])
plt.legend()
plt.title('Lys471 (back side) comparison across constructs')
plt.savefig(file_dir
            + 'Lys471_comparison'
            + '.svg',
            dpi=600,
            format='svg', transparent=True, bbox_inches='tight')


# prints runtime
print("--- %s seconds ---" % '%.3f' % (time.time() - start_time))
print("--- %s minutes ---" % '%.3f' % (time.time()/60 - start_time/60))
