import pandas as pd
import matplotlib.pyplot as plt
import os

username = os.getlogin()
filepath = os.path.join(r'C:\Users', username, r'OneDrive\Master Thesis\3 Project plan\Lab\Plots\Draft', username, r'In_Comparison\Regression_ED.txt')

start = 3635 # Start time in seconds
end = 23458 # End time in seconds

xfit = [i for i in range(start, end + 1) if i % 600 == 0 or i == start or i == end]
yfit = [((-4.36E-06 * i) + 1.597129) for i in xfit]
data = {'Time [s]':xfit, 'E [V]':yfit}
df = pd.DataFrame(data, columns = ['Time [s]', 'E [V]'])
df.to_csv(filepath, header=True, index=None, sep='\t', mode='w')
print('Data from ED regression saved.')
#plt.plot(xfit, yfit)
#for i in range(0, len(xfit)):
#    plt.scatter(xfit[i]/3600, yfit[i], s = 20, marker = '_')
#plt.show()