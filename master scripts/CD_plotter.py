#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import csv
import pandas as pd
import matplotlib.pyplot as plt


header = """

Created on Fri Jul 30 18:25:45 2021 Eastern Time

This script analyzes CD data in .csv format and outputs figures.

@author: Victor Prieto

"""


# starts program runtime
start_time = time.time()
print('\n', header)
print('start time: %s Eastern Time' % time.ctime())

# =============================================================================
# locate csv files to open and read data
# =============================================================================

filename = ("/Users/victorprieto/Desktop/research/archive/"
            + "cd/ctFCP1 charge variant CD data")

sheet = pd.read_excel(filename + '.xlsx')

print(sheet.head())

sheet['wavelength'] = sheet['wavelength'].astype("category")

wavelength = sheet["wavelength"].tolist()

wavelength = sheet['wavelength'].tolist()
CD_3K = sheet['CD 3K'].tolist()
CD_KRK = sheet['CD KRK'].tolist()
CD_EDE = sheet['CD EDE'].tolist()
CD_5KR = sheet['CD 5KR'].tolist()
CD_WT = sheet['CD WT'].tolist()

# =============================================================================
# plotting section
# =============================================================================

plt.plot(wavelength, CD_3K, 'c')
plt.plot(wavelength, CD_KRK, 'm')
plt.plot(wavelength, CD_EDE, 'r')
plt.plot(wavelength, CD_5KR, 'b')
plt.plot(wavelength, CD_WT, 'grey')

plt.ylabel('ellipticity', fontsize=10)
plt.xlabel('wavelength', fontsize=10)
plt.xlim(205, 255)
plt.ylim(-45, 2)

#plt.show()

target_directory = ("/Users/victorprieto/Desktop/research/archive/"
                    + "cd/")
plt.savefig(target_directory + 'Fcp1 charge variant CD.svg', format='svg', dpi=600)

# prints runtime
print("--- %s seconds ---" % '%.3f' % (time.time() - start_time))
print("--- %s minutes ---" % '%.3f' % (time.time()/60 - start_time/60))
