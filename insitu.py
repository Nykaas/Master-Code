import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from scipy.signal import savgol_filter

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
            #if 'cm2' in xlabel: # Correct for sample area
            #    xdata = list(map(lambda x: x / A_sample, xdata))
                #print(f'Current corrected: {sheet}, {name}, (A = {A_sample})')
            #Add for ylabel
            
            ### Sheet plotting ###
            if sheet == 'Polarization':
                if switch:
                    plt.plot(xdata, y_smooth, linestyle = '-', color = colors[color_index], label = name)
                    switch = False
                    color_index += 1
                else:
                    plt.plot(xdata, y_smooth, linestyle = '--', color = colors[color_index], label = name)
                    switch = True
                    color_index += 1
            elif sheet == 'Polarization_1h' or sheet == 'Sheet1':
                if len(xdata) % 2 == 0:
                    x_smooth, y_smooth = smooth(xdata, ydata)
                    #x_smooth = savgol_filter(xdata, len(xdata)-1, 3)
                    #y_smooth = savgol_filter(ydata, len(ydata)-1, 3)
                else:
                    x_smooth = savgol_filter(xdata, len(xdata)-1, 3)
                    y_smooth = savgol_filter(ydata, len(ydata)-1, 3)
                print(sheet, name)
                print(xdata[0:10])
                print(x_smooth[0:10])
                plt.plot(xdata, ydata, label = name)
                plt.plot(x_smooth, y_smooth, '-.', label = name)
            elif sheet == 'Durability':
                plt.plot(xdata/3600, ydata, label = name)
            else:
                plt.plot(xdata, ydata, label = name)
        plot_settings(xlabel, ylabel, title, columns, sheet, excelfile)

def smooth(xdata, ydata):
    if len(xdata) % 2 == 0:
        x_smooth = savgol_filter(xdata, len(xdata)-1, 3)
        y_smooth = savgol_filter(ydata, len(ydata)-1, 3)
    else:
        x_smooth = savgol_filter(xdata, len(xdata)-1, 3)
        y_smooth = savgol_filter(ydata, len(ydata)-1, 3)
    return x_smooth, y_smooth