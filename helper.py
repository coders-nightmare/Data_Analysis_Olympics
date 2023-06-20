import pandas as pd
import numpy as np

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

def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
        x['Year'] = x['Year'].astype('str')
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')

    return x
def country_year_list(df):
    years=df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'Overall')

    countries=np.unique(df['region'].dropna().values).tolist()
    countries.sort()
    countries.insert(0,'Overall')

    return years,countries

def participating_nations_over_time(df):
    nations_over_time=df.drop_duplicates(['Year','region'])['Year'].value_counts().reset_index().sort_values('Year')
    return nations_over_time

def events_played_over_time(df):
    events_over_time=df.drop_duplicates(['Year','Event'])['Year'].value_counts().reset_index().sort_values('Year')
    return events_over_time
def athletes_played_over_time(df):
    athletes_over_time=df.drop_duplicates(['Year','Name'])['Year'].value_counts().reset_index().sort_values('Year')
    return athletes_over_time
def most_successful(df,sport):
    temp_df=df.dropna(subset=['Medal'])
    
    if sport !='Overall':
        temp_df=temp_df[temp_df['Sport']==sport]
    x= temp_df['Name'].value_counts().reset_index().head(15).merge(df,on='Name',how='left')[['Name','count','Sport','region']].drop_duplicates('Name')
    x.rename(columns={'count':'Medals'},inplace=True)
    return x

def yearwise_medal_tally(df,country):
    temp_df=df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)

    new_df=temp_df[temp_df['region']==country]
    final_df=new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df

def country_event_heatmap(df,country):
    temp_df=df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)

    new_df=temp_df[temp_df['region']==country]
    pt=new_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0)
    return pt

def most_successful_countrywise(df,country):
    temp_df=df.dropna(subset=['Medal'])
    
    temp_df=temp_df[temp_df['region']==country]
    x= temp_df['Name'].value_counts().reset_index().head(10).merge(df,on='Name',how='left')[['Name','count','Sport']].drop_duplicates('Name')
    x.rename(columns={'count':'Medals'},inplace=True)
    return x

