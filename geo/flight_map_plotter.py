import os
import pandas as pd
import folium

# File paths
current_dir = os.path.dirname(__file__)
flight_path_csv_path = os.path.join(current_dir, "..", "output/routes", "flight_path.csv")
emissions_summary_csv_path = os.path.join(current_dir, "..", "output/emissions", "emissions_summary.csv")

# Load data
flight_path_df = pd.read_csv(flight_path_csv_path)
emissions_summary_df = pd.read_csv(emissions_summary_csv_path)
emissions_summary_df = emissions_summary_df[emissions_summary_df["Phase"] != "Total"]

# Emission data per phase
co_em = emissions_summary_df["CO Emissions (g)"].tolist()
nox_em = emissions_summary_df["NOx Emissions (g)"].tolist()
hc_em = emissions_summary_df["HC Emissions (g)"].tolist()

# Start point for map
start_coords = (flight_path_df["Latitude"].iloc[0], flight_path_df["Longitude"].iloc[0])
m = folium.Map(location=start_coords, zoom_start=6)

# Add polyline for route
folium.PolyLine(
    list(zip(flight_path_df["Latitude"], flight_path_df["Longitude"])),
    color='blue', weight=1, opacity=0.5,
).add_to(m)

# Scale factor for circle radius (meters per gram)
scale_factor = 0.5  # Adjust this value to get appropriate visibility

# Add circles for emissions
for idx, row in flight_path_df.iterrows():
    lat, lon = row["Latitude"], row["Longitude"]
    
    folium.Circle(
        location=(lat, lon),
        radius=co_em[idx] * scale_factor,
        color="#56B4E9",
        fill=True,
        fill_color="#56B4E9",
        fill_opacity=0.4,
        popup=f"CO: {co_em[idx]:.1f} g"
    ).add_to(m)
    
    folium.Circle(
        location=(lat, lon),
        radius=nox_em[idx] * scale_factor,
        color="#E69F00",
        fill=True,
        fill_color="#E69F00",
        fill_opacity=0.4,
        popup=f"NOₓ: {nox_em[idx]:.1f} g"
    ).add_to(m)
    
    folium.Circle(
        location=(lat, lon),
        radius=hc_em[idx] * scale_factor,
        color="#009E73",
        fill=True,
        fill_color="#009E73",
        fill_opacity=0.4,
        popup=f"HC: {hc_em[idx]:.1f} g"
    ).add_to(m)

# Save to file
m.save("output/flight_path_emissions_map.html")
