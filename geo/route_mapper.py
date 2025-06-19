import os
import pandas as pd
import numpy as np

def map_flight_path():
    current_dir = os.path.dirname(__file__)
    airports_csv_path = os.path.join(current_dir, "..", "output/routes", "origin_destination_data.csv")
    test_flight_profile_csv_path = os.path.join(current_dir, "..", "flight-profiles", "test_flight_profile.csv")

    airports_df = pd.read_csv(airports_csv_path)
    test_flight_profile_df = pd.read_csv(test_flight_profile_csv_path)

    origin_data = airports_df.iloc[0]
    destin_data = airports_df.iloc[1]

    coord_origin = (float(origin_data["Latitude"]), float(origin_data["Longitude"]))
    coord_destin = (float(destin_data["Latitude"]), float(destin_data["Longitude"]))

    start_loc = (coord_origin[0]+coord_destin[0])/2, (coord_origin[1]+coord_destin[1])/2

    # --- Temporarily adding equidistant spacing between coordinates
    phase_speeds = test_flight_profile_df["Speed (kts)"].tolist()
    phase_durations = test_flight_profile_df["Duration (min)"].tolist()

    # Calculate cumulative ratios
    phase_distances = [phase_speeds[i] * phase_durations[i] for i in range(len(phase_speeds))]
    phase_distance_ratios = [d / sum(phase_distances) for d in phase_distances]
    cumulative_ratios = np.cumsum([0] + phase_distance_ratios)

    # Use midpoints of each segment for placement
    midpoints = [(cumulative_ratios[i] + cumulative_ratios[i + 1]) / 2 for i in range(len(phase_distance_ratios))]

    # Interpolate to get lat/lon at midpoints
    lat_list = np.interp(midpoints, [0, 1], [coord_origin[0], coord_destin[0]])
    lon_list = np.interp(midpoints, [0, 1], [coord_origin[1], coord_destin[1]])


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

    return start_loc
