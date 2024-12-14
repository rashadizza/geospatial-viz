import pandas as pd
import folium
from datetime import datetime
import streamlit as st
from streamlit_folium import folium_static
import json
import os

st.title("Sebaran Kasus Positif COVID-19 di Indonesia per 1 Mei 2021")

# Load data
file_path = 'covid_19_indonesia_time_series_all.csv'
covid_data = pd.read_csv(file_path)

# Convert Date to datetime format
covid_data['Date'] = pd.to_datetime(covid_data['Date'], format='%m/%d/%Y', errors='coerce')
filtered_data = covid_data[covid_data['Date'] == datetime(2021, 5, 1)]

# Aggregate data per province
aggregated_data = (
    filtered_data.groupby(['Province'])
    .agg({'Total Cases': 'sum'})
    .reset_index()
)

# Load GeoJSON file for Indonesia provinces
geojson_path = 'indonesia.geojson'  # GeoJSON file for provinces
if not os.path.exists(geojson_path):
    st.error("GeoJSON file for Indonesia provinces is missing.")
else:
    with open(geojson_path, 'r') as f:
        provinces_geojson = json.load(f)

# Create the map
indonesia_map = folium.Map(location=[-2.5489, 118.0149], zoom_start=5)

# Add choropleth layer to the map
folium.Choropleth(
    geo_data=provinces_geojson,
    name='choropleth',
    data=aggregated_data,
    columns=['Province', 'Total Cases'],
    key_on='feature.properties.name',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Total Kasus Positif COVID-19'
).add_to(indonesia_map)

# Display map
folium_static(indonesia_map)
