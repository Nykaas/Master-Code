import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

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
                xdata = list(map(lambda x: x / A_sample, xdata))
                print(f'Current corrected: {sheet}, {name}, (A = {A_sample})')

            ### Sheet plotting ###
            if sheet == 'Polarization':
                if switch:
                    plt.plot(xdata, ydata, linestyle = '-', color = colors[color_index], label = name)
                    switch = False
                    color_index += 1
                else:
                    plt.plot(xdata, ydata, linestyle = '--', color = colors[color_index], label = name)
                    switch = True
                    color_index += 1
            elif sheet == 'Durability':
                plt.plot(xdata/3600, ydata, label = name)
            else:
                plt.plot(xdata, ydata, label = name)
        plot_settings(xlabel, ylabel, title, columns, sheet, excelfile)