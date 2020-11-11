import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

from plot import plot_settings

def in_situ_plot(df, excelfile):
    print('Doing insitu stuff!')
    for sheet in df: # Iterate sheet name as key in df dictionary
        print(sheet)
        columns = list(df[sheet].columns)
        for i in range(1, len(columns), 3): # Iterate data columns
            xdata = np.array(df[sheet][columns[i]].tolist())
            ydata = np.array(df[sheet][columns[i+1]].tolist())
            name = columns[i+2]
            xlabel = df[sheet]['Graph_settings'][1]
            ylabel = df[sheet]['Graph_settings'][2]
            
            ### Sheet plotting ###
            #if sheet == 'Polarization' or sheet == 'EIS' or sheet == 'Durability': # Plot without further calculation
            plt.plot(xdata, ydata, label = name)

        plot_settings(xlabel, ylabel, columns, sheet, excelfile)