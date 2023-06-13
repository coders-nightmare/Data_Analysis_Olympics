import pandas as pd


def medal_tally(df):
    # df.groupby('NOC').sum()[['Gold','Silver','Bronze']].sort_values(['Gold','Silver','Bronze'],ascending=False)
    # we can see that medal tally is not match original tally because it is based on players not on country therefore in team events it is counting one gold medal multiple times as it is distributed to each player

    # Solving it by removing duplicates on the basis of
    #team,noc,games,year, city, sport,event and medal

    medal_tally = df.drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values(
        ['Gold', 'Silver', 'Bronze'], ascending=False).reset_index()
    medal_tally['Total'] = medal_tally[[
        'Gold', 'Silver', 'Bronze']].sum(axis=1)

    medal_tally[['Gold', 'Silver', 'Bronze', 'Total']
                ] = medal_tally[['Gold', 'Silver', 'Bronze', 'Total']].apply(pd.to_numeric)
    return medal_tally
