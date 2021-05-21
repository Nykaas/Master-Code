import os
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

def plot_settings(xlabel, ylabel, columns, sheet, excelfile, ECSA_norm, ax):
    if sheet == 'Efficiency':
        plt.ylabel(ylabel, fontsize = 27)
    else:
        plt.xlabel(xlabel, fontsize = 17) # Include fontweight='bold' to bold the label
        plt.ylabel(ylabel, fontsize = 17) # Include fontweight='bold' to bold the label
    plt.xticks(fontsize = 17)
    plt.yticks(fontsize = 17)
    #plt.grid(b=True, which='major', color='#999999', linestyle='-', alpha=0.5)
    plt.minorticks_on() # Show the minor grid lines with very faint and almost transparent grey lines
    #plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
    #plt.xlim(-0.1,0.2)
    #plt.ylim(-3,3)
    if sheet == 'Tafel':
        if ECSA_norm:
            plt.xlim(-2,)
        else:
            plt.xlim(0,)
    if sheet == 'Impedance': # Complex plots require equal xticks and yticks
        if ECSA_norm:
            plt.xlim(0, 800)
            plt.ylim(0, 800)
        else:
            plt.xlim(0, 25)
            plt.ylim(0, 25)
    if 'T-Impedance' in sheet: # Complex plots require equal xticks and yticks
        plt.xlim(0, 30)
        plt.ylim(0, 30)

    if 'Durability' in sheet:
        plt.xlim(0, 6)
  
    if len(columns)-1 > 3:
        if sheet == 'Efficiency':
            plt.legend(fontsize = 17, loc = 'lower right')
        elif '10to100' in sheet:
            plt.legend(fontsize = 17, loc = 'center', ncol = 5, columnspacing = 1, bbox_to_anchor=(0.5, 1.11))
        elif 'Stability' in sheet:
            plt.legend(fontsize = 17, loc = 'center', ncol = 5, columnspacing = 1, bbox_to_anchor=(0.5, 1.11))
            ax.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
            ax.xaxis.set_major_locator(plt.MaxNLocator(5))
        elif 'ED' in excelfile and 'Evstime' in sheet:
            plt.legend(fontsize = 17, loc = 'center', ncol = 2, columnspacing = 1, bbox_to_anchor=(0.5, 1.11))
        else:
            plt.legend(fontsize = 17)
    username = os.getlogin()
    if ECSA_norm:
        filepath = os.path.join(r'C:\Users', username, r'OneDrive\Master Thesis\3 Project plan\Lab\Plots\Draft', username, excelfile[:-5], f'{sheet}_ECSA') # for data in onedrive
    else:
        filepath = os.path.join(r'C:\Users', username, r'OneDrive\Master Thesis\3 Project plan\Lab\Plots\Draft', username, excelfile[:-5], sheet) # for data in onedrive
    plt.savefig(filepath, dpi = 300, bbox_inches='tight')
    plt.clf()


def get_markersize():
    return 4

def get_markerinterval(x):
    return int(len(x)*0.1)