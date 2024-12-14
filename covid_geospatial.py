import pandas as pd
import folium
from datetime import datetime
import streamlit as st
from streamlit_folium import folium_static

st.title("Sebaran Kasus Positif COVID-19 di Indonesia per 1 Mei 2021")

file_path = 'covid_19_indonesia_time_series_all.csv' 

covid_data = pd.read_csv(file_path)

covid_data['Date'] = pd.to_datetime(covid_data['Date'], format='%m/%d/%Y', errors='coerce')

filtered_data = covid_data[covid_data['Date'] == datetime(2021, 5, 1)]

# Agregasi data berdasarkan lokasi yang lebih spesifik
if 'City' in filtered_data.columns:
    group_by_columns = ['City', 'Latitude', 'Longitude']
else:
    group_by_columns = ['Province', 'Latitude', 'Longitude']

aggregated_data = (
    filtered_data.groupby(group_by_columns)
    .agg({'Total Cases': 'sum'})
    .reset_index()
)

# Buat peta interaktif dengan Folium
indonesia_map = folium.Map(location=[-2.5489, 118.0149], zoom_start=5)

# Tambahkan marker untuk setiap lokasi
for _, row in aggregated_data.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=row['Total Cases']**1 / 70,
        color='red',
        fill=True,
        fill_color='red',
        fill_opacity=0.6,
        popup=(
            f"Provinsi: {row['Province']}<br>"
            f"Total Kasus: {row['Total Cases']}"
        )
    ).add_to(indonesia_map)

folium_static(indonesia_map)
