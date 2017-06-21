import pandas as pd
from scipy import stats
import pickle


states_dict = pickle.load(open('pkls/states_dict.pkl', 'r'))

# Load the category specific scoring data
chick_df = pd.read_pickle('pkls/cat_state_score_chicken.pkl')
ribs_df = pd.read_pickle('pkls/cat_state_score_ribs.pkl')
pork_df = pd.read_pickle('pkls/cat_state_score_pork.pkl')
brisk_df = pd.read_pickle('pkls/cat_state_score_brisket.pkl')
over_df = pd.read_pickle('pkls/cat_state_score_overall.pkl')

cat_dict = {'chicken': chick_df,
            'ribs': ribs_df,
            'pork': pork_df,
            'brisket': brisk_df,
            'overall': over_df}

cols = ["state_full",
            "count_chicken", "mean_chicken",  "std_chicken",   "skew_chicken",
            "count_ribs",    "mean_ribs",     "std_ribs",      "skew_ribs",
            "count_pork",    "mean_pork",     "std_pork",      "skew_pork",
            "count_brisket", "mean_brisket",  "std_brisket",   "skew_brisket",
            "count_overall", "mean_overall",  "std_overall",   "skew_overall",]
# create the summary stats df
df = pd.DataFrame(data=None, columns=cols, index=chick_df.index)

# for each row representing a state's scores
for cat in cat_dict.keys():
    cat_df = cat_dict[cat]
    for i, row in cat_df.iterrows():
        row = row.dropna()

        count = row.size
        mean = row.mean()
        std = row.std()
        skew = stats.skew(row)

        df.set_value(i, 'state_full', states_dict[i])
        df.set_value(i, "count_" + cat, count)
        df.set_value(i, "mean_" + cat, mean)
        df.set_value(i, "std_" + cat, std)
        df.set_value(i, "skew_" + cat, skew)

df.to_pickle('pkls/score_summaries.pkl')
df.to_csv('csvs/score_summaries.csv')

