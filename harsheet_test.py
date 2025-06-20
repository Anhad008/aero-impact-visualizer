import streamlit as st
import pandas as pd
import json

st.set_page_config(page_title="Flight Emissions Configuration", layout="centered")

# Load engine data
with open("data/engines-data.json") as f:
    engine_data = json.load(f)

# Load phases
phases_df = pd.read_csv("output/emissions/emissions_summary.csv")
phase_options = phases_df[phases_df['Phase'] != 'Total']['Phase'].tolist()
engine_options = list(engine_data.keys())

# Title
st.title("Configure Flight Phases")

# Engine selection
selected_engine = st.selectbox("Select Engine", engine_options)
engine_info = engine_data[selected_engine]


col1, col2 = st.columns(2)

# Extract and format all fields except phases
text_fields = {k: v for k, v in engine_info.items() if k.lower() != "phases"}
phases_data = engine_info.get("Phases", {})

for i, (key, value) in enumerate(text_fields.items()):
    with col1 if i % 2 == 0 else col2:
        st.markdown(f"**{key.replace('_', ' ').title()}**: <span style='background-color:#1a1a1a;padding:2px 6px;border-radius:4px;color:lightgreen;'>{value}</span>", unsafe_allow_html=True)

# Handle Phases nicely
with st.expander("📊 Phase Emission Details", expanded=False):
    for phase, details in phases_data.items():
        st.markdown(f"**🛫 {phase}**")
        st.markdown(f"- Power Setting (%): `{details.get('Power Setting (%)', 'N/A')}`")
        st.markdown(f"- Fuel Flow (kg/s): `{details.get('Fuel Flow (kg/s)', 'N/A')}`")

        emission_indices = details.get("Emission Indices (g/kg fuel)", {})
        if emission_indices:
            emission_md = "- Emission Indices(g/kg fuel):\n"
        for key, value in emission_indices.items():
            emission_md += f"  - {key}: `{value}`\n"

        st.markdown(emission_md)
    

# Phase selection
selected_phase = st.selectbox("Select Phase:", phase_options)
phase_duration = st.number_input(f"Enter duration for {selected_phase} (in s)", min_value=0)

# Load and process airport data
airport_df = pd.read_csv("data/airports.csv")

# Drop rows where lat/lon & iata/icao code is missing
airport_df = airport_df.dropna(subset=['lat_decimal', 'lon_decimal', 'iata_code', 'icao_code'])

airport_df['label'] = airport_df.apply(
    lambda row: f"{row['iata_code']}/{row['icao_code']} – {row['name']} – {row['city']} – {row['country']}",
    axis=1
)

# Select origin
origin_label = st.selectbox("Select Origin Airport", airport_df['label'], key="origin")

# Filter destination options to exclude origin
filtered_dest_df = airport_df[airport_df['label'] != origin_label]

# Select destination
destination_label = st.selectbox("Select Destination Airport", filtered_dest_df['label'], key="destination")

# Retrieve info
origin_info = airport_df[airport_df['label'] == origin_label].iloc[0]
dest_info = airport_df[airport_df['label'] == destination_label].iloc[0]

# Display route
st.markdown(f"✈️ **Route:** {origin_info['iata_code']} → {dest_info['iata_code']}")

input_data = pd.DataFrame([
            {
                "IATA_Code": origin_info['iata_code'],
                "Latitude": origin_info['lat_decimal'],
                "Longitude": origin_info['lon_decimal']
            },
            {
                "IATA_Code": dest_info['iata_code'],
                "Latitude": dest_info['lat_decimal'],
                "Longitude": dest_info['lon_decimal']
            }
        ])

df = input_data
with st.form("save_form"):
    submit = st.form_submit_button("Save to CSV")
    if submit:
        csv_path = "output/routes/origin_destination_data.csv"

        # Overwrite the CSV every time
        input_data.to_csv(csv_path, index=False)
        st.success("Save Succesful!")




