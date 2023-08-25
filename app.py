import plotly.figure_factory as ff
import streamlit as st
import pandas as pd
import preprocessor
import helper
import seaborn as sns 
import plotly.express as px 
import matplotlib.pyplot as plt

df = pd.read_csv('./athlete_events.csv')
region_df = pd.read_csv("./noc_regions.csv")
df = preprocessor.preprocess(df, region_df)
st.sidebar.title("Olympic Analysis")
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis',
     'Country-wise Analysis', 'Athlete wise Analysis')
)


if user_menu == 'Medal Tally':
    st.sidebar.title(user_menu)
    years,countries=helper.country_year_list(df)
    selected_year=st.sidebar.selectbox("Select Year",years)
    selected_country=st.sidebar.selectbox("Select Country",countries)
    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year) + " Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " overall performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " performance in " + str(selected_year) + " Olympics")
    st.table(medal_tally)
if user_menu=='Overall Analysis':
    editions=df['Year'].unique().shape[0]-1
    #olympic 1906 is discarded
    cities=df['City'].unique().shape[0]
    sports=df['Sport'].unique().shape[0]
    events=df['Event'].unique().shape[0]
    athletes=df['Name'].unique().shape[0]
    nations=df['region'].unique().shape[0]
    st.title("Top Statistics")
    col1,col2,col3=st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Hosts')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)
    col1,col2,col3=st.columns(3)
    with col1:
        st.header('Events')
        st.title(events)
    with col2:
        st.header('Nations')
        st.title(nations)
    with col3:
        st.header('Atheletes')
        st.title(athletes)
    
    st.title("Participating Nations Over The Years")
    nations_over_time=helper.participating_nations_over_time(df)
    fig=px.line(nations_over_time,x="Year",y="count")
    st.plotly_chart(fig)
    fig,ax=plt.subplots()
    ax=sns.barplot(data=nations_over_time,x='Year',y='count')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

    st.title("Events Held Over The Years")
    events_over_time=helper.events_played_over_time(df)
    fig=px.line(events_over_time,x="Year",y="count")
    st.plotly_chart(fig)
    fig,ax=plt.subplots()
    ax=sns.barplot(data=events_over_time,x='Year',y='count')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

    st.title("Athletes Played Over The Years")
    athletes_over_time=helper.athletes_played_over_time(df)
    fig=px.line(athletes_over_time,x="Year",y="count")
    st.plotly_chart(fig)
    fig,ax=plt.subplots()
    ax=sns.barplot(data=athletes_over_time,x='Year',y='count')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

    st.title("No. of Events Over Time(Every Sport)")
    x=df.drop_duplicates(['Year','Sport','Event'])
    pivot_table_events=x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0)
    fig,ax=plt.subplots(figsize=(20,20))
    ax=sns.heatmap(pivot_table_events,annot=True)
    st.pyplot(fig)


    st.title("Most Successful Athletes")
    sport_list=df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport=st.selectbox('Select a sport',sport_list)
    x=helper.most_successful(df,selected_sport)
    st.table(x)

if user_menu=='Country-wise Analysis':
    st.sidebar.title('Country-Wise Analysis')

    country_list=df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country=st.sidebar.selectbox("Select a Country",country_list)
    country_df=helper.yearwise_medal_tally(df,selected_country)
    # st.table(country_df)
    fig=px.line(country_df,x='Year',y='Medal')
    st.title(selected_country+' Medal Tally Over The Years')
    st.plotly_chart(fig)
    try:
        st.title(selected_country+' excels in the following sports')
        pt=helper.country_event_heatmap(df,selected_country)
        fig,ax=plt.subplots(figsize=(20,20))
        ax=sns.heatmap(pt,annot=True)
        st.pyplot(fig)
    except:
        st.title('None')

    st.title("Top 10 Athletes of "+selected_country)
    top10_df=helper.most_successful_countrywise(df,selected_country)
    st.table(top10_df)

if user_menu=='Athlete wise Analysis':

    athlete_df=df.drop_duplicates(['Name','region'])


    x1=athlete_df['Age'].dropna()
    x2=athlete_df[athlete_df['Medal']=='Gold']['Age'].dropna()
    x3=athlete_df[athlete_df['Medal']=='Silver']['Age'].dropna()
    x4=athlete_df[athlete_df['Medal']=='Bronze']['Age'].dropna()

    fig=ff.create_distplot([x1,x2,x3,x4],['Age Distribution','Gold Medalist','Silver Medalist',
    'Bronze Medalist'],show_hist=False,show_rug=False)
    # fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    #sport wise age distribution
    x=[]
    name=[]
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
    'Swimming', 'Badminton', 'Sailing', 'Gymnastics','Art Competitions', 'Handball', 'Weightlifting', 'Wrestling','Water Polo', 'Hockey', 'Rowing', 'Fencing','Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing','Tennis', 'Golf', 'Softball', 'Archery','Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
    'Rhythmic Gymnastics', 'Rugby Sevens',
    'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df=athlete_df[athlete_df['Sport']==sport]
        x.append(temp_df[temp_df['Medal']=='Gold']['Age'].dropna())
        name.append(sport)

    
    fig=ff.create_distplot(x,name,show_hist=False,show_rug=False)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    sport_list=df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df,selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(data=temp_df,x="Weight",y='Height',hue="Medal",style='Sex',s=60)
    st.pyplot(fig)

    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    st.plotly_chart(fig)

