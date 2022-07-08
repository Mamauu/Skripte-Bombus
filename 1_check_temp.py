import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def _get_lines_from_file(filename, lines=None):
	if lines is None:
		with open(filename, "r") as f:
			lines = f.readlines()
	return lines

def get_temp(filename, lines=None):
	trigger = "T="
	temp_list = list()
	lines = _get_lines_from_file(filename=filename, lines=lines)
	for i, line in enumerate(lines):
		line = line.strip()
		if trigger in line:
			mom = np.array(line.split())
			#print(mom)
			temp_list.append(float(mom[2]))
	return temp_list

def running_mean(x, N):
    cumsum = np.cumsum(np.insert(x, 0, 0)) 
    return (cumsum[N:] - cumsum[:-N]) / float(N)
   
results_pre = np.genfromtxt("2_results.txt",skip_header=1, skip_footer=0)
calcs = results_pre.shape[0]
print("Anzahl Rechnungen: ",calcs)

temp_list2 = list()
for i in range(1,calcs):
	temp = get_temp(f"vasp_data/OSZICAR_{i}")
	temp_list2.extend(temp)

mean_area = 100
temp_running = running_mean(temp_list2,mean_area)

for i in range(int(mean_area/2)):
	temp_list2.insert(0,7)

print("Durchschnitt",np.average(temp_list2))
print("stddev",np.std(temp_list2))

plt.plot(temp_list2,label="temp")
plt.plot(temp_running,label="temp running (50fs)")
plt.axhline(300)
#plt.xlim(10000,30000)
plt.ylim(150,450)
plt.xlabel("steps / 0,5fs")
plt.ylabel("temperature / K")
plt.legend()

plt.savefig("2_temp.png", dpi=500)
plt.show()
plt.close()


