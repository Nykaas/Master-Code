import os
import matplotlib.pyplot as plt

def plot_settings(xlabel, ylabel, columns, sheet, excelfile, ECSA_norm):
    plt.xlabel(xlabel, fontsize = 12) # Include fontweight='bold' to bold the label
    plt.ylabel(ylabel, fontsize = 12) # Include fontweight='bold' to bold the label
    plt.xticks(fontsize = 12)
    plt.yticks(fontsize = 12)
    #plt.xlim(-5,95)
    if len(columns) > 3:
        if sheet == 'Efficiency':
            plt.legend(fontsize = 12, loc = 'lower right')
        elif sheet == '10to100':
            plt.legend(fontsize = 10, loc = 'center', ncol = 5, columnspacing = 1, bbox_to_anchor=(0.5, 1.07))
        else:
            plt.legend(fontsize = 12)
    username = os.getlogin()
    if ECSA_norm:
        filepath = os.path.join(r'C:\Users', username, r'OneDrive\Master Thesis\3 Project plan\Lab\Plots\Draft', username, excelfile[:-5], f'{sheet}_ECSA') # for data in onedrive
    else:
        filepath = os.path.join(r'C:\Users', username, r'OneDrive\Master Thesis\3 Project plan\Lab\Plots\Draft', username, excelfile[:-5], sheet) # for data in onedrive
    plt.savefig(filepath, dpi = 300, bbox_inches='tight')
    plt.clf()
