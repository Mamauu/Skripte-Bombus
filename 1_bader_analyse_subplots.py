import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
sys.path.append('/fibus/fs2/04/con4309/Skripte-Bombus')
from vasp import bader
#from vasp import calc

def gaussian(x, mu, sig): #erzeugt Gaussians aus Breite und Höhe
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))
    
par_start = 1
par_stop  = 7
header = 1

data = np.genfromtxt("HILLSPOT",skip_header=header, skip_footer=0)

x_values = np.linspace(par_start, par_stop, 500)
y=np.zeros(500)

for i in range(data.shape[0]):
    h   = data[i][1]
    w   = data[i][2]
    pos = data[i][0]
    y = y + h*gaussian(x_values, pos, w)



calcs = 1000
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


Ne_charge = (8-zval_Ne_list)*18
time = index*51/1000
fig, axs = plt.subplots(2, 2)
for i in range(atom_counts[4]):
	axs[0, 0].plot(time,Iod_abstand_list[:,i],label=f"Abstand Iod{i+1} [A]",color="tab:orange")
#axs[0, 0].plot([0.200*51,0.200*51],[2,7],"b:")
axs[0, 0].set_xlabel('time / ps')
axs[0, 0].set_ylabel('Distance Iodine / $\AA$')
axs[0, 0].axvline(0.2*51, color='black')
#axs[0, 0].set_title("Abstand Iod")
#axs[0, 0].legend()

axs[0, 1].plot(time,dipole,label="Potential / V",color="tab:blue")
axs[0, 1].plot(time,Ne_charge,label="zval_change / e",color="tab:red")
#axs[0, 1].plot([0.2*51,0.2*51],[0,3],"b:")
axs[0, 1].set_xlabel('time / ps')
axs[0, 1].set_ylabel('Potential / V and charge / e')
axs[0, 1].axvline(0.2*51, color='black')
axs[0, 1].legend()

axs[1, 0].plot(x_values, -y,color="black")
axs[1, 0].set_xlabel("Distance / $\AA$")
axs[1, 0].set_ylabel("Metadynamic Potential / eV")

axs[1, 1].plot(time,charge_atom_list[:,4],color="tab:purple", label="Iod Charge [e]")
axs[1, 1].set_xlabel('time / ps')
axs[1, 1].set_ylabel('Bader charge iodine / e')
axs[1, 1].axvline(0.2*51, color='black')
#axs[1, 0].legend()




fig.tight_layout()
plt.show()
plt.savefig("2_combined_plot.png", dpi=500)
plt.close()


