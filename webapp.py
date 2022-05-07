# Importing the required libraries and modules
import streamlit as st
import pandas as pd
import sqlite3

# Connecting to the database
connection=sqlite3.connect("partnersearchapp.sqlite") 

# Image at the top of the webapp
st.image('KDT logo.jpg')

# Title of the webapp
st.title('Partner search tool')

# Dataframe to ensure only the existing countries in participants are shown in the select box
checked_countries = pd.read_sql('''SELECT countries.Country AS Country
FROM participants, countries
WHERE participants.country == countries.acronym''', connection)

# Saving the selected country in the select box
option = st.selectbox('Country:', checked_countries['Country'].unique())

# Creating the dataframe of participants of the selected country grouped by project year and in descending order of contribution
custom_participants=pd.read_sql('''SELECT participants.shortName, participants.name, participants.activityType, participants.organizationURL, COUNT(participants.projectID) as count_project, SUM(ecContribution) as sum_ecContribution, projects.year as year
FROM participants, projects, countries
WHERE participants.projectID == projects.projectID AND participants.country == countries.acronym AND countries.Country == '{}' 
GROUP BY projects.year
ORDER BY sum_ecContribution DESC'''.format(option) , connection, index_col = 'year')

# Creating a plot of the contribution per year of a given country
st.header('Yearly EC contribution in {} (€)'.format(option))
st.bar_chart(custom_participants['sum_ecContribution'])

# Printing the participants' dataframe
st.header('Participants in {}'.format(option))
st.write(custom_participants)

# Download button for the participants' dataset in csv format
st.download_button(label="Download the participants' dataset",data=custom_participants.to_csv().encode('utf-8'), file_name='Participants in {}.csv'.format(option), mime='text/csv')

# Creating the dataframe of coordinators of the selected country in ascending order by shortName
coordinators=pd.read_sql('''SELECT participants.shortName, participants.name, participants.activityType, projects.acronym
FROM participants, projects, countries
WHERE participants.projectID == projects.projectID AND participants.country == countries.acronym AND countries.Country == '{}' AND participants.role == "coordinator"
ORDER BY shortName'''.format(option) , connection)

# Printing the coordinators' dataframe with a condition in case it is empty
if len(coordinators.index) == 0:
  st.write('No project coordinators available in {}'.format(option))
else:
  st.header('Coordinators in {}'.format(option))
  st.write(coordinators)
  # Download button for the coordinators' dataset in csv format
  st.download_button(label="Download the coordinators' dataset",data=coordinators.to_csv().encode('utf-8'), file_name='Project coordinators in {}.csv'.format(option), mime='text/csv')
