import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
from timeit import default_timer as timer

from CV import ex_situ_plot
from ED import ED_plot
from insitu import in_situ_plot

### Constants ###
start = timer()
username = os.getlogin()

### Variables ###
excelfiles = [
    'Ex_Comparison.xlsx',
    'In_Comparison.xlsx',
    'ED.xlsx'
]
excelfile = excelfiles[2]
offset_Hg = 0.93 # V at 14 pH 1.0 M KOH
bath_pH = 3.7 # Input bath pH for deposition process
offset_Ag = 0.197 + (0.0591 * bath_pH) # V
#ECSA_norm = 'Yes' # Normalize currents in plot by ECSA
#ECSA = 356.82
ECSA_norm = 'No' # Normalize currents in plot by SA

### Functions ###
def get_dataframe():
    filepath = os.path.join(r'C:\Users', username, r'OneDrive\Master Thesis\3 Project plan\Lab\Data', excelfile) # for data in onedrive
    df = pd.read_excel(filepath, sheet_name = None) # None can be list of sheet names in string
    return df

def makedir():
    filepath = os.path.join(r'C:\Users', username, r'OneDrive\Master Thesis\3 Project plan\Lab\Plots\Draft', username, excelfile[:-5])
    if not os.path.isdir(filepath):
        os.makedirs(filepath)

def writer(ECSA_norm):
    if ECSA_norm == 'Yes':
        filepath = os.path.join(r'C:\Users', username, r'OneDrive\Master Thesis\3 Project plan\Lab\Plots\Draft', username, excelfile[:-5], r'Data_ECSA.xlsx') # for data in onedrive
    else:
        filepath = os.path.join(r'C:\Users', username, r'OneDrive\Master Thesis\3 Project plan\Lab\Plots\Draft', username, excelfile[:-5], r'Data.xlsx') # for data in onedrive
    writer = pd.ExcelWriter(filepath)
    return writer

def get_area(ECSA_norm): # cm^2
    if 'RDE' in excelfile:
        return 0.196
    elif 'Ex' in excelfile or 'ED' in excelfile:
        if ECSA_norm == 'Yes':
            return ECSA
        return 12.5
    elif 'In' in excelfile:
        return 6.25
    
def plot(df, excelfile):
    if 'Ex' in excelfile:
        ex_situ_plot(df, writer(ECSA_norm), get_area(ECSA_norm), offset_Hg, excelfile, ECSA_norm)
    elif 'In' in excelfile:
        in_situ_plot(df, excelfile, get_area(ECSA_norm), ECSA_norm)
    elif 'ED' in excelfile:
        ED_plot(df, excelfile, get_area(ECSA_norm), offset_Ag, writer(ECSA_norm), ECSA_norm)

makedir()
df = get_dataframe()
plot(df, excelfile)
if ECSA_norm == 'Yes':
    print(f'Plots/Data from {excelfile} normalized by ECSA saved in {(timer()-start):.2f}s! Have a great day {username.capitalize()}.')
else:
    print(f'Plots/Data from {excelfile} normalized by SA saved in {(timer()-start):.2f}s! Have a great day {username.capitalize()}.')