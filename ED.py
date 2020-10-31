import matplotlib.pyplot as plt
import numpy as np

from plot import plot_settings

def ED_plot(df):
    for sheet in df: # Iterate sheet name as key in df dictionary
        columns = list(df[sheet].columns)
        for i in range(1, len(columns), 3): # Iterate data columns
            xdata = np.array(df[sheet][columns[i]].tolist())
            ydata = np.array(df[sheet][columns[i+1]].tolist())
            if len(columns) == 3: # Disable legend
                plt.plot(xdata, ydata)
            else: # Enable legend
                plt.plot(xdata, ydata, label = columns[i+2])
                plt.legend()
        labels = df[sheet][columns[0]].tolist()
        plot_settings(labels, sheet)
