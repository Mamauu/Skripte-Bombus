import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
sys.path.append('/fibus/fs2/04/con4309/Skripte-Bombus')
from vasp import bader
#from vasp import calc

results_pre = np.genfromtxt("2_results.txt",skip_header=1, skip_footer=0)
calcs = results_pre.shape[0]
print("schritte: ",calcs)

zval = [4, 0, 6, 1, 7, 1]
atoms, atom_types, atom_counts, box = bader.get_atom_types()

charge_total_list, charge_atom_list, zval_Ne_list = bader.bader_charge_for_all_steps(atom_types,atom_counts,zval,calcs)
#bader.bader_plot(charge_total_list, charge_atom_list, zval_Ne_list,atom_types)

atom_type_list = atom_types

#for i in range(charge_total_list.shape[0]):
#	print(np.sum(charge_total_list[i]))

plt.plot(charge_total_list[:,0], label="Carbon", color="black")
plt.plot(charge_total_list[:,3]+charge_total_list[:,2], label="Hydrogen+Oxygen", color="green")
#plt.plot(charge_total_list[:,3], label="Hydrogen", color="orange")
plt.plot(charge_total_list[:,1], label="Neon", color="blue")
plt.plot(charge_total_list[:,4], label="Iodine", color="Purple")
plt.plot([0,calcs],[0,0],"k:")
plt.xlabel('steps / 38fs')
plt.ylabel('bader charge total / e')
plt.legend(loc="lower left")
plt.tight_layout()
plt.savefig("2_bader_time.png", dpi=300)
#plt.show()
plt.close()

#plottet die Bader Ladungen
x = (8-zval_Ne_list)*18
minimum = np.min(x)
maximum = np.max(x)
print("shape of x and y: ",x.shape,charge_atom_list.shape)

#for i, name in enumerate(atom_type_list):
	#plt.scatter(x,charge_total_list[:,i], label=name)
	#coef = np.polyfit(x,charge_total_list[:,i]-charge_total_list[0,i],1)
	#poly1d_fn = np.poly1d(coef) 
	#plt. plot(x, poly1d_fn(x))
plt.rcParams.update({'font.size': 15})

plt.scatter(x,charge_total_list[:,0], label="Carbon", color="black", linewidths=1)
plt.scatter(x,charge_total_list[:,4], label="Iodine", color="Purple", linewidths=1)
#plt.scatter(x,charge_total_list[:,5], label="Sodium", color="#AB5CF2", linewidths=1)
#plt.scatter(x,charge_total_list[:,2]+charge_total_list[:,3], label="Water", color="blue", linewidths=1)
#plt.plot([0,0],[-1,-1])

plt.scatter(x,charge_total_list[:,1], label="Neon", color="c", linewidths=1)
#plt.plot([0,np.max(x)],[0,np.max(x)*18], label="ZVAL", color="c")

#plt.axhline()
plt.xlabel('ZVAL change total / e')
plt.ylabel('bader charge total / e')
#plt.xlim(minimum,maximum)
plt.legend(loc="lower left")
plt.tight_layout()

plt.savefig("2_baderplot2.png", dpi=300)
#plt.show()
plt.close()



