import pandas as pd
import numpy as np
from scipy import signal
import math

def process_xy_data(x, y, num_datapoints, smooth, trim):
    x = x[~np.isnan(x)]
    y = y[~np.isnan(y)]
    
    if smooth:
        b, a = signal.butter(6, 0.2, analog=False)
        x = signal.filtfilt(b, a, x)
        y = signal.filtfilt(b, a, y)
    
    if trim:
        array_size = np.round(np.linspace(0, len(x) - 1, num_datapoints)).astype(int)
        x_ = np.array([])
        y_ = np.array([])
        for i in array_size:
            x_ = np.append(x_, x[i])
            y_ = np.append(y_, y[i])
        x, y = x_, y_
    
    return x, y