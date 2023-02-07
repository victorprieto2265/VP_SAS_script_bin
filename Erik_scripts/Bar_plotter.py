''# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 09:38:08 2017

@author: Erik Cook
"""


from tkinter import filedialog
import tkinter
import numpy as np
import matplotlib.pyplot as plt

#file =open("N_000_campari_traj.pdb", "r")
root = tkinter.Tk()
root.withdraw()


#Place all files requested into an array.
file = filedialog.askopenfilename()   

data = np.loadtxt(file)

plt.figure(figsize=(10,6))
figure = plt.bar(data[:,0], data[:,1], color = "royalblue", edgecolor = "white", width = 1)

plt.title("ctFCP1_M961C_MTSL CON PRE")
plt.tick_params(axis='both', which='major', labelsize=16)
plt.ylabel('$I_{para}/I_{dia}$', fontsize = 20)
plt.xlabel('Residue Index', fontsize = 20)
plt.xlim(np.min(data[:,0]), np.max(data[:,0]))
