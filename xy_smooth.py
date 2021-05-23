import pandas as pd
import numpy as np
from scipy import signal
import math

def smooth_xy(x, y, smooth, excelfile, name, sheet):
    x = x[~np.isnan(x)]
    y = y[~np.isnan(y)]
    if smooth:
        if 'In_' in excelfile:
            if sheet == 'Durability':
                if name == 'NF':
                    freq = 0.0015
                else:
                    freq = 0.005
            elif sheet == 'Polarization_1h':
                if 'ED' in name or 'ELD' in name:
                    freq = 0.001
                elif name == 'NF':
                    freq = 0.003
                elif name == 'Ir/NF':
                    freq = 0.005
            elif sheet == 'Polarization_end':
                if name == 'Ir/NF':
                    freq = 0.005
                else:
                    freq = 0.0005

        elif 'Ex_' in excelfile:
            if 'Electrodeposition' in excelfile:
                freq = 0.01
            else:
                freq = 0.1
        elif 'ED' or 'ELD' in excelfile:
            freq = 0.01
        else:
            print('No smooth')
        b, a = signal.butter(4, freq, analog=False)
        x = signal.filtfilt(b, a, x)
        y = signal.filtfilt(b, a, y)
    return x, y