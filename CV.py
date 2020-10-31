import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

from plot import plot_settings

def ex_situ_plot(df, writer, A_sample, offset_Hg, excelfile):
    for sheet in df: # Iterate sheet name as key in df dictionary
        columns = list(df[sheet].columns)
        for i in range(1, len(columns), 3): # Iterate data columns
            xdata = np.array(df[sheet][columns[i]].tolist())
            ydata = np.array(df[sheet][columns[i+1]].tolist())
            if 'cm-2' in df[sheet]['Graph_settings'][2]: # Correct for sample area
                ydata = list(map(lambda y: y / A_sample, ydata))
                print(f'Current corrected: {sheet} {columns[i+2]} (A={A_sample})')
            if sheet == 'ECSA-alpha': # Calculating ECSA and RF by Alpha method
                save_alpha_data(xdata, ydata, A_sample, writer, offset_Hg)
            if sheet == 'ECSA-cap': # Linear regression for ECSA capacitance method & RF
                save_cap_data(xdata, ydata, A_sample, writer, columns, i)
            elif len(columns) == 3:
                plt.plot(xdata + offset_Hg, ydata)
            else:
                plt.plot(xdata + offset_Hg, ydata, label = columns[i+2])
        if len(columns) > 3:
            plt.legend()
        labels = df[sheet][columns[0]].tolist()
        plot_settings(labels, sheet, excelfile)

def save_alpha_data(xdata, ydata, A_sample, writer, offset_Hg):
    integral = 0
    for i in range(0, len(xdata)-1):
        temp = (ydata[i+1] + ydata[i]) * (xdata[i+1] + xdata[i] - offset_Hg*2)
        integral += temp
    charge = -1000 * (integral/100)              
    alpha_data = {'Charge, Q [µF]':[charge], 'ECSA [cm2]':[charge/514], 'RF':[charge/(514*A_sample)]}
    ECSA_alpha_df = pd.DataFrame(alpha_data, columns = ['Charge, Q [µF]', 'ECSA [cm2]', 'RF'])
    ECSA_alpha_df.to_excel(writer, index = False, header=True, sheet_name='ECSA-alpha')
    writer.save()

def save_cap_data(xdata, ydata, A_sample, writer, columns, i):
    c = 40 # uF/cm^2
    if 'mA' in columns[i+1]:
        ydata = list(map(lambda y: y*1000, ydata)) # mA to uA
        print(ydata)
    cdl, b = np.polyfit(xdata, ydata, 1)
    if len(columns) == 3:
        plt.plot(xdata, cdl*xdata + b)
    else:
        plt.plot(xdata, cdl*xdata + b,  label = columns[i+2])
    plt.scatter(xdata, ydata, marker = 'x')
    cdl, b = np.polyfit(xdata/1000, ydata, 1)
    capacitance_data = {'Double layer capacitance [µF]':[cdl], 'ECSA [cm2]':[cdl/c], 'RF':[cdl/(c*A_sample)]}
    ECSA_cap_df = pd.DataFrame(capacitance_data, columns = ['Double layer capacitance [µF]', 'ECSA [cm2]', 'RF'])
    ECSA_cap_df.to_excel(writer, index = False, header=True, sheet_name='ECSA-cap')
    writer.save()
