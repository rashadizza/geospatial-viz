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

aggregated_data = (
    filtered_data.groupby(group_by_columns)
    .agg({'Total Cases': 'sum'})
    .reset_index()
)

# Buat peta interaktif dengan Folium
indonesia_map = folium.Map(location=[-2.5489, 118.0149], zoom_start=5)

# Tambahkan marker untuk setiap lokasi pada tingkat detail lebih tinggi
for _, row in aggregated_data.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=row['Total Cases']**0.5 / 50,  # Sesuaikan skala ukuran lingkaran
        color='blue',
        fill=True,
        fill_color='blue',
        fill_opacity=0.6,
        popup=(
            f"Lokasi: {row[group_by_columns[0]]}<br>"
            f"Total Kasus: {row['Total Cases']}"
        )
    ).add_to(indonesia_map)

# Tampilkan peta di Streamlit
folium_static(indonesia_map)
