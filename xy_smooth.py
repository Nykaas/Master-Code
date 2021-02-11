import pandas as pd
import numpy as np
from scipy import signal
import math

def smooth_xy(x, y, smooth):
    x = x[~np.isnan(x)]
    y = y[~np.isnan(y)]
    if smooth:
        b, a = signal.butter(4, 0.05, analog=False)
        x = signal.filtfilt(b, a, x)
        y = signal.filtfilt(b, a, y)
    return x, y