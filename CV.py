import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

from plot import plot_settings

def ex_situ_plot(df, writer, A_sample, offset_Hg, excelfile):
    capacitance_data = []
    alpha_data = []
    eta_data = []
    for sheet in df: # Iterate sheet name as key in df dictionary
        columns = list(df[sheet].columns)
        for i in range(1, len(columns), 3): # Iterate data columns
            x = np.array(df[sheet][columns[i]].tolist())
            y = np.array(df[sheet][columns[i+1]].tolist())
            name = columns[i+2]
            title = df[sheet]['Graph_settings'][0]
            xlabel = df[sheet]['Graph_settings'][1]
            ylabel = df[sheet]['Graph_settings'][2]
            if 'cm2' in xlabel or 'cm2' in ylabel: # Correct for sample area
                y /= A_sample
                print(f'Current corrected: {sheet} {name} (A={A_sample})')
            
            #if 'A' in name: # Change to current density in label, not working at the moment
            #    idx = name.find('A')
            #    print(name, idx)
            #    name = name[0:idx-4] + str(round(idx/A_sample, 2)) + r' A$\mathdefault{cm^{-2}}$' + name[idx+1:]
                
            
            ### Sheet plotting ###
            if sheet == 'FullRange' or sheet == 'LSV': # Plot without further calculation
                plt.plot(x + offset_Hg, y, label = name)
            elif sheet == 'ECSA-alpha': # ECSA & RF alpha method
                plt.plot(x, y, label = name)
                save_alpha_data(x, y, A_sample, writer, offset_Hg, alpha_data, name)
            elif sheet == 'ECSA-cap': # ECSA & RF capacitance method
                y, x, cdl, b = save_cap_data(x, y, A_sample, writer, columns, i, capacitance_data, name)
                plt.plot(x, cdl*x + b,  label = name)
                plt.scatter(x, y, marker = 'x')
            elif sheet == 'Tafel': # Plot tafel
                plt.plot(np.log10(y), x + offset_Hg - 1.23, label = name)
                save_overpotential(x, y, writer, offset_Hg, eta_data, name)

        plot_settings(xlabel, ylabel, title, columns, sheet, excelfile)

def save_alpha_data(x, y, A_sample, writer, offset_Hg, alpha_data, name):
    integral = 0
    for i in range(0, len(x)-1):
        temp = (y[i+1] + y[i]) * (x[i+1] + x[i] - offset_Hg*2)
        integral += temp
    charge = -1000 * (integral/100)              
    alpha_temp = {'Sample': name, 'Charge, Q [µF]':round(charge,2), 'ECSA [cm2]':round(charge/514,2), 'RF':round(charge/(514*A_sample),2)}
    alpha_data.append(alpha_temp)
    ECSA_alpha_df = pd.DataFrame(alpha_data, columns = ['Sample', 'Charge, Q [µF]', 'ECSA [cm2]', 'RF'])
    ECSA_alpha_df.to_excel(writer, index = False, header=True, sheet_name='ECSA-alpha')
    writer.save()

def save_cap_data(x, y, A_sample, writer, columns, i, capacitance_data, name):
    c = 40 # uF/cm^2
    if 'mA' in columns[i+1]:
        y *= 1000 # mA to uA
        print(f'mA to uA for {name}')
    cdl, b = np.polyfit(x/1000, y, 1)
    capacitance_temp = {'Sample': name, 'Double layer capacitance [µF]':round(cdl,2), 'ECSA [cm2]':round(cdl/c,2), 'ECSA [m2]':round(cdl/c,2)/(100**2), 'RF':round(cdl/(c*A_sample),2)}
    capacitance_data.append(capacitance_temp)
    ECSA_cap_df = pd.DataFrame(capacitance_data, columns = ['Sample', 'Double layer capacitance [µF]', 'ECSA [cm2]', 'ECSA [m2]', 'RF'])
    ECSA_cap_df.to_excel(writer, index = False, header=True, sheet_name='ECSA-cap')
    writer.save()
    cdl, b = np.polyfit(x, y, 1)
    return y, x, cdl, b


def save_overpotential(x, y, writer, offset_Hg, eta_data, name):
    for i, j in enumerate(y):
        if round(j, 1) == 10:
            break
    eta_temp = {'Sample': name,'Current density [mA cm-2]':y[i], 'Overpotential [mV]':round((x[i] + offset_Hg - 1.23)*1000,2)}
    eta_data.append(eta_temp)
    eta_df = pd.DataFrame(eta_data, columns = ['Sample', 'Current density [mA cm-2]', 'Overpotential [mV]'])
    eta_df.to_excel(writer, index = False, header=True, sheet_name='Overpotential')
    writer.save()
