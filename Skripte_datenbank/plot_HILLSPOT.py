import matplotlib.pyplot as plt
import numpy as np

"""
liest HILLPOT ein und plottet die Gaussians
"""

def gaussian(x, mu, sig): #erzeugt Gaussians aus Breite und Höhe
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))
    
#Parameter, die gesetzt werden müssen
name = "Iod2"
step = 10 # alle wie viele Schritte wird Gaussian geschrieben
par_start = 1
par_stop  = 6
header = 1

data = np.genfromtxt("HILLSPOT",skip_header=header, skip_footer=0)

#plottet Reaktionskoordiante über zeit
position = data[:,0]
plt.plot(position)
plt.xlabel(f"Anzahl Gaussians [1 pro {step}]")
plt.ylabel("Distanz [Angström]")
plt.savefig(f"2_HILLSPOT_position_{name}.png", dpi=300)
plt.show()
plt.close()

x_values = np.linspace(par_start, par_stop, 500)
y=np.zeros(500)

for i in range(data.shape[0]):
    h   = data[i][1]
    w   = data[i][2]
    pos = data[i][0]
    y = y + h*gaussian(x_values, pos, w)

#plottet Energie über Reaktionskoordiante 
plt.plot(x_values, -y)
plt.xlabel("Distanz [Angström]")
plt.ylabel("Metadynamic Potential [eV]")
plt.savefig(f"2_HILLSPOT_energy_{name}.png", dpi=300)
plt.show()
plt.close()



