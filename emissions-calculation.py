import pandas as pd

# Reading Data Files
test_flight_profile = pd.read_csv("flight-profiles/test-fligh-profile.csv")

# Importing Variables from Data Files
profile_duration_min = test_flight_profile['Duration (min)']    # Duration for All Phases (minutes)

# Calculations 
profile_duration_seconds = profile_duration_min * 60    # Duration for All Phases (seconds)

