import streamlit as st
import pandas as pd
import sqlite3

connection=sqlite3.connect("partnersearchapp.sqlite") #We are connecting to the database.

dropcountries=pd.read_sql('''SELECT Country FROM countries''',connection)

st.image('KDT logo.jpg')

st.title('Partner search tool')

# Creating a dataframe to ensure only the existing countries are shown in the select box
checked_countries = pd.read_sql('''SELECT countries.Country AS Country
FROM participants, countries
WHERE participants.country == countries.acronym''', connection)

option = st.selectbox('Country:', checked_countries['Country'].unique())

custom_participants=pd.read_sql('''SELECT participants.shortName, participants.name, participants.activityType, participants.organizationURL, COUNT(participants.projectID) as count_project, SUM(ecContribution) as sum_ecContribution, projects.year as year
FROM participants, projects, countries
WHERE participants.projectID == projects.projectID AND participants.country == countries.acronym AND countries.Country == '{}' 
GROUP BY projects.year
ORDER BY sum_ecContribution DESC'''.format(option) , connection, index_col = 'year')

st.write(custom_participants)

# Creating a plot of the overall aggregated contribution per year. This will allow us to see if we approached the problem correctly, and then proceed with the view per country.
st.header('Yearly EC contribution in {} (€)'.format(option))
st.bar_chart(custom_participants['sum_ecContribution'])

st.header('Participants in {}'.format(option))
st.write(custom_participants)
