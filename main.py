import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
from timeit import default_timer as timer

from CV import set_cv_plot, save_alpha_data, save_cap_data
from ED import set_ed_plot

### Constants ###
start = timer()
username = os.getlogin()

### Variables ###
excelfiles = [
    'CV_Ni_RDE_2909.xlsx',
    'CV_NiF_2910.xlsx',
    'CV_Comparison.xlsx'
]
excelfile = excelfiles[1]
A_sample = 12.5 # cm^2
offset_Hg = 0.9063 # V at 13.7 pH 0.5 M KOH
excelfile = 'CV_Ni_RDE_2909.xlsx'
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

def plot(df, excelfile):
    if 'CV' in excelfile:
        set_cv_plot(df, writer(), A_sample, offset_Hg, excelfile)
    if 'ED' in excelfile:
        set_ed_plot(df)

makedir()
df = get_dataframe()
plot(df, excelfile)
print(f'Plots/Data from {excelfile} saved in {(timer()-start):.2f}s! Have a great day {username}.')