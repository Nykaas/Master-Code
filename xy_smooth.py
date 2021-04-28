import pandas as pd
import numpy as np
from scipy import signal
import math

def smooth_xy(x, y, smooth, excelfile):
    x = x[~np.isnan(x)]
    y = y[~np.isnan(y)]
    if smooth:
        if 'In' in excelfile:
            freq = 0.01
        elif 'ED' in excelfile:
            freq = 0.05
        else:
            freq = 0.1
        b, a = signal.butter(4, freq, analog=False)
        x = signal.filtfilt(b, a, x)
        y = signal.filtfilt(b, a, y)
    return x, y