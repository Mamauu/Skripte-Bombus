# Skripte Bombus
Skripte zum laufen und analysieren von Vasp Rechnungen

#vasp					/ Modul mit Funktionen
	calc.py				/ Potentiostat / Funktionen während der Rechnung
	bader.py			/ Analyse bader, Distanz etc.

# feste Skripte
save_bashrc.sh / bashrc 	/ backups bashrc
bader + chgsum.pl 			/ kopierte Skripte für bader Analyse
plot_energy					/ plottet OSZICAR für jeden Potentiostat schritt
plot_energy_single.py		/ plottet OSZICAR

# Skripte Datenbank
plot_HILLSPOT.py			/ plottet Metadynamic Hills
1_density_water.py  		/ checks denstiy profile of water along z
1_plot_LOCPOT+Fermi.py		/ plottet das Potential und die Fermi energie über die länge der Zelle
1_check_temp.py				/ misst temperatur
1_plot_bader.py				/ plottet bader data
1_bader_analyse_subplots.py	/ auswertung der bader daten mit 4 subplots

1_potentiostat_9.2.23.py	/ beispiel skript zum ausführen des Potentiostaten
1_file_managment_9.2.23.sh	/ passendes bash skript
run.bombus					/ sbatch skript zum rechnung starten







