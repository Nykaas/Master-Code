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


def get_CV(df, excelfile, save_graphs=True, save_data=True):
    ''' Iterate over excel workbook sheets to find data and save graphs and relevant data
    Args:
        - df: Pandas DataFrame of excel workbook
        - excelfile: Path to excelfile for given process in variables
        - save_graphs: True/False, saves graphs from workbook
        - save_data: True/False, saves relevant data from raw excel file to a new tidy excel file
    '''
    if save_data == True: # Creating file and writing object
        filepath = os.path.join(r'C:\Users', username, r'OneDrive\Specialization Project\3_Project plan\Lab\Plots\Draft', username, r'CV_data.xlsx') # for data in onedrive
        writer = pd.ExcelWriter(filepath)
    for sheet in df: # Iterate sheet name as key in df dictionary
        columns = list(df[sheet].columns)
        for i in range(1, len(columns), 3): # Iterate data columns
            xdata = np.array(df[sheet][columns[i]].tolist())
            ydata = np.array(df[sheet][columns[i+1]].tolist())
            if excelfile == 'CV_Ni_RDE.xlsx' and sheet != ('ECSA-cap' or 'ECSA-alpha'): # Correct Hg offset
                xdata = list(map(lambda x: x + offset_Hg, xdata)) 
            if sheet == 'ECSA-alpha': # Calculating ECSA and RF by Alpha method
                    xdata = np.array(xdata)
                    ydata = np.array(ydata)
                    integral = 0
                    for i in range(0, len(xdata)-1):
                        temp = (ydata[i+1] + ydata[i]) * (xdata[i+1] + xdata[i] - offset_Hg*2)
                        integral += temp
                    charge = -1000 * (integral/100)              
                    alpha_data = {'Charge, Q [µF]':[charge], 'ECSA [cm2]':[charge/514], 'RF':[charge/(514*6.25)]}
                    ECSA_alpha_df = pd.DataFrame(alpha_data, columns = ['Charge, Q [µF]', 'ECSA [cm2]', 'RF'])
                    ECSA_alpha_df.to_excel(writer, index = False, header=True, sheet_name='ECSA-alpha')
            if sheet == 'ECSA-cap': # Linear regression for ECSA capacitance method & RF
                if save_graphs == True:
                    m, b = np.polyfit(xdata, ydata, 1)
                    plt.scatter(xdata, ydata, marker = 'x')
                    plt.plot(xdata, m*xdata + b)
                if save_data == True:
                    m, b = np.polyfit(xdata/1000, ydata, 1)
                    capacitane_data = {'Double layer capacitance [µF]':[m], 'ECSA [cm2]':[m/40], 'RF':[m/(40*6.25)]}
                    ECSA_cap_df = pd.DataFrame(capacitane_data, columns = ['Double layer capacitance [µF]', 'ECSA [cm2]', 'RF'])
                    ECSA_cap_df.to_excel(writer, index = False, header=True, sheet_name='ECSA-cap')
            elif len(columns) == 3 and save_graphs == True: # Disable legend
                plt.plot(xdata, ydata)
            else: # Enable legend
                if save_graphs == True:
                    plt.plot(xdata, ydata, label = columns[i+2])
                    plt.legend()
        if save_graphs == True:
            labels = df[sheet][columns[0]].tolist()
            plt.title(labels[0])
            plt.xlabel(labels[1])
            plt.ylabel(labels[2])
            graph_filepath = os.path.join(r'C:\Users', username, r'OneDrive\Specialization Project\3_Project plan\Lab\Plots\Draft', username, sheet) # for data in onedrive
            plt.savefig(graph_filepath, dpi = 300)
            plt.clf()
    if save_graphs == True and save_data == False:
        print('Graphs saved! Have a great day', username + '.')
    elif save_graphs == False and save_data == True:
        writer.save()
        print('Data saved! Have a great day', username + '.')
    elif save_graphs == True and save_data == True:
        writer.save()
        print('Data and graphs saved! Have a great day', username + '.')

df = get_dataframe(excelfile)
get_CV(df, excelfile, save_graphs=True, save_data=True)
