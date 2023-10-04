import streamlit as st
import pandas as pd
import numpy as np
import folium
from folium.plugins import HeatMap
from sklearn.ensemble import RandomForestClassifier

# Load data from Streamlit GitHub repository
data = pd.read_csv("open_source_data_v8.csv", sep=',')

# Sidebar
st.sidebar.image("Tire_image.jpeg")
tire_brand = st.sidebar.selectbox("Tire Brand", data['Tire_Brand'].unique())
location = st.sidebar.selectbox("Location", data['Location'].unique())
heatmap_button = st.sidebar.button("Heatmap")

# Main content
st.title("Tire Recycling AI App")
st.write("Select Tire Brand and Location to view heatmap, and then predict tire condition.")

if heatmap_button:
    st.subheader("Heatmap of Tire Brand Counts")
    
    # Filter data based on selected Tire Brand and Location
    filtered_data = data[(data['Tire_Brand'] == tire_brand) & (data['Location'] == location)]
    
    # Create a heatmap using Folium
    m = folium.Map(location=[0, 0], zoom_start=1)
    heat_data = [[row['Latitude'], row['Longitude']] for index, row in filtered_data.iterrows()]
    HeatMap(heat_data).add_to(m)
    
    # Display the map
    st.write(m)

    # Dropdowns for additional features
    st.subheader("Select Tread Depth, Odometer Reading, and Age:")
    tread_depth = st.selectbox("Tread Depth", list(range(3, 13)))
    odometer_reading = st.selectbox("Odometer Reading", list(range(10000, 60001, 1000)))
    age = st.selectbox("Age", list(range(1, 6)))
    predict_button = st.button("Predict")

    if predict_button:
        # Mock prediction using a RandomForest classifier (you should replace this with your actual model)
        X = filtered_data[['Tread_Depth', 'Odometer_Reading', 'Age']]
        y = filtered_data['Condition']
        clf = RandomForestClassifier()
        clf.fit(X, y)
        prediction = clf.predict([[tread_depth, odometer_reading, age]])

        st.subheader("AI Prediction Result:")
        if prediction[0] == 'Used':
            st.write("AI algorithm predicts that the condition of the tire is used.")
        else:
            st.write("AI algorithm predicts that the tire has to be scrapped.")
