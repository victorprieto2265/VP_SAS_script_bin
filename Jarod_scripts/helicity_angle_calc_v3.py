# -*- coding: utf-8 -*-
"""
Created on Thu May 28 10:44:09 2020

@author: Jarod Olson
"""

#just a little thing to see how long running the code takes my computer
import time
start_time = time.time()

import numpy as np

#this is where the folder is that contains 10,000 different files each with the coordinates stored of a bunch of 
#different atoms of a peptide
import os

import os.path

folder_path = r'C:\Users\Jarod Olson\Desktop\Showalter Research\Campari\Individual Frames'

i = 0

angles_phi = []
angles_psi = []
residue_count_list = []

count = []

j = 0

k = 0

x_values_C = []
y_values_C = []
z_values_C = []
x_values_N = []
y_values_N = []
z_values_N = []
x_values_CA = []
y_values_CA = []
z_values_CA = []

#for loops for every file in the folder_path I indicated
for data_file in sorted(os.listdir(folder_path)):

    #defined some variables here so that I can break my for loop later and also keep track of what file the code is on or what atom the code is on
    residue_count = 0

    #defined these variables for use later to recall 3 adjacent atoms by their index position
    g = j - 1
    h = g - 1
    #these are empty lists that will store the coordinates (split up) and angles of the atoms
    
    
    #opens the file to read it and reads every line
    pdb_file = open(data_file, mode='r')
    coordinates = pdb_file.readlines()
    for line in coordinates:
        
        if line.startswith('ATOM') and line[13:15] == 'N ':
            
            x_values_N.append(float(line[30:38]))
            y_values_N.append(float(line[38:46]))
            z_values_N.append(float(line[46:54]))
        
        if line.startswith('ATOM') and line[13:15] ==  'CA':
            
            x_values_CA.append(float(line[30:38]))
            y_values_CA.append(float(line[38:46]))
            z_values_CA.append(float(line[46:54]))    
            
        if line.startswith('ATOM') and line[13:15] == 'C ':
            
            #slices the coordinates out of the file and appends them to the list
            x_values_C.append(float(line[30:38]))
            y_values_C.append(float(line[38:46]))
            z_values_C.append(float(line[46:54]))
            
            #if j >= 1 then g should = 0 so the following arrays should work
            if j >= 1:
                #set up the arrays using the pre-defined variables to determine the index
                #might need to multiply a by -1?
                p0_phi = np.array([x_values_C[h], y_values_C[h], z_values_C[h]])
                p1_phi = np.array([x_values_N[g], y_values_N[g], z_values_N[g]])
                p2_phi = np.array([x_values_CA[g], y_values_CA[g], z_values_CA[g]])
                p3_phi = np.array([x_values_C[g], y_values_C[g], z_values_C[g]])
                
                b0_phi = -1.0*(p1_phi - p0_phi)
                b1_phi = p2_phi - p1_phi
                b2_phi = p3_phi - p2_phi
                
                b1_phi /= np.linalg.norm(b1_phi)
                
                v_phi = b0_phi - np.dot(b0_phi, b1_phi)*b1_phi
                w_phi = b2_phi - np.dot(b2_phi, b1_phi)*b1_phi
                
                x_phi = np.dot(v_phi, w_phi)
                y_phi = np.dot(np.cross(b1_phi, v_phi), w_phi)
                
                angles_phi.append(float(np.degrees(np.arctan2(y_phi, x_phi))))
                
                count.append(k)
                k += 1
                
                #same thing as above but calculating psi instead, double check these calculations are correct
                
                p0_psi = np.array([x_values_N[g], y_values_N[g], z_values_N[g]])
                p1_psi = np.array([x_values_CA[g], y_values_CA[g], z_values_CA[g]])
                p2_psi = np.array([x_values_C[g], y_values_C[g], z_values_C[g]])
                p3_psi = np.array([x_values_N[j], y_values_N[j], z_values_N[j]])
                
                b0_psi = -1.0*(p1_psi - p0_psi)
                b1_psi = p2_psi - p1_psi
                b2_psi = p3_psi - p2_psi
                
                b1_psi /= np.linalg.norm(b1_psi)
                
                v_psi = b0_psi - np.dot(b0_psi, b1_psi)*b1_psi
                w_psi = b2_psi - np.dot(b2_psi, b1_psi)*b1_psi
                
                x_psi = np.dot(v_psi, w_psi)
                y_psi = np.dot(np.cross(b1_psi, v_psi), w_psi)
              
                angles_psi.append(float(np.degrees(np.arctan2(y_psi, x_psi))))
                
                #trying to figure out how to write the residue numbers with the angles to a txt file
                residue_count_list.append(residue_count)
            #for every CA atom I take the coordinates from, j increases by 1
            j += 1
            g = j - 1
            h = g - 1
            
            residue_count += 1
            
        #"END" signals the end of the file so it makes sure to do this at the end of each file it reads
        #if "END" in line:
            
            #p = 0
            
            #helix = []
            
            #for listitem in angles_phi:
                
                #need to define the number range
                #if angles_phi[int(p)] >= -71 and angles_phi[int(p)] <= -57 and angles_psi[int(p)] >= -48 and angles_psi[int(p)] <= -34:
                    
                    #helix.append("y")
                    
                    #p += 1
                    
                #else:
                    
                    #helix.append("n")
                    
                    #p += 1
            
            #v = i + 1 
            
            #trying to save to a different folder
            #save_path = r'C:\Users\Jarod Olson\Desktop\Showalter Research\Campari\Individual Frames Angles'
            #helix_path = os.path.join(save_path, 'helix_' + "{:05d}".format(v) + '.txt')
            #with open(helix_path, 'w') as filehandle:
                #for listitem in helix:
                    #filehandle.write('%s\n' % listitem)
                    
         
            
            #writes y or n to another file I can pull them out of later
    pdb_file.close()
    
    i += 1
    #makes sure this code only reads the first 10,000 files because those are the ones with the coordinates
    if i == 10000:
        break

del count[-1]

save_path2 = r'C:\Users\Jarod Olson\Desktop\Showalter Research\Campari\python_phi_psi'
helix_path2 = os.path.join(save_path2, 'python_phi_psi_N_008.txt')
with open(helix_path2, 'w') as filehandle:
    for listitem in count:
        filehandle.write(str(residue_count_list[listitem]) + '   ' + str(angles_phi[listitem]) + '   ' + str(angles_psi[listitem]) + '\n')

#below is old code when checking out that the proper indexes were being iterated through
        
#save_path3 = r'C:\Users\Jarod Olson\Desktop\Showalter Research\Campari\python_phi_psi'
#helix_path3 = os.path.join(save_path3, 'python_coordinates_N_008.txt')
#with open(helix_path3, 'w') as filehandle:
    #for listitem in j_list:
        #filehandle.write(str(x_values_N[listitem]) + '   ' + str(y_values_N[listitem]) + '   ' + str(z_values_N[listitem]) + '\n' + str(x_values_CA[listitem]) + '   ' + str(y_values_CA[listitem]) + '   ' + str(z_values_CA[listitem]) + '\n' + str(x_values_C[listitem]) + '   ' + str(y_values_C[listitem]) + '   ' + str(z_values_C[listitem]) + '\n')

print("--- %s seconds ---" % (time.time() - start_time))