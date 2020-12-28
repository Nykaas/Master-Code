import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

labels = ['NF', 'NiFe/NF', 'Ir/NF']
# delta = [765, 321, -156]
# Efficiency = 1.48/E
before = [81.4, 81.7, 90.9]
after = [86.4, 85.6,88.4]

x = np.arange(len(labels))
width = 0.35

fig, ax = plt.subplots(figsize=(9,7))
rects1 = ax.bar(x - width/2, before, width, label = 'Before', color = 'C7')
rects2 = ax.bar(x + width/2, after, width, label='After', color = 'C3')

# ax.set_xlim([-0.35,2.35])
ax.legend(fontsize = 20, loc='lower right')
ax.set_ylabel('Efficiency [%]', fontsize = 20)
plt.xticks(x, labels, fontsize = 20)


def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize = 20)


autolabel(rects1)
autolabel(rects2)

fig.tight_layout()

plt.yticks(fontsize = 20)
plt.ylim(0,99)
plt.show()
# plt.savefig('Efficiency_bar_plot.png' ,dpi = 300, bbox_inches='tight')