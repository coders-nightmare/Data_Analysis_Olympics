import streamlit as st
import pandas as pd
import preprocessor
import helper

df = pd.read_csv('./athlete_events.csv')
region_df = pd.read_csv("./noc_regions.csv")
df = preprocessor.preprocess(df, region_df)

user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis',
     'Country-wise Analysis', 'Athlete wise Analysis')
)


if user_menu == 'Medal Tally':
    st.title(user_menu)
    medal_tally = helper.medal_tally(df)
    st.dataframe(medal_tally)
else:
    st.title('Medal List Of Each Player')
    st.dataframe(df)
