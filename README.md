# KCBS Barbeque Competition Analytics

This project explores KCBS competition data from 2013-2016. I used Python (selenium, beautiful soup) to pull the data from the KCBS website. Data analysis will include choropleths (colored maps) based on competition meta-data, and state-by-state score data comparisons.

## Choropleths

The visuals folder contains choropleths on three measures in the data. These maps were made with Tableau. They include;

* competitions per state (red)
* total prize dollars per state (green)
* average prize dollars per (prized) competition (gold)

## Scoring

In Progress...

Plotting the cumulative distribution function of category scores from the 5 most competing states (Missouri, Kansas, California, Tennessee, Georgia) seems to show stronger scoring in Georgia and Tennessee. 

The similarity between plot lines correspond to geographic proximity and(/or in the case of California) contest counts. As a result, the higher scoring in Tennessee and Georgia may be a significant effect or the result of regional scoring biases or a smaller sample size.

[CDF plots](visuals/cdf_scores.png)

## Data Sources

Competition Data: http://www.kcbs.us/events.

A change in KCBS scoring standards went into effect on July 2013. Competition data is limited to contests after that date.

Scoring Information: http://www.kcbs.us/news.php?id=687

Feel free to reach out for csv/pickle files (pandas dataframes). The largest file (~50mb) holds every competition from July 2013 onwards, and includes score result sub-tables (chicken, ribs, pork, brisket, overall).
