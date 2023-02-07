#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script analyzes the xyz coordinates taken from frames from Campari trajectory pdb files 
and plots the interresidue distance between the residue of interest and all other residues. 

The script will prompt you to name the file that the data will be exported to, 
then a popup should appear to select the pdb files (select as many as you want).
                                               
This script does not require the PDBcombiner written by Erik Cook, and is instead intended for many pdb files, each containing a single frame. 

This script will break if you enter in an invalid residue name and/or number.

This script was written to work with ctFCP1, which has 83 residues (879-961), plus a cloning artifact of GPG
and a tryptophan, making it 87 residues long (875-961). 
This script will need to be rewritten for proteins of different length (particularly roi_position, residueID, 
and residue_index).

Based on script written by Erik Cook.

Created on Thu Oct 11 14:27:27 2018

@author: Victor Prieto
"""

from tkinter import filedialog
import tkinter
import numpy as np
import matplotlib.pyplot as plt
import sys

#tells tkinter to search for the filename and open the filedialog window
root = tkinter.Tk()
root.withdraw()

fileName = input("Name your output file: ")

#request for information about residue of interest
roi_identity = input('enter the three letter code (capitalized) for the residue of interest: ')
roi_position_input = input('enter the three number position for the residue of interest: ')

roi_position = str(int(roi_position_input)+38)

#roi stands for residue_of_interest
roi = roi_identity + " A " + roi_position

#Place all files requested into an array.
files = filedialog.askopenfilenames()

fileNumber = 0
processedmodels = 0

aveDistance = np.array([])
distanceArray = np.array([])

#Find the Rg for each model of each replica.  
for file in files:
    pdbTraj =open(file, "r")
    model = []
    m = 1
    roi_model = []
    for line in pdbTraj:
        
        residueID = int((str(line)[23:26]).strip())

        #identifies the line in the PDB file which corresponds to the alpha carbon for a cysteine
        #and appends the xyz coordinates to the array labeled 'model'        
        
        if "ATOM" in line:
            appendage = [float((str(line)[30:38]).strip()), float((str(line)[39:46]).strip()), float((str(line)[46:54]).strip())]
            model.append(appendage)
            residueID += 1
        
        #same thing as above, but finds the xyz coordinates for the residue of interest and 
        #appends them to array labeled 'roi_model'        
        
        if roi in line:
        
            roi_model = [float((str(line)[30:38]).strip()), float((str(line)[39:46]).strip()), float((str(line)[46:54]).strip())]
            
#        elif ("ENDMDL" in line) or ("END" in line) or not(line):
        if residueID == 1000:

            residueID = int((str(line)[23:26]).strip())
            
            for i in model:
                dis = np.sqrt(((i[0]-roi_model[0])**2)+((i[1]-roi_model[1])**2)+((i[2]-roi_model[2])**2))
                distanceArray = np.append(distanceArray, dis)                
                        
            if processedmodels == 0:
                aveDistance = distanceArray
                            
            else:
                aveDistance = aveDistance + distanceArray
            
            
            #Empty distanceArray and model array.
            distanceArray = np.array([])
            model = []

            if processedmodels % 100 == 0:
                print ('number of processed models: ', processedmodels)    
            processedmodels = processedmodels + 1

print('total distance sum before averaging: \n', aveDistance)
print('number of processed models: \n', processedmodels)

aveDistance = aveDistance/processedmodels

print('average distance: \n', aveDistance)

np.savetxt(str(fileName) + '.txt', aveDistance)
residue_index = np.arange(876, 962, 1)     
pdbTraj.close()
    
fig,ax=plt.subplots(figsize = (10,6))
figure = plt.plot(residue_index, aveDistance)
title = 'interresidue distance: ' + roi_identity + roi_position_input
plt.title(title, fontsize = "20")
plt.ylabel('distance (angstroms)', fontsize = 20)
plt.xlabel('residue index', fontsize = 20)

fileNumber = fileNumber + 1    

plt.show()

sys.exit()