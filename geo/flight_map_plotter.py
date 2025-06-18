import os
import pandas as pd
import folium
from folium.plugins import MiniMap
from folium.plugins import PolyLineTextPath

# File paths
current_dir = os.path.dirname(__file__)
airports_csv_path = os.path.join(current_dir, "..", "data", "origin_destination_data.csv")
flight_path_csv_path = os.path.join(current_dir, "..", "output/routes", "flight_path.csv")
emissions_summary_csv_path = os.path.join(current_dir, "..", "output/emissions", "emissions_summary.csv")

# Load data
airports_df = pd.read_csv(airports_csv_path)
flight_path_df = pd.read_csv(flight_path_csv_path)
emissions_summary_df = pd.read_csv(emissions_summary_csv_path)
emissions_summary_df = emissions_summary_df[emissions_summary_df["Phase"] != "Total"]

# Getting Airport Coords
origin_data = airports_df[airports_df["IATA"] == "JFK"]
destin_data = airports_df[airports_df["IATA"] == "YYZ"]

coord_origin = (float(origin_data["Latitude"].iloc[0]), float(origin_data["Longitude"].iloc[0]))
coord_destin = (float(destin_data["Latitude"].iloc[0]), float(destin_data["Longitude"].iloc[0]))

# Emission data per phase
co_em = emissions_summary_df["CO Emissions (g)"].tolist()
nox_em = emissions_summary_df["NOx Emissions (g)"].tolist()
hc_em = emissions_summary_df["HC Emissions (g)"].tolist()

# Start point for map
m = folium.Map(location=coord_origin, zoom_start=6)

# Add polyline for route
route = folium.PolyLine(
    [coord_origin, coord_destin],
    color='black', weight=1, opacity=0.5,
).add_to(m)

arrow_path = PolyLineTextPath(
    route,
    '➤',       # Arrow character
    repeat=True,
    offset=12,  # Distance between arrows (in pixels)
    attributes={'fill': 'black', 'font-weight': 'bold', 'font-size': '8'}
)
m.add_child(arrow_path)

# Add origin marker
folium.Marker(
    location=coord_origin,
    popup="JFK Airport (Origin)",
    icon=folium.Icon(color='blue', icon='plane-departure', prefix='fa')
).add_to(m)

# Add destination marker
folium.Marker(
    location=coord_destin,
    popup="YYZ Airport (Destination)",
    icon=folium.Icon(color='red', icon='plane-arrival', prefix='fa')
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

m.add_child(MiniMap(toggle_display=True))

# Save to file
m.save("output/routes/flight_path_emissions_map.html")
