# Importing the data and necessary commands.
import streamlit as st
import pandas as pd
import sqlite3

# #2. Database creation.

connection=sqlite3.connect("partnersearchapp.sqlite") #We are connecting to the database.
cur=connection.cursor()

custom_participants=pd.read_sql('''SELECT projects.year, SUM(ecContribution) AS grants, countries.Country
FROM participants, projects, countries
WHERE participants.projectID == projects.projectID AND participants.country == countries.acronym 
GROUP BY projects.year''', connection)

print(custom_participants)

option = st.selectbox('Country:', custom_participants['Country'].unique())

custom_participants=pd.read_sql('''SELECT projects.year, SUM(ecContribution) AS grants, countries.Country
FROM participants, projects, countries
WHERE participants.projectID == projects.projectID AND participants.country == countries.acronym AND countries.Country == '{}' 
GROUP BY projects.year'''.format(option) , connection)

# Creating a plot of the overall aggregated contribution per year. This will allow us to see if we approached the problem correctly, and then proceed with the view per country.
st.bar_chart(custom_participants['grants'])