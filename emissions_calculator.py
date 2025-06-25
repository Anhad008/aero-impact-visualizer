import pandas as pd 
import numpy as np
import json
import os

def calc_pollutant_emissions(): 
    # ---Reading Data Files---
    test_flight_profile = pd.read_csv("flight-profiles/test_flight_profile.csv")
    with open ("data/engines-data.json") as f:
        data = json.load(f)

    # ---Extract the phase-wise emission for the CFM56-5B4/2P engine from the JSON datafile---
    phases = data["CFM56-5B4/2P"]["Phases"]

    # ---Importing Variables from Data---
    phase_data = []
    for phase_name, details in phases.items():
        ei  = details["Emission Indices (g/kg fuel)"]
        phase_data.append({
            "Phase": phase_name,
            "Fuel Flow (kg/s)": details["Fuel Flow (kg/s)"],
            "HC (g/kg)": ei["HC"],
            "CO (g/kg)": ei["CO"],
            "NOx (g/kg)": ei["NOx"]
        })

    phases_df = pd.DataFrame(phase_data)     # Dataframe containing data for all phases

    fuel_flow_rates = phases_df["Fuel Flow (kg/s)"] # Extract the fuel flow rates for All Phases (in kg per second)
    ei_HC = phases_df["HC (g/kg)"]                  # Extract the Emission Index for Hydrocarbons for All Phases (g/kg of fuel)
    ei_CO = phases_df["CO (g/kg)"]                  # Extract the Emission Index for Carbon Monoxide for All Phases (g/kg of fuel)
    ei_NOx = phases_df["NOx (g/kg)"]                # Extract the Emission Index for Nitrogen Oxides for All Phases (g/kg of fuel)

    phases = test_flight_profile["Phase"] # Extract Phase data from CSV datafile
    profile_duration_min = test_flight_profile['Duration (min)'] # Duration for All Phases (minutes)


    # ---Calculations--- 
    profile_duration_seconds = profile_duration_min * 60  # Duration for All Phases (seconds)

    fuel_burned = fuel_flow_rates * profile_duration_seconds # Fuel burned for All Phases (kg)

    hc_emissions = ei_HC * fuel_burned      # HC emissions in Fuel Burned
    co_emissions = ei_CO * fuel_burned      # CO emissions in Fuel Burned
    nox_emissions = ei_NOx * fuel_burned    # NOx emissions in Fuel Burned

    total_duration = profile_duration_seconds.sum()     # Total Duration of Flight
    total_fuel_burned = fuel_burned.sum()               # Total Fuel Burned
    total_co_emissions = co_emissions.sum()             # Total Carbon Monoxide Emissions
    total_hc_emissions = hc_emissions.sum()             # Total Hydrocarbon Emissions
    total_nox_emissions = nox_emissions.sum()           # Total Nitrogen Oxides Emissions

    # ---Create a DataFrame for Total Emissions Summary---
    total_data = pd.DataFrame([{
        "Phase":"Total",
        "Duration (s)":total_duration,
        "Fuel Burned (kg)":total_fuel_burned,
        "HC Emissions (g)":total_hc_emissions,
        "NOx Emissions (g)":total_nox_emissions,
        "CO Emissions (g)":total_co_emissions,
        "Noise Emissions (EPNdB)":total_co_emissions,
    }])

    # ---Create Phase-wise Emissions Summary DataFrame---
    phases_summary_df = pd.DataFrame({
        "Phase":phases,
        "Duration (s)":profile_duration_seconds,
        "Fuel Flow (kg/s)":fuel_flow_rates,
        "Fuel Burned (kg)":fuel_burned,
        "HC Emissions (g)":hc_emissions,
        "NOx Emissions (g)":nox_emissions,
        "CO Emissions (g)":co_emissions,
        "Noise Emissions (EMNdB)":co_emissions
    })

    phases_summary_df = pd.concat([phases_summary_df, total_data], ignore_index=True) # Adding the total data column calculated to the main dataframe

    phases_summary_df = phases_summary_df.round(3) # Rounding off the calculated data to 3 decimal places


    # ---Saving Outputs---
    output_dir = "output/emissions"
    output_file = os.path.join(output_dir, "summary.csv")

    phases_summary_df.to_csv(output_file, index=False)
    os.makedirs(output_dir, exist_ok=True)

def calc_noise_emissions():
    # ---Reading Data Files---
    test_flight_profile = pd.read_csv("flight-profiles/test_flight_profile.csv")
    aircraft_engine_combinations = pd.read_csv("data/aircraft_engine_combinations.csv", sep=';')
    emissions_df = pd.read_csv("output/emissions/emissions_summary.csv")

    # ---Extracting Data---
    phases = test_flight_profile["Phase"]
    alt_ft = test_flight_profile["Altitude (ft)"]

    # Example: filter and sort for A320-214 + CFM56-5B4/2P
    aircraft_engine_combinations = aircraft_engine_combinations[~aircraft_engine_combinations["Engine"].str.contains(",", na=False)]

    df_filtered = aircraft_engine_combinations[
        (aircraft_engine_combinations['TYPE'].str.contains("A320")) & 
        (aircraft_engine_combinations['Engine'].str.contains("CFM56-5B4/2P"))
    ]

    # Sort by certification date or margin
    df_filtered_sorted = df_filtered.sort_values("Certif Date", ascending=False)

    aircraft_engine_data = df_filtered_sorted.iloc[0]

    nEngines = aircraft_engine_data["Number of engines"]
    phase_noise = [
        70,
        aircraft_engine_data["Lateral/Full Power(EPNdB)"],
        aircraft_engine_data["FO(EPNdB)"],
        50,
        aircraft_engine_data["Approach(EPNdB)"]
        ]
    
    ground_noise = []
    ref_dists = [100, 2000, 6500, 10000, 2000]

    for i in range(len(phases)):
        alt_m = alt_ft[i] * 0.3048
        ref = ref_dists[i]
        noise_db = phase_noise[i] if alt_m == 0 else phase_noise[i] - 20 * np.log10(alt_m / ref)
        ground_noise.append(round(noise_db, 2))


    emissions_df_no_total = emissions_df[emissions_df["Phase"] != "Total"].copy()
    emissions_df_no_total["Noise Emissions (EPNdB)"] = ground_noise
    emissions_df_final = pd.concat([emissions_df_no_total, emissions_df[emissions_df["Phase"] == "Total"]], ignore_index=True)
    emissions_df_final.to_csv("output/emissions/emissions_summary.csv", index=False)

