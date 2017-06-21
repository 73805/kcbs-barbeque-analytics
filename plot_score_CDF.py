import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt

# Load the cleaned data
df = pd.read_pickle('pkls/scoring_table.pkl')
states_dict = pickle.load(open('pkls/states_dict.pkl', 'r'))

# Load the category specific scoring data
chick_df = pd.read_pickle('pkls/cat_state_score_chicken.pkl')
ribs_df = pd.read_pickle('pkls/cat_state_score_ribs.pkl')
pork_df = pd.read_pickle('pkls/cat_state_score_pork.pkl')
brisk_df = pd.read_pickle('pkls/cat_state_score_brisket.pkl')

cat_dict = {'chicken': chick_df,
            'ribs': ribs_df,
            'pork': pork_df,
            'brisket': brisk_df}

# explicit list for ordering (keys doesnt preserve order)
cats_basic = ['chicken', 'ribs', 'pork', 'brisket']

# Get the top n states by contest count
top_n = 5
df = df.sort_values(by="contest_count", ascending=False)
df = df.head(top_n)
top_states = list(df['state'])

plot_dict = {'chicken': 221,'ribs': 222,
             'pork': 223,   'brisket': 224}

plt.figure()

for cat in cats_basic:
    cat_df = cat_dict[cat]
    state_names = []
    plt.subplot(plot_dict[cat])
    for state in top_states:
        state_names.append(states_dict[state])
        data = cat_df.loc[state].dropna()

        x = np.sort(data)
        y = np.arange(1, x.size + 1) / float(x.size)

        plt.plot(x, y)

    plt.title("CDF of " + str(cat).title() + " Scores")
    plt.xlabel("scores")
    plt.ylabel("probability")
    plt.legend(state_names, loc='best')
    plt.margins(0.02)

plt.show()
