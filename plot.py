import os
import matplotlib.pyplot as plt

def plot_settings(xlabel, ylabel, columns, sheet, excelfile, ECSA_norm):
    plt.xlabel(xlabel, fontsize = 14) # Include fontweight='bold' to bold the label
    plt.ylabel(ylabel, fontsize = 14) # Include fontweight='bold' to bold the label
    plt.xticks(fontsize = 14)
    plt.yticks(fontsize = 14)
    #plt.grid(b=True, which='major', color='#999999', linestyle='-', alpha=0.5)
    plt.minorticks_on() # Show the minor grid lines with very faint and almost transparent grey lines
    #plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
    #plt.xlim(-0.1,0.2)
    #plt.ylim(-3,3)
    if sheet == 'Tafel':
        plt.xlim(0,)
    if sheet == 'Impedance': # Complex plots require equal xticks and yticks
        plt.xlim(0,25)
        plt.ylim(0,25)
    if 'Tafel-Impedance' in sheet: # Complex plots require equal xticks and yticks
        plt.xlim(0,0.03)
        plt.ylim(0,0.03)
    if len(columns) > 3:
        if sheet == 'Efficiency':
            plt.legend(fontsize = 14, loc = 'lower right')
        elif sheet == '10to100':
            plt.legend(fontsize = 14, loc = 'center', ncol = 5, columnspacing = 1, bbox_to_anchor=(0.5, 1.07))
        else:
            plt.legend(fontsize = 14)
    username = os.getlogin()
    if ECSA_norm:
        filepath = os.path.join(r'C:\Users', username, r'OneDrive\Master Thesis\3 Project plan\Lab\Plots\Draft', username, excelfile[:-5], f'{sheet}_ECSA') # for data in onedrive
    else:
        filepath = os.path.join(r'C:\Users', username, r'OneDrive\Master Thesis\3 Project plan\Lab\Plots\Draft', username, excelfile[:-5], sheet) # for data in onedrive
    plt.savefig(filepath, dpi = 300, bbox_inches='tight')
    plt.clf()
