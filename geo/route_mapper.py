import os
import pandas as pd
import numpy as np
from geopy.distance import geodesic

current_dir = os.path.dirname(__file__)
airports_csv_path = os.path.join(current_dir, "..", "data", "airports.csv")
test_flight_profile_csv_path = os.path.join(current_dir, "..", "flight-profiles", "test_flight_profile.csv")

airports_df = pd.read_csv(airports_csv_path)
test_flight_profile_df = pd.read_csv(test_flight_profile_csv_path)

origin_data = airports_df[airports_df["iata_code"] == "JFK"]
destin_data = airports_df[airports_df["iata_code"] == "YYZ"]

coord_origin = (float(origin_data["lat_decimal"].iloc[0]), float(origin_data["lon_decimal"].iloc[0]))
coord_destin = (float(destin_data["lat_decimal"].iloc[0]), float(destin_data["lon_decimal"].iloc[0]))

distance_profile = geodesic(coord_origin, coord_destin)

# --- Temporarily adding equidistant spacing between coordinates
phase_coord = (np.linspace(coord_origin[0], coord_destin[0], 5).tolist(), np.linspace(coord_origin[1], coord_destin[1], 5).tolist())

# Save coords to flight path
lat_list, lon_list = phase_coord

phases = test_flight_profile_df["Phase"].tolist()
durations = test_flight_profile_df["Duration (min)"].tolist()

flight_path_df = pd.DataFrame({
    "Phase": phases,
    "Duration (min)": durations,
    "Latitude": lat_list,
    "Longitude": lon_list
})

output_path = os.path.join(current_dir, "..", "output", "routes", "flight_path.csv")
os.makedirs(os.path.dirname(output_path), exist_ok=True)
flight_path_df.to_csv(output_path, index=False)

print(f"Flight path saved to {output_path}")
