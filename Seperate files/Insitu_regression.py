import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy import signal

def smooth(x, y):
    x = x[~np.isnan(x)]
    y = y[~np.isnan(y)]
    b, a = signal.butter(2, 0.01, analog=False)
    xs = signal.filtfilt(b, a, x)
    ys = signal.filtfilt(b, a, y)
    return xs, ys

colors = ['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6']


### Nickel felt ###

df = pd.read_excel('NF_Comparison.xlsx')
columns = list(df.columns)
x = np.array(df[columns[0]].tolist())
y = np.array(df[columns[2]].tolist())

temp = []
for i in range(0, len(x)):
    if x[i] > 1800:
        temp.append(x[i])
        
yfit = np.array([(1414.47 + 56.96*np.log(i)) for i in temp])
xfit = np.array(temp)

xs, ys = smooth(x, y)
xfit_s, yfit_s = smooth(xfit, yfit)
plt.plot(xs/3600, ys/1000, label = r'NF (0.5 A $\mathdefault{cm^{-2}}$)', color = colors[0])
plt.plot(xfit_s/3600, yfit_s/1000, '--', color = colors[0])

#########################################################

### Iridium ###

df = pd.read_excel('Ir_Comparison.xlsx')
columns = list(df.columns)
x = np.array(df[columns[0]].tolist())
y = np.array(df[columns[2]].tolist())

temp = []
for i in range(0, len(x)):
    if x[i] > 1800:
        temp.append(x[i]/3600)
        
yfit = np.array([(0.0098*i) + 1.853 for i in temp])
xfit = np.array(temp)

xs, ys = smooth(x, y)
xfit_s, yfit_s = smooth(xfit, yfit)
plt.plot(xs/3600, ys/1000, label = r'Ir/NF (1.0 A $\mathdefault{cm^{-2}}$)', color = colors[2])
plt.plot(xfit_s, yfit_s, '--', color = colors[2])

#########################################################


plt.legend(fontsize = 12)
plt.xlabel('Time [h]', fontsize = 12)
plt.ylabel('Cell voltage [V]', fontsize = 12)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
# plt.savefig('Insitu_regression.png' ,dpi = 300, bbox_inches='tight')
plt.show()