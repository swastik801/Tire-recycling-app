import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from folium.plugins import HeatMap

# Load the data
data = pd.read_csv('open_source_datasetv2.csv')

# Calculate the number of recycled tires at each location
recycled_tires = data.groupby(['Latitude', 'Longitude', 'Tire Brand', 'Recycling Facility']).size().reset_index(name='RecycledTires')

# Create a select box for the tire brands
selected_brand = st.selectbox('Select a tire brand', recycled_tires['Tire Brand'].unique())

# Filter the data for the selected tire brand
filtered_data = recycled_tires[recycled_tires['Tire Brand'] == selected_brand]

# Create a select box for the recycling facilities
selected_facility = st.selectbox('Select a recycling facility', filtered_data['Recycling Facility'].unique())

# Filter the data for the selected recycling facility
filtered_data = filtered_data[filtered_data['Recycling Facility'] == selected_facility]

# Create a map centered around the mean latitude and longitude values
m = folium.Map(location=[filtered_data['Latitude'].mean(), filtered_data['Longitude'].mean()], zoom_start=13)

# Create a heatmap layer and add it to the map
HeatMap(filtered_data[['Latitude', 'Longitude', 'RecycledTires']].values.tolist()).add_to(m)

# Display the map in the Streamlit app
folium_static(m)
