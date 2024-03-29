import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from xy_smooth import smooth_xy

from plot import plot_settings
from plot import get_markersize
from plot import get_markerinterval

def in_situ_plot(df, writer, excelfile, smooth, markers, ECSA_norm, In_situ_correction):
    A_sample = 6.25 # cm^2
    colors = ['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6']
    ECSA_norm = False
    for sheet in df: # Iterate sheet name as key in df dictionary
        print(f'--- {sheet} ---')
        columns = list(df[sheet].columns)
        switch = True
        color_index = 0
        markers_idx = 0
        data = []
        fig, ax = plt.subplots()

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
                xlabel = r'$E_{\mathdefault{cell}}$ [V]'
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
            
            elif sheet == 'Polarization_1h' or sheet == 'Polarization_end':
                y /= A_sample
                print(f'{name} | I/{A_sample:.2f}[cm^2]')
                ylabel = r'$i$ [mA $\mathdefault{cm^{-2}}$]'
                xlabel = r'$E_{\mathdefault{cell}}$ [V]'
                if In_situ_correction:
                    x -= (y/1000)*R
                save_Pol_data(x, y, data, writer, name, sheet)
                x, y = smooth_xy(x, y, smooth, excelfile, name, sheet)
                plt.plot(x, y, label = name, marker = markers[markers_idx], markevery = get_markerinterval(x), markersize = get_markersize())

            elif 'Durability' in sheet:
                xlabel = r'$t$ [h]'
                ylabel = r'$E_{\mathdefault{cell}}$ [V]'
                if In_situ_correction:
                    y -= 3.125*R
                
                x /= 3600
                x = x[~np.isnan(x)]
                y = y[~np.isnan(y)]
                a, b = np.polyfit(x, y, 1)
                a, b = save_reg_durability(a, b, name, sheet, data, writer)
                x, y = smooth_xy(x, y, smooth, excelfile, name, sheet)
                ax.plot(x, a*x + b, color=colors[color_index], linestyle='dashed')
                ax.plot(x, y, label = name, marker = markers[markers_idx], markevery = get_markerinterval(x), markersize = get_markersize())
                color_index += 1
                
                #annotate(a, b, y, name)

            elif sheet == 'EIS':
                x *= A_sample * 1000
                y *= A_sample *-1000
                print(f'{name} | Ω*{A_sample:.2f}[cm^2]')
                xlabel = r'$Z_{\mathdefault{real}}\ [\mathdefault{mΩ \ cm^2]}$'
                ylabel = r'$-Z_{\mathdefault{imag}}\ [\mathdefault{mΩ \ cm^2]}$'
                if switch:
                    plt.scatter(x, y, color = colors[color_index], label = name, marker = markers[markers_idx])
                    switch = False
                else:
                    plt.plot(x, y, linestyle = 'dashed', color = colors[color_index], label = name, marker = markers[markers_idx])
                    switch = True
                    color_index += 1     
            
            elif 'EIS_1h' in sheet or 'EIS_end' in sheet:
                x *= A_sample
                y *= A_sample *-1
                print(f'{name} | Ω*{A_sample:.2f}[cm^2]')
                xlabel = r'$Z_{\mathdefault{real}}\ [\mathdefault{mΩ \ cm^2]}$'
                ylabel = r'$-Z_{\mathdefault{imag}}\ [\mathdefault{mΩ \ cm^2]}$'
                if 'fit' in name:
                    plt.plot(x*1000, y*1000, linestyle = 'dashed', color = colors[color_index])
                    save_EIS_data(x, data, writer, name, sheet)
                    color_index += 1
                else:
                    plt.scatter(x*1000, y*1000, s = get_markersize()**2, label = name, marker = markers[markers_idx], color = colors[color_index])

            markers_idx +=1
        plot_settings(xlabel, ylabel, columns, sheet, excelfile, ECSA_norm, In_situ_correction, ax)

### Functions ###
def save_EIS_data(x, data, writer, name, sheet):
    R_sol = round(min(x),2)
    R_pol = round(max(x)-min(x),2)
    temp = {'Sample': name, 'R, sol [ohm cm2]':R_sol, 'R, pol [ohm cm2]':R_pol}
    data.append(temp)
    df = pd.DataFrame(data, columns = ['Sample', 'R, sol [ohm cm2]', 'R, pol [ohm cm2]'])
    df.to_excel(writer, index = False, header=True, sheet_name=sheet)
    writer.save()

def save_Pol_data(x, y, data, writer, name, sheet):
    temp = {'Sample': name, 'Max current [mA/cm2]':round(max(y)), 'Cell voltage [V]': round(x[np.where(y==max(y))][0],2)}
    data.append(temp)
    df = pd.DataFrame(data, columns = ['Sample', 'Max current [mA/cm2]', 'Cell voltage [V]'])
    df.to_excel(writer, index = False, header=True, sheet_name=sheet)
    writer.save()

def save_reg_durability(a, b, name, sheet, data, writer):
    temp = {'Sample' : name, 'a [mV]': a*1000, 'b [V]': b}
    data.append(temp)
    df = pd.DataFrame(data, columns = ['Sample', 'a [mV]', 'b [V]'])
    df.to_excel(writer, index = False, header=True, sheet_name=sheet)
    writer.save()
    return a, b

def annotate(a, b, y, name):
    mid = int(len(y) / 2)
    text = f'{a*1000:.2f}' + r' mV$\mathdefault{h^{-1}}$' + f'{b:.2f} V'
    plt.annotate(
        text,
        xy=(3, y[mid]), # 3 h , half y len
        xytext=(0.2, y[mid]), # text pos
        arrowprops=dict(facecolor='black', arrowstyle='simple'),
        fontsize=14
    )