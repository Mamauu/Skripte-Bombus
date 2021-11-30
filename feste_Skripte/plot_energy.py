import matplotlib.pyplot as plt

"""
plottet die Energie aus dem OSZICAR
"""

time = []
energy = []

with open("OSZICAR") as temp_f2:
    datafile = temp_f2.readlines()
for line in datafile:
    if 'E0= ' in line:
        a = line.split()
        time.append(float(a[0]))
        energy.append(float(a[8]))       

plt.plot(time,energy)
plt.xlabel("Zeitschritte [0.5 fs]")
plt.ylabel("Energie [eV]")
plt.savefig("2_energy",dpi=300)
plt.show()
plt.close()



