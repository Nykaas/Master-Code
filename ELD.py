import matplotlib.pyplot as plt
import numpy as np

from plot import plot_settings
from plot import get_markersize
from xy_smooth import smooth_xy
from plot import get_markerinterval

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

        if 'OCP' in sheet or 'NiFe' in sheet:
            bath_pH = df[sheet]['Graph_settings'][3]
        else:
            bath_pH = 5
            
        offset_Ag = 0.197 + (0.0591 * bath_pH) # V
        print(f'AgCl to RHE offset = {offset_Ag:.2f} V at pH {bath_pH}')
        
        for i in range(1, len(columns), 3): # Iterate data columns
            x = np.array(df[sheet][columns[i]].tolist())
            y = np.array(df[sheet][columns[i+1]].tolist())
            if 'Plating' not in sheet:
                name = columns[i+2]
                x, y = smooth_xy(x, y, smooth, excelfile, name, sheet)

            if 'pH' in sheet and 'Plating' not in sheet:
                bath_pH = df[sheet][name][0]
                offset_Ag = 0.197 + (0.0591 * bath_pH)
                print(f'AgCl to RHE offset = {offset_Ag:.2f} V at pH {bath_pH}')

            if 'RDE' in sheet or 'RDE' in name: # RDE
                A_sample = 0.196 # cm^2
                print(f'Area RDE = {A_sample}')
            
            elif 'NF' in name or 'Nickel felt' in name:
                A_sample = ECSA
                print(f'ECSA NF = {A_sample:.2f}')
           
            else:
                A_sample = 5 # cm^2
                print(f'Area {name} = {A_sample}')
            
            ### Plot ###
            if 'LSV' in sheet: # Evans diagram
                xlabel = r'log $i$ [mA $\mathdefault{cm^{-2}}$]'
                ylabel = r'$E$ [$\mathdefault{V_{RHE}}$]'
                plt.plot(np.log10(abs(y/A_sample)), x + offset_Ag, label = name, marker = markers[markers_idx], markevery = get_markerinterval(x), markersize = get_markersize())

            elif 'OCP' in sheet: # Potential transient
                xlabel = r'$t$ [min]'
                ylabel = r'$E$ [$\mathdefault{V_{RHE}}$]'
                plt.plot(x/60, y + offset_Ag, label = name, marker = markers[markers_idx], markevery = get_markerinterval(x), markersize = get_markersize())

            elif 'Plating' in sheet:
                if 'Temperature' in sheet:
                    xlabel = r'$T$ [K]'
                elif 'pH' in sheet:
                    xlabel = 'pH'
                    offset_Ag = 0
                else:
                    xlabel = r'Concentration [M]'

                if 'Ipl' in sheet:
                    ylabel = r'$i$ [mA $\mathdefault{cm^{-2}}$]'
                    plt.plot(x, y/A_sample, label = name, marker = markers[markers_idx], markersize = get_markersize())
                else:
                    ylabel = r'$E$ [$\mathdefault{V_{RHE}}$]'
                    plt.plot(x, y + offset_Ag, label = name, marker = markers[markers_idx], markersize = get_markersize())
            
            markers_idx += 1
        plot_settings(xlabel, ylabel, columns, sheet, excelfile, ax = None, ECSA_norm=False, In_situ_correction=False)

def get_ECSA(df):
    columns = list(df['ECSA-cap'].columns)
    x = np.array(df['ECSA-cap'][columns[1]].tolist())
    y = np.array(df['ECSA-cap'][columns[2]].tolist())
    cdl, b = np.polyfit(x, y, 1) # cdl [F]
    c = 40e-6 # F/cm^2
    ECSA = cdl / c # ECSA [cm^2]
    return ECSA