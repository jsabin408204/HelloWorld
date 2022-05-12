# Importing the required libraries and modules
import streamlit as st
import pandas as pd
import sqlite3
import numpy as np

# Connecting to the database
connection=sqlite3.connect("partnersearchapp.sqlite") 

# Image at the top of the webapp
st.image('KDT logo.jpg')

# Title of the webapp
st.title('Partner search tool')

# Dataframe to ensure only the existing countries in participants are shown in the select box and to have their acronyms
checked_countries = pd.read_sql('''SELECT countries.Country AS Country, countries.Acronym AS Acronym
FROM participants, countries
WHERE participants.country == countries.acronym''', connection)

# Saving the selected country from the select box, generating its acronym and printing the chosen country with its acronym
country_option = st.selectbox('Country:', checked_countries['Country'].unique())
acronym_option = checked_countries[checked_countries['Country'] == country_option].Acronym.sample().item()
st.write('You selected {}-{}'.format(acronym_option, country_option))

year_preference = st.sidebar.radio('Display preference:', ['All years', 'Specific year'])

if year_preference == 'Specific year':
  checked_year = pd.read_sql('''SELECT projects.year AS Year FROM projects, participants 
  WHERE participants.country == '{}' AND participants.projectID == projects.projectID'''.format(acronym_option), connection)
  year_option = st.selectbox('Year:', np.unique(checked_year['Year']))
  custom_participants=pd.read_sql('''SELECT participants.shortName, participants.name, participants.activityType, participants.organizationURL, COUNT(participants.projectID) as count_project, SUM(ecContribution) as sum_ecContribution, projects.year as year
  FROM participants, projects, countries
  WHERE participants.projectID == projects.projectID AND participants.country == countries.acronym AND countries.Country == '{}' AND projects.year == '{}'
  GROUP BY projects.year
  ORDER BY sum_ecContribution DESC'''.format(country_option, year_option), connection, index_col = 'year')
  coordinators=pd.read_sql('''SELECT participants.shortName, participants.name, participants.activityType, projects.acronym, projects.year AS year
  FROM participants, projects, countries
  WHERE participants.projectID == projects.projectID AND participants.country == countries.acronym AND countries.Country == '{}' AND participants.role == "coordinator" AND projects.year == '{}'
  ORDER BY shortName'''.format(country_option, year_option), connection, index_col = 'year')
else:
  custom_participants=pd.read_sql('''SELECT participants.shortName, participants.name, participants.activityType, participants.organizationURL, COUNT(participants.projectID) as count_project, SUM(ecContribution) as sum_ecContribution, projects.year as year
  FROM participants, projects, countries
  WHERE participants.projectID == projects.projectID AND participants.country == countries.acronym AND countries.Country == '{}'
  GROUP BY projects.year
  ORDER BY sum_ecContribution DESC'''.format(country_option), connection, index_col = 'year')
  coordinators=pd.read_sql('''SELECT participants.shortName, participants.name, participants.activityType, projects.acronym, projects.year AS year
  FROM participants, projects, countries
  WHERE participants.projectID == projects.projectID AND participants.country == countries.acronym AND countries.Country == '{}' AND participants.role == "coordinator"
  ORDER BY shortName'''.format(country_option), connection, index_col = 'year')

# Creating a plot of the contribution per year of a given country
st.header('Yearly EC contribution in {} (€)'.format(country_option))
st.bar_chart(custom_participants['sum_ecContribution'])
if year_preference == 'All years':
  with st.expander('See difference between two years'):
    available_years = custom_participants.index.tolist()
    available_years.sort()
    first_year = st.radio('First year:', available_years)
    available_years_after = [year for year in available_years if year > first_year]
    if len(available_years_after) > 0:
      second_year = st.radio('Second year:', available_years_after)
      difference = custom_participants.loc[second_year, 'sum_ecContribution'] - custom_participants.loc[first_year, 'sum_ecContribution']
      st.metric('''Aggregated grants in {} and change with respect to {} '''.format(second_year, first_year), custom_participants.loc[second_year, 'sum_ecContribution'], round(difference,2))
    else:
      st.write('''No available years after {} '''.format(int(first_year)))

# Printing the participants' dataframe
st.header('Participants in {}'.format(country_option))
st.write(custom_participants)

# Download button for the participants' dataset in csv format
st.download_button(label="Download the participants' dataset",data=custom_participants.to_csv().encode('utf-8'), file_name='Participants in {}.csv'.format(country_option), mime='text/csv')

# Printing the coordinators' dataframe with a condition in case it is empty for a given country
st.header('Project coordinators in {}'.format(country_option))
if len(coordinators.index) == 0:
  st.write('No project coordinators available in {}'.format(country_option))
else:
  st.write(coordinators)
  # Download button for the coordinators' dataset in csv format
  st.download_button(label="Download the coordinators' dataset",data=coordinators.to_csv().encode('utf-8'), file_name='Project coordinators in {}.csv'.format(country_option), mime='text/csv')
