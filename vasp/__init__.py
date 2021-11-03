
#how to use this module
#import sys
#sys.path.append('/fibus/fs2/04/con4309/code') 
#import vasp
#from vasp import test
#test.hello()


"""
file_managment.sh
#works for C/Ne/O/H/Iod/Na systems

i=$1
zval=$2
cp CONTCAR POSCAR
cp HILLSPOT PENALTYPOT

line=2330
substitute="   POMASS =   20.180; ZVAL   =    $zval    mass and valenz"
awk -v where="$line" -v what="$substitute" 'FNR==where {print what; next} 1' POTCAR_base > POTCAR

mpirun -machinefile machinefile_$SLURM_JOBID -np $SLURM_NTASKS vasp_gam

#cp XDATCAR data/XDATCAR_$i
cp OSZICAR data/OSZICAR_$i
cp OUTCAR  data/OUTCAR_$i
cp CONTCAR data/CONTCAR_$i #rausnehmen wenn Abstände auch aus XDATCAR_all datei ausgelsen werden können
#cp LOCPOT  data/LOCPOT_$i  
#cp AECCAR0 data/AECCAR0_$i
#cp AECCAR2 data/AECCAR2_$i
#cp CHGCAR  data/CHGCAR_$i  

/fibus/fs2/04/con4309/Scripts/chgsum.pl AECCAR0 AECCAR2
/fibus/fs2/04/con4309/Scripts/bader CHGCAR -ref CHGCAR_sum
cp BCF.dat bader/BCF_$i.dat  

rm CHGCAR_sum AVF.dat BCF.dat
rm CHG

exit


import subprocess
import numpy as np
import sys
sys.path.append('/fibus/fs2/04/con4309/code')
from vasp import calc

calc.XDATCAR_header() #erzeugt XDATCAR_all datei und liest header aus POSCAR ein
f = open("2_results.txt", "w") #write header for the results file
f.write("index zval_ne target Potential Dipol Dipol_dev \n")
f.close()

#setzt parameter
zval = 8.000 #startpunkt festlegen
ramp = False
target_max = 1.5
steps = 10

for i in range(1,steps+1):
	if ramp == True: #setzt target zum maximalen Wert oder erhöht diesen linear
		target = target_max*(i)/steps
	else:
		target = target_max

	#startet die rechnung mit neuem zval
	subprocess.call(['bash','1_file_managment.sh',str(i),str("{0:0.3f}".format(zval))]) 
	#rechnet Potential nach dem Rechenschritt aus
	dipole,dipole_dev = calc.get_dipole_moments_average(["OUTCAR"]) #in diesem Fall nur eine Datei, daher hat die liste nur ein Objekt
	locpot_dim, atoms = calc.locpot_info()
	dichte, potential = calc.locpot_potential(locpot_dim,atoms)

	# schreibt die ergebnisse raus
	calc.XDATCAR_only_pos() #kopiet XDATCAR dateien ohne ihren header zusammen
	f = open("2_results.txt", "a")
	f.write(str(i)+" "+str("{0:0.3f}".format(zval))+" "+str("{0:0.3f}".format(target))+" "+str("{0:0.3f}".format(potential))+" "+str("{0:0.5f}".format(dipole[0]))+" "+str("{0:0.5f}".format(dipole_dev[0]))+"\n")
	f.close()

	#bestimmt wieweit ZVAL abgeändert wird.
	dif = abs(target - potential)
	change = round(dif * 10)/1000
	if change > 0.005:
		change = 0.005

	if potential < target:
		zval = zval-change
	if potential > target:
		zval = zval+change
"""










