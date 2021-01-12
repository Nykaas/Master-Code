import os
import matplotlib.pyplot as plt

def plot_settings(xlabel, ylabel, columns, sheet, excelfile):
    plt.xlabel(xlabel, fontsize = 12) # Include fontweight='bold' to bold the label
    plt.ylabel(ylabel, fontsize = 12) # Include fontweight='bold' to bold the label
    plt.xticks(fontsize = 12)
    plt.yticks(fontsize = 12)
    #plt.xlim(-5,95)
    if len(columns) > 3:
        if sheet == 'Efficiency':
            plt.legend(fontsize = 12, loc = 'lower right')
        else:
            plt.legend(fontsize = 12)
    username = os.getlogin()
    filepath = os.path.join(r'C:\Users', username, r'OneDrive\Master Thesis\3 Project plan\Lab\Plots\Draft', username, excelfile[:-5], sheet) # for data in onedrive
    plt.savefig(filepath, dpi = 300, bbox_inches='tight')
    plt.clf()
