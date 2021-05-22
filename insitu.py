import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from xy_smooth import smooth_xy

from plot import plot_settings
from plot import get_markersize
from plot import get_markerinterval

def in_situ_plot(df, writer, excelfile, smooth, markers, ECSA_norm, In_situ_correction):
    A_sample = 6.25 # cm^2
    colors = ['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6']
    for sheet in df: # Iterate sheet name as key in df dictionary
        print(f'--- {sheet} ---')
        columns = list(df[sheet].columns)
        switch = True
        color_index = 0
        markers_idx = 0
        eff_start = []
        eff_after = []
        data = []

        for i in range(1, len(columns), 3): # Iterate data columns
            x = np.array(df[sheet][columns[i]].tolist())
            y = np.array(df[sheet][columns[i+1]].tolist())
            name = columns[i+2]
            xlabel = df[sheet]['Graph_settings'][1]
            ylabel = df[sheet]['Graph_settings'][2]

            if In_situ_correction and 'EIS' not in sheet:
                R = 6.25 * df[sheet][name][0]
                print(f'Cell voltage corrected for ohmic resistance : {int(1000*R)} [mohm cm2]')

            if 'NiFeED/NF' in name:
                name = name.replace('NiFeED/NF', str(r'NiFe$\mathdefault{_{ED}}$/NF'))
            
            if 'NiFeELD/NF' in name:
                name = name.replace('NiFeELD/NF', str(r'NiFe$\mathdefault{_{ELD}}$/NF'))
            
            ### Sheet plotting ###
            if sheet == 'Polarization':
                y /= A_sample
                print(f'{name} | I/{A_sample:.2f}[cm^2]')
                ylabel = r'$i$ [mA $\mathdefault{cm^{-2}}$]'
                xlabel = r'$\mathit{E_{cell}}$ [V]'
                x, y = smooth_xy(x, y, smooth, excelfile, name, sheet)
                if In_situ_correction:
                    x -= (y/1000)*R
                if switch:
                    plt.plot(x, y, color = colors[color_index], label = name, marker = markers[markers_idx], markevery = get_markerinterval(x), markersize = get_markersize())
                    switch = False
                else:
                    plt.plot(x, y, linestyle = 'dashed', color = colors[color_index], label = name, marker = markers[markers_idx], markevery = get_markerinterval(x), markersize = get_markersize())
                    switch = True
                    color_index += 1
            
            elif sheet == 'Polarization_1h' or sheet == 'Polarization_end' or sheet == 'Polarization_end_full':
                y /= A_sample
                print(f'{name} | I/{A_sample:.2f}[cm^2]')
                ylabel = r'$i$ [mA $\mathdefault{cm^{-2}}$]'
                xlabel = r'$\mathit{E_{cell}}$ [V]'
                x, y = smooth_xy(x, y, smooth, excelfile, name, sheet)
                if In_situ_correction:
                    x -= (y/1000)*R
                plt.plot(x, y, label = name, marker = markers[markers_idx], markevery = get_markerinterval(x), markersize = get_markersize())
                save_Pol_data(y, data, writer, name, sheet)
                if In_situ_correction:
                    if sheet == 'Polarization_1h':
                        plt.xlim(1.5, 1.85)
                    else:
                        plt.xlim(1.3, 1.8)
                else:
                    plt.xlim(1.55, 1.95)

            elif 'Durability' in sheet:
                xlabel = r'$t$ [h]'
                ylabel = r'$\mathit{E_{cell}}$ [V]'
                if In_situ_correction:
                    y -= 3.125*R
                if 'fit' in name:
                    plt.scatter(x/3600, y, s = get_markersize(), marker = '_')
                else:
                    x, y = smooth_xy(x, y, smooth, excelfile, name, sheet)
                    plt.plot(x/3600, y, label = name, marker = markers[markers_idx], markevery = get_markerinterval(x), markersize = get_markersize())
                
            elif sheet == 'EIS':
                x *= A_sample
                y *= A_sample *-1
                print(f'{name} | Ω*{A_sample:.2f}[cm^2]')
                xlabel = r'$\mathdefault{Z_{real}\ [Ω \ cm^2]}$'
                ylabel = r'$\mathdefault{-Z_{imag}\ [Ω \ cm^2]}$'
                if switch:
                    plt.scatter(x, y, color = colors[color_index], label = name, marker = markers[markers_idx])
                    switch = False
                else:
                    plt.plot(x, y, linestyle = 'dashed', color = colors[color_index], label = name, marker = markers[markers_idx])
                    switch = True
                    color_index += 1
                plt.xlim(0, 0.8)
                plt.ylim(0, 0.8)     
            
            elif sheet == 'EIS_1h' or sheet == 'EIS_end':
                x *= A_sample
                y *= A_sample *-1
                print(f'{name} | Ω*{A_sample:.2f}[cm^2]')
                xlabel = r'$\mathdefault{Z_{real}\ [Ω \ cm^2]}$'
                ylabel = r'$\mathdefault{-Z_{imag}\ [Ω \ cm^2]}$'
                if 'fit' in name:
                    plt.plot(x, y, linestyle = 'dashed', label = name.split()[0], marker = markers[markers_idx], markevery = get_markerinterval(x), markersize = get_markersize())
                    save_EIS_data(x, data, writer, name, sheet)
                    color_index += 1
                #else:
                #    plt.scatter(x, y, s = get_markersize()*5, label = name, marker = markers[markers_idx])                    
                if sheet == 'EIS_1h':
                    plt.xlim(0, 0.3)
                    plt.ylim(0, 0.3)
                else:
                    plt.xlim(0, 0.8)
                    plt.ylim(0, 0.8)

            elif sheet == 'Efficiency':
                # Data appending
                labels = ['NF', 'Ir/NF', r'NiFe$\mathdefault{_{ED}}$/NF', r'NiFe$\mathdefault{_{ELD}}$/NF'] # add 'NiFe/NF ELD' when available
                print(f'{name} | I/{A_sample:.2f}[cm^2]')              
                for k,j in enumerate(y):
                    if j/A_sample >= 500:
                        if 'before' in name:
                            eff_start.append(round(100*(1.48/x[k]), 1))
                        else:
                            eff_after.append(round(100*(1.48/x[k]), 1))
                        break
                # Plotting
                if len(eff_after) == len(labels):
                    w = np.arange(len(labels))
                    width = 0.35
                    fig, ax = plt.subplots(figsize=(9,7))
                    rects1 = ax.bar(w - width/2, eff_start, width, label = 'Pre', color = 'C7')
                    rects2 = ax.bar(w + width/2, eff_after, width, label= 'Post', color = 'C3')
                    ylabel = 'Efficiency [%]'
                    xlabel = ''
                    plt.xticks(w, labels, fontsize = 27)
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
                    plt.ylim(0,100)

            markers_idx +=1
        plot_settings(xlabel, ylabel, columns, sheet, excelfile, ECSA_norm, In_situ_correction)

### Functions ###
def save_EIS_data(x, data, writer, name, sheet):
    R_sol = round(min(x),2)
    R_pol = round(max(x)-min(x),2)
    temp = {'Sample': name, 'R, sol [ohm cm2]':R_sol, 'R, pol [ohm cm2]':R_pol}
    data.append(temp)
    df = pd.DataFrame(data, columns = ['Sample', 'R, sol [ohm cm2]', 'R, pol [ohm cm2]'])
    df.to_excel(writer, index = False, header=True, sheet_name=sheet)
    writer.save()

def save_Pol_data(y, data, writer, name, sheet):
    temp = {'Sample': name, 'Max current [mA/cm2]':round(max(y))}
    data.append(temp)
    df = pd.DataFrame(data, columns = ['Sample', 'Max current [mA/cm2]'])
    df.to_excel(writer, index = False, header=True, sheet_name=sheet)
    writer.save() 