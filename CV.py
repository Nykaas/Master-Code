import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

from plot import plot_settings

def ex_situ_plot(df, writer, A_sample, offset_Hg, excelfile):
    capacitance_data = []
    eta_data = []
    for sheet in df: # Iterate sheet name as key in df dictionary
        columns = list(df[sheet].columns)
        for i in range(1, len(columns), 3): # Iterate data columns
            x = np.array(df[sheet][columns[i]].tolist())
            y = np.array(df[sheet][columns[i+1]].tolist())
            name = columns[i+2]
            name_print = name
            xlabel = df[sheet]['Graph_settings'][1]
            ylabel = df[sheet]['Graph_settings'][2]
            
            if 'cm2' in xlabel or 'cm2' in ylabel and sheet != 'ECSA-cap': # Correct for sample area
                y /= A_sample
                print(f'{sheet} | {name_print} | I/Area A={A_sample}')
            
            if 'A' in name: # Change to current density in label
                idx = name.find('-')
                current_density = float(name[idx+1:idx+4])/A_sample
                name = name.replace(name[idx+1:idx+4],  f'{current_density:.2f}')
                name = name.replace('A', r'A $\mathdefault{cm^{-2}}$')

            ### Sheet plotting ###
            if sheet == 'FullRange':
                xlabel = r'Potential [V, RHE]'
                ylabel = r'Current density [mA $\mathdefault{cm^{-2}}$]'
                plt.plot(x + offset_Hg, y, label = name)
            
            elif sheet == 'ECSA-cap': # ECSA & RF capacitance method
                if 'mA' in columns[i+1]:
                    y *= 1000
                    print(f'{sheet} | {name_print} | mA to uA')
                xlabel = r'Scan rate [mV $\mathdefault{s^{-1}}$]'
                ylabel = r'Charging current [μA $\mathdefault{cm^{-2}}$]'
                cdl, b = get_ECSA_data(x, y, writer, columns, capacitance_data, name, A_sample, name_print)
                plt.plot(x, (cdl*x + b) / A_sample, label = name)
                plt.scatter(x, y / A_sample, marker = 'x')
            
            elif sheet == 'LSV':
                xlabel = r'Potential [V, RHE]'
                ylabel = r'Current density [mA $\mathdefault{cm^{-2}}$]'
                plt.plot(x + offset_Hg, y, label = name)

            elif sheet == 'Tafel':
                xlabel = r'log i [mA $\mathdefault{cm^{-2}}$]'
                ylabel = r'Overpotential [V, RHE]'
                plt.plot(np.log10(y), x + offset_Hg - 1.23, label = name)
                save_overpotential(x, y, writer, offset_Hg, eta_data, name, name_print)

        plot_settings(xlabel, ylabel, columns, sheet, excelfile)

### Functions ###
def get_ECSA_data(x, y, writer, columns, capacitance_data, name, A_sample, name_print):
    c = 40 # uF/cm^2
    cdl, b = np.polyfit(x/1000, y, 1)
    capacitance_temp = {'Sample': name.replace(r'A $\mathdefault{cm^{-2}}$', 'A cm-2'), 'Samplee': name_print,'Double layer capacitance [µF]':round(cdl,2), 'ECSA [cm2]':round(cdl/c,2), 'ECSA [m2]':round(cdl/c,2)/(100**2), 'RF':round(cdl/(c*A_sample),2)}
    capacitance_data.append(capacitance_temp)
    ECSA_cap_df = pd.DataFrame(capacitance_data, columns = ['Sample', 'Samplee', 'Double layer capacitance [µF]', 'ECSA [cm2]', 'ECSA [m2]', 'RF'])
    ECSA_cap_df.to_excel(writer, index = False, header=True, sheet_name='ECSA-cap')
    writer.save()
    cdl, b = np.polyfit(x, y, 1)
    return cdl, b

def save_overpotential(x, y, writer, offset_Hg, eta_data, name, name_print):
    for i, j in enumerate(y):
        if round(j, 1) == 10:
            break
    eta_temp = {'Sample': name.replace(r'A $\mathdefault{cm^{-2}}$', 'A cm-2'), 'Samplee': name_print ,'Current density [mA cm-2]':round(y[i],2), 'Overpotential [mV]':round((x[i] + offset_Hg - 1.23)*1000,2)}
    eta_data.append(eta_temp)
    eta_df = pd.DataFrame(eta_data, columns = ['Sample', 'Samplee' ,'Current density [mA cm-2]', 'Overpotential [mV]'])
    eta_df.to_excel(writer, index = False, header=True, sheet_name='Overpotential')
    writer.save()
