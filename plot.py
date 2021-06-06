import os
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

def plot_settings(xlabel, ylabel, columns, sheet, excelfile, ECSA_norm, In_situ_correction, ax):
    if sheet == 'Efficiency':
        plt.ylabel(ylabel, fontsize = 27)
    else:
        plt.xlabel(xlabel, fontsize = 17) # Include fontweight='bold' to bold the label
        plt.ylabel(ylabel, fontsize = 17) # Include fontweight='bold' to bold the label
    plt.xticks(fontsize = 17)
    plt.yticks(fontsize = 17)
    plt.minorticks_on() # Show the minor grid lines with very faint and almost transparent grey lines
    
    if 'Ex_' in excelfile:
        if sheet == 'Tafel':
            plt.xlim(-1.5, )
            plt.ylim(0.25, )
        elif sheet == 'Impedance': # Complex plots require equal xticks and yticks
            plt.xlim(0, 800)
            plt.ylim(0, 800)
        elif 'T-Impedance' in sheet: # Complex plots require equal xticks and yticks
            plt.xlim(0, 30)
            plt.ylim(0, 30)
        elif sheet == 'Delta_performance':
            plt.ylim(-47, 30)
        elif sheet == 'Delta_EIS':
            plt.ylim(-80, 150)

    if 'In_' in excelfile:
        if 'Durability' in sheet:
            plt.xlim(0, )
        elif 'Impedance' in excelfile:
            if '01' in sheet:
                plt.xlim(0, 900)
                plt.ylim(0, 900)
            elif '02' in sheet:
                plt.xlim(0, 350)
                plt.ylim(0, 350)
            elif '03' in sheet:
                plt.xlim(0, 300)
                plt.ylim(0, 300)
            else:
                plt.xlim(0, 250)
                plt.ylim(0, 250)
        elif 'EIS' in sheet:
            plt.xlim(0, 350)
            plt.ylim(0, 350)
        elif 'Pol' in sheet:
            plt.xlim(1.5)
  
    if len(columns)-1 > 3:
        if sheet == 'Efficiency':
            plt.legend(fontsize = 17, loc = 'lower right')
        elif '10to100' in sheet:
            plt.legend(fontsize = 17, loc = 'center', ncol = 5, columnspacing = 1, bbox_to_anchor=(0.5, 1.11))
        elif 'Stability' in sheet:
            plt.legend(fontsize = 17, loc = 'center', ncol = 5, columnspacing = 1, bbox_to_anchor=(0.5, 1.11))
            ax.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
            ax.xaxis.set_major_locator(plt.MaxNLocator(5))
        elif 'Durability' in sheet:
            ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
            ax.yaxis.set_major_locator(plt.MaxNLocator(6))
            plt.legend(fontsize = 17)
        elif 'ED' in excelfile and 'Evstime' in sheet:
            plt.legend(fontsize = 17, loc = 'center', ncol = 2, columnspacing = 1, bbox_to_anchor=(0.5, 1.11))
        else:
            plt.legend(fontsize = 17)
    username = os.getlogin()
    if ECSA_norm:
        filepath = os.path.join(r'C:\Users', username, r'OneDrive\Master Thesis\3 Project plan\Lab\Plots\Draft', username, excelfile[:-5], f'{sheet}_ECSA') # for data in onedrive
    elif In_situ_correction and 'In' in excelfile:
        filepath = os.path.join(r'C:\Users', username, r'OneDrive\Master Thesis\3 Project plan\Lab\Plots\Draft', username, excelfile[:-5], f'{sheet}_iR') # for data in onedrive
    else:
        filepath = os.path.join(r'C:\Users', username, r'OneDrive\Master Thesis\3 Project plan\Lab\Plots\Draft', username, excelfile[:-5], sheet) # for data in onedrive
    plt.savefig(filepath, dpi = 300, bbox_inches='tight')
    plt.clf()


def get_markersize():
    return 6

def get_markerinterval(x):
    return int(len(x)*0.1)