import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
from timeit import default_timer as timer

from CV import ex_situ_plot, save_alpha_data, save_cap_data
from ED import ED_plot

### Constants ###
start = timer()
username = os.getlogin()

### Variables ###
excelfiles = [
    '0000_Ex_Comparison.xlsx',
    '2909_Ex_Ni_RDE.xlsx',
    '2910_Ex_NiF.xlsx',
    '3010_Ex_NiFe_5min.xlsx',
    '3010_Ex_NiFe_10min.xlsx'
]
excelfile = excelfiles[0]
offset_Hg = 0.9063 # V at 13.7 pH 0.5 M KOH
excelfile = 'CV_NiF_NiFe_5min_3010.xlsx'
#excelfile = 'ED_NiFe_1.xlsx'

### Functions ###
def get_dataframe():
    filepath = os.path.join(r'C:\Users', username, r'OneDrive\Specialization Project\3_Project plan\Lab\Data', excelfile) # for data in onedrive
    df = pd.read_excel(filepath, sheet_name = None) # None can be list of sheet names in string
    return df

def makedir():
    filepath = os.path.join(r'C:\Users', username, r'OneDrive\Specialization Project\3_Project plan\Lab\Plots\Draft', username, excelfile[:-5])
    if not os.path.isdir(filepath):
        os.makedirs(filepath)

def writer():
    filepath = os.path.join(r'C:\Users', username, r'OneDrive\Specialization Project\3_Project plan\Lab\Plots\Draft', username, excelfile[:-5], r'CV_data.xlsx') # for data in onedrive
    writer = pd.ExcelWriter(filepath)
    return writer

def get_area(): # cm^2
    if 'RDE' in excelfile:
        return 0.196 # might not be correct, revise
    elif 'Ex' in excelfile:
        return 15
    elif 'In' in excelfile:
        return 12.5 # might not be correct, revise
    
def plot(df, excelfile):
    if 'Ex' in excelfile:
        ex_situ_plot(df, writer(), get_area(), offset_Hg, excelfile)
    elif 'In' in excelfile:
        return None
    if 'ED' in excelfile:
        ED_plot(df)

makedir()
df = get_dataframe()
plot(df, excelfile)
print(f'Plots/Data from {excelfile} saved in {(timer()-start):.2f}s! Have a great day {username}.')