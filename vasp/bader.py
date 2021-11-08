import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

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


def bader_charge_from_bcf(filename,zval,atom_types,atom_counts):
	"""
	reads the bader results (BCF) and calculates the charge of the different atom types
	Args:
		filename  (str): location of the BCF file from bader
		zval (list): zvalue of all atoms at this step
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
		charge_atom.append((data_sp['charge'].sum()/anzahl)-zval[i])
		charge_total.append(((data_sp['charge'].sum()/anzahl)-zval[i])*anzahl)
		#print(atom_types[i],"per atom:",(data_sp['charge'].sum()/anzahl)-zval[i])
		#print(atom_types[i],"total   :",((data_sp['charge'].sum()/anzahl)-zval[i])*anzahl)
	return charge_atom, charge_total


def bader_charge_for_all_steps(atom_types,atom_counts,zval,calcs=20):
	"""
	reads the charge via the bader_from_bcf function for every Potentiostat step and writes it in the 2_bader.txt file
	Args:
		calcs (int): number of Potentiostat steps
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
	x = (8-zval_Ne_list)
	maximum = np.max(x)

	for i, name in enumerate(atom_type_list):
		plt.scatter(x,charge_atom_list[:,i], label=name)
	plt.axhline()
	plt.xlabel('ZVAL change per atom in e')
	plt.ylabel('Ladung per atom in e')
	plt.xlim(0,maximum)
	plt.legend(loc="upper right")
	plt.show()
	plt.savefig("2_baderplot_atom.png", dpi=300)
	plt.close()

	x = (8-zval_Ne_list)*18
	maximum = np.max(x)

	for i, name in enumerate(atom_type_list):
		plt.scatter(x,charge_total_list[:,i], label=name)
	plt.axhline()
	plt.xlabel('ZVAL change total in e')
	plt.ylabel('Ladung total in e')
	plt.xlim(0,maximum)
	plt.legend(loc="upper right")
	plt.show()
	plt.savefig("2_baderplot_total.png", dpi=300)
	plt.close()
	
	#ax1.plot([0,2.4],[0,2.4],   c='r')
	#ax1.plot([0,2.4],[0,-2.4],  c='b')
	return 0





