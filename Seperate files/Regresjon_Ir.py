import pandas as pd
import matplotlib.pyplot as plt
import os
username = os.getlogin()
filepath = os.path.join(r'C:\Users', username, r'OneDrive\Master Thesis\3 Project plan\Lab\Plots\Draft', username, r'In_Comparison\Regression_Ir.txt')

start = 4232 # Start time in seconds
end = 34188 # End time in seconds

xfit = [i for i in range(start, end + 1) if i % 600 == 0 or i == start or i == end]
yfit = [((1.29E-06 * i) + 1.661097) for i in xfit]
data = {'Time [s]':xfit, 'E [V]':yfit}
df = pd.DataFrame(data, columns = ['Time [s]', 'E [V]'])
df.to_csv(filepath, header=True, index=None, sep='\t', mode='w')
print('Data from Ir/NF regression saved.')
# plt.plot(xfit, yfit)
# plt.show()