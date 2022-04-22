# Importing the data and necessary commands.
import streamlit as st
import pandas as pd
import sqlite3

# #2. Database creation.

connection=sqlite3.connect("partnersearchapp.sqlite") #We are connecting to the database.
cur=connection.cursor()
participants.to_sql("Participants",connection,if_exists="replace", index=False)
projects.to_sql("Projects",connection,if_exists="replace", index=False)
countries.to_sql("Countries",connection,if_exists="replace",index=False)
projects.head() #Let's check how everything got imported into the database. In this case, we are using participants daataframe.

custom_participants=pd.read_sql('''SELECT projects.year, SUM(ecContribution) AS grants, countries.Country
FROM participants, projects, countries
WHERE participants.projectID == projects.projectID AND participants.country == countries.acronym 
GROUP BY projects.year''', connection)

option = st.selectbox('Country:', custom_participants['Country'])

custom_participants=pd.read_sql('''SELECT projects.year, SUM(ecContribution) AS grants, countries.Country
FROM participants, projects, countries
WHERE participants.projectID == projects.projectID AND participants.country == countries.acronym AND participants.country == '{}'
GROUP BY projects.year'''.format(option) , connection)

# Creating a plot of the overall aggregated contribution per year. This will allow us to see if we approached the problem correctly, and then proceed with the view per country.
custom_participants['grants'].plot(kind = 'bar', title = 'Total received grants overall by year')
st.bar_chart(custom_participants['grants'])
