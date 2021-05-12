import pandas as pd
import numpy as np
from scipy import signal
import math

def smooth_xy(x, y, smooth, excelfile, name, sheet):
    x = x[~np.isnan(x)]
    y = y[~np.isnan(y)]
    if smooth:
        if 'In' in excelfile:
            if 'ED' in name and 'end' in sheet:
                freq = 0.0003
            elif 'ED' in name and 'Durability' in sheet:
                freq = 0.02
            else:
                freq = 0.02
        elif 'ED' or 'ELD' in excelfile:
            freq = 0.01
        elif 'Electrodeposition' in excelfile:
            freq = 0.01
        else:
            freq = 0.1
        b, a = signal.butter(4, freq, analog=False)
        x = signal.filtfilt(b, a, x)
        y = signal.filtfilt(b, a, y)
    return x, y