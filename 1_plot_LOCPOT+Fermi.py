import subprocess
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append('/fibus/fs2/04/con4309/Skripte-Bombus')
from vasp import calc

#locpot auswertung
box = calc.get_box_POSCAR()
locpot_dim, atoms = calc.locpot_info()
dichte, potential = calc.locpot_potential(locpot_dim,atoms)

#get E-fermi
with open("OUTCAR") as temp_f2:
    datafile = temp_f2.readlines()
for line in datafile:
	if 'E-fermi' in line:
		a = line.split()
		print(a)
		e_fermi = a[2]
print(e_fermi)



#plotten
x3 = locpot_dim[2]	
min = np.min(dichte)-3
max = np.max(dichte)+3
plt.ylim(min,max)
plt.plot(dichte,   c='b')

plt.plot([0,x3], [e_fermi,e_fermi], c='black')
plt.plot([x3-16,x3-16],[-50,50],   c='r')
plt.plot([4,4],[-50,50],   c='r')
plt.xlabel('z [bins]')
plt.ylabel('V [eV]')

plt.savefig(f"2_locpot+Fermi.png", dpi=300)
plt.show()
plt.close()










