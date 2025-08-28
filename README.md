# PhonePe-Transaction-Insights
This project aims to analyze and visualize aggregated values of payment categories, create maps for total values at state and district levels, and identify top-performing states, districts, and pin codes.
# Streamlit Dashboard link
https://projectphonepe.streamlit.app/
# Objectives of the Project
Analyze digital payment trends.
Visualize transaction volumes and values.
Understand regional adoption patterns.
Our goal was to extract meaningful insights from the Pulse data and present them in a way that’s easy to understand and actionable.
# Tools & Technologies Used
Python (Pandas, Plotly)
Streamlit for dashboard
GitHub for version control
PhonePe Pulse API
Sqlalchemy
We used Python for data wrangling and visualization, and Streamlit to build an interactive dashboard. GitHub helped us collaborate and track changes.
# Data Collection & Cleaning
Extract JSON files from Pulse GitHub repo and this files are converted into dataframe using pandas..
The datafranes are pushed into Mysql using sqlalchemy in the Tidb cloud server and database is created.
The database has nine tables which are queryed and cleaned to get a structured data.
This datas are converted into .csv files using pandas.
This files are used in phonepe_dashgit.py tocreate dashboard using the streamlit app.
