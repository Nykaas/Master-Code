import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy import signal
import math

Rs = 0.4 # ohm
Rp = 1 # ohm
dE = 0.25 # V
C = 40 # mF/cm^2
time = np.linspace(1,30000,300)
y = []

for t in time:
    I = (dE/(Rs+Rp)) * (1 + ((Rs/Rp)*math.exp((-Rs-Rp)/(Rs*Rp*C))*t))
    y.append(I)
plt.plot(time, y)
plt.show()