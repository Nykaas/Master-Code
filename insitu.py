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

        # Efficiency lists
        eff_before = []
        eff_after = []

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
                ylabel = r'$\mathdefault{-Z_{imaginary}\ [Ω \ cm^2]}$'

            if sheet == 'Polarization':
                xs, ys = smooth(x, y)
                if switch:
                    plt.plot(xs, ys, color = colors[color_index], label = name)
                    switch = False
                else:
                    plt.plot(xs, ys, linestyle = '--', color = colors[color_index], label = name)
                    switch = True
                    color_index += 1
            
            elif sheet == 'Polarization_1h' or sheet == 'Polarization_end':
                xs, ys = smooth(x, y)
                plt.plot(xs, ys, label = name)

            elif sheet == 'Efficiency':
                # Data appending
                labels = ['NF', 'NiFe/NF', 'Ir/NF']                
                for k,j in enumerate(x):
                    if j >= 500:
                        if 'before' in name:
                            eff_before.append(round(100*(1.48/y[k]), 1))
                        else:
                            eff_after.append(round(100*(1.48/y[k]), 1))
                        break
                
                # Plotting
                if len(eff_after) == len(labels):
                    w = np.arange(len(labels))
                    width = 0.35

                    fig, ax = plt.subplots(figsize=(9,7))
                    rects1 = ax.bar(w - width/2, eff_before, width, label = 'Before', color = 'C7')
                    rects2 = ax.bar(w + width/2, eff_after, width, label='After', color = 'C3')

                    ylabel = 'Efficiency [%]'
                    xlabel = ''
                    plt.xticks(w, labels)

                    def autolabel(rects):
                        for rect in rects:
                            height = rect.get_height()
                            ax.annotate('{}'.format(height),
                                        xy=(rect.get_x() + rect.get_width() / 2, height),
                                        xytext=(0, 3),  # 3 points vertical offset
                                        textcoords="offset points",
                                        ha='center', va='bottom', fontsize = 20)


                    autolabel(rects1)
                    autolabel(rects2)

                    fig.tight_layout()
                    plt.ylim(0,99)

            elif sheet == 'Durability':
                if 'Ir' in name:
                    color1 = 'C2'
                    name = r'Ir/NF (1.0 A $\mathdefault{cm^{-2}}$)'
                elif 'Fe' in name:
                    color1 = 'C0'
                    name = r'NiFe/NF (0.5 A $\mathdefault{cm^{-2}}$)(temp)'
                else:
                    color1 = 'C0'
                    name = r'NF (0.5 A $\mathdefault{cm^{-2}}$)'
                xs, ys = smooth(x, y)
                plt.plot(xs/3600, ys, label = name, color=color1)
            
            elif sheet == 'EIS':
                if switch:
                    plt.plot(x, y, color = colors[color_index], label = name)
                    switch = False
                else:
                    plt.plot(x, y, linestyle = ':', color = colors[color_index], label = name)
                    switch = True
                    color_index += 1     
            else:
                if 'fit' in name:
                    plt.plot(x, y*-1, linestyle = '--', color = colors[color_index])
                    color_index += 1
                else:
                    plt.scatter(x, y, s = 8, label = name, color = colors[color_index])
        
        plot_settings(xlabel, ylabel, columns, sheet, excelfile, ECSA_norm)

def smooth(x, y):
    x = x[~np.isnan(x)]
    y = y[~np.isnan(y)]
    b, a = signal.butter(2, 0.01, analog=False)
    xs = signal.filtfilt(b, a, x)
    ys = signal.filtfilt(b, a, y)
    return xs, ys