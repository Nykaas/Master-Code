import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math

from plot import plot_settings
from CE import get_current_efficiency
from xy_smooth import smooth_xy

def ED_plot(df, excelfile, A_sample, bath_pH, writer, smooth, markers):
    offset_Ag = 0.197 + (0.0591 * bath_pH) # V
    print(f'AgCl to RHE offset = {offset_Ag:.2f} V at pH {bath_pH}')
    CE_data = []
    for sheet in df: # Iterate sheet name as key in df dictionary
        print(f'--- {sheet} ---')
        columns = list(df[sheet].columns)
        markers_idx = 0
        for i in range(1, len(columns), 3): # Iterate data columns
            x = np.array(df[sheet][columns[i]].tolist())
            y = np.array(df[sheet][columns[i+1]].tolist())
            x, y = smooth_xy(x, y, smooth)
            name = columns[i+2]
            xlabel = df[sheet]['Graph_settings'][1]
            ylabel = df[sheet]['Graph_settings'][2]
            CE_toggle = df[sheet]['Graph_settings'][3]
            
            if 'A' in name: # Change to current density in label
                idx = name.find('-')
                current_density = (float(name[idx+1:idx+5])/A_sample) * 1000 # A to mA
                name = name.replace(name[idx+1:idx+5],  f'{current_density:.0f}')
                name = name.replace('A', r'mA $\mathdefault{cm^{-2}}$')
                print('Label: Current density')

            if 'V' in name: # Correct Ag/Cl offset in label
                idx = name.find('V')
                E = round(float(name[idx-4:idx-1]) + offset_Ag, 2)
                name = name.replace(name[idx-4:idx-1], str(E))
                name += ' RHE'
                print(f'Label: AgCl offset {name}')
            
            if CE_toggle == 'CE': # Current efficiency
                m_t, m_a, CE, loading, I, t = get_current_efficiency(df, sheet, name)
                save_CE_data(m_t, m_a, CE, loading, CE_data, writer, name, I, t)
            
            ### Plot ###
            if 'IE' in sheet: # CV
                xlabel = r'E [V vs. RHE]'
                ylabel = r'Current density [mA $\mathdefault{cm^{-2}}$]'
                plt.plot(x + offset_Ag, y/A_sample, label = name, marker = markers[markers_idx], markevery = 0.1)

            elif 'It' in sheet: # Constant potential
                xlabel = r'Time [s]'
                ylabel = r'Current density [mA $\mathdefault{cm^{-2}}$]'
                plt.plot(x, y/A_sample, label = name, marker = markers[markers_idx], markevery = 0.1)
            
            elif 'Et' in sheet: # Constant current
                xlabel = r'Time [s]'
                ylabel = r'E [V vs. RHE]'
                plt.plot(x, y + offset_Ag, label = name, marker = markers[markers_idx], markevery = 0.1)

            elif 'EI' in sheet: # CV switch axis
                ylabel = r'E [V vs. RHE]'
                xlabel = r'Current density [mA $\mathdefault{cm^{-2}}$]'
                plt.plot(x/A_sample, y + offset_Ag, label = name, marker = markers[markers_idx], markevery = 0.1)
            
            markers_idx += 1
        plot_settings(xlabel, ylabel, columns, sheet, excelfile, ECSA_norm=False)

def save_CE_data(m_t, m_a, CE, loading, CE_data, writer, name, I, t):
    CE_temp = {'Sample': name.replace(r'A $\mathdefault{cm^{-2}}$', 'A cm-2'), 'Current [A]': I, 'Time [s]': t, 'm_t [g]':round(m_t,2), 'm_a [g]':round(m_a,2), 'CE [%]':round(CE,2), 'Loading [mg/cm2]':round(loading,2)}
    CE_data.append(CE_temp)
    CE_df = pd.DataFrame(CE_data, columns = ['Sample', 'Current [A]', 'Time [s]', 'm_t [g]', 'm_a [g]', 'CE [%]', 'Loading [mg/cm2]'])
    CE_df.to_excel(writer, index = False, header=True, sheet_name='CE')
    writer.save()
