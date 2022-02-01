import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
sys.path.append('/fibus/fs2/04/con4309/Skripte-Bombus')
from vasp import bader
#from vasp import calc

calcs = 300
#atom_types=["Pt","Ne","O","H"]
#atom_counts = [18, 18, 64, 128]
#zval = [10, 0, 6, 1]
#atom_types = ["C ","Ne","O ","H ","I ","Na"]
#atom_counts = [60, 18, 38, 76, 2, 2]
zval = [4, 0, 6, 1, 7, 1]
atoms, atom_types, atom_counts, box = bader.get_atom_types()


charge_total_list, charge_atom_list, zval_Ne_list = bader.bader_charge_for_all_steps(atom_types,atom_counts,zval,calcs)
bader.bader_plot(charge_total_list, charge_atom_list, zval_Ne_list,atom_types)

results = np.genfromtxt("2_results.txt",skip_header=1, skip_footer=0)
index = results[:,0]
zval_Ne_list = results[:,1]
target = results[:,2]
potential = results[:,3]
dipole = results[:,4]

plt.scatter(index,potential, label="Potential (eV?)",c="orange")
plt.scatter(index,dipole, label="Dipole (eA?)",c="b")
plt.plot(index,target, label="target(Dipole)",c="b")

plt.xlabel('index')
plt.ylabel('potential / Dipole in V?')
plt.legend(loc="upper left")
plt.show()
plt.savefig("2_potential_dipole.png", dpi=300)
plt.close()


names,numbers_np = bader.file_names_int(calcs,"data/CONTCAR_",ending="")
Iod_abstand_list=[]

for i, name in enumerate(names):
	Iod_abstand_step = bader.get_distance(atoms, atom_types, atom_counts, box,filename=name)
	Iod_abstand_list.append(Iod_abstand_step)
Iod_abstand_list = np.array(Iod_abstand_list)

for i in range(atom_counts[4]):
	plt.plot(Iod_abstand_list[:,i],label=f"Iod{i+1}")
plt.xlabel('Rechnungs index (ca. 50fs)')
plt.ylabel('Abstand Iod in A')
plt.legend(loc="upper left")
plt.show()
plt.savefig("2_abstand_Iod.png", dpi=300)
plt.close()


fig, ax1 = plt.subplots()
Ne_charge = (8-zval_Ne_list)*18
for i in range(atom_counts[4]):
	ax1.plot(index,Iod_abstand_list[:,i],label=f"Abstand Iod{i+1} [A]")
ax1.plot(index,dipole,label="Potential [V]")
ax1.plot(index,Ne_charge,label="zval_change [e]")
ax1.set_xlabel('Rechnungs index (ca. 50fs)')
ax1.set_ylabel('alles mögliche')

ax2 = ax1.twinx() 
ax2.plot(charge_atom_list[:,4],color="k", label="Iod Charge [e]")
ax2.set_ylabel('Iod Charge [e]')

ax1.legend(loc="lower center")
ax2.legend(loc="upper center")
plt.show()
plt.savefig("2_combined_plot.png", dpi=300)
plt.close()


"""
names,numbers_np = bader.file_names_int(calcs,"data/CONTCAR_",ending="")

for i in [1]:
	distanz_list = vasp.get_distance(names,indezes,box)
	#vasp.plot_distance(zval_Ne_list,distanz_list,neon_number)
	x = (8-zval_Ne_list)*neon_number
	plt.scatter(x, distanz_list,label="Distanz")
	plt.xlabel('ZVAL change in e')
	plt.ylabel('Distanz in A')
	plt.legend(loc="lower left")
	plt.savefig("2_distanz.png")
	plt.show()
"""
"""
#neon_number = atom_counts[1]
x = (8-zval_Ne_list)*18
maximum = np.max(x)

#plt.scatter(index,dipole, label="dipole",   c='black')
plt.scatter(index,potential, label="potential",   c='b')
plt.plot([0,200],[0,4],   c='b')
plt.scatter(index,x, label="charge",   c='r')
plt.scatter(index,charge_atom_list[:,4], label="iod charge",   c='tab:orange')


#plt.scatter(potential,charge_atom_list[:,4], label="test")
#plt.scatter(x,charge_atom_list[:,0], label="C")
#plt.scatter(x,charge_atom_list[:,1], label="Ne")
#plt.scatter(x,charge_atom_list[:,2], label="O")
#plt.scatter(x,charge_atom_list[:,3], label="H")
#plt.scatter(x,charge_atom_list[:,4], label="Iod")
#plt.scatter(x,charge_atom_list[:,5], label="Na")
#plt.axhline()
#plt.xlabel('ZVAL change total in e')
#plt.ylabel('Ladung per atom in e')
#plt.xlim(0,maximum)
plt.legend(loc="upper left")
plt.show()
plt.savefig("2_baderplot.png", dpi=300)

#ax1.plot([0,2.4],[0,2.4],   c='r')
#ax1.plot([0,2.4],[0,-2.4],   c='b')

"""
