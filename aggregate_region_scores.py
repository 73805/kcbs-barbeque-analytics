import pandas as pd
import pickle

# Load the cleaned data
df = pd.read_pickle('pkls/contest_data_cleaned.pkl')

# columns represent a single state's scores

contest_states = list(df.state.unique())
contest_categories = ['overall', 'chicken', 'ribs', 'pork', 'brisket']


# minimum scores for consideration (below a 5/5/5 (100 single or 400 overall))
min_score_gen = 100
min_score_ovr = 480

# col_dict contains dictionaries to convert into dataframes. Each category will have a
# dataframe where each column will represent a state's scores in that category.
#   chicken = pd.DataFrame({'il': series, 'ma': series ... }) from col_dict['chicken']
col_dict = {}
for cat in contest_categories:
    col_dict[cat] = {}
    for state in contest_states:
        col_dict[cat][state] = pd.Series(data=None)

# for each state
for state in contest_states:
    # create a state-specific data subset
    state_df = df[df.state == state]
    # for each contest in the state-specific subset
    for i, row in state_df.iterrows():
        # for each category in the contest
        for cat in contest_categories:
            if isinstance(row[cat], pd.DataFrame):
                cat_df = row[cat]
                # filter out scores lower than minimums
                if cat == 'overall':
                    cat_df = cat_df[cat_df.score >= min_score_ovr]
                else:
                    cat_df = cat_df[cat_df.score >= min_score_gen]
                # update the column dictionary
                col_dict[cat][state] = col_dict[cat][state].append(cat_df.score)
            else:
                continue
    print "Finished scores for ", state

# reset all series indices for cleanliness
for cat in col_dict.keys():
    for state in col_dict[cat].keys():
        col_dict[cat][state] = col_dict[cat][state].reset_index(drop=True)

# Produce category-specific data frames from the column dictionaries

# chicken
chick_df = pd.DataFrame(data=col_dict['chicken'])
chick_df = chick_df.transpose()
# ribs
ribs_df = pd.DataFrame(data=col_dict['ribs'])
ribs_df = ribs_df.transpose()
# pork
pork_df = pd.DataFrame(data=col_dict['pork'])
pork_df = pork_df.transpose()
# brisket
brisk_df = pd.DataFrame(data=col_dict['brisket'])
brisk_df = brisk_df.transpose()
# overall
over_df = pd.DataFrame(data=col_dict['overall'])
over_df = over_df.transpose()

chick_df.to_pickle('pkls/cat_state_score_chicken.pkl')
ribs_df.to_pickle('pkls/cat_state_score_ribs.pkl')
pork_df.to_pickle('pkls/cat_state_score_pork.pkl')
brisk_df.to_pickle('pkls/cat_state_score_brisket.pkl')
over_df.to_pickle('pkls/cat_state_score_overall.pkl')

chick_df.to_csv('csvs/cat_state_score_chicken.csv')
ribs_df.to_csv('csvs/cat_state_score_ribs.csv')
pork_df.to_csv('csvs/cat_state_score_pork.csv')
brisk_df.to_csv('csvs/cat_state_score_brisket.csv')
over_df.to_csv('csvs/cat_state_score_overall.csv')
