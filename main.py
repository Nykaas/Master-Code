import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
import os


### Declare variables ###
username = os.getlogin()
process = 'CV_Ni'
offset_Hg = 0.9

### Functions ###
def get_process(process):
    if process == 'CV_Ni':
        excelfile = 'CV_Ni_RDE.xlsx'
        sheets = ['10', '20', '30', '40', '50', '60', '70', '80', '90', '100', '10cycles', 'Alpha', '10to100', 'Capacitance'] # Name of sheets in excelfile
    if process == 'example process':
        excelfile = 'example.xlsx'
        sheets = ['nameofsheet']
    return excelfile, sheets

def get_dataframe(process, excelfile, sheets):
    ''' Create pandas dataframe from excel data
    Args:
        sheets: List of excel sheet names
    Returns:
        df: DataFrame dictionary with sheet name as key
    '''
    filepath = os.path.join(r'C:\Users', username, r'OneDrive\Specialization Project\3_Project plan\Lab\Data', excelfile) # for data in onedrive
    df = pd.read_excel(filepath, sheet_name = sheets)
    return df

def set_graph(df):
    ''' Iterate over excel workbook sheets to find graph data and save picture
    Args:
        - df: Pandas DataFrame of excel workbook
    '''
    for sheet in df: # Iterate sheet name as key in df dictionary
        columns = list(df[sheet].columns)
        for i in range(1, len(columns), 3): # Iterate BCD data columns
            xdata = df[sheet][columns[i]].tolist() # B column
            if process == 'CV_Ni':
                xdata = list(map(lambda x: x + offset_Hg, xdata)) # Correct Hg offset 0.9 V
            ydata = df[sheet][columns[i+1]].tolist() # C column
            if len(columns) == 3: # Disable legend
                plt.plot(xdata, ydata) # D column
            else: # Enable legend
                plt.plot(xdata, ydata, label = columns[i+2]) # D
                plt.legend()
        labels = df[sheet][columns[0]].tolist() # A column
        plt.title(labels[0]) # column A, row 2
        plt.xlabel(labels[1]) # column A, row 3
        plt.ylabel(labels[2]) # column A, row 4
        graph_filepath = os.path.join(r'C:\Users', username, r'OneDrive\Specialization Project\3_Project plan\Lab\Plots\Draft', username, sheet) # for data in onedrive
        plt.savefig(graph_filepath, dpi = 300)
        plt.clf()
    print('Graphs saved! Have a great day', username + '.')

excelfile, sheets = get_process(process)
df = get_dataframe(process, excelfile, sheets)
set_graph(df)


