import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties


N = 2
training = (70, 73)
training_std = (10, 10)

ind = np.arange(N)  # the x locations for the groups
width = 0.35       # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(ind, training, width, color='r', yerr=training_std)

k_fold = (69, 71)
k_fold_std = (10, 10)
rects2 = ax.bar(ind + width, k_fold, width, color='y', yerr=k_fold_std)


test = (69, 71)
test_std = (3, 5)
rects3 = ax.bar(ind + 2 * width, test, width, color='b', yerr=test_std)


# add some text for labels, title and axes ticks
ax.set_ylabel('Scores')
ax.set_title('Scores by Classifier and Dataset')
ax.set_xticks(ind + width)
ax.set_xticklabels(('NB', 'LR'))


fontP = FontProperties()
fontP.set_size('small')


ax.legend((rects1[0], rects2[0], rects3[0]), ('Training', 'K Fold Cross Validation', 'Test'), prop = fontP)


# def autolabel(rects):
#     # attach some text labels
#     for rect in rects:
#         height = rect.get_height()
#         ax.text(rect.get_x() + rect.get_width()/4., 1.05*height,
#                 '%d' % int(height),
#                 ha='center', va='bottom')

# autolabel(rects1)
# autolabel(rects2)
# autolabel(rects3)

plt.show()