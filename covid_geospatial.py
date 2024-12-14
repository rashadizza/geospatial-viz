import pandas as pd
import folium
from datetime import datetime
import streamlit as st
from streamlit_folium import folium_static

# CSS custom untuk mengubah background menjadi hitam
page_bg = """
<style>
body {
    background-color: black;
    color: white;
}
h1, h2, h3, h4, h5, h6 {
    color: white;
}
.stApp {
    background-color: black;
}
</style>
"""

# Menambahkan CSS ke dalam aplikasi Streamlit
st.markdown(page_bg, unsafe_allow_html=True)

# Judul Aplikasi
st.title("Sebaran Kasus Positif COVID-19 di Indonesia per 1 Mei 2021")

# Path ke file data
file_path = 'covid_19_indonesia_time_series_all.csv' 

# Load data COVID-19
covid_data = pd.read_csv(file_path)

# Konversi kolom Date ke datetime
covid_data['Date'] = pd.to_datetime(covid_data['Date'], format='%m/%d/%Y', errors='coerce')

# Filter data untuk tanggal 1 Mei 2021
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
        radius=row['Total Cases']**0.5 / 70,
        color='red',
        fill=True,
        fill_color='red',
        fill_opacity=0.6,
        popup=(
            f"Provinsi: {row['Province']}<br>"
            f"Total Kasus: {row['Total Cases']}"
        )
    ).add_to(indonesia_map)

# Tampilkan peta
folium_static(indonesia_map)
