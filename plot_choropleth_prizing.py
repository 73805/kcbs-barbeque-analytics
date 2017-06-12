import pandas as pd
import plotly.plotly as py

# Load the cleaned data
df = pd.read_pickle('pkls/scoring_table.pkl')

# Impute the missing states
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

missing_states = list(set(states_dict.keys()) - set(list(df.state.unique())))

demo_row = {'state': 'NA', 'state_full': 'NA', 'contest_count': 0, 'chicken_score': 0,
            'ribs_score': 0, 'pork_score': 0, 'brisket_score': 0,
            'overall_score': 0, 'best_category': 'NA',
            'prize_total': 0, 'prize_count': 0, 'prize_average_prized': 0, 'prized_average_all': 0}

for missing in missing_states:
    new_row = demo_row.copy()
    new_row['state'] = missing
    new_row['state_full'] = states_dict[missing]
    df.loc[-1] = new_row
    df.index = df.index + 1


# Data Prep Steps
df['state'] = map(lambda x: x.upper(), df['state'])
# Text formatting
df['text'] = ('<b>' + df.state_full + '</b><br>' +
              '<b>Hosted:</b> ' + df.contest_count.astype(int).astype(str) + ' contests' + '<br>' +
              '<b>Avg Prize (all):</b> ' + '$' + df.average_prize_all.astype(int).astype(str) + '<br>' +
              '<b>Avg Prize (prized):</b> ' + '$' + df.average_prize_prized.astype(int).astype(str))

# Create map
# https://datascience.stackexchange.com/questions/9616/how-to-create-us-state-heatmap

scl = [[0.0, 'rgb(245, 231, 235)'], [1.0, 'rgb(170, 0, 50)']]

data = [ dict(
        type='choropleth',
        colorscale = scl,
        autocolorscale = False,
        locations = df['state'],
        z = df['prize_total'].astype(float),
        locationmode = 'USA-states',
        text = df['text'],
        hoverinfo = 'text',
        marker = dict(
            line = dict (
                color = 'rgb(255,255,255)',
                width = 2
            )
        ),
        colorbar = dict(
            title = "USD"
        )
    ) ]

layout = dict(
        title = 'KCBS Prize Dollars per State <br> from 7/13/2013 to 12/31/2016',
        geo = dict(
            scope='usa',
            projection=dict( type='albers usa' ),
            showlakes = False
        ),
    )

fig = dict( data=data, layout=layout )

url = py.plot( fig, filename='d3-cloropleth-map' )