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
        - excelfile: Path to excelfile for given process in variables
    '''
    for sheet in df: # Iterate sheet name as key in df dictionary
        columns = list(df[sheet].columns)
        for i in range(1, len(columns), 3): # Iterate data columns
            xdata = np.array(df[sheet][columns[i]].tolist())
            ydata = np.array(df[sheet][columns[i+1]].tolist())
            if excelfile == 'CV_Ni_RDE.xlsx' and sheet != ('ECSA-cap' or 'ECSA-alpha'): # Correct Hg offset
                xdata = list(map(lambda x: x + offset_Hg, xdata)) 
            if sheet == 'ECSA-cap': # Linear regression for ECSA capacitance method & RF
                #xdata = np.array(xdata)
                #ydata = np.array(ydata)
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

def save_data(df, excelfile):
    ''' Saves relevant data from raw excel file to a new tidy excel file
    Args:
         df: Pandas DataFrame of excel workbook
         excelfile: Path to excelfile for given process in variables
    '''
    graph_filepath = os.path.join(r'C:\Users', username, r'OneDrive\Specialization Project\3_Project plan\Lab\Plots\Draft', username, r'CV_data.xlsx') # for data in onedrive
    for sheet in df: # Iterate sheet name as key in df dictionary
        columns = list(df[sheet].columns)
        for i in range(1, len(columns), 3): # Iterate data columns
            xdata = np.array(df[sheet][columns[i]].tolist())
            ydata = np.array(df[sheet][columns[i+1]].tolist())
            if excelfile == 'CV_Ni_RDE.xlsx' and sheet != ('ECSA-cap' or 'ECSA-alpha'): # Correct Hg offset
                xdata = list(map(lambda x: x + offset_Hg, xdata)) 
            if sheet == 'ECSA-cap': # Calculating ECSA and RF by Capacitance method
                #xdata = np.array(xdata)
                #ydata = np.array(ydata)
                m, b = np.polyfit(xdata/1000, ydata, 1)
                capacitane_data = {'Double layer capacitance [µF]':[m], 'ECSA [cm2]':[m/40], 'RF':[m/(40*6.25)]}
                ECSA_cap_df = pd.DataFrame(capacitane_data, columns = ['Double layer capacitance [µF]', 'ECSA [cm2]', 'RF'])
                #ECSA_cap_df.to_excel(graph_filepath, index = False, header=True, sheet_name='ECSA-cap')
            if sheet == 'ECSA-alpha': # Calculating ECSA and RF by Alpha method
                xdata = np.array(xdata)
                ydata = np.array(ydata)
                integral = 0
               """  for i in range(0, len(xdata)-1):
                    temp = (ydata[i]+ydata[i+1]) * (xdata[i]+xdata[i+1])
                    integral += temp
                    print(xdata[i]-offset_Hg, ydata[i], temp) """
                charge = 1000 * (integral/100)
                print(integral, charge)                
                alpha_data = {'Charge, Q [µF]':[charge], 'ECSA [cm2]':[integral/514], 'RF':[integral/(514*6.25)]}
                ECSA_alpha_df = pd.DataFrame(alpha_data, columns = ['Charge, Q [µF]', 'ECSA [cm2]', 'RF'])
                #ECSA_alpha_df.to_excel(graph_filepath, index = False, header=True, sheet_name='ECSA-alpha')
    print('Data is saved! Have a great day', username + '.')

df = get_dataframe(excelfile)
#set_graph(df, excelfile)
save_data(df, excelfile)
