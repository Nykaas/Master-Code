import numpy as np
from scipy import signal

def smooth_xy(x, y, smooth, excelfile, name, sheet):
    x = x[~np.isnan(x)]
    y = y[~np.isnan(y)]
    if smooth:
        if 'In_' in excelfile:
            if sheet == 'Durability':
                if name == 'NF':
                    freq = 0.001
                elif 'ED' in name:
                    freq = 0.0005
                elif 'ELD' in name:
                    freq = 0.0006
                else:
                    freq = 0.001
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
            if 'LSV' in sheet:
                if 'ELD' in name:
                    freq = 0.05
                else:
                    freq = 0.05
            elif 'Tafel' in sheet:
                if 'ELD' in name:
                    freq = 0.03
                elif 'ED' in name:
                    freq = 0.04
                else:
                    freq = 0.05
            elif 'Electrodeposition' in excelfile:
                freq = 0.01
            else:
                freq = 0.1
        elif 'ED_' or 'ELD_' in excelfile:
            if 'Electrolytes' in excelfile:
                if 'All' in sheet:
                    freq = 0.03
                else:
                    freq = 0.05
            else:
                freq = 0.01
        else:
            print('No smooth')
        b, a = signal.butter(4, freq, analog=False)
        x = signal.filtfilt(b, a, x)
        y = signal.filtfilt(b, a, y)
    return x, y