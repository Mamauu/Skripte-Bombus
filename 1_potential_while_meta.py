import subprocess
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append('/fibus/fs2/04/con4309/Skripte-Bombus')
from vasp import calc

def running_mean(x, N):
    cumsum = np.cumsum(np.insert(x, 0, 0)) 
    return (cumsum[N:] - cumsum[:-N]) / float(N)

box = calc.get_box_POSCAR()
dipole_moments = calc.get_dipole_moments()


potential = []

for i in range(len(dipole_moments)):
	potential_dipol = calc.dipol_to_potential(dipole_moments[i],box)
	potential.append(potential_dipol)

x = np.linspace(0,25,len(potential), endpoint=True)


plt.plot(x, potential)
plt.plot([np.min(x), np.max(x)],[2, 2],'k:')
plt.ylim(0,4)
plt.xlabel('time [ps]')
plt.ylabel('potential [V]')
plt.show()
plt.savefig("2_dipol_meta.png", dpi=300)
plt.close()






