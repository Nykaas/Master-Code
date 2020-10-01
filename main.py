import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
import os


### Declare variables ###
username = os.getlogin()
excelfile = 'CV_Ni_RDE.xlsx'
offset_Hg = 0.9063 # V at 13.7 pH 0.5 M KOH

### Functions ###
def get_dataframe(excelfile):
    ''' Create pandas dataframe from excel data
    Args:
        excelfile: Path to excelfile for given process in variables
    Returns:
        df: DataFrame dictionary with sheet name as key
    '''
    filepath = os.path.join(r'C:\Users', username, r'OneDrive\Specialization Project\3_Project plan\Lab\Data', excelfile) # for data in onedrive
    df = pd.read_excel(filepath, sheet_name = None) # None can be list of sheet names in string
    return df

def set_graph(df, excelfile):
    ''' Iterate over excel workbook sheets to find graph data and save picture
    Args:
        - df: Pandas DataFrame of excel workbook
    '''
    for sheet in df: # Iterate sheet name as key in df dictionary
        columns = list(df[sheet].columns)
        for i in range(1, len(columns), 3): # Iterate data columns
            xdata = df[sheet][columns[i]].tolist()
            ydata = df[sheet][columns[i+1]].tolist()
            if excelfile == 'CV_Ni_RDE.xlsx' and sheet != 'ECSA': # Correct Hg offset 0.9 V
                xdata = list(map(lambda x: x + offset_Hg, xdata)) 
            if sheet == 'ECSA': # Linear regression for ECSA & RF
                xdata = np.array(xdata)
                ydata = np.array(ydata)
                m, b = np.polyfit(xdata, ydata, 1)
                plt.scatter(xdata, ydata, marker = 'x')
                plt.plot(xdata, m*xdata + b)
            elif len(columns) == 3: # Disable legend
                plt.plot(xdata, ydata)
            else: # Enable legend
                plt.plot(xdata, ydata, label = columns[i+2])
                plt.legend()
        labels = df[sheet][columns[0]].tolist()
        plt.title(labels[0])
        plt.xlabel(labels[1])
        plt.ylabel(labels[2])
        graph_filepath = os.path.join(r'C:\Users', username, r'OneDrive\Specialization Project\3_Project plan\Lab\Plots\Draft', username, sheet) # for data in onedrive
        plt.savefig(graph_filepath, dpi = 300)
        plt.clf()
    print('Graphs saved! Have a great day', username + '.')

df = get_dataframe(excelfile)
set_graph(df, excelfile)


