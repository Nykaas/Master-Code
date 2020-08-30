import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
import os

### Declare variables ###
sheets = ['Template', 'Lab1'] # Name of sheets in Workbook to be plotted
username = os.getlogin()

def get_dataframe(sheets):
    ''' Create pandas dataframe from excel data
    Args:
        sheets: List of excel sheet names
    Returns:
        df: DataFrame dictionary with sheet name as key
    '''
    workbook_filepath = os.path.join(r'C:\Users', username, r'OneDrive\Specialization Project\3_Project plan\Lab\Data\Workbook.xlsx') # for data in onedrive
    df = pd.read_excel(workbook_filepath, sheet_name = sheets)
    return df

def set_graph(df):
    ''' Iterate over excel workbook sheets to find graph data and save picture
    Args:
        - df: Pandas DataFrame
    '''
    for sheet in df: # Iterate sheet name as key in df dictionary
        columns = list(df[sheet].columns)
        for i in range(1, len(columns), 3): # Iterate BCD data columns
            xdata = df[sheet][columns[i]].tolist() # B
            ydata = df[sheet][columns[i+1]].tolist() # C
            plt.plot(xdata, ydata, label = columns[i+2]) # D
        labels = df[sheet][columns[0]].tolist() # A column
        plt.title(labels[0])
        plt.xlabel(labels[1])
        plt.ylabel(labels[2])
        plt.legend()
        plt.grid()
        graph_filepath = os.path.join(r'C:\Users', username, r'OneDrive\Specialization Project\3_Project plan\Lab\Plots\Draft', username, sheet) # for data in onedrive
        plt.savefig(graph_filepath, dpi = 300)
        plt.clf()
    print('Graphs saved! Have a great day', username + '.')

df = get_dataframe(sheets)
set_graph(df)