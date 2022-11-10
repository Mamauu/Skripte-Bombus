import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
sys.path.append('/fibus/fs2/04/con4309/Skripte-Bombus') #change to the folder with my functions called "vasp"
from vasp import bader
#from vasp import calc


def get_starts(filename, lines):
	#gives all the line numbers with the trigger in it
	trigger = "Direct configuration="
	result_list = list()
	
	for i, line in enumerate(lines):
		line = line.strip()
		if trigger in line:
			result_list.append(i)
	return result_list

listH = list()
listO = list()
lines = list()
atoms, atom_types, atom_counts, box = bader.get_atom_types() #get information of the system

f = open("XDATCAR_all","r")
lines_normal = f.readlines()

for i, line in enumerate(lines_normal): #gives formated data
	line = line.strip()
	lines.append(line)
f.close()
print("XDATCAR file readin")

result_list = get_starts("XDATCAR",lines) #gives all the line numbers with the trigger in it
atoms_toH = atom_counts[0]+atom_counts[1]
atoms_toO = atom_counts[0]+atom_counts[1]+atom_counts[2]

#read all H atoms
for i, step_start in enumerate(result_list):
	for j in range(atom_counts[2]):
		n_line_withH = step_start+atoms_toH+j+1
		line_H = lines[n_line_withH]
		#print(line_H)
		value_H = float(line_H.split()[2])*box[2]
		listH.append(value_H)

#read all O atoms
for i, step_start in enumerate(result_list):
	for j in range(atom_counts[3]):
		n_line_withO = step_start+atoms_toO+j+1
		line_O = lines[n_line_withO]
		#print(line_O)
		value_O = float(line_O.split()[2])*box[2]
		listO.append(value_O)


hist, bin_edges = np.histogram(listO, bins=np.arange(5,25,0.1))
hist2, bin_edges2 = np.histogram(listH, bins=np.arange(5,25,0.1))
print(hist, bin_edges)

mass = 16*1.66053906660*10**-24
mass2 = 1*1.66053906660*10**-24
calcs = len(result_list)
volume = box[0]*10**-8*box[1]*10**-8*0.2*10**-8
hist_density = hist / calcs * mass / volume
hist_density2 = hist2 / calcs * mass2 / volume
hist_densityall = hist_density+hist_density2

plt.plot(hist_densityall)
plt.xlabel("bins (0.1A)")
plt.ylabel("g/cm^3")
plt.savefig("2_hist.png", dpi=300)
plt.show()
plt.close()








"""
for i in result_list:
	#print (i)
	for j in range(atom_counts[2]):
		print(i,j)
		#print(pos_data[i+j+fest_atoms+1])
		
	for j in range(atom_counts[3]):	
		print(i,j)
		#print(pos_data[i+j+fest_atoms+atom_counts[2]+1])
		
"""
#positions[i][0] = float(pos_filter[0])*box[0]
#positions[i][1] = float(pos_filter[1])*box[1]
#positions[i][2] = float(pos_filter[2])*box[2]
	
"""

results_pre = np.genfromtxt("2_results.txt",skip_header=1, skip_footer=0)
calcs = results_pre.shape[0]


def get_distance(atoms, atom_types, atom_counts, box,filename="CONTCAR"):
	#gibt für jedes Iod den Abstand zum nächsten Iod aus
	#inputs durch get_atom_types() gegeben
	minval_list=[]
	f = open(filename,"r")
	all_lines = f.readlines()
	positions = np.zeros(shape=(atoms,3))
	box2 = freud.Box(box[0],box[1],box[2])

	for i in range(atoms):
		pos_line = all_lines[i+9] # liest Zeile mit Position ein
		pos_filter = list(filter(None,pos_line.split(" "))) #bereinigt Linien und schreibt sie in Liste
		pos = [float(pos_filter[0]),float(pos_filter[1]),float(pos_filter[2])] #konvertiert Werte zu float
		positions[i][0] = float(pos_filter[0])*box[0]
		positions[i][1] = float(pos_filter[1])*box[1]
		positions[i][2] = float(pos_filter[2])*box[2]

	for i,type in enumerate(atom_types):
		if type == "I":
			atom_before_iod = sum(atom_counts[0:i])
			atoms_iod = atom_counts[i]

	pos_iod=positions[atom_before_iod:atom_before_iod+atoms_iod]

	for i in range(atoms_iod):
		distance_iod = box2.compute_all_distances(pos_iod[i],pos_iod)
		minval = np.min(distance_iod[np.nonzero(distance_iod)])
		minval_list.append(minval)
	#print("geringster Abstand zum nächsten Iod: ",minval_list)
	return minval_list


def _get_lines_from_file(filename, lines=None):
	if lines is None:
		with open(filename, "r") as f:
			lines = f.readlines()
	return lines
	
def get_starts(filename, lines=None):
	lines = _get_lines_from_file(filename=filename, lines=lines)
	trigger = "Direct configuration="
	result_list = list()
	
	for i, line in enumerate(lines):
		line = line.strip()
		if trigger in line:
			result_list.append(i)
	return result_list, lines
	
def get_pos(result_list, pos_data, atoms):
	for i in result_list:
		x = np.array(pos_data[i:i+atoms])
		print(x)
	return 

"""




