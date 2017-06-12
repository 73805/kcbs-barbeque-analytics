import pandas as pd
import pickle

'''
    Score Calculation:
        Average of the top 5 performers in each category (including overall)
'''

df = pd.read_pickle('pkls/contest_data_cleaned_2016.pkl')

demo_row = {'state': 'NA', 'state_full': 'NA', 'contest_count': 0, 'chicken_score': 0,
            'ribs_score': 0, 'pork_score': 0, 'brisket_score': 0,
            'overall_score': 0, 'best_category': 'NA',
            'prize_total': 0, 'prize_count': 0, 'prize_average_prized': 0, 'prize_average_all': 0}
sf = pd.DataFrame(data=None, columns=demo_row.keys())


contest_states = list(df.state.unique())
contest_categories = ['overall', 'chicken', 'ribs', 'pork', 'brisket']
# scoring dictionary with aggregators for score and team-count
score_demo =   {'overall':  {'score': 0, 'team_count': 0},
                'chicken':  {'score': 0, 'team_count': 0},
                'ribs':     {'score': 0, 'team_count': 0},
                'pork':     {'score': 0, 'team_count': 0},
                'brisket':  {'score': 0, 'team_count': 0}}

# For each state where contests were held
for state in contest_states:
    # create state-specific dataframe
    state_df = df[df.state == state]
    # create a new row dict
    new_row = demo_row.copy()
    # get basic data
    new_row['state'] = state
    new_row['state_full'] = state_df.iloc[0].state_full
    new_row['contest_count'] = state_df.shape[0]
    new_row['prize_total'] = state_df.prize.sum()
    new_row['prize_count'] = new_row['contest_count'] - ((state_df.prize == 0.0).sum())

    # create new scoring 'sheet' to aggregate category-specific scores
    score = score_demo.copy()
    # for each contest in the state
    for i, row in state_df.iterrows():
        # for each category
        for cat in contest_categories:
            # get the nested dataframe from the category cell in the contest's row
            if isinstance(row[cat], pd.DataFrame):
                score_df = row[cat]
                # extract the top 5 rows of the category
                top_5 = score_df[score_df.place <= 5]
                # aggregate team count and scores for averaging
                score[cat]['team_count'] = score[cat]['team_count'] + top_5.shape[0]
                score[cat]['score'] = score[cat]['score'] + top_5.score.sum()

    # Calculate and set average scores in the new row
    new_row['overall_score'] = score['overall']['score'] / score['overall']['team_count']
    new_row['chicken_score'] = score['chicken']['score'] / score['chicken']['team_count']
    new_row['ribs_score'] = score['ribs']['score'] / score['ribs']['team_count']
    new_row['pork_score'] = score['pork']['score'] / score['pork']['team_count']
    new_row['brisket_score'] = score['brisket']['score'] / score['brisket']['team_count']

    # Extract category name with highest score
    max_dict = {'chicken': new_row['chicken_score'],
                'ribs': new_row['ribs_score'],
                'pork': new_row['pork_score'],
                'brisket': new_row['brisket_score']}
    new_row['best_category'] = max(max_dict, key=max_dict.get)

    # insert new row
    sf.loc[-1] = new_row
    sf.index = sf.index + 1
    print "Finished scores for ", state

# Calculate average prize column
sf['prize_average_all'] = sf['prize_total'] / sf['contest_count']
sf['prize_average_prized'] = sf['prize_total'] / sf['prize_count']

# Save the Scoring dataframe to a new file
with open('pkls/scoring_table_2016.pkl', 'wb') as f:
    pickle.dump(sf, f)

# Write out a CSV for sharing!
sf.to_csv('csvs/kcbs_data_2016.csv', index=False)