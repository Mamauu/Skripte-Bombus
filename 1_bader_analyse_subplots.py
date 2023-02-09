import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
sys.path.append('/fibus/fs2/04/con4309/Skripte-Bombus') #change to the folder with my functions called "vasp"
from vasp import bader
#from vasp import calc

def gaussian(x, mu, sig): #erzeugt Gaussians aus Breite und Höhe
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))
    
par_start = 1 #low barrier for plotting metadynamic potential
par_stop  = 9 #high barrier
header = 1    #number of hills ignored
x_values = np.linspace(par_start, par_stop, 500)
meta_sum = np.zeros(500)

data = np.genfromtxt("HILLSPOT",skip_header=header, skip_footer=0) #read in metydanmic hills
y_list_potential = [] #list with potentials where metadynamic is plottet

for i in range(data.shape[0]):
    h   = data[i][1]
    w   = data[i][2]
    pos = data[i][0]
    meta_sum = meta_sum + h*gaussian(x_values, pos, w)
    if (i+1) % 200 == 0:
    	y_list_potential.append(-meta_sum)
    	print(i," Hier wird potential geplottet")

plot_meta = True #activate plotting of metadynamic
if plot_meta == True:
	#plottet Reaktionskoordiante über zeit
	position = data[:,0]
	plt.plot(position)
	plt.xlabel("Anzahl Gaussians ")
	plt.ylabel("distance [Angström]")
	plt.savefig("2_HILLSPOT_position.png", dpi=300)
	#plt.show()
	plt.close()

	#plottet Energie über Reaktionskoordiante 
	plt.plot(x_values, -meta_sum)
	plt.xlabel("Distanz [Angström]")
	plt.ylabel("Metadynamic Potential [eV]")
	plt.savefig("2_HILLSPOT_energy.png", dpi=300)
	#plt.show()
	plt.close()

#read in lots of stuff
zval = [4, 0, 6, 1, 7, 1] #zval of different atoms in Order
atoms, atom_types, atom_counts, box = bader.get_atom_types() #get information of the system

results_pre = np.genfromtxt("2_results.txt",skip_header=1, skip_footer=0)
calcs = results_pre.shape[0]
print("schritte: ",calcs)
results = results_pre[0:calcs]
print("shape results: ",results.shape)
index = results[:,0]
zval_Ne_list = results[:,1]
target = results[:,2]
potential_dipole = results[:,3]
#potential = results[:,5]


#calculates the bader charges
charge_total_list, charge_atom_list, zval_Ne_list = bader.bader_charge_for_all_steps(atom_types,atom_counts,zval,calcs)
#bader.bader_plot(charge_total_list, charge_atom_list, zval_Ne_list,atom_types) #activate to plot zval agsinst bader charge for different atoms

names,numbers_np = bader.file_names_int(calcs,"vasp_data/CONTCAR_",ending="")
Iod_abstand_list=[]

#get distance of iodine to each other
for i, name in enumerate(names):
	Iod_abstand_step = bader.get_distance(atoms, atom_types, atom_counts, box, filename=name)
	Iod_abstand_list.append(Iod_abstand_step)
Iod_abstand_list = np.array(Iod_abstand_list)


#2x2 plot with all the stuff
Ne_charge = (8-zval_Ne_list)*18 #change here number of Neon
time = index*38/1000 #change here length of the single calculations (here 51fs)
fig, axs = plt.subplots(2, 2)
for i in range(atom_counts[4]):
	axs[0, 0].plot(time,Iod_abstand_list[:,i],label=f"Abstand Iod{i+1} [A]",color="tab:orange")
#axs[0, 0].plot([0.200*51,0.200*51],[2,7],"b:")
axs[0, 0].set_xlabel('time / ps')
axs[0, 0].set_ylabel('Distance Iodine / $\AA$')
#axs[0, 0].set_title("Abstand Iod")
#axs[0, 0].legend()

axs[0, 1].plot(time,potential_dipole,label="Potential / V",color="tab:blue")
axs[0, 1].plot(time,Ne_charge,label="zval_change / e",color="tab:red")
#axs[0, 1].plot([0.2*51,0.2*51],[0,3],"b:")
axs[0, 1].set_xlabel('time / ps')
axs[0, 1].set_ylabel('Potential / V and charge / e')
axs[0, 1].legend()

for i,y_values in enumerate(y_list_potential):
	axs[1, 0].plot(x_values, y_values, label="{} ps".format(int(10+i*200*50/1000))) #,color="black"  
axs[1, 0].set_xlabel("Distance / $\AA$")
axs[1, 0].set_ylabel("Metadynamic Potential / eV")
#axs[1, 0].legend(loc="lower right")

axs[1, 1].plot(time,charge_atom_list[:,4],color="tab:purple", label="Iod Charge [e]")
axs[1, 1].set_xlabel('time / ps')
axs[1, 1].set_ylabel('Bader charge iodine / e')


fig.tight_layout()
plt.savefig("2_combined_plot.png", dpi=500)
plt.show()
plt.close()







