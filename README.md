# KCBS Barbeque Competition Analytics

This project explores KCBS competition data from 2013-2016. I used Python (selenium, beautiful soup) to pull the data from the KCBS website. Data analysis will include choropleths (colored maps) based on competition meta-data, and state-by-state score data comparisons.

## Choropleths

The visuals folder contains choropleths on three measures in the data. These maps were made with Tableau. They include;

* [competitions per state](visuals/contest_counts_2016.png)
* [total prize dollars per state](visuals/total_prizing_2016.png)
* [average prize dollars per (prized) competition](visuals/average_prizing_2016.png)

## Scoring

In Progress...

Plotting the cumulative distribution function of category scores from the 5 most competing states (Missouri, Kansas, California, Tennessee, Georgia) seems to show stronger scoring in Georgia and Tennessee. 

[Comparative CDF plots of category scores](visuals/cdf_scores.png)

The similarity between plot lines correspond to geographic proximity and/or the number of contest held in each state (Georgia and Tennessee are 4th/5th).

The higher scores in Tennessee and Georgia may be a significant effect, but additional testing needs to look at the significance of these states' distributions while controlling for the sample size. Another culprit could be regional scoring biases.

## Team Names

Creative team names are a tradition of the competitive barbeque circuit. Using the team names from my data set, I created a [wordcloud](visuals/wordcloud.png) to visualize the themes of these names. An automatic name generator might be a fun challenge, but the names are often pun-y which could be hard to automate.

A full list of names can be found [on the KCBS website](https://www.kcbs.us/teams/all/1).

## Data Sources

Competition Data: http://www.kcbs.us/events.

A change in KCBS scoring standards went into effect on July 2013. Competition data is limited to contests after that date.

Scoring Information: http://www.kcbs.us/news.php?id=687

Feel free to reach out for csv/pickle files (pandas dataframes). The largest file (~50mb) holds every competition from July 2013 onwards, and includes score result sub-tables (chicken, ribs, pork, brisket, overall).
