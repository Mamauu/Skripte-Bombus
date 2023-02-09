
#works for C/Ne/O/H/Iod/Na systems

i=$1
zval=$2

cp CONTCAR POSCAR
cp HILLSPOT PENALTYPOT

line=2330
substitute="   POMASS =   20.180; ZVAL   =    $zval    mass and valenz"
awk -v where="$line" -v what="$substitute" 'FNR==where {print what; next} 1' POTCAR_base > POTCAR

mpirun -machinefile machinefile_$SLURM_JOBID -np $SLURM_NTASKS vasp_gam

cp 2_locpot* vasp_data/
cp OSZICAR vasp_data/OSZICAR_$i
cp OUTCAR  vasp_data/OUTCAR_$i
cp CONTCAR vasp_data/CONTCAR_$i


/fibus/fs2/04/con4309/Skripte-Bombus/feste_Skripte/chgsum.pl AECCAR0 AECCAR2
sleep 1
/fibus/fs2/04/con4309/Skripte-Bombus/feste_Skripte/bader CHGCAR -ref CHGCAR_sum
sleep 1
cp BCF.dat bader_data/BCF_$i.dat  
cp ACF.dat bader_data/ACF_$i.dat  

rm CHGCAR_sum AVF.dat BCF.dat
rm CHG
rm 2_locpot*


exit





