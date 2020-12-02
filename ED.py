import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy import signal

from plot import plot_settings

def ED_plot(df, excelfile, A_sample, offset_Ag, writer):
    data = []
    for sheet in df: # Iterate sheet name as key in df dictionary
        columns = list(df[sheet].columns)
        for i in range(1, len(columns), 3): # Iterate data columns
            x = np.array(df[sheet][columns[i]].tolist())
            y = np.array(df[sheet][columns[i+1]].tolist())
            xs, ys = smooth(x, y)
            name = columns[i+2]
            current = df[sheet][name][0]
            xlabel = df[sheet]['Graph_settings'][1]
            ylabel = df[sheet]['Graph_settings'][2]
            save_ED(current, A_sample, data, name, writer)
            
            if 'A' in name: # Change to current density in label
                idx = name.find('-')
                current_density = (float(name[idx+1:idx+5])/A_sample) * 1000 # A to mA
                name = name.replace(name[idx+1:idx+5],  f'{current_density:.0f}')
                name = name.replace('A', r'mA $\mathdefault{cm^{-2}}$')

            ### Plot ###
            #plt.plot(x, y + offset_Ag, '--', label = columns[i+2]) # To check if smoothnes align
            plt.plot(xs, ys + offset_Ag, color = 'C1', label = name)

        plot_settings(xlabel, ylabel, columns, sheet, excelfile)

def smooth(x, y):
    x = x[~np.isnan(x)]
    y = y[~np.isnan(y)]
    b, a = signal.butter(4, 0.01, analog=False)
    xs = signal.filtfilt(b, a, x)
    ys = signal.filtfilt(b, a, y)
    return xs, ys

def save_ED(current, A_sample, data, name, writer):  
    data_temp = {'Sample': name, 'Area [cm-2]': A_sample, 'Current [A]': current, 'Current density [A cm-2]': current/A_sample}
    data.append(data_temp)
    eta_df = pd.DataFrame(data, columns = ['Sample', 'Area [cm-2]', 'Current [A]', 'Current density [A cm-2]'])
    eta_df.to_excel(writer, index = False, header=True, sheet_name='Current')
    writer.save()
