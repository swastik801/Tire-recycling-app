import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static
from sklearn.ensemble import RandomForestClassifier

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

    # Add dropdowns for Tread_Depth, Odometer_Reading and Age
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

    # Add a button for the heatmap
    if st.sidebar.button("Show Heatmap"):
        folium_static(m)
        
    # Add a button for prediction
    if st.sidebar.button("Predict"):
        # Use trained model to make prediction
        prediction = model.predict([[tread_depth, odometer_reading, age]])[0]
        st.write(f"AI algorithm predicts that condition of Tire is {prediction}")

if __name__ == "__main__":
    main()
