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
A_sample = 6.25 # cm^2
offset_Hg = 0.9063 # V at 13.7 pH 0.5 M KOH
excelfile = 'CV_Ni_RDE.xlsx'
#excelfile = 'ED_NiFe_1.xlsx'

### Functions ###
def get_dataframe(excelfile):
    filepath = os.path.join(r'C:\Users', username, r'OneDrive\Specialization Project\3_Project plan\Lab\Data', excelfile) # for data in onedrive
    df = pd.read_excel(filepath, sheet_name = None) # None can be list of sheet names in string
    return df

def plot(df, excelfile):
    filepath = os.path.join(r'C:\Users', username, r'OneDrive\Specialization Project\3_Project plan\Lab\Plots\Draft', username, r'CV_data.xlsx') # for data in onedrive
    writer = pd.ExcelWriter(filepath)
    if 'CV' in excelfile:
        set_cv_plot(df, writer, A_sample, offset_Hg)    
    if 'ED' in excelfile:
        set_ed_plot(df)

df = get_dataframe(excelfile)
plot(df, excelfile)
print(f'Data and graphs saved in {(timer()-start):.2f}s! Have a great day {username}.')