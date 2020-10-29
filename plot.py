import os
import matplotlib.pyplot as plt

def plot_settings(labels, sheet, excelfile):
    plt.title(labels[0])
    plt.xlabel(labels[1])
    plt.ylabel(labels[2])
    username = os.getlogin()
    filepath = os.path.join(r'C:\Users', username, r'OneDrive\Specialization Project\3_Project plan\Lab\Plots\Draft', username, excelfile[:-5], sheet) # for data in onedrive
    plt.savefig(filepath, dpi = 300)
    plt.clf()
