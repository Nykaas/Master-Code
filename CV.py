import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import math
from xy_smooth import smooth_xy

from plot import plot_settings
from CE import get_current_efficiency

def ex_situ_plot(df, writer, offset_Hg, excelfile, ECSA_norm, smooth, markers):
    A_sample = 12.5 # cm^2
    capacitance_data = []
    eta_data = []
    CV_data = []
    EIS_data = []
    A_sample_RF = A_sample
    if ECSA_norm:
        reference = 'NF'
        ECSA_samples = get_ECSA(df)
    
    for sheet in df: # Iterate sheet name as key in df dictionary
        print(f'--- {sheet} ---')
        columns = list(df[sheet].columns)
        xlabel = df[sheet]['Graph_settings'][1]
        ylabel = df[sheet]['Graph_settings'][2]
        symbols_count = 0
        for i in range(1, len(columns), 3): # Iterate data columns
            x = np.array(df[sheet][columns[i]].tolist())
            y = np.array(df[sheet][columns[i+1]].tolist())
            name = columns[i+2]
            if ECSA_norm == 'Yes':
                A_sample = float(df[sheet][name][0])
            name_print = name
                    
            if 'A' in str(name): # Change to current density in label
                idx = name.find('-')
                current_density = (float(name[idx+1:idx+5])/A_sample) * 1000 # A to mA
                name = name.replace(name[idx+1:idx+5],  f'{current_density:.0f}')
                name = name.replace('A', r'mA $\mathdefault{cm^{-2}}$')
                print(f'{sheet} | {name_print} | A to mA legend')
            
            ### Sheet plotting ###
            if sheet == 'FullRange':
                xlabel = r'Potential [V, RHE]'
                ylabel = r'Current density [mA $\mathdefault{cm^{-2}}$]'
                if ECSA_norm:
                    A_sample = ECSA_samples[name]
                y /= A_sample
                print(f'{name_print} | I/{A_sample:.1f}[cm^2]')
                x, y = smooth_xy(x, y, smooth)
                plt.plot(x + offset_Hg, y, label = name, marker = markers[symbols_count], markevery = 0.1)
            
            elif sheet == 'ECSA-cap': # ECSA & RF capacitance method
                xlabel = r'Scan rate [mV $\mathdefault{s^{-1}}$]'
                ylabel = r'Charging current [mA $\mathdefault{cm^{-2}}$]'
                if ECSA_norm:
                    A_sample = ECSA_samples[name]
                y /= A_sample
                print(f'{name_print} | I/{A_sample:.1f}[cm^2]')
                cdl, b = get_ECSA_data(x, y, writer, columns, capacitance_data, name, A_sample_RF, name_print)
                plt.plot(x, (cdl*x + b) / A_sample, label = name)
                plt.scatter(x, y / A_sample, marker = markers[symbols_count])
            
            elif sheet == 'LSV':
                xlabel = r'Potential [V, RHE]'
                ylabel = r'Current density [mA $\mathdefault{cm^{-2}}$]'
                if ECSA_norm:
                    A_sample = ECSA_samples[name]
                y /= A_sample
                print(f'{name_print} | I/{A_sample:.1f}[cm^2]')
                x, y = smooth_xy(x, y, smooth)
                plt.plot(x + offset_Hg, y, label = name, marker = markers[symbols_count], markevery = 0.1)

            elif sheet == 'Tafel':
                xlabel = r'log i [mA $\mathdefault{cm^{-2}}$]'
                ylabel = r'Overpotential [V, RHE]'
                if ECSA_norm:
                    A_sample = ECSA_samples[name]
                y /= A_sample
                print(f'{name_print} | I/{A_sample:.1f}[cm^2]')
                x, y = smooth_xy(x, y, smooth)
                plt.plot(np.log10(y), x + offset_Hg - 1.23, label = name, marker = markers[symbols_count], markevery = 0.1)
                x = np.array(df[sheet][columns[i]].tolist())
                y = np.array(df[sheet][columns[i+1]].tolist())
                y /= A_sample
                save_overpotential(x, y, writer, offset_Hg, eta_data, name, name_print)

            elif sheet == '10to100':
                xlabel = r'Potential [V, RHE]'
                ylabel = r'Current density [mA $\mathdefault{cm^{-2}}$]'
                if ECSA_norm:
                    A_sample = ECSA_samples[reference]
                y /= A_sample
                print(f'{name_print} | I/{A_sample:.1f}[cm^2]')
                x, y = smooth_xy(x, y, smooth)
                name = name.replace('mV/s', r'mV $\mathdefault{s^{-1}}$')
                plt.plot(x, y, label = name, marker = markers[symbols_count], markevery = 0.1)
            
            elif sheet == 'Impedance':
                if ECSA_norm:
                    A_sample = ECSA_samples[reference]
                y *= A_sample *-1
                x *= A_sample
                print(f'{name_print} | I*{A_sample:.1f}[cm^2]')
                xlabel = r'$\mathdefault{Z_{real}\ [Ω \ cm^2]}$'
                ylabel = r'$\mathdefault{-Z_{imaginary}\ [Ω \ cm^2]}$'
                if 'fit' in name:
                    plt.plot(x, y)
                    save_EIS_data(x, EIS_data, writer, name)
                else:
                    plt.scatter(x, y, s = 8, label = name)

            symbols_count += 1

        plot_settings(xlabel, ylabel, columns, sheet, excelfile, ECSA_norm)

### Functions ###
def save_EIS_data(x, EIS_data, writer, name):
    temp = {'Sample': name.replace(r'A $\mathdefault{cm^{-2}}$', 'A cm-2'), 'R, sol [ohm cm2]':round(min(x),2), 'R, pol [ohm cm2]':round(max(x)-min(x) ,2)}
    EIS_data.append(temp)
    df = pd.DataFrame(EIS_data, columns = ['Sample', 'R, sol [ohm cm2]', 'R, pol [ohm cm2]'])
    df.to_excel(writer, index = False, header=True, sheet_name='EIS')
    writer.save()

def get_ECSA_data(x, y, writer, columns, capacitance_data, name, A_sample_RF, name_print):
    cdl, b = np.polyfit(x, y, 1) # cdl [F]
    c = 40e-6 # F/cm^2
    ECSA = cdl / c # ECSA [cm^2]
    # Save data
    capacitance_temp = {'Sample': name.replace(r'A $\mathdefault{cm^{-2}}$', 'A cm-2'), 'Cdl [F]':round(cdl,2), 'ECSA [cm2]':round(ECSA,2), 'RF':round(ECSA/A_sample_RF,2)}
    capacitance_data.append(capacitance_temp)
    ECSA_cap_df = pd.DataFrame(capacitance_data, columns = ['Sample', 'Cdl [F]', 'ECSA [cm2]', 'RF'])
    ECSA_cap_df.to_excel(writer, index = False, header=True, sheet_name='ECSA-cap')
    writer.save()
    return cdl, b

def get_ECSA(df):
    ECSA_samples = {}
    columns = list(df['ECSA-cap'].columns)
    for i in range(1, len(columns), 3): # Iterate data columns
        name = columns[i+2]
        x = np.array(df['ECSA-cap'][columns[i]].tolist())
        y = np.array(df['ECSA-cap'][columns[i+1]].tolist())
        cdl, b = np.polyfit(x, y, 1) # cdl [F]
        c = 40e-6 # F/cm^2
        ECSA = cdl / c # ECSA [cm^2]
        ECSA_samples[name] = ECSA
    return ECSA_samples

def save_overpotential(x, y, writer, offset_Hg, eta_data, name, name_print):
    for i, j in enumerate(y):
        if 10.1 >= round(j, 1) >= 10.0:
            break
    eta_temp = {'Sample': name.replace(r'A $\mathdefault{cm^{-2}}$', 'A cm-2'), 'Current density [mA cm-2]':round(y[i],2), 'Overpotential [mV]':round((x[i] + offset_Hg - 1.23)*1000,2), 'Max current density [mA cm-2]':round(y[-1],2)}
    eta_data.append(eta_temp)
    eta_df = pd.DataFrame(eta_data, columns = ['Sample','Current density [mA cm-2]', 'Overpotential [mV]', 'Max current density [mA cm-2]'])
    eta_df.to_excel(writer, index = False, header=True, sheet_name='Overpotential')
    writer.save()
