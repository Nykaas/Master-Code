import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from xy_smooth import smooth_xy

from plot import plot_settings
from plot import get_markersize
from plot import get_markerinterval

def ex_situ_plot(df, writer, offset_Hg, excelfile, ECSA_norm, smooth, markers, In_situ_correction):
    A_sample = 12.5 # cm^2
    A_sample_RF = A_sample
    colors = ['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6']
    if 'Electrodeposition' in excelfile or 'Electroless' in excelfile:
        ECSA_norm = False
    if ECSA_norm:
        ECSA_samples = get_ECSA(df)
    
    for sheet in df: # Iterate sheet name as key in df dictionary
        print(f'--- {sheet} ---')
        columns = list(df[sheet].columns)
        symbols_count = 0
        color_index = 0
        data = []
        switch = True
        fig, ax = plt.subplots()

        for i in range(1, len(columns), 3): # Iterate data columns
            x = np.array(df[sheet][columns[i]].tolist())
            y = np.array(df[sheet][columns[i+1]].tolist())
            name = columns[i+2]
            name_print = name
            
            ### Sheet plotting ###
            if 'FullRange' in sheet:
                xlabel = r'$E$ [$\mathdefault{V_{RHE}}$]'
                ylabel = r'$i$ [mA $\mathdefault{cm^{-2}}$]'
                if ECSA_norm:
                    A_sample = ECSA_samples[name]
                y /= A_sample
                print(f'{name_print} | I/{A_sample:.1f}[cm^2]')
                x, y = smooth_xy(x, y, smooth, excelfile, name, sheet)
                plt.plot(x + offset_Hg, y, label = get_label(name), marker = markers[symbols_count], markevery = get_markerinterval(x), markersize = get_markersize())
            
            elif 'ECSA-cap' in sheet: # ECSA & RF capacitance method
                xlabel = r'$v$ [mV $\mathdefault{s^{-1}}$]'
                ylabel = r'$\mathit{I_c}$ [mA]'
                print(f'{name_print} | No normalizing')
                x = x[~np.isnan(x)]
                y = y[~np.isnan(y)]
                cdl, b = get_ECSA_data(x, y, writer, columns, data, name, A_sample_RF, name_print)
                plt.plot(x, (cdl*x + b), label = get_label(name))
                plt.scatter(x, y, marker = markers[symbols_count])
            
            elif 'LSV' in sheet:
                xlabel = r'$E$ [$\mathdefault{V_{RHE}}$]'
                ylabel = r'$i$ [mA $\mathdefault{cm^{-2}}$]'
                if ECSA_norm:
                    A_sample = ECSA_samples[name]
                y_op = y/A_sample_RF
                y /= A_sample
                print(f'{name_print} | I/{A_sample:.1f}[cm^2]')
                save_overpotential(x, y_op, writer, offset_Hg, data, name, sheet)
                x, y = smooth_xy(x, y, smooth, excelfile, name, sheet)
                plt.plot(x + offset_Hg, y, label = get_label(name), marker = markers[symbols_count], markevery = get_markerinterval(x), markersize = get_markersize())

            elif 'Tafel' in sheet:
                xlabel = r'log $i$ [mA $\mathdefault{cm^{-2}}$]'
                ylabel = r'$\eta$ [$\mathdefault{V_{RHE}}$]'
                if ECSA_norm:
                    A_sample = ECSA_samples[name]
                y /= A_sample
                print(f'{name_print} | I/{A_sample:.1f}[cm^2]')
                x, y = smooth_xy(x, y, smooth, excelfile, name, sheet)
                plt.plot(np.log10(abs(y)), x + offset_Hg - 1.23, label = get_label(name), marker = markers[symbols_count], markevery = get_markerinterval(x), markersize = get_markersize())

            elif '10to100' in sheet:
                xlabel = r'$E$ [$\mathdefault{V_{RHE}}$]'
                ylabel = r'$i$ [μA $\mathdefault{cm^{-2}}$]'
                if ECSA_norm:
                    name_10 = df[sheet]['Graph_settings'][3] # Cell A5 in excel 10-100 sheet
                    A_sample = ECSA_samples[name_10]
                y /= A_sample
                print(f'{name_print} | I/{A_sample:.1f}[cm^2]')
                plt.plot(x + offset_Hg, y*1000, label = get_label(name), marker = markers[symbols_count], markevery = get_markerinterval(x), markersize = get_markersize())
            
            elif 'Stability' in sheet:
                xlabel = r'$E$ [$\mathdefault{V_{RHE}}$]'
                ylabel = r'$i$ [μA $\mathdefault{cm^{-2}}$]'
                if 'NF' in sheet:
                    spec_color = colors[0]
                elif 'ED' in sheet:
                    spec_color = colors[1]
                elif 'ELD' in sheet:
                    spec_color = colors[2]
                else:
                    spec_color = colors[color_index+1]
                if ECSA_norm:
                    name_10 = df[sheet]['Graph_settings'][3] # Cell A5 in excel 10-100 sheet
                    A_sample = ECSA_samples[name_10]
                y /= A_sample
                print(f'{name_print} | I/{A_sample:.1f}[cm^2]')
                if switch:
                    ax.plot(x + offset_Hg, y*1000, color = spec_color, label = get_label(name), marker = markers[symbols_count], markevery = get_markerinterval(x), markersize = get_markersize())
                    switch = False
                else:
                    ax.plot(x + offset_Hg, y*1000, linestyle = 'dashed', color = spec_color, label = get_label(name), marker = markers[symbols_count], markevery = get_markerinterval(x), markersize = get_markersize())
                    switch = True
                    color_index += 1

            elif sheet == 'Impedance':
                if ECSA_norm and 'fit' not in name:
                    A_sample = ECSA_samples[name]
                y *= A_sample *-1
                x *= A_sample
                xlabel = r'$\mathdefault{Z_{real}\ [Ω \ cm^2]}$'
                ylabel = r'$\mathdefault{-Z_{imag}\ [Ω \ cm^2]}$'
                if 'fit' in name:
                    print(f'{name_print} | Ω*{A_sample:.1f}[cm^2]')
                    plt.plot(x, y, linestyle='dashed')
                    save_EIS_data(x, data, writer, name, sheet)
                else:
                    plt.scatter(x, y, s = get_markersize()*5, label = get_label(name), marker = markers[symbols_count])

            elif 'T-Impedance' in sheet:
                I_ss = float(df[sheet][columns[i+2]][0])/1000
                xlabel = r'$\mathdefault{Z_{t, real}\ [mV]}$'
                ylabel = r'$\mathdefault{-Z_{t, imag}\ [mV]}$'
                if 'fit' in name:
                    print(f'{name_print} | No normalizing')
                    R_sol = save_tafel_impedance(x, data, writer, name, sheet, I_ss)
                    plt.plot(((x-R_sol)*I_ss)*1000, (y*I_ss*-1)*1000, linestyle='dashed')
                else:
                    print(f'{name_print} | No normalizing')
                    plt.scatter(((x-min(x))*I_ss)*1000, (y*I_ss*-1)*1000, s = get_markersize(), label = get_label(name), marker = markers[symbols_count])
            else:
                plt.plot(x,y)

            symbols_count += 1

        plot_settings(xlabel, ylabel, columns, sheet, excelfile, ECSA_norm, In_situ_correction, ax)

### Functions ###
def save_EIS_data(x, data, writer, name, sheet):
    R_sol = round(min(x),2)
    R_pol = round(max(x)-min(x),2)
    temp = {'Sample': name.replace(r'A $\mathdefault{cm^{-2}}$', 'A cm-2'), 'R, sol [ohm cm2]':R_sol, 'R, pol [ohm cm2]':R_pol}
    data.append(temp)
    df = pd.DataFrame(data, columns = ['Sample', 'R, sol [ohm cm2]', 'R, pol [ohm cm2]'])
    df.to_excel(writer, index = False, header=True, sheet_name='EIS')
    writer.save()    

def save_tafel_impedance(x, data, writer, name, sheet, I_ss):
    R_sol = min(x)
    R_pol = max(x)-min(x)
    bzt = R_pol*I_ss*1000
    temp = {'Sample': name.replace(r'A $\mathdefault{cm^{-2}}$', 'A cm-2'), 'Current [mA]':round(I_ss*1000,2), 'Tafel impedance [mV]':round(bzt ,2)}
    data.append(temp)
    df = pd.DataFrame(data, columns = ['Sample', 'Current [mA]', 'Tafel impedance [mV]'])
    df.to_excel(writer, index = False, header=True, sheet_name=sheet)
    writer.save()
    return R_sol

def get_ECSA_data(x, y, writer, columns, data, name, A_sample_RF, name_print):
    cdl, b = np.polyfit(x, y, 1) # cdl [F]
    c = 40e-6 # F/cm^2
    ECSA = cdl / c # ECSA [cm^2]
    # Save data
    temp = {'Sample': name.replace(r'A $\mathdefault{cm^{-2}}$', 'A cm-2'), 'Cdl [mF]':round(cdl*1000,2), 'ECSA [cm2]':round(ECSA,2), 'RF':round(ECSA/A_sample_RF,2)}
    data.append(temp)
    df = pd.DataFrame(data, columns = ['Sample', 'Cdl [mF]', 'ECSA [cm2]', 'RF'])
    df.to_excel(writer, index = False, header=True, sheet_name='ECSA-cap')
    writer.save()
    return cdl, b

def get_ECSA(df):
    ECSA_samples = {}
    columns = list(df['ECSA-cap'].columns)
    for i in range(1, len(columns), 3): # Iterate data columns
        name = columns[i+2]
        x = np.array(df['ECSA-cap'][columns[i]].tolist())
        y = np.array(df['ECSA-cap'][columns[i+1]].tolist())
        x = x[~np.isnan(x)]
        y = y[~np.isnan(y)]
        cdl, b = np.polyfit(x, y, 1) # cdl [F]
        c = 40e-6 # F/cm^2
        ECSA = cdl / c # ECSA [cm^2]
        ECSA_samples[name] = ECSA
    return ECSA_samples

def save_overpotential(x, y, writer, offset_Hg, data, name, sheet):
    for i, j in enumerate(y):
        if round(j, 1) >= 9.9:
            break
    temp = {'Sample': name.replace(r'A $\mathdefault{cm^{-2}}$', 'A cm-2'), 'Current density [mA cm-2]':round(y[i],2), 'Overpotential [mV]':round((x[i] + offset_Hg - 1.23)*1000,2), 'Max current density [mA cm-2]':round(y[-1],2)}
    data.append(temp)
    df = pd.DataFrame(data, columns = ['Sample','Current density [mA cm-2]', 'Overpotential [mV]', 'Max current density [mA cm-2]'])
    df.to_excel(writer, index = False, header = True, sheet_name = sheet)
    writer.save()

def get_AgCl_offset(): # For ED potential labels Ex situ
    pH = 3.00
    offset_AgCl = 0.197 + (0.0591 * pH) # V
    print(f'AgCl to RHE offset = {offset_AgCl:.2f} V at pH {pH}')
    return offset_AgCl

def get_label(name):
    if 'NiFeED/NF' in name:
        name = name.replace('NiFeED/NF', str(r'NiFe$\mathdefault{_{ED}}$/NF'))
    if 'NiFeELD/NF' in name:
        name = name.replace('NiFeELD/NF', str(r'NiFe$\mathdefault{_{ELD}}$/NF'))
    if 'A' in str(name): # Change to current density in label
        idx = name.find('-')
        current_density = (float(name[idx+1:idx+5])/A_sample) * 1000 # A to mA
        name = name.replace(name[idx+1:idx+5],  f'{current_density:.0f}')
        name = name.replace('A', r'mA $\mathdefault{cm^{-2}}$')
        print(f'{sheet} | {name_print} | A to mA legend')
    if '-' in name and 'V' in name: # Correct Ag/Cl offset in label
        print(name)
        offset_AgCl = get_AgCl_offset()
        idx = name.find('V')
        E = round(float(name[idx-5:idx-1]) - offset_AgCl, 2) # - offset since float is positive from excel
        name = name.replace(name[idx-5:idx-1], str(E))
        print(f'Label: AgCl offset {name}')
    if 'mV/s' in name:
        name = name.replace('mV/s', r'mV $\mathdefault{s^{-1}}$')
    if '1st' in name:
        name = name.replace('1st', r'$\mathdefault{1^{st}}$')
    if '10000th' in name:
        name = name.replace('10000th', r'$\mathdefault{10000^{th}}$')

    return name