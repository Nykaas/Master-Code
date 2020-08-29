import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import os

def get_df(sheets):
    #df = pd.read_excel(r'.\Data\Workbook.xlsx', sheet_name = sheets) #For github data
    filepath = os.path.join(r'C:\Users', os.getlogin(), r'OneDrive\Specialization Project\3_Project plan\Lab\Data\Workbook.xlsx') # for data in onedrive
    df = pd.read_excel(filepath, sheet_name = sheets)
    return df

sheets = ['Template', 'Lab1'] # Name of sheets in Workbook to be plotted
df = get_df(sheets)

def set_graph(df):
    ''' Iterate over excel workbook sheets to find graph data and save picture
    Args:
        - df: Pandas DataFrame
    '''
    for sheet in sheets:
        columns = list(df[sheet].columns)
        labels = df[sheet][columns[0]].tolist()
        for i in range(1, len(columns), 3):
            xdata = df[sheet][columns[i]].tolist()
            ydata = df[sheet][columns[i+1]].tolist()
            plt.plot(xdata, ydata, label = columns[i+2])
        plt.title(labels[0])
        plt.xlabel(labels[1])
        plt.ylabel(labels[2])
        plt.legend()
        plt.grid()
        #filepath = os.path.join(r'.\Plots', sheet) #for data on Github folder
        filepath = os.path.join(r'C:\Users', os.getlogin(), r'OneDrive\Specialization Project\3_Project plan\Lab\Plots', sheet) # for data in onedrive
        plt.savefig(filepath, dpi = 100)
        plt.clf()

set_graph(df)