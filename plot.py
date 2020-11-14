import os
import matplotlib.pyplot as plt

def plot_settings(xlabel, ylabel, columns, sheet, excelfile):
    if len(columns) > 3:
        plt.legend()
    plt.xlabel(xlabel) # Include fontweight='bold' to bold the label
    plt.ylabel(ylabel) # Include fontweight='bold' to bold the label
    username = os.getlogin()
    filepath = os.path.join(r'C:\Users', username, r'OneDrive\Specialization Project\3_Project plan\Lab\Plots\Draft', username, excelfile[:-5], sheet) # for data in onedrive
    plt.savefig(filepath, dpi = 300, bbox_inches='tight')
    plt.clf()
