import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import freud

def file_names_int(calc_num,file_name,ending=""):
    """
    gives out names of files when doing x calculations
    Args:
        calc_num (int): Anzahl an Rechnungen
        file_name (str): start of the file like "CONTCAR_"
    Returns:
        names (list): name of files
        numbers_np (list): number of the calculation
    """
    names=[]
    numbers_np = np.arange(1,calc_num+1,1)
    for i in numbers_np:
        full_name=str(file_name)+str(i)+str(ending)
        names.append(full_name)
    return names,numbers_np


def get_atom_types(filename="POSCAR"): 
	"""
	liest atom types and count of them from the POSCAR
	Args:
		filename: /
	Returns:
		atoms (int): number of atoms 
		...
	"""
	file = open(filename)
	all_lines = file.readlines()
	atom_types_list = all_lines[5].split()
	atom_types = [str(i) for i in atom_types_list]
	atom_list = all_lines[6].split()
	atom_counts = [int(i) for i in atom_list]
	atoms = sum(atom_counts) 
	print("atomanzahl, typen, anzahl pro type: \n",atoms,atom_types, atom_counts)
	box = [0, 0, 0]
	box[0] = float(all_lines[2].split()[0])
	box[1] = float(all_lines[3].split()[1])
	box[2] = float(all_lines[4].split()[2])
	file.close()
	return  atoms, atom_types, atom_counts, box


def bader_charge_from_bcf(filename,zval,atom_types,atom_counts):
	"""
	reads the bader results (BCF) and calculates the charge of the different atom types
	Args:
		filename  (str): location of the BCF file from bader
		zval (list): zvalue of all atoms at this step
		atom_types (list):  names of the atoms
		atom_counts (list): number of atoms by type
	Returns:
		charge_atom  (list): list of the charge of the atom_types per atom
		charge_total (list): list of the charge of the atom_types total
	"""
	data = pd.read_csv(filename,skiprows=2,skipfooter=1,delim_whitespace=True,names=['a','b','c','d','charge','nummer','g'],engine='python')
	data_sort = data.sort_values(by='nummer')

	charge_atom  = []
	charge_total = []

	for i in range(len(atom_counts)):
		start = 1 + sum(atom_counts[0:i])
		stop  = sum(atom_counts[0:i+1])
		anzahl = stop-start+1

		data_sp = data_sort[(data_sort.nummer >= start) & (data_sort.nummer <= stop)]

		#print(data_sp)
		if atom_counts[i] > 0:
			charge_atom.append((data_sp['charge'].sum()/anzahl)-zval[i])
			charge_total.append(((data_sp['charge'].sum()/anzahl)-zval[i])*anzahl)
		if atom_counts[i] == 0:
			charge_atom.append(0)
			charge_total.append(0)			
		#print(atom_types[i],"per atom:",(data_sp['charge'].sum()/anzahl)-zval[i])
		#print(atom_types[i],"total   :",((data_sp['charge'].sum()/anzahl)-zval[i])*anzahl)
	return charge_atom, charge_total


def bader_charge_for_all_steps(atom_types,atom_counts,zval,calcs=20):
	"""
	reads the charge via the bader_from_bcf function for every Potentiostat step and writes it in the 2_bader.txt file
	Args:
		calcs (int): number of Potentiostat steps
		zval (list): zvalue of all atoms at this step
		atom_types (list):  names of the atoms
		atom_counts (list): number of atoms by type
	Returns:
		/
	"""
	f = open("2_bader.txt", "w")
	f.write("index zval_ne total charge of : C Ne O H I Na \n")
	names,numbers_np = file_names_int(calcs,"bader/BCF_",ending=".dat")

	results = np.genfromtxt("2_results.txt",skip_header=1, skip_footer=0)
	zval_Ne_list = results[:,1]
	charge_total_list = list()
	charge_atom_list = list()
	
	for i, name in enumerate(names):
		zval_Ne = zval_Ne_list[i]
		zval[1] = zval_Ne
		print(i,zval[1], name)

		charge_atom, charge_total = bader_charge_from_bcf(name,zval,atom_types,atom_counts)
		charge_total_list.append(charge_total)
		charge_atom_list.append(charge_atom)
		#print(charge_atom) #["C ","Ne","O ","H ","I ","Na"]
		#print(charge_total) #["C ","Ne","O ","H ","I ","Na"]

		f.write(str(i+1)+" "+str(zval[1])+" "+" ".join(str("{0:0.4f}".format(item)) for item in charge_total)+"\n")
	f.close()
	charge_total_list = np.array(charge_total_list)
	charge_atom_list = np.array(charge_atom_list)
	return charge_total_list, charge_atom_list,zval_Ne_list


def bader_plot(charge_total_list, charge_atom_list, zval_Ne_list,atom_type_list):
	#plottet die Bader Ladungen
	x = (8-zval_Ne_list)
	minimum = np.min(x)
	maximum = np.max(x)
	print("shape of x and y: ",x.shape,charge_atom_list.shape)

	for i, name in enumerate(atom_type_list):
		plt.scatter(x,charge_atom_list[:,i], label=name)
	plt.axhline()
	plt.xlabel('ZVAL change per atom in e')
	plt.ylabel('Ladung per atom in e')
	plt.xlim(minimum,maximum)
	plt.legend(loc="upper right")
	plt.show()
	plt.savefig("2_baderplot_atom.png", dpi=300)
	plt.close()

	x = (8-zval_Ne_list)*18
	minimum = np.min(x)
	maximum = np.max(x)

	for i, name in enumerate(atom_type_list):
		plt.scatter(x,charge_total_list[:,i]-charge_total_list[0,i], label=name)
		coef = np.polyfit(x,charge_total_list[:,i]-charge_total_list[0,i],1)
		poly1d_fn = np.poly1d(coef) 
		plt. plot(x, poly1d_fn(x))

	plt.axhline()
	plt.xlabel('ZVAL change total in e')
	plt.ylabel('Ladung total in e')
	plt.xlim(minimum,maximum)
	plt.legend(loc="upper right")
	plt.show()
	plt.savefig("2_baderplot_total.png", dpi=300)
	plt.close()
	
	#ax1.plot([0,2.4],[0,2.4],   c='r')
	#ax1.plot([0,2.4],[0,-2.4],  c='b')
	return 0


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



