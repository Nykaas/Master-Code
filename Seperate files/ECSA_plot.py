import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

A_sample = 15

df = pd.read_excel('Ex_Best_Sample.xlsx')
columns = list(df.columns)

x1 = np.array(df[columns[1]].tolist())
y1 = np.array(df[columns[2]].tolist())

x2 = np.array(df[columns[4]].tolist())
y2 = np.array(df[columns[5]].tolist())

cdl1, b1 = np.polyfit(x1, y1*1000, 1)
cdl2, b2 = np.polyfit(x2, y2*1000, 1)

fig, ax1 = plt.subplots()

color = 'C0'
ax1.set_xlabel(r'Scan rate [mV $\mathdefault{s^{-1}}$]', fontsize = 12)
ax1.set_ylabel(r'Charging current [μA $\mathdefault{cm^{-2}}$]', color=color, fontsize = 12)
ax1.plot(x1, (cdl1*x1 + b1) / A_sample, color=color, label = 'NF')
ax1.scatter(x1, (y1*1000) / A_sample, marker = 'x', color=color)
ax1.tick_params(axis='y', labelcolor=color)
ax1.set_ylim(-0.01*1000,0.1*1000)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'C1'
ax2.set_ylabel(r'Charging current [μA $\mathdefault{cm^{-2}}$]', color=color, fontsize = 12)  # we already handled the x-label with ax1
ax2.plot(x2, (cdl2*x2 + b2) / A_sample, color=color, label = 'NiFe/NF')
ax2.scatter(x2, (y2*1000) / A_sample, marker = 'x', color=color)
ax2.tick_params(axis='y', labelcolor=color)
ax2.set_ylim(-0.2*1000,2.5*1000)

fig.legend(loc='upper left', bbox_to_anchor=(0.12, 0.92), fontsize = 12)
# ax2.legend()
fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
# plt.savefig('ECSA-cap.png' ,dpi = 300, bbox_inches='tight')
plt.show()