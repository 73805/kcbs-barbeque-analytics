import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_pickle('pkls/contest_data.pkl')

# Extract tournaments with results (non-cancelled)
real_df = pd.DataFrame(data=None, columns=df.columns)
for i, row in df.iterrows():
    if isinstance(row.overall, pd.DataFrame):
        real_df.loc[-1] = row
        real_df.index = real_df.index + 1
    else:
        continue

# convert CBJ% to Float 0:100
for i, row in real_df.iterrows():
    perc = row.cbj_percentage
    if perc != 'NA':
        perc = perc[:-1] + '.0'
    else:
        perc = 'nan'
    real_df.set_value(i, 'cbj_percentage', perc)

real_df.cbj_percentage = real_df.cbj_percentage.astype('float')

