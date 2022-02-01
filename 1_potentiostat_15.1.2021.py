import subprocess
import numpy as np
import sys
sys.path.append('/fibus/fs2/04/con4309/Skripte-Bombus')
from vasp import calc

calc.XDATCAR_header() #erzeugt XDATCAR_all datei und liest header aus POSCAR ein
f = open("2_results.txt", "w") #write header for the results file
f.write("index zval_ne target Potential Potential(Dipol) Dipol_dev(eA) \n")
f.close()

#setzt parameter
box = calc.get_box_POSCAR()
zval = 8.000
steps = 1000
ramp = True
start_V = 2
target_V = 2
target_list = calc.create_target_list(steps,start_V,target_V,ramp)

for i in range(1,steps+1):
	target = target_list[i-1]

	#startet die rechnung mit neuem zval
	subprocess.call(['bash','1_file_managment.sh',str(i),str("{0:0.3f}".format(zval))]) 

	#rechnet Potential nach dem Rechenschritt aus
	dipole,dipole_dev = calc.get_dipole_moments_average(["OUTCAR"]) #in diesem Fall nur eine Datei, daher hat die liste nur ein Objekt
	locpot_dim, atoms = calc.locpot_info()
	dichte, potential = calc.locpot_potential(locpot_dim,atoms)
	calc.plot_locpot(dichte,locpot_dim,i)
	potential_dipol = calc.dipol_to_potential(dipole[0],box)

	# schreibt die ergebnisse raus
	calc.XDATCAR_only_pos() #kopiet XDATCAR dateien ohne ihren header zusammen
	f = open("2_results.txt", "a")
	f.write(str(i)+" "+str("{0:0.3f}".format(zval))+" "+str("{0:0.3f}".format(target))+" "+str("{0:0.3f}".format(potential))+" "+str("{0:0.5f}".format(potential_dipol))+" "+str("{0:0.5f}".format(dipole_dev[0]))+"\n")
	f.close()

	#bestimmt wieweit ZVAL abgeändert wird.
	dif = abs(target - potential_dipol)
	change = round(dif * 5)/1000
	if change > 0.005:
		change = 0.005
	if potential_dipol < target:
		zval = zval-change
	if potential_dipol > target:
		zval = zval+change












