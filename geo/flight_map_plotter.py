import os
import pandas as pd
import numpy as np
import folium
from folium.plugins import MiniMap, HeatMap, PolyLineTextPath

def plot_pollutant_emissions_map(start_loc):
    # File paths
    current_dir = os.path.dirname(__file__)
    airports_csv_path = os.path.join(current_dir, "..", "output/routes", "origin_destination_data.csv")
    flight_path_csv_path = os.path.join(current_dir, "..", "output/routes", "flight_path.csv")
    emissions_summary_csv_path = os.path.join(current_dir, "..", "output/emissions", "emissions_summary.csv")

    # Load data
    airports_df = pd.read_csv(airports_csv_path)
    flight_path_df = pd.read_csv(flight_path_csv_path)
    emissions_summary_df = pd.read_csv(emissions_summary_csv_path)
    emissions_summary_df = emissions_summary_df[emissions_summary_df["Phase"] != "Total"]

    # Getting Airport Coords
    origin_data = airports_df.iloc[0]
    destin_data = airports_df.iloc[1]

    coord_origin = (float(origin_data["Latitude"]), float(origin_data["Longitude"]))
    coord_destin = (float(destin_data["Latitude"]), float(destin_data["Longitude"]))

    # Emission data per phase
    co_em = emissions_summary_df["CO Emissions (g)"].tolist()
    nox_em = emissions_summary_df["NOx Emissions (g)"].tolist()
    hc_em = emissions_summary_df["HC Emissions (g)"].tolist()

    # Start point for map
    m = folium.Map(location=start_loc, zoom_start=7)

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
    scale_factor = 1.2  # Adjust this value to get appropriate visibility

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

def plot_noise_emissions_map(start_loc):
    # Paths
    current_dir = os.path.dirname(__file__)
    airports_csv_path = os.path.join(current_dir, "..", "output/routes", "origin_destination_data.csv")
    flight_path_csv = os.path.join(current_dir, "..", "output/routes", "flight_path.csv")
    emissions_csv = os.path.join(current_dir, "..", "output/emissions", "emissions_summary.csv")

    # Load data
    airports_df = pd.read_csv(airports_csv_path)
    flight_df = pd.read_csv(flight_path_csv)
    emissions_df = pd.read_csv(emissions_csv)
    emissions_df = emissions_df[emissions_df["Phase"] != "Total"]
    ground_noise = emissions_df["Noise Emissions (EPNdB)"].tolist()

    # Getting Airport Coords
    origin_data = airports_df.iloc[0]
    destin_data = airports_df.iloc[1]

    coord_origin = (float(origin_data["Latitude"]), float(origin_data["Longitude"]))
    coord_destin = (float(destin_data["Latitude"]), float(destin_data["Longitude"]))

    # Prepare interpolated points
    heat_data = []
    n_points_per_phase = 1000

    for i in range(len(flight_df)):
        lat1, lon1 = flight_df.iloc[i]["Latitude"], flight_df.iloc[i]["Longitude"]
        
        if i < len(flight_df) - 1:
            lat2, lon2 = flight_df.iloc[i + 1]["Latitude"], flight_df.iloc[i + 1]["Longitude"]
        else:
            lat2, lon2 = coord_destin  # use destination coordinates for last segment

        noise = ground_noise[i]

        for t in np.linspace(0, 1, n_points_per_phase):
            lat = lat1 + t * (lat2 - lat1)
            lon = lon1 + t * (lon2 - lon1)
            # Normalize EPNdB to 0–1 range
            normalized_noise = max(0, min(1, (noise) / 70))  # Assume 30 dB min audible, 100 dB max possible
            heat_data.append([lat, lon, normalized_noise])


    # Initialize map
    m = folium.Map(location=start_loc, zoom_start=6)
    HeatMap(heat_data, radius=25, blur=15, max_zoom=8, min_opacity=0.1).add_to(m)
    m.add_child(MiniMap(toggle_display=True))

    # Save to file
    m.save("output/routes/flight_path_noise_map.html")
