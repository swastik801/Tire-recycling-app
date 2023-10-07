import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static
from sklearn.ensemble import RandomForestClassifier
import numpy as np

# Load the data
df = pd.read_csv("Tire_v1.csv", sep=',')

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

# Create a folium map
m = folium.Map(location=[40, -100], zoom_start=4)

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

    # Add a button for prediction
    if st.sidebar.button("Predict"):
        # Use trained model to make prediction
        tread_depth = st.sidebar.selectbox(
            "Select Tread Depth",
            df["Tread_Depth"].unique()
        )
        
        odometer_reading = st.sidebar.selectbox(
            "Select Odometer Reading",
            df["Odometer_Reading"].unique()
        )
        
        age = st.sidebar.selectbox(
            "Select Age",
            df["Age"].unique()
        )
        
        prediction = model.predict([[tread_depth, odometer_reading, age]])[0]
        st.write(f"AI algorithm predicts that condition of Tire is {prediction}")

    # Add a button for the heatmap
    if st.sidebar.button("Show Heatmap"):
        # Create a new DataFrame for heatmap data
        heatmap_data = df.groupby(['Latitude', 'Longitude']).size().reset_index(name='counts')

        # Add a heatmap layer to the map
        HeatMap(data=heatmap_data, radius=15).add_to(m)
        
        # Display the map with the heatmap
        folium_static(m)

if __name__ == "__main__":
    main()
