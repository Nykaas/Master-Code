import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from scipy import signal

from plot import plot_settings

def in_situ_plot(df, excelfile, A_sample):
    colors = ['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink']
    for sheet in df: # Iterate sheet name as key in df dictionary
        columns = list(df[sheet].columns)
        switch = True
        color_index = 0
        for i in range(1, len(columns), 3): # Iterate data columns
            xdata = np.array(df[sheet][columns[i]].tolist())
            ydata = np.array(df[sheet][columns[i+1]].tolist())
            name = columns[i+2]
            title = xlabel = df[sheet]['Graph_settings'][0]
            xlabel = df[sheet]['Graph_settings'][1]
            ylabel = df[sheet]['Graph_settings'][2]
            if 'cm2' in xlabel: # Correct for sample area
                xdata /= A_sample
                print(f'X normalized: {sheet}, {name}, (A = {A_sample})')
            if 'cm2' in ylabel: # Correct for sample area
                ydata /= A_sample
                print(f'Y normalized: {sheet}, {name}, (A = {A_sample})')
            
            ### Sheet plotting ###
            
            if sheet == 'Polarization':
                x_smooth, y_smooth = smooth(xdata, ydata)
                if switch:
                    plt.plot(x_smooth, y_smooth, color = colors[color_index], label = name)
                    switch = False
                else:
                    plt.plot(x_smooth, y_smooth, linestyle = ':', color = colors[color_index], label = name)
                    switch = True
                    color_index += 1
            
            elif sheet == 'Polarization_1h' or sheet == 'Polarization_end':
                x_smooth, y_smooth = smooth(xdata, ydata)
                plt.plot(xdata, ydata)
                plt.plot(x_smooth, y_smooth, label = name)
            
            elif sheet == 'Durability':
                x_smooth, y_smooth = smooth(xdata, ydata)
                plt.plot(xdata/3600, ydata) # s to h
                plt.plot(x_smooth/3600, y_smooth, label = name)
            
            else:
                plt.plot(xdata, ydata, label = name)
        
        plot_settings(xlabel, ylabel, title, columns, sheet, excelfile)

def smooth(xdata, ydata):
    xdata = xdata[~np.isnan(xdata)]
    ydata = ydata[~np.isnan(ydata)]
    b, a = signal.butter(2, 0.01, analog=False)
    x_smooth = signal.filtfilt(b, a, xdata)
    y_smooth = signal.filtfilt(b, a, ydata)
    return x_smooth, y_smooth