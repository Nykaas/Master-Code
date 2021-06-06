import matplotlib.pyplot as plt
import numpy as np
import os

Ni = ['Ni (100%)'],[13.41,14.75],[12.1,14.8]
Fe = ['Fe (>99.9%)'],[2.693,2.968],[0.807,0.893]
Ir = ['Ir (99.9%)'],[(2.77E3+163),(3.05E3+180)],[4.72E4,5.41E4]

metals = [Ni, Fe, Ir]
for data in metals:
    name = data[0][0]
    x = np.mean(data[1])
    y = np.mean(data[2])
    x_err = np.std(data[1])
    y_err = np.std(data[2])
    plt.errorbar(x, y, y_err, x_err, 'C0', ms = 4)
    if 'Ni' in name:
        plt.annotate(name, (x, y), textcoords="offset points", xytext=(0,10), ha='center', size = 17)
    elif 'Fe' in name:
        plt.annotate(name, (x, y), textcoords="offset points", xytext=(40,10), ha='center', size = 17)
    else:
        plt.annotate(name, (x, y), textcoords="offset points", xytext=(-50,-5), ha='center', size = 17)
    #plt.annotate(name, (x, y), textcoords="offset points", xytext=(0,5), ha='center', size = 17)
plt.yscale('log')
plt.xscale('log')
plt.ylabel(r'Price [USD kg$^{-1}$]', fontsize = 17)
plt.xlabel(r'CO$\mathdefault{_{2}}$  footprint [kg kg$^{-1}$]', fontsize = 17)
plt.xticks(fontsize = 17)
plt.yticks(fontsize = 17)
plt.minorticks_on()
#plt.show()

username = os.getlogin()
filepath = os.path.join(r'C:\Users', username, r'OneDrive\Master Thesis\3 Project plan\Lab\Plots\Draft', username, 'Price_vs_CO2') # for data in onedrive
plt.savefig(filepath, dpi = 300, bbox_inches='tight')
print('Plot saved!')
