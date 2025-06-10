import pandas as pd 
df = pd.read_json("test-flight-profile.json")
df['total_emissions'] = df['CO'] + df['NOx'] + df['HC']
