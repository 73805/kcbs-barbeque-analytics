import pandas as pd

# Load the cleaned data
df = pd.read_pickle('pkls/contest_data_cleaned.pkl')

cols = ["names"]
agg_df = pd.DataFrame(data=None, columns=cols)

cats = ['chicken', 'ribs', 'pork', 'brisket', 'overall']
ser = pd.Series([])

for i, row in df.iterrows():
    for cat in cats:
        if isinstance(row[cat], pd.DataFrame):
            cat_df = row[cat]
            names = cat_df['name']
            names = names.str.lower()
            names = names.str.strip()
            ser = ser.append(names)

ser = ser.str.lower()
ser = ser.str.strip()
ser = ser.str.replace('[^\w\s]','')

agg_df['names'] = ser
agg_df = agg_df.drop_duplicates()
agg_df = agg_df.reset_index(drop=True)

f = open('names.txt', 'w')

for name in agg_df['names']:
    f.writelines(name + "\n")

f.close()