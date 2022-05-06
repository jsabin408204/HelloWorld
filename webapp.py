import streamlit as st
import pandas as pd
import sqlite3

connection=sqlite3.connect("partnersearchapp.sqlite") #We are connecting to the database.

dropcountries=pd.read_sql('''SELECT Country FROM countries''',connection)

st.title('Partner search tool')

option = st.selectbox('Country:', dropcountries["Country"].unique())

custom_participants=pd.read_sql('''SELECT projects.year, SUM(ecContribution) AS Grants, countries.Country
FROM participants, projects, countries
WHERE participants.projectID == projects.projectID AND participants.country == countries.acronym AND countries.Country == '{}' 
GROUP BY projects.year'''.format(option) , connection)

# Creating a plot of the overall aggregated contribution per year. This will allow us to see if we approached the problem correctly, and then proceed with the view per country.
st.header('Yearly EC contribution in {} (€)'.format(option))
st.bar_chart(custom_participants['grants'])

best=pd.read_sql('''SELECT participants.shortName, participants.name, participants.activityType, participants.organizationURL
FROM participants, projects, countries
WHERE participants.projectID == projects.projectID AND participants.country == countries.acronym AND countries.Country == '{}' 
GROUP BY projects.year'''.format(option) , connection)

st.header('Participants in {}'.format(option))
st.write(best)
