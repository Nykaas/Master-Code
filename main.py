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
    'Ex_Comparison.xlsx', # 0
    'In_Comparison.xlsx', # 1
    'ED.xlsx', # 2
]
excelfile = excelfiles[2]
offset_Hg = 0.93 # V at 14 pH 1.0 M KOH
bath_pH = 5.1 # ED electrolyte pH
ECSA_norm = True # Normalize currents with ECSA for exsitu only
smooth = True # Smooths x and y data
markers = ['v', 'o', 's', '*', 'x','1', '2', '3', '4', '8']


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
        ex_situ_plot(df, writer(ECSA_norm), get_area(), offset_Hg, excelfile, ECSA_norm, smooth, markers)
    elif 'In' in excelfile:
        in_situ_plot(df, excelfile, get_area(), smooth, markers)
    elif 'ED' in excelfile:
        ED_plot(df, excelfile, get_area(), bath_pH, writer(ECSA_norm=False), smooth, markers)

makedir()
df = get_dataframe()
plot(df, excelfile)

if ECSA_norm:
    print(f'Plots/Data from {excelfile} normalized by ECSA saved in {(timer()-start):.2f}s! Have a great day {username.capitalize()}.')
    print(f'Plots/Data from {excelfile} normalized by SA saved in {(timer()-start):.2f}s! Have a great day {username.capitalize()}.')
