import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static
from sklearn.ensemble import RandomForestClassifier
import numpy as np

# Load the data
df = pd.read_csv("Tire_2.csv", sep=',')

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

    # Display the image
    st.image("Tire_image.jpeg", use_column_width=True)

    # Create a sidebar
    st.sidebar.header("Options")

    # Add dropdowns for Odometer_Reading and Age
    odometer_reading = st.sidebar.selectbox(
        "Select Odometer Reading",
        [None] + list(df["Odometer_Reading"].unique())
    )
    
    age = st.sidebar.selectbox(
        "Select Age",
        [None] + list(df["Age"].unique())
    )

    # Add a button for prediction below Age option
    if odometer_reading is not None and age is not None and st.sidebar.button("Predict"):
        # Use trained model to make prediction
        prediction = model.predict([[0, odometer_reading, age]])[0]
        st.write(f"AI algorithm predicts that condition of Tire is {prediction}")

    # Add a selectbox for the tire brands and location
    brand = st.sidebar.selectbox(
        "Select a Tire Brand",
        [None] + list(df["Tire Brand"].unique())
    )

    location = st.sidebar.selectbox(
        "Select a Location",
        [None] + list(df["Location"].unique())
    )

    # Add a button for the heatmap below location option
    if brand is not None and location is not None and st.sidebar.button("Show Heatmap"):
        # Filter df_agg based on selected brand and location
        heatmap_data = df_agg[df_agg['Tire Brand'] == brand]
        
        # Get latitude and longitude of selected location
        lat, lon = df[df['Location'] == location][['Latitude', 'Longitude']].values[0]
        
        # Create a folium map centered at selected location
        m = folium.Map(location=[lat, lon], zoom_start=4)
        
        # Add a heatmap to the map based on filtered data
        HeatMap(data=heatmap_data[['Latitude', 'Longitude', 'counts']].values.tolist()).add_to(m)
        
        # Display the map with the heatmap
        folium_static(m)

if __name__ == "__main__":
    main()
