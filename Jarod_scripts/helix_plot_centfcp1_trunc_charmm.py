# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 02:41:13 2020

@author: Jarod Olson
"""

import time
start_time = time.time()

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

#Note- <alpha> 1 is 230K and 20 is 420K and everything else is ordered as would be expected

sheet = pd.read_excel('Helicity_Dataframe_centfcp1_trunc_charmm_pythonversion.xlsx')

heatmap1_data = pd.pivot_table(sheet, values='Helicity', index='<α>', columns='Residue Number')

f, ax = plt.subplots(figsize=(15,20))

ax = sns.heatmap(heatmap1_data, cmap='bone_r', vmin=0, vmax=100, yticklabels=True, square=True, cbar_kws=dict(shrink=0.35,use_gridspec=False,location="top"), ax=ax)

ax.axhline(y=0, color='k',linewidth=3)
ax.axhline(y=20, color='k',linewidth=3)
ax.axvline(x=0, color='k',linewidth=3)
ax.axvline(x=47, color='k',linewidth=3)
ax.tick_params(axis="x",direction="in",length=3)
ax.tick_params(axis="y",direction="in",length=3)

plt.savefig('helic_1dheatmap_centfcp1_trunc_charmm_all_residues.svg', bbox_inches='tight', format='svg', dpi = 600)

plt.show()

print("--- %s seconds ---" % (time.time() - start_time))
