import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from XY_data import process_xy_data

from plot import plot_settings

def in_situ_plot(df, excelfile, A_sample, ECSA_norm, smooth, trim, num_datapoints, symbols):
    colors = ['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6']
    for sheet in df: # Iterate sheet name as key in df dictionary
        print(f'--- {sheet} ---')
        columns = list(df[sheet].columns)
        switch = True
        color_index = 0
        symbols_idx = 0
        eff_start = []
        eff_after = []

        for i in range(1, len(columns), 3): # Iterate data columns
            x = np.array(df[sheet][columns[i]].tolist())
            y = np.array(df[sheet][columns[i+1]].tolist())
            name = columns[i+2]
            xlabel = df[sheet]['Graph_settings'][1]
            ylabel = df[sheet]['Graph_settings'][2]
            
            ### Sheet plotting ###
            if sheet == 'Polarization':
                if 'cm2' in xlabel:
                    x /= A_sample
                    print(f'X normalized: {sheet}, {name}, (A = {A_sample})')
                xlabel = r'Current density [mA $\mathdefault{cm^{-2}}$]'
                ylabel = 'Cell voltage [V]'
                x, y = process_xy_data(x, y, num_datapoints, smooth, trim)
                if switch:
                    plt.plot(x, y, color = colors[color_index], label = name, marker = symbols[symbols_idx])
                    switch = False
                else:
                    plt.plot(x, y, linestyle = '--', color = colors[color_index], label = name, marker = symbols[symbols_idx])
                    switch = True
                    color_index += 1
            
            elif sheet == 'Polarization_1h' or sheet == 'Polarization_end':
                if 'cm2' in xlabel:
                    x /= A_sample
                    print(f'X normalized: {sheet}, {name}, (A = {A_sample})')
                xlabel = r'Current density [mA $\mathdefault{cm^{-2}}$]'
                ylabel = 'Cell voltage [V]'
                x, y = process_xy_data(x, y, num_datapoints, smooth, trim)
                plt.plot(x, y, label = name, marker = symbols[symbols_idx])

            elif sheet == 'Efficiency':
                # Data appending
                labels = ['NF', 'NiFe/NF', 'Ir/NF']                
                for k,j in enumerate(x):
                    if j >= 500:
                        if 'before' in name:
                            eff_start.append(round(100*(1.48/y[k]), 1))
                        else:
                            eff_after.append(round(100*(1.48/y[k]), 1))
                        break
                # Plotting
                if len(eff_after) == len(labels):
                    w = np.arange(len(labels))
                    width = 0.35
                    fig, ax = plt.subplots(figsize=(9,7))
                    rects1 = ax.bar(w - width/2, eff_start, width, label = 'Before', color = 'C7')
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
                x, y = process_xy_data(x, y, num_datapoints, smooth, trim)
                if 'Ir' in name:
                    color1 = 'C2'
                    name = r'Ir/NF (1.0 A $\mathdefault{cm^{-2}}$)'
                elif 'Fe' in name:
                    color1 = 'C0'
                    name = r'NiFe/NF (0.5 A $\mathdefault{cm^{-2}}$)(temp)'
                else:
                    color1 = 'C0'
                    name = r'NF (0.5 A $\mathdefault{cm^{-2}}$)'
                plt.plot(x/3600, y, label = name, color=color1, marker = symbols[symbols_idx])
            
            if 'EIS' in sheet:
                if 'cm2' in xlabel:
                    x *= A_sample
                    print(f'X normalized: {sheet}, {name}, (A = {A_sample})')
                if 'cm2' in ylabel:
                    y *= A_sample
                    print(f'Y normalized: {sheet}, {name}, (A = {A_sample})')
                xlabel = r'$\mathdefault{Z_{real}\ [Ω \ cm^2]}$'
                ylabel = r'$\mathdefault{-Z_{imaginary}\ [Ω \ cm^2]}$'
                
            if sheet == 'EIS':
                if switch:
                    plt.plot(x, y, color = colors[color_index], label = name, marker = symbols[symbols_idx])
                    switch = False
                else:
                    plt.plot(x, y, linestyle = ':', color = colors[color_index], label = name, marker = symbols[symbols_idx])
                    switch = True
                    color_index += 1     
            
            elif sheet == 'EIS_1h' or sheet == 'EIS_end':
                if 'fit' in name:
                    plt.plot(x, y*-1, linestyle = '--', color = colors[color_index])
                    color_index += 1
                else:
                    plt.scatter(x, y, s = 8, label = name, color = colors[color_index], marker = symbols[symbols_idx])
            symbols_idx +=1
        plot_settings(xlabel, ylabel, columns, sheet, excelfile, ECSA_norm)
