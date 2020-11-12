import matplotlib.pyplot as plt
from scipy import interpolate
import numpy as np
from scipy.signal import savgol_filter


x = [604.41, 602.51, 616.81, 601.55, 592.97]
y = [1.46, 1.46, 1.46, 1.46, 1.46]
ynew = savgol_filter(y, 5, 3) # window size 51, polynomial order 3

plt.plot(x,y,'o',x,ynew,'-')
plt.show()
