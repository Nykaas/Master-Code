import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from scipy import signal

from plot import plot_settings

def in_situ_plot(df, excelfile, A_sample):
    colors = ['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6']
    for sheet in df: # Iterate sheet name as key in df dictionary
        columns = list(df[sheet].columns)
        switch = True
        color_index = 0
        for i in range(1, len(columns), 3): # Iterate data columns
            x = np.array(df[sheet][columns[i]].tolist())
            y = np.array(df[sheet][columns[i+1]].tolist())
            name = columns[i+2]
            xlabel = df[sheet]['Graph_settings'][1]
            ylabel = df[sheet]['Graph_settings'][2]
            if 'cm2' in xlabel: # Correct for sample area
                if 'EIS' in sheet:
                    x *= A_sample
                else:
                    x /= A_sample
                print(f'X normalized: {sheet}, {name}, (A = {A_sample})')
            if 'cm2' in ylabel: # Correct for sample area
                if 'EIS' in sheet:
                    y *= A_sample
                else:
                    y /= A_sample
                print(f'Y normalized: {sheet}, {name}, (A = {A_sample})')
            
            ### Sheet plotting ###
            
            if "Pol" in sheet:
                xlabel = r'Current density [mA $\mathdefault{cm^{-2}}$]'
                ylabel = 'Cell voltage [V]'
            elif "EIS" in sheet:
                xlabel = r'$\mathdefault{Z_{real}\ [Ω \ cm^2]}$'
                ylabel = r'$\mathdefault{Z_{imaginary}\ [Ω \ cm^2]}$'

            if sheet == 'Polarization':
                xs, ys = smooth(x, y)
                if switch:
                    plt.plot(xs, ys, color = colors[color_index], label = name)
                    switch = False
                else:
                    plt.plot(xs, ys, linestyle = ':', color = colors[color_index], label = name)
                    switch = True
                    color_index += 1
            
            elif sheet == 'Polarization_1h' or sheet == 'Polarization_end':
                xs, ys = smooth(x, y)
                plt.plot(xs, ys, label = name)
            
            elif sheet == 'Durability':
                if 'iridium' in name:
                    name = r'NF iridium (1 A $\mathdefault{cm^{-2}}$)'
                elif 'iron' in name:
                    name = r'NF nickel iron (0.5 A $\mathdefault{cm^{-2}}$)(temp)'
                else:
                    name = r'NF (0.5 A $\mathdefault{cm^{-2}}$)'
                xs, ys = smooth(x, y)
                plt.plot(xs/3600, ys, label = name)
            
            elif sheet == 'EIS':
                if switch:
                    plt.plot(x, y, color = colors[color_index], label = name)
                    switch = False
                else:
                    plt.plot(x, y, linestyle = ':', color = colors[color_index], label = name)
                    switch = True
                    color_index += 1     
            else:
                plt.plot(x, y, linewidth = 0.2, markersize = 4, marker = 'o', label = name)
        
        plot_settings(xlabel, ylabel, columns, sheet, excelfile)

def smooth(x, y):
    x = x[~np.isnan(x)]
    y = y[~np.isnan(y)]
    b, a = signal.butter(2, 0.01, analog=False)
    xs = signal.filtfilt(b, a, x)
    ys = signal.filtfilt(b, a, y)
    return xs, ys