import os
import pandas as pd
import numpy as np
import folium
from folium.plugins import MiniMap, HeatMap, PolyLineTextPath
from branca.element import Template, MacroElement


def add_legend(m):
    legend_html = """
    {% macro html(this, kwargs) %}

    <div style="
        position: fixed;
        bottom: 50px;
        left: 50px;
        width: 260px;
        height: 200px;
        background-color: white;
        border:2px solid grey;
        z-index:9999;
        font-size:14px;
        padding: 10px;
        border-radius: 8px;
        box-shadow: 2px 2px 6px rgba(0,0,0,0.3);
        ">
        <b style="font-size:16px;">Aero Impact Visualizer</b><br><br>
        <b>Pollutant Emissions:</b><br>
        <i style="color:#56B4E9;">●</i> CO (Carbon Monoxide)<br>
        <i style="color:#E69F00;">●</i> NOₓ (Nitrogen Oxides)<br>
        <i style="color:#009E73;">●</i> HC (Hydrocarbons)<br><br>
        <b>Noise Heatmap:</b><br>
        <div style="width:200px;
                    height:15px;
                    background: linear-gradient(to right, white, yellow, red);
                    border:1px solid black;"></div>
        <span style="font-size:12px;">Low → High Noise (EPNdB)</span>
    </div>

    {% endmacro %}
    """
    legend = MacroElement()
    legend._template = Template(legend_html)
    m.get_root().add_child(legend)


def plot_combined_emission_noise_map(start_loc):
    # Load data
    airports_df = pd.read_csv("output/origin_destination_data.csv")
    flight_df = pd.read_csv("output/routes/flight_path.csv")
    emissions_df = pd.read_csv("output/emissions/emissions_summary.csv")
    emissions_df = emissions_df[emissions_df["Phase"] != "Total"]

    # Airport Coords
    origin_data = airports_df.iloc[0]
    destin_data = airports_df.iloc[1]
    coord_origin = (float(origin_data["Latitude"]), float(origin_data["Longitude"]))
    coord_destin = (float(destin_data["Latitude"]), float(destin_data["Longitude"]))

    # Emissions per phase
    co_em = emissions_df["CO Emissions (g)"].tolist()
    nox_em = emissions_df["NOx Emissions (g)"].tolist()
    hc_em = emissions_df["HC Emissions (g)"].tolist()
    noise_list = emissions_df["Noise Emissions (EPNdB)"].tolist()

    # Map Initialization
    m = folium.Map(
        location=start_loc,
        zoom_start=6,
        tiles="cartodbpositron",
        control_scale=True
    )

    ####### Route Line #########
    route = folium.PolyLine(
        [coord_origin] + flight_df[['Latitude', 'Longitude']].values.tolist() + [coord_destin],
        color='black', weight=2, opacity=0.7
    ).add_to(m)

    arrow_path = PolyLineTextPath(
        route,
        '➤',
        repeat=True,
        offset=10,
        attributes={'fill': 'black', 'font-weight': 'bold', 'font-size': '10'}
    )
    m.add_child(arrow_path)

    ####### Airport Markers #######
    folium.Marker(coord_origin, popup="Origin Airport", icon=folium.Icon(color='green')).add_to(m)
    folium.Marker(coord_destin, popup="Destination Airport", icon=folium.Icon(color='red')).add_to(m)

    ####### Emission Circle Layer ########
    emission_layer = folium.FeatureGroup(name="Pollutant Emissions Markers", overlay=True, control=True)

    scale_factor = 1.2

    for idx, row in flight_df.iterrows():
        lat, lon = row["Latitude"], row["Longitude"]

        folium.Circle(
            location=(lat, lon),
            radius=co_em[idx] * scale_factor,
            color="#56B4E9",
            fill=True,
            fill_color="#56B4E9",
            fill_opacity=0.4,
            popup=f"CO: {co_em[idx]:.1f} g"
        ).add_to(emission_layer)

        folium.Circle(
            location=(lat, lon),
            radius=nox_em[idx] * scale_factor,
            color="#E69F00",
            fill=True,
            fill_color="#E69F00",
            fill_opacity=0.4,
            popup=f"NOₓ: {nox_em[idx]:.1f} g"
        ).add_to(emission_layer)

        folium.Circle(
            location=(lat, lon),
            radius=hc_em[idx] * scale_factor,
            color="#009E73",
            fill=True,
            fill_color="#009E73",
            fill_opacity=0.4,
            popup=f"HC: {hc_em[idx]:.1f} g"
        ).add_to(emission_layer)

    emission_layer.add_to(m)

    ####### Noise Heatmap Layer ########
    noise_layer = folium.FeatureGroup(name="Noise Heatmap", overlay=True, control=True)

    heat_data = []
    n_points_per_phase = 600

    for i in range(len(flight_df)):
        lat1, lon1 = flight_df.iloc[i]["Latitude"], flight_df.iloc[i]["Longitude"]
        if i < len(flight_df) - 1:
            lat2, lon2 = flight_df.iloc[i + 1]["Latitude"], flight_df.iloc[i + 1]["Longitude"]
        else:
            lat2, lon2 = coord_destin

        noise = noise_list[i]

        for t in np.linspace(0, 1, n_points_per_phase):
            lat = lat1 + t * (lat2 - lat1)
            lon = lon1 + t * (lon2 - lon1)
            normalized_noise = max(0, min(1, (noise) / 70))
            heat_data.append([lat, lon, normalized_noise])

    HeatMap(heat_data, radius=25, blur=15, max_zoom=8, min_opacity=0.1).add_to(noise_layer)
    noise_layer.add_to(m)

    ####### Add Controls ########
    m.add_child(MiniMap(toggle_display=True))
    folium.LayerControl(collapsed=False).add_to(m)

    ####### Add Legend ########
    add_legend(m)

    ####### Save ########
    output_path = "output/routes/flight_path_combined_map.html"
    m.save(output_path)
    print(f"Map saved to {output_path}")


# Run the function
plot_combined_emission_noise_map(start_loc=(43.677, -79.631))


    


    
