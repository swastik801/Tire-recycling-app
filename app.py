import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap

# Load the data
df = pd.read_csv("open_source_data_v8.csv", sep=',')

# Check if the DataFrame is loaded correctly
if "Latitude" in df.columns and "Longitude" in df.columns:
    st.write("DataFrame loaded successfully.")
else:
    st.write("Error: Latitude and Longitude columns not found in the DataFrame.")
    st.stop()  # Stop the Streamlit app if there's an issue with the dataset

# Aggregate count of Tire Brand for each location
df_agg = df.groupby(['Latitude', 'Longitude', 'Tire Brand']).size().reset_index(name='counts')

# Create a folium map
m = folium.Map(location=[40, -100], zoom_start=4)

# Add a heatmap to the map
HeatMap(data=df_agg[['Latitude', 'Longitude', 'counts']].values.tolist()).add_to(m)

# Streamlit app
def main():
    st.title("Tyre Recycling Sustainability")

    # Display the image
    st.image("Tire_image.jpeg", use_column_width=True)

    # Create a sidebar
    st.sidebar.header("Options")

    # Add a selectbox for the tire brands
    brand = st.sidebar.selectbox(
        "Select a Tire Brand",
        df["Tire Brand"].unique()
    )

    # Add a selectbox for the locations
    location = st.sidebar.selectbox(
        "Select a Location",
        df["Location"].unique()
    )

    # Add a button for the heatmap
    if st.sidebar.button("Show Heatmap"):
        folium_static(m)

if __name__ == "__main__":
    main()
