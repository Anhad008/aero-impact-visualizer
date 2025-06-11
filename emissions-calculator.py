import pandas as pd 
import json
import os

# Reading Data Files
test_flight_profile = pd.read_csv("flight-profiles/test-flight-profile.csv")
with open ("data/engines-data.json") as f:
    data = json.load(f)

phases = data["CFM56-5B4/2P"]["Phases"]

# Importing Variables from Data
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
ei_HC = phases_df["HC (g/kg)"] # Extract the Emission Index for Hydrocarbons for All Phases (g/kg of fuel)
ei_CO = phases_df["CO (g/kg)"] # Extract the Emission Index for Carbon Monoxide for All Phases (g/kg of fuel)
ei_NOx = phases_df["NOx (g/kg)"] # Extract the Emission Index for Nitrogen Oxides for All Phases (g/kg of fuel)

phases = test_flight_profile["Phase"]
profile_duration_min = test_flight_profile['Duration (min)']    # Duration for All Phases (minutes)


# Calculations 
profile_duration_seconds = profile_duration_min * 60    # Duration for All Phases (seconds)

fuel_burned = fuel_flow_rates * profile_duration_seconds # Fuel burned for All Phases (kg)

hc_emissions = ei_HC * fuel_burned # HC emissions in Fuel Burned
co_emissions = ei_CO * fuel_burned # CO emissions in Fuel Burned
nox_emissions = ei_NOx * fuel_burned # NOx emissions in Fuel Burned

total_duration = profile_duration_seconds.sum()
total_fuel_burned = fuel_burned.sum() # Total Fuel Burned
total_co_emissions = co_emissions.sum() # Total Carbon Monoxide Emissions
total_hc_emissions = hc_emissions.sum() # Total Hydrocarbon Emissions
total_nox_emissions = nox_emissions.sum() # Total Nitrogen Oxides Emissions

total_data = pd.DataFrame([{
    "Phase":"Total",
    "Duration (s)":total_duration,
    "Fuel Burned (kg)":total_fuel_burned,
    "HC emissions (g)":total_hc_emissions,
    "NOx emissions (g)":total_nox_emissions,
    "CO emissions (g)":total_co_emissions,
}])

phases_summary_df = pd.DataFrame({
    "Phase":phases,
    "Duration (s)":profile_duration_seconds,
    "Fuel Flow (kg/s)":fuel_flow_rates,
    "Fuel Burned (kg)":fuel_burned,
    "HC emissions (g)":hc_emissions,
    "NOx emissions (g)":nox_emissions,
    "CO emissions (g)":co_emissions,
})
phases_summary_df = pd.concat([phases_summary_df, total_data], ignore_index=True)


# ---Saving Outputs---
output_dir = "output/emissions"
output_file = os.path.join(output_dir, "summary.csv")

phases_summary_df.to_csv(output_file, index=False)
os.makedirs(output_dir, exist_ok=True)
