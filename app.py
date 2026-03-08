import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium
from PIL import Image
import numpy as np
import cv2
import math
from geopy.geocoders import Nominatim
from streamlit_js_eval import get_geolocation

st.title("🚦 Road Rakshak – AI Road Safety System")
st.write("Smart Road Monitoring System for Accident Prevention")

# -----------------------------
# MODULE 1 – Pothole Detection
# -----------------------------

st.header("Module 1 : Pothole Detection")

uploaded_file = st.file_uploader("Upload Road Image")

if uploaded_file is not None:

    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Road Image", use_column_width=True)

    img_array = np.array(image)

    gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)

    edge_pixels = np.sum(edges > 0)

    if edge_pixels > 15000:
        st.error("⚠ Possible Pothole / Damaged Road Detected")
    else:
        st.success("✅ Road Looks Safe")


# -----------------------------
# MODULE 2 – Accident Analytics
# -----------------------------

st.header("Module 2 : Accident Data Analysis")

try:

    df = pd.read_csv("accident_data.csv")

    st.subheader("Dataset Preview")
    st.write(df.head())

    st.subheader("Accidents by Location")

    location_counts = df["Location"].value_counts()

    fig, ax = plt.subplots()
    location_counts.plot(kind="bar", ax=ax)

    st.pyplot(fig)

    st.subheader("Accidents by Cause")

    cause_counts = df["Cause"].value_counts()

    fig2, ax2 = plt.subplots()
    cause_counts.plot(kind="pie", autopct="%1.1f%%", ax=ax2)

    st.pyplot(fig2)

except:
    st.warning("Upload accident_data.csv file to enable analytics")


# -----------------------------
# MODULE 3 – Accident Hotspot Map
# -----------------------------

st.header("Module 3 : Accident Hotspot Map")

try:

    map_center = [16.5062, 80.6480]  # Vijayawada, Andhra Pradesh

    accident_map = folium.Map(location=map_center, zoom_start=13)

    for i, row in df.iterrows():

        folium.CircleMarker(
            location=[row["Latitude"], row["Longitude"]],
            radius=6,
            popup=row["Location"],
            color="red",
            fill=True
        ).add_to(accident_map)

    st_folium(accident_map, width=700)

except:
    st.write("Map data not available")


# -----------------------------
# MODULE 4 – Civic Complaint
# -----------------------------

st.header("Module 4 : Civic Complaint Generator")

name = st.text_input("Your Name")
location_issue = st.text_input("Road Location")

issue = st.selectbox(
    "Issue Type",
    ["Pothole", "Broken Road", "Water Logging", "Streetlight Not Working"]
)

if st.button("Generate Complaint"):

    complaint = f"""
To  
Municipal Corporation

Subject: Road Issue Complaint

Respected Sir/Madam,

I am {name}, a resident of this city.

I would like to report a road issue at {location_issue}.
The issue is related to {issue}.

This problem may lead to accidents.
Please take necessary action.

Thank you.

Sincerely  
{name}
"""

    st.text_area("Generated Complaint", complaint, height=250)


# -----------------------------
# MODULE 5 – Emergency Police Alert
# -----------------------------

st.header("Module 5 : Emergency Police Alert")

accident_location = st.text_input("Enter Accident Location")

geolocator = Nominatim(user_agent="road_rakshak")

police_stations = {
    "Central Police Station": [17.3855, 78.4810],
    "North Police Station": [17.4000, 78.4900],
    "South Police Station": [17.3600, 78.4700]
}

def distance(lat1, lon1, lat2, lon2):
    return math.sqrt((lat1-lat2)**2 + (lon1-lon2)**2)

if st.button("Send Accident Alert to Police"):

    try:

        location = geolocator.geocode(accident_location)

        lat = location.latitude
        lon = location.longitude

        nearest_station = None
        min_dist = 999

        for station, coords in police_stations.items():

            d = distance(lat, lon, coords[0], coords[1])

            if d < min_dist:
                min_dist = d
                nearest_station = station

        message = f"""
🚨 Accident Alert 🚨

Location: {accident_location}
Coordinates: {lat}, {lon}

Nearest Police Station:
{nearest_station}

Immediate assistance required.
"""

        st.text_area("Police Alert Message", message, height=200)

        st.success("Alert generated for nearest police station")

    except:
        st.error("Location not found. Please enter a valid place.")


# -----------------------------
# MODULE 6 – Family Emergency Alert
# -----------------------------

st.header("Module 6 : Family Emergency Alert")

family_name = st.text_input("Family Member Name")
family_phone = st.text_input("Family Member Phone Number")

family_location = st.text_input("Accident Location for Family Alert")

if st.button("Send Family Alert"):

    try:

        location = geolocator.geocode(family_location)

        lat = location.latitude
        lon = location.longitude

        alert_message = f"""
🚨 Emergency Alert 🚨

Dear {family_name},

A road accident has been detected.

Location: {family_location}
Coordinates: {lat}, {lon}

Please contact immediately.

Sent by Road Rakshak Safety System.
"""

        st.text_area("Emergency Message", alert_message, height=200)

        st.success("Emergency alert prepared for family member.")

    except:
        st.error("Location not found. Please enter a valid place.")


# -----------------------------
# MODULE 7 – Automatic GPS Detection
# -----------------------------

st.header("Module 7 : Automatic Location Detection")

if st.button("Detect My Location"):

    location = get_geolocation()

    if location is not None:

        lat = location["coords"]["latitude"]
        lon = location["coords"]["longitude"]

        st.success("Location Detected")

        st.write("Latitude:", lat)
        st.write("Longitude:", lon)

        st.info("This location can be used to send accident alerts.")