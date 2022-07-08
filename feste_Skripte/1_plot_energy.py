import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append('/fibus/fs2/04/con4309/Skripte-Bombus')
from vasp import bader

"""
plottet die Energie aus dem OSZICAR
"""

def is_outlier(points, thresh=3.5):
    """
    Returns a boolean array with True if points are outliers and False 
    otherwise.

    Parameters:
    -----------
        points : An numobservations by numdimensions array of observations
        thresh : The modified z-score to use as a threshold. Observations with
            a modified z-score (based on the median absolute deviation) greater
            than this value will be classified as outliers.

    Returns:
    --------
        mask : A numobservations-length boolean array.

    References:
    ----------
        Boris Iglewicz and David Hoaglin (1993), "Volume 16: How to Detect and
        Handle Outliers", The ASQC Basic References in Quality Control:
        Statistical Techniques, Edward F. Mykytka, Ph.D., Editor. 
    """
    if len(points.shape) == 1:
        points = points[:,None]
    median = np.median(points, axis=0)
    diff = np.sum((points - median)**2, axis=-1)
    diff = np.sqrt(diff)
    med_abs_deviation = np.median(diff)

    modified_z_score = 0.6745 * diff / med_abs_deviation

    return modified_z_score > thresh

time = []
energy = []

results_pre = np.genfromtxt("2_results.txt",skip_header=1, skip_footer=0)
calcs = results_pre.shape[0]
print("schritte: ",calcs)

names,numbers_np = bader.file_names_int(calcs,"vasp_data/OSZICAR_",ending="")

for i, name in enumerate(names):
    with open(name) as temp_f2:
        datafile = temp_f2.readlines()
    for line in datafile:
        if 'E0= ' in line:
            a = line.split()
            time.append(float(a[0]))
            energy.append(float(a[8]))       

energy = np.array(energy)
filtered = energy[~is_outlier(energy)]
plt.plot(filtered)
plt.xlabel("Zeitschritte [0.5 fs]")
plt.ylabel("Energie [eV]")
plt.savefig("2_energy",dpi=300)
plt.show()
plt.close()



