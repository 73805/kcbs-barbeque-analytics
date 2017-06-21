import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Load the category specific scoring data
df = pd.read_pickle('pkls/score_summaries.pkl')

xs = df['mean_chicken']
ys = df['std_chicken']
zs = df['count_chicken']

fig1 = plt.figure(1)
ax = fig1.add_subplot(111, projection='3d')

ax.scatter(xs, ys, zs)
ax.set_xlabel('Mean Score')
ax.set_ylabel('Std deviation')
ax.set_zlabel('Number of Scores')


plt.show()