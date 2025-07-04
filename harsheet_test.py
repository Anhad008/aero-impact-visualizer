import streamlit as st
import pandas as pd
import json
import os
import streamlit.components.v1 as components

from plot_emissions import (
    plot_bar_summary,
    plot_pie_summary,
    plot_fuel_flow_summary,
    plot_emissions_line_summary
)

# Streamlit Page Setup
st.set_page_config(page_title="Aero-Environmental Impact Visualizer", layout="wide")

# Load Data
with open("data/engines-data.json") as f:
    engine_data = json.load(f)

phases_df = pd.read_csv("output/emissions/emissions_summary.csv")
phase_options = phases_df[phases_df['Phase'] != 'Total']['Phase'].tolist()
engine_options = list(engine_data.keys())

# Load Airports
airport_df = pd.read_csv("data/airports.csv")
airport_df = airport_df.dropna(subset=['lat_decimal', 'lon_decimal', 'iata_code', 'icao_code'])
airport_df['label'] = airport_df.apply(
    lambda row: f"{row['iata_code']}/{row['icao_code']} – {row['name']} – {row['city']} – {row['country']}",
    axis=1
)
airport_labels = ["-- Select an Airport --"] + airport_df['label'].tolist()

# Sidebar Layout
st.sidebar.title("Flight Configuration")

selected_engine = st.sidebar.selectbox("Select Engine", engine_options)
engine_info = engine_data[selected_engine]
selected_phase = st.sidebar.selectbox("Select Phase", phase_options)
phase_duration = st.sidebar.number_input(f"Duration for {selected_phase} (seconds)", min_value=0)

st.sidebar.markdown("---")

st.sidebar.subheader("Select Airports")
origin_label = st.sidebar.selectbox("Origin Airport", airport_labels, key="origin")
destination_label = st.sidebar.selectbox("Destination Airport", airport_labels, key="destination")

# Main Title
st.title("Aero-Environmental Impact Visualizer")
st.caption("🌍 Visualize the environmental impact of flights in terms of emissions and noise")

# Engine Info
st.subheader("Engine Configuration")
col1, col2 = st.columns(2)
text_fields = {k: v for k, v in engine_info.items() if k.lower() != "phases"}
phases_data = engine_info.get("Phases", {})

for i, (key, value) in enumerate(text_fields.items()):
    with col1 if i % 2 == 0 else col2:
        st.markdown(
            f"**{key.replace('_', ' ').title()}**: "
            f"<span style='background-color:#d1d1d1;padding:3px 8px;border-radius:4px;color:black;'>{value}</span>",
            unsafe_allow_html=True
        )

with st.expander("📊 Engine Phase Emission Details"):
    for phase, details in phases_data.items():
        st.markdown(f"**🛫 {phase}**")
        st.markdown(f"- Power Setting (%): `{details.get('Power Setting (%)', 'N/A')}`")
        st.markdown(f"- Fuel Flow (kg/s): `{details.get('Fuel Flow (kg/s)', 'N/A')}`")
        emission_indices = details.get("Emission Indices (g/kg fuel)", {})
        if emission_indices:
            st.markdown("- **Emission Indices (g/kg fuel):**")
            for key, val in emission_indices.items():
                st.markdown(f"  - {key}: `{val}`")

# Route Section
st.subheader("Selected Route")
if origin_label != "-- Select an Airport --" and destination_label != "-- Select an Airport --":
    origin_info_df = airport_df[airport_df['label'] == origin_label]
    dest_info_df = airport_df[airport_df['label'] == destination_label]

    if not origin_info_df.empty and not dest_info_df.empty:
        origin_info = origin_info_df.iloc[0]
        dest_info = dest_info_df.iloc[0]

        st.markdown(f"✈️ **Route:** {origin_info['iata_code']} → {dest_info['iata_code']}")

        input_data = pd.DataFrame([
            {"IATA_Code": origin_info['iata_code'], "Latitude": origin_info['lat_decimal'], "Longitude": origin_info['lon_decimal']},
            {"IATA_Code": dest_info['iata_code'], "Latitude": dest_info['lat_decimal'], "Longitude": dest_info['lon_decimal']}
        ])

        if st.button("Save Flight Data"):
            input_data.to_csv("output/origin_destination_data.csv", index=False)
            st.success("Saved flight data!")

        st.markdown("---")
        st.subheader("📊 Emission Visualizations")

        summary_df = pd.read_csv("output/emissions/emissions_summary.csv")
        st.plotly_chart(plot_bar_summary(summary_df), use_container_width=True)
        st.plotly_chart(plot_pie_summary(summary_df), use_container_width=True)
        st.plotly_chart(plot_fuel_flow_summary(summary_df), use_container_width=True)
        st.plotly_chart(plot_emissions_line_summary(summary_df), use_container_width=True)

        st.subheader("📅 Download Emissions Data")
        with open("output/emissions/emissions_summary.csv", "rb") as f:
            st.download_button("Download Emissions CSV", f, file_name="emissions_summary.csv", key="emissions_csv")

        st.markdown("---")
        st.subheader("🌍 Combined Flight Emissions & Noise Map")

        map_path = "output/routes/flight_path_combined_map.html"
        if os.path.exists(map_path):
            with open(map_path, 'r', encoding='utf-8') as f:
                html_data = f.read()
            components.html(html_data, height=650, scrolling=False)

            st.subheader("📅 Download Flight Map")
            with open(map_path, "rb") as f:
                st.download_button("Download Flight Map (HTML)", f, file_name="flight_map.html", key="map_html")
        else:
            st.error("Map not found. Please generate it first.")
    else:
        st.error("Could not find selected airport details. Please reselect.")
else:
    st.warning("Please select both origin and destination airports.")











