import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import math
from scipy import signal

from plot import plot_settings
from CE import get_current_efficiency

def ex_situ_plot(df, writer, A_sample, offset_Hg, excelfile):
    capacitance_data = []
    eta_data = []
    CE_data = []
    CV_data = []
    EIS_data = []
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
                if sheet == 'Impedance':
                    y *= A_sample *-1
                    x *= A_sample
                    print(f'{sheet} | {name_print} | I*Area A = {A_sample}')
                else:
                    y /= A_sample
                    print(f'{sheet} | {name_print} | I/Area A = {A_sample}')
            
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
                xs, ys = smooth(x, y)
                #plt.plot(x + offset_Hg, y, label = name) #check alignment
                plt.plot(xs + offset_Hg, ys, label = name)
                set_annotations(xs, ys, offset_Hg, name, writer, CV_data)
                m_1 = (df[sheet][name][0])
                m_2 = (df[sheet][name][1])
                I = (df[sheet][name][2])
                t = (df[sheet][name][3])
                if math.isnan(m_1) == False:
                    m_t, m_a, CE, loading = get_current_efficiency(m_1, m_2, I, t)
                    save_CE_data(m_t, m_a, CE, loading, CE_data, writer, name, name_print)
            
            elif sheet == 'ECSA-cap': # ECSA & RF capacitance method
                xlabel = r'Scan rate [mV $\mathdefault{s^{-1}}$]'
                ylabel = r'Charging current [mA $\mathdefault{cm^{-2}}$]'
                cdl, b = get_ECSA_data(x, y, writer, columns, capacitance_data, name, A_sample, name_print)
                plt.plot(x, (cdl*x + b) / A_sample, label = name)
                print(f'{sheet} | {name_print} | I/Area A = {A_sample}')
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

            elif sheet == '10to100':
                xlabel = r'Potential [V, RHE]'
                ylabel = r'Current density [mA $\mathdefault{cm^{-2}}$]'
                name = name.replace('mV/s', r'mV $\mathdefault{s^{-1}}$')
                plt.plot(x, y, label = name)
            
            elif sheet == 'Impedance':
                xlabel = r'$\mathdefault{Z_{real}\ [Ω \ cm^2]}$'
                ylabel = r'$\mathdefault{-Z_{imaginary}\ [Ω \ cm^2]}$'
                if 'fit' in name:
                    plt.plot(x, y, linestyle = '--')
                    save_EIS_data(x, EIS_data, writer, name)
                else:
                    plt.scatter(x, y, s = 8, label = name)

            else:
                plt.plot(x, y, label = name)

        plot_settings(xlabel, ylabel, columns, sheet, excelfile)

### Functions ###
def save_EIS_data(x, EIS_data, writer, name):
    temp = {'Sample': name.replace(r'A $\mathdefault{cm^{-2}}$', 'A cm-2'), 'R, sol [ohm cm2]':round(min(x),2), 'R, pol [ohm cm2]':round(max(x)-min(x) ,2)}
    EIS_data.append(temp)
    df = pd.DataFrame(EIS_data, columns = ['Sample', 'R, sol [ohm cm2]', 'R, pol [ohm cm2]'])
    df.to_excel(writer, index = False, header=True, sheet_name='EIS')
    writer.save()

def save_CE_data(m_t, m_a, CE, loading, CE_data, writer, name, name_print):
    CE_temp = {'Sample': name.replace(r'A $\mathdefault{cm^{-2}}$', 'A cm-2'), 'm_t [g]':round(m_t,2), 'm_a [g]':round(m_a,2), 'CE [%]':round(CE,2), 'Loading [mg/cm2]':round(loading,2)}
    CE_data.append(CE_temp)
    ECSA_cap_df = pd.DataFrame(CE_data, columns = ['Sample', 'm_t [g]', 'm_a [g]', 'CE [%]', 'Loading [mg/cm2]'])
    ECSA_cap_df.to_excel(writer, index = False, header=True, sheet_name='CE')
    writer.save()

def get_ECSA_data(x, y, writer, columns, capacitance_data, name, A_sample, name_print):
    # Calculations
    cdl, b = np.polyfit(x, y, 1) # cdl [F]
    c = 40e-6 # F/cm^2
    ecsa = cdl / c # ecsa [cm^2]
    # Save data
    capacitance_temp = {'Sample': name.replace(r'A $\mathdefault{cm^{-2}}$', 'A cm-2'), 'Cdl [F]':round(cdl,2), 'ECSA [cm2]':round(ecsa,2), 'RF':round(ecsa/A_sample,2)}
    capacitance_data.append(capacitance_temp)
    ECSA_cap_df = pd.DataFrame(capacitance_data, columns = ['Sample', 'Cdl [F]', 'ECSA [cm2]', 'RF'])
    ECSA_cap_df.to_excel(writer, index = False, header=True, sheet_name='ECSA-cap')
    writer.save()
    return cdl, b

def save_overpotential(x, y, writer, offset_Hg, eta_data, name, name_print):
    for i, j in enumerate(y):
        if round(j, 1) == 10:
            break
    eta_temp = {'Sample': name.replace(r'A $\mathdefault{cm^{-2}}$', 'A cm-2'), 'Current density [mA cm-2]':round(y[i],2), 'Overpotential [mV]':round((x[i] + offset_Hg - 1.23)*1000,2)}
    eta_data.append(eta_temp)
    eta_df = pd.DataFrame(eta_data, columns = ['Sample','Current density [mA cm-2]', 'Overpotential [mV]'])
    eta_df.to_excel(writer, index = False, header=True, sheet_name='Overpotential')
    writer.save()

def set_annotations(x, y, offset_Hg, name, writer, CV_data):
    # Oxidation
    idx = np.argmax(y)
    text = f'{y[idx]:.1f}' + r' mA $\mathdefault{cm^{-2}}$'
    E_ox = round(x[idx], 2) + offset_Hg
    i_ox = round(y[idx], 1)
    if 'NiFe' not in name: # Offset to prevent text collision
        pos = y[idx]-1
    else:
        pos = y[idx]
    plt.annotate(
        text,
        xy=(x[idx] + offset_Hg, y[idx]),
        xytext=(1.1, pos),
        arrowprops=dict(facecolor='black', arrowstyle='simple'),
    )
    
    # Reduction
    idx = np.argmin(y[50:-100])
    x_ = x[50:-50]
    y_ = y[50:-50]
    text = f'{y_[idx]:.1f}' + r' mA $\mathdefault{cm^{-2}}$'
    E_red = round(x_[idx], 2) + offset_Hg
    i_red = round(y_[idx], 1)
    plt.annotate(
        text,
        xy=(x_[idx] + offset_Hg, y_[idx]),
        xytext=(1.25, y_[idx]),
        arrowprops=dict(facecolor='black', arrowstyle='simple')
    )

    CV_temp = {'Sample': name.replace(r'A $\mathdefault{cm^{-2}}$', 'A cm-2'), 'E, Ox [V]':E_ox, r'i, Ox [mA cm-2]':i_ox, 'E, Red [V]':E_red, r'i, Red [mA cm-2]':i_red}
    CV_data.append(CV_temp)
    CV_df = pd.DataFrame(CV_data, columns = ['Sample', 'E, Ox [V]', r'i, Ox [mA cm-2]', 'E, Red [V]', r'i, Red [mA cm-2]'])
    CV_df.to_excel(writer, index = False, header=True, sheet_name='CV')
    writer.save()

def smooth(x, y):
    x = x[~np.isnan(x)]
    y = y[~np.isnan(y)]
    b, a = signal.butter(2, 0.03, analog=False)
    xs = signal.filtfilt(b, a, x)
    ys = signal.filtfilt(b, a, y)
    return xs, ys
