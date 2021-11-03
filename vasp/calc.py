import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math


def XDATCAR_header(): 
    """
    erzeugt XDATCAR_all datei und liest header aus POSCAR ein
    Args/Returns:
	    /
    """
    f_XDAT_all = open("XDATCAR_all", "w") 
    f_header = open("POSCAR","r")
    all_lines = f_header.readlines()
    f_XDAT_all.writelines(all_lines[:7])
    f_header.close()
    f_XDAT_all.close()
    return 0


def locpot_info(filename="LOCPOT"): 
    """
    get infos from the LOCPOT file
    Args:
        filename (str): /
    Returns:
        locpot_dim (list): x,y,z dimensionen der locpot datei
        atoms (int): number of atoms 
    """
    locpot_dim = [0,0,0]

    file = open(filename)
    all_lines = file.readlines()
    atom_list = all_lines[6].split()
    atom_list2 = [int(i) for i in atom_list]
    atoms = sum(atom_list2) 

    locpot_dim[0] = int(all_lines[atoms+9].split()[0])
    locpot_dim[1] = int(all_lines[atoms+9].split()[1])
    locpot_dim[2] = int(all_lines[atoms+9].split()[2])
    print("locpot dimension und atomanzahl",locpot_dim,atoms)
    return locpot_dim, atoms


def _clean_line(line):
    return line.replace("-", " -")


def _get_lines_from_file(filename, lines=None):
    """
    If lines is None read the lines from the file with the filename filename.
    Args:
        filename (str): file to read lines from
        lines (list/ None): list of lines

    Returns:
        list: list of lines
    """
    if lines is None:
        with open(filename, "r") as f:
            lines = f.readlines()
    return lines


def get_dipole_moments(filename="OUTCAR", lines=None):
    """
    Get the average electric dipole moment at every ionic step
    Args:
        filename (str): Filename of the OUTCAR file to parse
        lines (list/None): lines read from the file
    Returns:
        list: A list of dipole moments in (eA) for each ionic step
    """
    moment_trigger = "dipolmoment"
    istep_trigger = "FREE ENERGIE OF THE ION-ELECTRON SYSTEM (eV)"
    dip_moms = list()
    lines = _get_lines_from_file(filename=filename, lines=lines)
    istep_mom = list()
    for i, line in enumerate(lines):
        line = line.strip()
        if istep_trigger in line:
            dip_moms.append(np.average(istep_mom))
            istep_mom = list()
        if moment_trigger in line:
            line = _clean_line(line)
            mom = np.array([float(val) for val in line.split()[1:4]])
            istep_mom.append(mom[2])
    return dip_moms


def get_dipole_moments_average(names):
    """
    reads dipole moment for all given filenames
    Args:
		names (list): filenames
    Returns:
    	dipole_list (list): list with the average dipol for this OUTCAR file
    """ 
    dipole_list = []
    dipole_list_dev=[]
    for i in names:
        print("Datei Dipol berechnung",i)
        file = open(i)
        dipole_moments = get_dipole_moments(filename=i)
        dipole_average = np.average(dipole_moments)
        dipole_dev = np.std(dipole_moments)
        print("dipole:",dipole_average, dipole_dev)
        dipole_list.append(dipole_average)
        dipole_list_dev.append(dipole_dev)
    return dipole_list, dipole_list_dev
    
    
def locpot_potential(locpot_dim,atoms,filename="LOCPOT"):
	"""
	read Potential from LOCPOT file
	Args:
		filename = filename of The LOCPOT
		locpot_dim = dimensions of the locpot file
		atoms = number of atoms
	Returns:
		dichte: potential verlauf entlanf z in eV
		potential: potential in eV
	""" 
	dichte = []
	print("datei potential:",filename)
	x1 = locpot_dim[0]
	x2 = locpot_dim[1]
	x3 = locpot_dim[2]	
	data = np.genfromtxt(filename,skip_header=atoms+10, skip_footer=0)
	data2 = data.reshape(1,x1*x2*x3)
	grid = np.zeros([x1, x2, x3])

	for j in range(x3):
		zaler=0
		zaler2=0
		for k in range(x1*x2): #write  1 z slice
			value = data2[0][k+j*x1*x2]

			if zaler > x1-1:
				zaler = zaler-x1
				zaler2+=1
			
			grid[zaler][zaler2][j]=value #write 1 x slice
			zaler+=1
	
	for j in range(x3):
		z_dichte2 = sum(grid[:,:,j])
		z_dichte = sum(z_dichte2)/x1/x2
		dichte.append(z_dichte)

	potential = dichte[x3-20]-dichte[5]
	print("potential:", potential)
	return dichte, potential
    
    
    
    
    
    
    
    
