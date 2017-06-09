import pandas as pd
import datetime
import pickle

df = pd.read_pickle('pkls/contest_data_raw.pkl')

# Remove tournaments without results (cancelled)
real_df = pd.DataFrame(data=None, columns=df.columns)
for i, row in df.iterrows():
    if isinstance(row.overall, pd.DataFrame):
        real_df.loc[-1] = row
        real_df.index = real_df.index + 1
    else:
        continue

print "Removed Cancellations!"

# Split location column into city and state columns
states_dict = {'ak': 'Alaska', 'al': 'Alabama', 'ar': 'Arkansas', 'az': 'Arizona', 'ca': 'California',
         'co': 'Colorado', 'ct': 'Connecticut', 'de': 'Delaware', 'fl': 'Florida', 'ga': 'Georgia',
         'hi': 'Hawaii', 'ia': 'Iowa', 'id': 'Idaho', 'il': 'Illinois', 'in': 'Indiana',
         'ks': 'Kansas', 'ky': 'Kentucky', 'la': 'Louisiana', 'ma': 'Massachusetts',
         'md': 'Maryland', 'me': 'Maine', 'mi': 'Michigan', 'mn': 'Minnesota', 'mo': 'Missouri',
         'ms': 'Mississippi', 'mt': 'Montana', 'nc': 'North Carolina', 'nd': 'North Dakota',
         'ne': 'Nebraska', 'nh': 'New Hampshire', 'nj': 'New Jersey', 'nm': 'New Mexico',
         'nv': 'Nevada', 'ny': 'New York', 'oh': 'Ohio', 'ok': 'Oklahoma', 'or': 'Oregon',
         'pa': 'Pennsylvania', 'ri': 'Rhode Island', 'sc': 'South Carolina', 'sd': 'South Dakota',
         'tn': 'Tennessee', 'tx': 'Texas', 'ut': 'Utah', 'va': 'Virginia', 'vt': 'Vermont',
         'wa': 'Washington', 'wi': 'Wisconsin', 'wv': 'West Virginia', 'wy': 'Wyoming'}
states = states_dict.keys()

for i, row in real_df.iterrows():
    locat = row.location
    locat = locat.split(',')
    city = locat[0].strip()
    state = locat[-1].strip().lower()
    if state == 'dc':
        state = 'md'
    if state in states:
        real_df.set_value(i, 'keep', True)
        real_df.set_value(i, 'state_full', states_dict[state])
    else:
        real_df.set_value(i, 'keep', False)
    real_df.set_value(i, 'city', city)
    real_df.set_value(i, 'state', state)

print "Split location column into city and state columns!"

real_df = real_df[real_df.keep == True]
rea_df = real_df.drop('keep', 1)
print "Removed contests from outside of the 50 States."

# Convert CBJ% to Float 0:100, and normalize Prize values
for i, row in real_df.iterrows():
    cbj = row.cbj_percentage
    prize = row.prize
    if prize == 'NA':
        prize = 0
    real_df.set_value(i, 'prize', prize)
    if cbj != 'NA':
        cbj = cbj[:-1] + '.0'
    else:
        cbj = 'nan'
    real_df.set_value(i, 'cbj_percentage', cbj)

real_df.prize = real_df.prize.astype('float')
real_df.cbj_percentage = real_df.cbj_percentage.astype('float')

print "Converted CBJ Percentage and Prize Values to Floats!"

# Parse Date String to datetime
m_dict = {"January": "01", "February": "02", "March": "03", "April": "04",
        "May": "05", "June": "06", "July": "07", "August": "08", "September": "09",
        "October": "10", "November": "11", "December": "12"}
for i, row in real_df.iterrows():
    ds = row.date_str
    ds = ds.split(',')
    year = ds[-1].strip()
    m_d = ds[0].split(' ')
    month = m_d[0].strip()
    month = m_dict[month]
    day = str(m_d[1].strip())
    date_concat = month + "-" + day + "-" + year
    real_df.set_value(i, 'date_str', date_concat)

real_df.date = pd.to_datetime(real_df.date_str, infer_datetime_format=True)

print "Converted Date strings to datetimes!"

# Remove competitions before the scoring update (July 13, 2013)
early_cutoff = datetime.date(2013, 6, 13)
real_df = real_df[real_df.date > early_cutoff]

print "Removed Competitions pre-dating scoring changes!"


# Save the cleaned data to a new pickle file
with open('pkls/contest_data_cleaned.pkl', 'wb') as f:
    pickle.dump(real_df, f)

print "Saved out new dataframe to a pickle file"
