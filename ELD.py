import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from plot import plot_settings
from plot import get_markersize
from xy_smooth import smooth_xy

def ELD_plot(df, excelfile, writer, smooth, markers):
    ECSA = get_ECSA(df)
    for sheet in df: # Iterate sheet name as key in df dictionary
        if sheet == 'ECSA-cap':
            continue
        print(f'--- {sheet} ---')
        columns = list(df[sheet].columns)
        markers_idx = 0
        xlabel = df[sheet]['Graph_settings'][1]
        ylabel = df[sheet]['Graph_settings'][2]
        bath_pH = 5
        offset_Ag = 0.197 + (0.0591 * bath_pH) # V
        print(f'AgCl to RHE offset = {offset_Ag:.2f} V at pH {bath_pH}')
        
        for i in range(1, len(columns), 3): # Iterate data columns
            #data = []
            x = np.array(df[sheet][columns[i]].tolist())
            y = np.array(df[sheet][columns[i+1]].tolist())
            if 'Plating' not in sheet:
                x, y = smooth_xy(x, y, smooth)
            name = columns[i+2]
            if 'pH' in sheet:
                bath_pH = df[sheet][name][0]
                offset_Ag = 0.197 + (0.0591 * bath_pH)
                print(f'AgCl to RHE offset = {offset_Ag:.2f} V at pH {bath_pH}')

            if 'GC' in sheet or 'Glassy carbon' in name: # Glassy carbon
                A_sample = 0.196 # cm^2
                print(f'Area GC = {A_sample}')
            
            elif 'NF' in name or 'Nickel felt' in name:
                A_sample = ECSA
                print(f'ECSA NF = {A_sample:.2f}')
           
            else:
                A_sample = 5 # cm^2
                print(f'Area {name} = {A_sample}')
            
            ### Plot ###
            if 'CXV' in sheet: # CV
                xlabel = r'E [V vs. RHE]'
                ylabel = r'Current density [mA $\mathdefault{cm^{-2}}$]'
                name = name.replace('C', r'$\degree$C')
                plt.plot(x + offset_Ag, y/A_sample, label = name, marker = markers[markers_idx], markevery = 0.1)

            elif 'CV' in sheet: # Evans diagram
                xlabel = r'log i [mA $\mathdefault{cm^{-2}}$]'
                ylabel = r'E [V vs. RHE]'
                if 'Temperature' in sheet:
                    name = name.replace('C', r'$\degree$C')
                plt.plot(np.log10(abs(y/A_sample)), x + offset_Ag, label = name, marker = markers[markers_idx], markevery = 0.1)

            elif 'OCP' in sheet: # Immersion potential monitoring
                xlabel = r'Time [min]'
                ylabel = r'E [V vs. RHE]'
                plt.plot(x/60, y + offset_Ag, label = name, marker = markers[markers_idx], markevery = 0.1)

            elif 'Plating' in sheet:
                xlabel = r'E [V vs. RHE]'
                ylabel = r'Current density [mA $\mathdefault{cm^{-2}}$]'
                name = name.replace('C', r'$\degree$C')
                plt.scatter(x + offset_Ag, y/A_sample, label = name, marker = markers[markers_idx], s = 8)
                #save_plating_data(x, y, data, writer, name, sheet, offset_Ag, A_sample)
            
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

def save_plating_data(x, y, data, writer, name, sheet, offset_Ag, A_sample):
    temp = {'Parameter': name, 'E, ELD [V]':round(x[0] + offset_Ag,2), 'i, ELD [mA cm-2]':round(y[0]/A_sample,2)}
    data.append(temp)
    df = pd.DataFrame(data, columns = ['Parameter', 'E, ELD [V]', 'i, ELD [mA cm-2]'])
    df.to_excel(writer, index = False, header=True, sheet_name='Plating_data')
    writer.save()