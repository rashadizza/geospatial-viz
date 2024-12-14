import pandas as pd
import folium
from datetime import datetime
import streamlit as st
from streamlit_folium import folium_static
import os

st.title("Sebaran Kasus Positif COVID-19 di Indonesia per 1 Mei 2021")

file_path = 'covid_19_indonesia_time_series_all.csv' 
covid_data = pd.read_csv(file_path)

covid_data['Date'] = pd.to_datetime(covid_data['Date'], format='%m/%d/%Y', errors='coerce')
filtered_data = covid_data[covid_data['Date'] == datetime(2021, 5, 1)]

aggregated_data = (
    filtered_data.groupby(['Province', 'Latitude', 'Longitude'])
    .agg({'Total Cases': 'sum'})
    .reset_index()
)

indonesia_map = folium.Map(location=[-2.5489, 118.0149], zoom_start=5)

# Tambahkan blok warna berdasarkan jumlah kasus
for _, row in aggregated_data.iterrows():
    geo_json = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [row['Longitude'] - 0.5, row['Latitude'] - 0.5],
                            [row['Longitude'] + 0.5, row['Latitude'] - 0.5],
                            [row['Longitude'] + 0.5, row['Latitude'] + 0.5],
                            [row['Longitude'] - 0.5, row['Latitude'] + 0.5],
                            [row['Longitude'] - 0.5, row['Latitude'] - 0.5]
                        ]
                    ]
                },
                "properties": {
                    "Total Cases": row['Total Cases']
                }
            }
        ]
    }

    color = "#ffcccc" if row['Total Cases'] < 1000 else "#ff6666" if row['Total Cases'] < 10000 else "#cc0000"

    folium.GeoJson(
        geo_json,
        style_function=lambda feature, color=color: {
            "fillColor": color,
            "color": "black",
            "weight": 0.5,
            "fillOpacity": 0.6
        }
    ).add_to(indonesia_map)

folium_static(indonesia_map)
