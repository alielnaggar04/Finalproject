import streamlit as st
import pandas as pd
import pydeck as pdk
import matplotlib.pyplot as plt
import numpy as np

# Function to load and process data
def load_data(path):
    df = pd.read_csv(path)
    df.rename(columns={"LONGITUDE": "lon", "LATITUDE": "lat"}, inplace=True)
    return df

# Load the data
df_bos = load_data("/Users/alielnaggar/Desktop/School/Uni/CS 230/Final/Parking_Meters.csv")

# Sidebar for navigation and meter ID search
with st.sidebar:
    st.title("Navigation and Features")
    page = st.radio("Go to", ("Home", "Heatmap"))

    # Search for a specific meter
    st.subheader("Explore Specific Meters")
    selected_meter_id = st.selectbox("Select a Meter ID", df_bos['METER_ID'].unique())
    meter_details = df_bos[df_bos['METER_ID'] == selected_meter_id]
    if not meter_details.empty:
        st.write("Selected Meter Details:", meter_details)
    else:
        st.write("No details available for the selected Meter ID.")

# Home Page
def home_page():
    st.title("Boston Parking Meters Analysis - Home")

    # Display full dataset
    st.write("Parking Meters Data:", df_bos)

    # Map visualization
    st.subheader("Parking Meter Locations")
    tooltip = {"html": "<b>Meter ID:</b> {METER_ID}<br><b>Street:</b> {STREET}<br><b>Rate:</b> {BASE_RATE}<br><b>Status:</b> {METER_STATE}", "style": {"backgroundColor": "orange", "color": "white"}}
    scatter_layer = pdk.Layer(
        'ScatterplotLayer',
        data=df_bos,
        get_position='[lon, lat]',
        get_radius=20,
        get_color=[255, 165, 0, 140],
        pickable=True
    )
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/streets-v11',
        initial_view_state=pdk.ViewState(
            latitude=df_bos["lat"].mean(),
            longitude=df_bos["lon"].mean(),
            zoom=11
        ),
        layers=[scatter_layer],
        tooltip=tooltip
    ))

    # Pie chart
    st.subheader("Pie Chart of Meters by Street (Top 6 Streets)")
    top_streets = dict(df_bos['STREET'].value_counts().nlargest(6))
    other_count = df_bos['STREET'].value_counts().iloc[6:].sum()
    top_streets['Other'] = other_count
    fig, ax = plt.subplots()
    ax.pie(top_streets.values(), labels=top_streets.keys(), autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    plt.title('Top 6 Streets Distribution of Meters')
    st.pyplot(fig)

    # Bar chart
    st.subheader("Top Streets with Most Meters")
    st.bar_chart(df_bos['STREET'].value_counts().head(10))

# Heatmap Page
def heatmap_page():
    st.title("Boston Parking Meters Analysis - Heatmap")
    plt.hist2d(df_bos['lon'], df_bos['lat'], bins=[np.arange(df_bos['lon'].min(), df_bos['lon'].max(), 0.01), np.arange(df_bos['lat'].min(), df_bos['lat'].max(), 0.01)], cmap='YlOrRd')
    plt.colorbar(label='Number of Meters')
    plt.title("Density of Parking Meters in Boston")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    st.pyplot(plt.gcf())

# Display the selected page
if page == "Home":
    home_page()
elif page == "Heatmap":
    heatmap_page()
