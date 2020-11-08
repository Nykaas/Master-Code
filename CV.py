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
            xdata = np.array(df[sheet][columns[i]].tolist())
            ydata = np.array(df[sheet][columns[i+1]].tolist())
            name = columns[i+2]
            xlabel = df[sheet]['Graph_settings'][1]
            ylabel = df[sheet]['Graph_settings'][2]
            if 'cm-2' in xlabel or 'cm-2' in ylabel: # Correct for sample area
                ydata = list(map(lambda y: y / A_sample, ydata))
                print(f'Current corrected: {sheet} {name} (A={A_sample})')
            
            ### Sheet plotting ###
            if sheet == 'FullRange' or sheet == 'LSV': # Plot without further calculation
                plt.plot(xdata + offset_Hg, ydata, label = name)
            elif sheet == 'ECSA-alpha': # ECSA & RF alpha method
                plt.plot(xdata, ydata, label = name)
                save_alpha_data(xdata, ydata, A_sample, writer, offset_Hg, name)
            elif sheet == 'ECSA-cap': # ECSA & RF capacitance method
                ydata, xdata, cdl, b = save_cap_data(xdata, ydata, A_sample, writer, columns, i, capacitance_data, name)
                plt.plot(xdata, cdl*xdata + b,  label = name)
                plt.scatter(xdata, ydata, marker = 'x')
            elif sheet == 'Tafel': # Plot tafel
                plt.plot(np.log10(ydata), xdata + offset_Hg - 1.23, label = name)
                save_overpotential(xdata, ydata, writer, offset_Hg, eta_data, name)

        plot_settings(xlabel, ylabel, columns, sheet, excelfile)

def save_alpha_data(xdata, ydata, A_sample, writer, offset_Hg, alpha_data, name):
    integral = 0
    for i in range(0, len(xdata)-1):
        temp = (ydata[i+1] + ydata[i]) * (xdata[i+1] + xdata[i] - offset_Hg*2)
        integral += temp
    charge = -1000 * (integral/100)              
    alpha_temp = {'Sample': name, 'Charge, Q [µF]':round(charge,2), 'ECSA [cm2]':round(charge/514,2), 'RF':round(charge/(514*A_sample),2)}
    alpha_data.append(alpha_temp)
    ECSA_alpha_df = pd.DataFrame(alpha_data, columns = ['Sample', 'Charge, Q [µF]', 'ECSA [cm2]', 'RF'])
    ECSA_alpha_df.to_excel(writer, index = False, header=True, sheet_name='ECSA-alpha')
    writer.save()

def save_cap_data(xdata, ydata, A_sample, writer, columns, i, capacitance_data, name):
    c = 40 # uF/cm^2
    if 'mA' in columns[i+1]:
        ydata = list(map(lambda y: y*1000, ydata)) # mA to uA
    cdl, b = np.polyfit(xdata/1000, ydata, 1)
    capacitance_temp = {'Sample': name, 'Double layer capacitance [µF]':round(cdl,2), 'ECSA [cm2]':round(cdl/c,2), 'ECSA [m2]':round(cdl/c,2)/(100**2), 'RF':round(cdl/(c*A_sample),2)}
    capacitance_data.append(capacitance_temp)
    ECSA_cap_df = pd.DataFrame(capacitance_data, columns = ['Sample', 'Double layer capacitance [µF]', 'ECSA [cm2]', 'ECSA [m2]', 'RF'])
    ECSA_cap_df.to_excel(writer, index = False, header=True, sheet_name='ECSA-cap')
    writer.save()
    cdl, b = np.polyfit(xdata, ydata, 1)
    return ydata, xdata, cdl, b


def save_overpotential(xdata, ydata, writer, offset_Hg, eta_data, name):
    for i,j in enumerate(ydata):
        if round(j, 1) == 10:
            break       
    eta_temp = {'Sample': name,'Current density [mA cm-2]':round(ydata[i],1), 'Overpotential [mV]':round((xdata[i] + offset_Hg - 1.23)*1000,2)}
    eta_data.append(eta_temp)
    eta_df = pd.DataFrame(eta_data, columns = ['Sample', 'Current density [mA cm-2]', 'Overpotential [mV]'])
    eta_df.to_excel(writer, index = False, header=True, sheet_name='Overpotential')
    writer.save()