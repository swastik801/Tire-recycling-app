import streamlit as st
import pandas as pd
import leafmap

# Load the datas
df = pd.read_csv("open_source_data_v8.csv")

# Create a leafmap map
m = leafmap.Map(center=[40, -100], zoom=4, tiles="stamentoner")

# Add a heatmap to the map
m.add_heatmap(
    "open_source_data_v8.csv",
    latitude="latitude",
    longitude="longitude",
    value="pop_max",
    name="Heat map",
    radius=20,
)

# Streamlit app
def main():
    st.title("Tyre Recycling Sustainability")

    # Display the image
    st.image("Tire_image.jpeg")

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
        st.pydeck_chart(m)

if __name__ == "__main__":
    main()
