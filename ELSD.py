import matplotlib.pyplot as plt
#import pandas as pd
import numpy as np
#import math

from plot import plot_settings
from xy_smooth import smooth_xy

def ELSD_plot(df, excelfile, bath_pH, writer, smooth, markers):
    offset_Ag = 0.197 + (0.0591 * bath_pH) # V
    print(f'AgCl to RHE offset = {offset_Ag:.2f} V at pH {bath_pH}')
    ECSA = get_ECSA(df)
    for sheet in df: # Iterate sheet name as key in df dictionary
        if sheet == 'ECSA-cap':
            continue
        print(f'--- {sheet} ---')
        columns = list(df[sheet].columns)
        markers_idx = 0
        xlabel = df[sheet]['Graph_settings'][1]
        ylabel = df[sheet]['Graph_settings'][2]
        
        for i in range(1, len(columns), 3): # Iterate data columns
            x = np.array(df[sheet][columns[i]].tolist())
            y = np.array(df[sheet][columns[i+1]].tolist())
            x, y = smooth_xy(x, y, smooth)
            name = columns[i+2]

            if 'GC' in sheet or 'Glassy carbon' in name: # Glassy carbon
                A_sample = 0.196 # cm^2
                print(f'Area GC = {A_sample}')
            
            elif 'NF' in name or 'Nickel felt' in name:
                A_sample = ECSA
                print(f'ECSA NF = {A_sample:.2f}')
           
            else:
                A_sample = 15 # cm^2
                #A_sample = ECSA
                print(f'Area {name} = {A_sample}')
            
            ### Plot ###
            if 'CV' in sheet: # CV
                xlabel = r'E [V vs. RHE]'
                ylabel = r'Current density [mA $\mathdefault{cm^{-2}}$]'
                plt.plot(x + offset_Ag, y/A_sample, label = name, marker = markers[markers_idx], markevery = 0.1)

            elif 'OCV' in sheet: # Immersion potential monitoring
                xlabel = r'Time [s]'
                ylabel = r'E [V vs. RHE]'
                plt.plot(x, y + offset_Ag, label = name, marker = markers[markers_idx], markevery = 0.1)
            
            markers_idx += 1
        plot_settings(xlabel, ylabel, columns, sheet, excelfile, ECSA_norm=False)

def get_ECSA(df):
    columns = list(df['ECSA-cap'].columns)
    x = np.array(df['ECSA-cap'][columns[1]].tolist())
    y = np.array(df['ECSA-cap'][columns[2]].tolist())
    cdl, b = np.polyfit(x, y, 1) # cdl [F]
    c = 40e-6 # F/cm^2
    ECSA = cdl / c # ECSA [cm^2]
    return ECSA