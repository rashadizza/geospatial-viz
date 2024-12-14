import pandas as pd
import folium
from datetime import datetime
import streamlit as st
from streamlit_folium import folium_static

st.title("Sebaran Kasus Positif COVID-19 di Indonesia per 1 Mei 2021")

# Path ke file data
file_path = 'covid_19_indonesia_time_series_all.csv' 

# Load data COVID-19
covid_data = pd.read_csv(file_path)

# Konversi kolom Date ke datetime
covid_data['Date'] = pd.to_datetime(covid_data['Date'], format='%m/%d/%Y', errors='coerce')

# Filter data untuk tanggal 1 Mei 2021
filtered_data = covid_data[covid_data['Date'] == datetime(2021, 5, 1)]

# Agregasi data berdasarkan lokasi yang lebih spesifik jika tersedia
if 'City' in filtered_data.columns:
    group_by_columns = ['City', 'Latitude', 'Longitude']
else:
    group_by_columns = ['Province', 'Latitude', 'Longitude']  # Gunakan Provinsi jika City tidak tersedia

# Agregasi Total Kasus
aggregated_cases = (
    filtered_data.groupby(group_by_columns)
    .agg({'Total Cases': 'sum'})
    .reset_index()
)

# Agregasi Total Kematian
aggregated_deaths = (
    filtered_data.groupby(group_by_columns)
    .agg({'Total Deaths': 'sum'})
    .reset_index()
)

# Peta 1: Total Kasus COVID-19
indonesia_map_cases = folium.Map(location=[-2.5489, 118.0149], zoom_start=5)
marker_cluster_cases = MarkerCluster().add_to(indonesia_map_cases)

for _, row in aggregated_cases.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=row['Total Cases']**0.5 / 100,  # Skala ukuran lingkaran
        color='blue',
        fill=True,
        fill_color='blue',
        fill_opacity=0.6,
        popup=(
            f"Lokasi: {row[group_by_columns[0]]}<br>"
            f"Total Kasus: {row['Total Cases']}"
        )
    ).add_to(marker_cluster_cases)

# Peta 2: Total Kematian COVID-19
indonesia_map_deaths = folium.Map(location=[-2.5489, 118.0149], zoom_start=5)
marker_cluster_deaths = MarkerCluster().add_to(indonesia_map_deaths)

for _, row in aggregated_deaths.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=row['Total Deaths']**0.5 / 50,  # Skala ukuran lingkaran
        color='red',
        fill=True,
        fill_color='red',
        fill_opacity=0.6,
        popup=(
            f"Lokasi: {row[group_by_columns[0]]}<br>"
            f"Total Kematian: {row['Total Deaths']}"
        )
    ).add_to(marker_cluster_deaths)

# Tampilkan kedua peta secara bersamaan
print("Peta Total Kasus:")
display(indonesia_map_cases)
print("\nPeta Total Kematian:")
display(indonesia_map_deaths)
