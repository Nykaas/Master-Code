import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import os

def get_df(sheets):
    df = pd.read_excel(r'.\Data\Workbook.xlsx', sheet_name = sheets)
    return df

sheets = ['Sheet1', 'Sheet2'] # Name of sheets in Workbook to be plotted
df = get_df(sheets)

def set_graph(df):
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
        filepath = os.path.join(r'.\Plots', sheet)
        plt.savefig(filepath, dpi = 100)
        plt.clf()

set_graph(df)