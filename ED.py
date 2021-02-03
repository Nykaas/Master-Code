import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy import signal
import math

from plot import plot_settings
from CE import get_current_efficiency

def ED_plot(df, excelfile, A_sample, offset_Ag, writer, ECSA_norm):
    CE_data = []
    for sheet in df: # Iterate sheet name as key in df dictionary
        columns = list(df[sheet].columns)
        for i in range(1, len(columns), 3): # Iterate data columns
            x = np.array(df[sheet][columns[i]].tolist())
            y = np.array(df[sheet][columns[i+1]].tolist())
            xs, ys = smooth(x, y)
            name = columns[i+2]
            xlabel = df[sheet]['Graph_settings'][1]
            ylabel = df[sheet]['Graph_settings'][2]
            
            if 'A' in name: # Change to current density in label
                idx = name.find('-')
                current_density = (float(name[idx+1:idx+5])/A_sample) * 1000 # A to mA
                name = name.replace(name[idx+1:idx+5],  f'{current_density:.0f}')
                name = name.replace('A', r'mA $\mathdefault{cm^{-2}}$')
            m_1 = (df[sheet][name][0])
            m_2 = (df[sheet][name][1])
            I = (df[sheet][name][2])
            t = (df[sheet][name][3])
            if math.isnan(m_1) == False:
                m_t, m_a, CE, loading = get_current_efficiency(m_1, m_2, I, t)
                save_CE_data(m_t, m_a, CE, loading, CE_data, writer, name, I, t)
            
            ### Plot ###
            #plt.plot(x/60, y + offset_Ag, '--', label = columns[i+2]) # To check if smoothnes align
            plt.plot(xs/60, ys + offset_Ag, color = 'C1', label = name)

        plot_settings(xlabel, ylabel, columns, sheet, excelfile, ECSA_norm)

def smooth(x, y):
    x = x[~np.isnan(x)]
    y = y[~np.isnan(y)]
    b, a = signal.butter(4, 0.01, analog=False)
    xs = signal.filtfilt(b, a, x)
    ys = signal.filtfilt(b, a, y)
    return xs, ys

def save_CE_data(m_t, m_a, CE, loading, CE_data, writer, name, I, t):
    CE_temp = {'Sample': name.replace(r'A $\mathdefault{cm^{-2}}$', 'A cm-2'), 'Current [A]': I, 'Time [s]': t, 'm_t [g]':round(m_t,2), 'm_a [g]':round(m_a,2), 'CE [%]':round(CE,2), 'Loading [mg/cm2]':round(loading,2)}
    CE_data.append(CE_temp)
    ECSA_cap_df = pd.DataFrame(CE_data, columns = ['Sample', 'Current [A]', 'Time [s]', 'm_t [g]', 'm_a [g]', 'CE [%]', 'Loading [mg/cm2]'])
    ECSA_cap_df.to_excel(writer, index = False, header=True, sheet_name='CE')
    writer.save()
