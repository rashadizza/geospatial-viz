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

# filter data dari tanggal 1 Mei 2021
df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y', errors='coerce')
filtered_data = df[df['Date'] == datetime(2021, 5, 1)]

# kelompok data berdasarkan provinsi dan hitung total kasus positif
aggregated_data = (
    filtered_data.groupby(['Province', 'Latitude', 'Longitude'])
    .agg({'Total Cases': 'sum'})
    .reset_index()
)

# membuat peta menggunakan folium
indonesia_map = folium.Map(location=[-2.5489, 118.0149], zoom_start=5)
# Peta 1: Total Kasus COVID-19
indonesia_map_cases = folium.Map(location=[-2.5489, 118.0149], zoom_start=5)
marker_cluster_cases = MarkerCluster().add_to(indonesia_map_cases)

for _, row in aggregated_data.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=row['Total Cases']**0.5 / 100,
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
