import streamlit as st
import pandas as pd
import leafmap

# Load the dataset
df = pd.read_csv("open_source_data_v8.csv")

# Check and convert "Latitude" and "Longitude" to numeric if they are not already
if not pd.api.types.is_numeric_dtype(df["Latitude"]):
    df["Latitude"] = pd.to_numeric(df["Latitude"], errors="coerce")

if not pd.api.types.is_numeric_dtype(df["Longitude"]):
    df["Longitude"] = pd.to_numeric(df["Longitude"], errors="coerce")

# Create a leafmap map
m = leafmap.Map(center=[40, -100], zoom=4, tiles="stamentoner")

# Add a heatmap to the map
m.add_heatmap(
    df,
    latitude="Latitude",
    longitude="Longitude",
    value="Pincode",
    name="Heat map",
    radius=20,
)

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
        st.write(m)

if __name__ == "__main__":
    main()
