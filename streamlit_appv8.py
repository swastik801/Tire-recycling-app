import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static
from sklearn.ensemble import RandomForestClassifier
import numpy as np

# Load the data
df = pd.read_csv("Tire_3.csv", sep=',', header=0)

# Check if the DataFrame is loaded correctly
if "Latitude" in df.columns and "Longitude" in df.columns:
    st.write("DataFrame loaded successfully.")
else:
    st.write("Error: Latitude and Longitude columns not found in the DataFrame.")
    st.stop()  # Stop the Streamlit app if there's an issue with the dataset

# Convert Tread_Depth to float and replace NaN values with 0
df['Tread_Depth'] = pd.to_numeric(df['Tread_Depths'], errors='coerce')
df['Tread_Depth'].fillna(0, inplace=True)

# Replace infinite values with finite numbers
df.replace([np.inf, -np.inf], np.nan, inplace=True)

# Aggregate count of Tire Brand for each location
df_agg = df.groupby(['Latitude', 'Longitude', 'Tire Brand']).size().reset_index(name='counts')

# Prepare data for Random Forest model
X = df[['Tread_Depth', 'Odometer_Reading', 'Age']]
y = df['Condition']  # Assuming 'Condition' is your target variable

# Train Random Forest model
model = RandomForestClassifier(random_state=42)
model.fit(X, y)

# Streamlit app
def main():
    st.title("Tyre Recycling Sustainability")

    # Add a big, bold message to the app
    st.markdown("<h1 style='text-align: center; font-size: 50px; font-family: Arial, sans-serif;'>Remaining Life of Tyre</h1>", unsafe_allow_html=True)

    # Display the image
    st.image("Tire_image.jpeg", use_column_width=True)

    # Create a sidebar
    st.sidebar.header("Options")

    # Add dropdowns for Odometer_Reading, Age, and Tread_Depth
    odometer_reading = st.sidebar.selectbox(
        "Select Odometer Reading",
        [None] + list(df["Odometer_Reading"].unique())
    )
    
    age = st.sidebar.selectbox(
        "Select Age",
        [None] + list(df["Age"].unique())
    )
    
    tread_depth = st.sidebar.selectbox(
        "Select Tread Depth",
        [None] + list(df["Tread_Depth"].unique())
    )

    # Add "Tire Brand" and "Location" dropdowns with default blank values
    tire_brand = st.sidebar.selectbox(
        "Select Tire Brand",
        [None] + list(df["Tire Brand"].unique())
    )
    
    location = st.sidebar.selectbox(
        "Select Location",
        [None] + list(df["Location"].unique())
    )

    # Calculate remaining life of tire based on tread depth and display visualization
    if odometer_reading is not None and age is not None and tread_depth is not None:
        remaining_life = model.predict([[tread_depth, odometer_reading, age]])
        if remaining_life == 1:
            st.markdown("<p style='color:green; font-weight: bold;'>This tire can be reused!</p>", unsafe_allow_html=True)
        else:
            st.markdown("<p style='color:red; font-weight: bold;'>This tire should be scrapped.</p>", unsafe_allow_html=True)

    # Show heatmap button if both Tire Brand and Location are selected
    if tire_brand is not None and location is not None:
        if st.button("Show Heatmap"):
            # Create a map using Folium and display it in Streamlit
            m = folium.Map(location=[df['Latitude'].mean(), df['Longitude'].mean()], zoom_start=6)
            heat_data = [[row['Latitude'], row['Longitude']] for index, row in df[(df['Tire Brand'] == tire_brand) & (df['Location'] == location)].iterrows()]
            HeatMap(heat_data).add_to(m)
            folium_static(m)
    
if __name__ == "__main__":
    main()
