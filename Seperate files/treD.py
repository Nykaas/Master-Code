import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy import signal
import os
from mpl_toolkits.mplot3d import Axes3D

def treD_plot(df, excelfile, A_sample):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for sheet in df: # Iterate sheet name as key in df dictionary
        columns = list(df[sheet].columns)
        for i in range(1, len(columns), 3): # Iterate data columns
            x = np.array(df[sheet][columns[i]].tolist())
            y = np.array(df[sheet][columns[i+1]].tolist()) * 1000
            z = np.array(df[sheet][columns[i+2]].tolist())
            x = x[~np.isnan(x)]
            y = y[~np.isnan(y)]
            z = z[~np.isnan(z)]
            xlabel = df[sheet]['Graph_settings'][1]
            ylabel = df[sheet]['Graph_settings'][2]
            zlabel = df[sheet]['Graph_settings'][3]
            if 'cm2' in ylabel: # Correct for sample area
                y /= A_sample
                print(f'{sheet} | I/Area A={A_sample}')

            ### Plot ###
            ax.scatter(x, y, z)
        plt.grid()
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_zlabel(zlabel)
        username = os.getlogin()
        filepath = os.path.join(r'C:\Users', username, r'OneDrive\Specialization Project\3_Project plan\Lab\Plots\Draft', username, excelfile[:-5], sheet) # for data in onedrive
        plt.savefig(filepath, dpi = 300, bbox_inches='tight')
        plt.clf()

