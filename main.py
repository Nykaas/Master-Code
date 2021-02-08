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
    'ED.xlsx',
    'ED_Polarization.xlsx'
]
excelfile = excelfiles[3]
offset_Hg = 0.93 # V at 14 pH 1.0 M KOH
bath_pH = 1.1 # ED electrolyte pH
ECSA_norm = True # Normalize currents with ECSA (True) or SA (False)
smooth = True # Smooths x and y data
trim, num_datapoints = True, 30 # Specify number of datapoints
symbols = ['v', 'o', 's', '*', 'x','1', '2', '3', '4', '8']


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
    if ECSA_norm:
        filepath = os.path.join(r'C:\Users', username, r'OneDrive\Master Thesis\3 Project plan\Lab\Plots\Draft', username, excelfile[:-5], r'Data_ECSA.xlsx') # for data in onedrive
    else:
        filepath = os.path.join(r'C:\Users', username, r'OneDrive\Master Thesis\3 Project plan\Lab\Plots\Draft', username, excelfile[:-5], r'Data.xlsx') # for data in onedrive
    writer = pd.ExcelWriter(filepath)
    return writer

def get_area(): # cm^2
    if 'RDE' in excelfile:
        return 0.196
    elif 'Ex' in excelfile or 'ED' in excelfile:
        return 12.5
    elif 'In' in excelfile:
        return 6.25
    
def plot(df, excelfile):    
    if 'Ex' in excelfile:
        ex_situ_plot(df, writer(ECSA_norm), get_area(), offset_Hg, excelfile, ECSA_norm, smooth, trim, num_datapoints, symbols)
    elif 'In' in excelfile:
        in_situ_plot(df, excelfile, get_area(), ECSA_norm, smooth, trim, num_datapoints, symbols)
    elif 'ED' in excelfile:
        ED_plot(df, excelfile, get_area(), bath_pH, writer(ECSA_norm), ECSA_norm, smooth, trim, num_datapoints, symbols)

makedir()
df = get_dataframe()
plot(df, excelfile)

if ECSA_norm:
    print(f'Plots/Data from {excelfile} normalized by ECSA saved in {(timer()-start):.2f}s! Have a great day {username.capitalize()}.')
else:
    print(f'Plots/Data from {excelfile} normalized by SA saved in {(timer()-start):.2f}s! Have a great day {username.capitalize()}.')
