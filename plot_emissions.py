import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

def plot_bar_summary(summary_df):
    phases = summary_df["Phase"]
    co_emm = summary_df["CO Emissions (g)"]
    nox_emm = summary_df["NOx Emissions (g)"]
    hc_emm = summary_df["HC Emissions (g)"]

    fig = go.Figure([
        go.Bar(
            name='HC Emissions', 
            legendgroup='HC',
            x=phases, 
            y=hc_emm, 
            text=hc_emm.apply(lambda x: f'{x:.3f}'), 
            textposition='inside', 
            textfont=dict(
                    size=10,              # Font size of the text on bars
                    color='white'         # Font color (e.g., 'white' if inside bar)
                ),
            hovertemplate='Pollutant: HC<br>Phase: %{x}<br>Emissions: %{y:.3f} g<extra></extra>',
            marker=dict(color='#009E73') 
            ),
        go.Bar(
            name='NOx Emissions', 
            legendgroup='NOx',
            x=phases, 
            y=nox_emm,
            text=nox_emm.apply(lambda x: f'{x:.3f}'),
            textposition='inside',
            textfont=dict(
                    size=10,              # Font size of the text on bars
                    color='white'         # Font color (e.g., 'white' if inside bar)
                ),
            hovertemplate='Pollutant: NOx<br>Phase: %{x}<br>Emissions: %{y:.3f} g<extra></extra>',
            marker=dict(color='#E69F00') 
            ),
        go.Bar(
            name='CO Emissions', 
            legendgroup='CO',
            x=phases, 
            y=co_emm,
            text=co_emm.apply(lambda x: f'{x:.3f}'),
            textposition='inside',
            textfont=dict(
                    size=10,              # Font size of the text on bars
                    color='white'         # Font color (e.g., 'white' if inside bar)
                ),
            hovertemplate='Pollutant: CO<br>Phase: %{x}<br>Emissions: %{y:.3f} g<extra></extra>',
            marker=dict(color='#56B4E9') 
            )
    ])

    fig.update_layout(
        barmode='group',
        yaxis_type='log', 
        template='simple_white',
        title='<b>Engine Emissions by Flight Phase for CFM56-5B4/2P</b><br><sup>Log scale used to highlight variation across pollutants</sup>',

        bargap=0.15,         # Space between groups
        bargroupgap=0.05,    # Space between bars within a group

        # Stylistic Formatting
        height=650,  # Increase vertical space (good for log scale)
        margin=dict(
            l=80,   # Left margin (space for y-axis labels)
            r=40,   # Right margin
            t=100,  # Top margin (space for title + subtitle)
            b=80    # Bottom margin (space for x-axis labels)
        ),
        title_font=dict(
            size=22,
            family="Arial",
            color="black"
        ),
        font=dict(
            size=13, 
            family="Arial"
        ),
        legend=dict(
            font=dict(size=12),
            orientation="h", # horizontal legend
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),

        # Formatting x-axis
        xaxis=dict(
            title='Flight Phase'
        ),
        
        # Formatting y-axis
        yaxis=dict(
            type='log',
            title='Emissions (g, log scale)',
            tickvals=[1, 10, 100, 1000, 10000, 100000],
            tickformat=',',
            showgrid=True,
            gridcolor='lightgrey',
            gridwidth=1
        )
    )

    fig.show()


def plot_pie_summary(summary_df):
    # Filter data
    summary_df_excl_total = summary_df[summary_df["Phase"] != "Total"]
    summary_df_total = summary_df[summary_df["Phase"] == "Total"]

    # Extract values
    phases = summary_df_excl_total["Phase"]
    co_em = summary_df_excl_total["CO Emissions (g)"]
    nox_em = summary_df_excl_total["NOx Emissions (g)"]
    hc_em = summary_df_excl_total["HC Emissions (g)"]


    # Sort by value descending
    sorted_co_data = sorted(zip(phases, co_em), key=lambda x: x[1], reverse=True)
    sorted_nox_data = sorted(zip(phases, nox_em), key=lambda x: x[1], reverse=True)
    sorted_hc_data = sorted(zip(phases, hc_em), key=lambda x: x[1], reverse=True)

    # Your color palette from largest to smallest
    color_palette_co = ["#4197CA", "#64B6E2", "#9AD3F1", "#BCE3F6", "#DEF2FA"]
    color_palette_nox = ["#CB8712", "#E69F00", "#F1B733", "#F7CD66", "#FCE399"]
    color_palette_hc = ["#00664E", "#009E73", "#33B384", "#66C495", "#99D6B1"]

    # Unzip
    sorted_co_phases, sorted_co_em = zip(*sorted_co_data)
    sorted_nox_phases, sorted_nox_em = zip(*sorted_nox_data)
    sorted_hc_phases, sorted_hc_em = zip(*sorted_hc_data)

    # Assign colors
    sorted_colors_co = color_palette_co[:len(sorted_co_em)]
    sorted_colors_nox = color_palette_nox[:len(sorted_co_em)]
    sorted_colors_hc = color_palette_hc[:len(sorted_co_em)]

    sorted_nox_phases = [f"NOx / {phase}" for phase in sorted_nox_phases]
    sorted_co_phases = [f"CO / {phase}" for phase in sorted_co_phases]
    sorted_hc_phases = [f"HC / {phase}" for phase in sorted_hc_phases]

    em_data = sorted_nox_em + sorted_co_em + sorted_hc_em
    em_phases = sorted_nox_phases + sorted_co_phases + sorted_hc_phases
    em_colors = color_palette_nox + color_palette_co + color_palette_hc

    total_co = summary_df_total["CO Emissions (g)"]
    total_nox = summary_df_total["NOx Emissions (g)"]
    total_hc = summary_df_total["HC Emissions (g)"]

    total_em = pd.concat([total_nox, total_co, total_hc])

    fig=go.Figure()

    # Create subplot layout
    fig = make_subplots(
        rows=1, cols=4,
        column_widths=[0.25, 0.25, 0.25, 0.25],
        specs=[
            [{"type": "domain"}, {"type": "domain"}, {"type": "domain"}, {"type": "domain"}]
        ],
        subplot_titles=(
            "<b>NOₓ Emissions (g)</b><br><sup>Emission of NOx tracked across Phases</sup>", 
            "<b>CO Emissions (g)</b><br><sup>Emission of CO tracked across Phases</sup>", 
            "<b>HC Emissions (g)</b><br><sup>Emission of HC tracked across Phases</sup>",
            '<b>Engine Emissions Breakdown (g)</b><br><sup>Outer Ring: Total Data; Inner Ring: Phase-Wise Data</sup>'
        )
    )

    # INNER - TOTAL
    fig.add_trace(
        go.Pie(
            domain=dict(x=[0.0, 0.5]), 
            labels=["NOx", "CO", "HC"],
            textinfo='none',
            values=total_em,
            hole=0.3,
            sort=False,
            direction='clockwise',
            rotation=0,
            showlegend=False,
            hovertemplate='Pollutant: %{label}<br>Percentage: %{percent}<br>Emissions: %{value:.1f} g<extra></extra>',
            marker=dict(
                colors=("#E69F00","#64B6E2","#009E73"),
                line=dict(
                    color='white',
                    width=0.5
                )
            )
        ),
        row=1, col=4
    )

    # OUTER - PHASES
    fig.add_trace(
        go.Pie(
            domain=dict(x=[0.0, 0.5]),
            labels=em_phases,
            values=em_data,
            textinfo='none',
            hole=0.75,
            sort=False,
            direction='clockwise',
            rotation=0,
            showlegend=False,
            hovertemplate='Pollutant / Phase: %{label}<br>Percentage: %{percent}<br>Emissions: %{value:.1f} g<extra></extra>',
            marker=dict(
                colors=em_colors,
                line=dict(
                    color='white',
                    width=0.5 
                )
            )
        ),
        row=1, col=4
    )

    fig.add_trace(
        go.Pie(
            labels=sorted_nox_phases,
            values=sorted_nox_em,
            name="NOx",
            pull=[0.05],
            textinfo='none',
            legendgroup="NOx",
            showlegend=True,
            marker=dict(colors=sorted_colors_nox),
            hovertemplate='Phase: %{label}<br>Percentage: %{percent}<br>Emissions: %{value:.1f} g<extra></extra>',
            domain=dict(y=[0.66, 0.86]),  # Shifted further down
            sort=False,
            direction="clockwise",
            rotation=0
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Pie(
            labels=sorted_co_phases,
            values=sorted_co_em,
            name="CO",
            pull=[0.05],
            textinfo='none',
            legendgroup="CO",
            showlegend=True,
            marker=dict(colors=sorted_colors_co),
            hovertemplate='Phase: %{label}<br>Percentage: %{percent}<br>Emissions: %{value:.1f} g<extra></extra>',
            domain=dict(y=[0.36, 0.56]),  # Shifted further down
            sort=False,
            direction="clockwise",
            rotation=0
        ),
        row=1, col=2
    )

    fig.add_trace(
        go.Pie(
            labels=sorted_hc_phases,
            values=sorted_hc_em,
            name="HC",
            pull=[0.05],
            textinfo='none',
            legendgroup="HC",
            showlegend=True,
            marker=dict(colors=sorted_colors_hc),
            hovertemplate='Phase: %{label}<br>Percentage: %{percent}<br>Emissions: %{value:.1f} g<extra></extra>',
            domain=dict(y=[0.06, 0.26]),  # Shifted further down
            sort=False,
            direction="clockwise",
            rotation=0
        ),
        row=1, col=3
    )

    # Layout settings
    fig.update_layout(
        height=700,
        template='simple_white',
        title_font=dict(size=20),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.15, 
            xanchor='center',
            x=0.5,
            title=None,
            font=dict(size=12)
        ),
        margin=dict(l=20, r=20, t=80, b=80),
        font=dict(size=12),
    )

    fig.show()

def plot_fuel_flow_summary(summary_df):
    summary_df_excl_total = summary_df[summary_df['Phase'] != 'Total'].copy()

    # Compute key time points
    summary_df_excl_total['Start Time (s)'] = summary_df_excl_total['Duration (s)'].cumsum() - summary_df_excl_total['Duration (s)']
    summary_df_excl_total['End Time (s)'] = summary_df_excl_total['Duration (s)'].cumsum()
    summary_df_excl_total['Mid Time (s)'] = (summary_df_excl_total['Start Time (s)'] + summary_df_excl_total['End Time (s)']) / 2

    # Get values for flat extrapolation
    start_time = summary_df_excl_total['Start Time (s)'].iloc[0]
    end_time = summary_df_excl_total['End Time (s)'].iloc[-1]
    first_flow = summary_df_excl_total['Fuel Flow (kg/s)'].iloc[0]
    last_flow = summary_df_excl_total['Fuel Flow (kg/s)'].iloc[-1]

    # Construct extended x and y
    x_extended = [start_time] + summary_df_excl_total['Mid Time (s)'].tolist() + [end_time]
    y_extended = [first_flow] + summary_df_excl_total['Fuel Flow (kg/s)'].tolist() + [last_flow]

    # Plot with filled area
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x_extended,
        y=y_extended,
        mode='lines+markers',
        name='Fuel Flow (kg/s)',
        line=dict(color='rgba(255,0,0,0.3)'),
        marker=dict(color="#C44E52"),
        text=["Flat Start"] + summary_df_excl_total['Phase'].tolist() + ["Flat End"],
        hovertemplate="Fuel Flow: %{y:.2f} kg/s<br>Time: %{x:.0f} s<extra></extra>"
    ))

    fig.add_trace(go.Scatter(
        x=x_extended,
        y=y_extended,
        mode='lines',
        fill='tozeroy',
        name='Fuel Used (kg)',
        line=dict(color='rgba(255,0,0,0.3)'),
        marker=dict(color="#C44E52"),
        text=["Flat Start"] + summary_df_excl_total['Phase'].tolist() + ["Flat End"],
        hovertemplate="Fuel Flow: %{y:.2f} kg/s<br>Time: %{x:.0f} s<extra></extra>"
    ))

    fig.update_layout(
        xaxis_title='Time (s)',
        yaxis_title='Fuel Flow (kg/s)',
        title='<b>Fuel Flow (kg/s) over Time (s)</b><br><sup>Midpoints used for phase-level fuel flow; extended flat to full mission time</sup>',
        template='simple_white',
        showlegend=True,
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgrey',
            range=[0 , x_extended[-1]]
        ),
        yaxis=dict(
            showgrid=True, 
            gridwidth=1, 
            gridcolor='lightgrey'
        )
    )

    fig.show()

def plot_emissions_line_summary(summary_df):
    summary_df_excl_total = summary_df[summary_df['Phase'] != 'Total'].copy()

    # Extract values
    phases = summary_df_excl_total["Phase"]
    co_em = summary_df_excl_total["CO Emissions (g)"]
    nox_em = summary_df_excl_total["NOx Emissions (g)"]
    hc_em = summary_df_excl_total["HC Emissions (g)"]

    # Compute key time points
    summary_df_excl_total['Start Time (s)'] = summary_df_excl_total['Duration (s)'].cumsum() - summary_df_excl_total['Duration (s)']
    summary_df_excl_total['End Time (s)'] = summary_df_excl_total['Duration (s)'].cumsum()
    summary_df_excl_total['Mid Time (s)'] = (summary_df_excl_total['Start Time (s)'] + summary_df_excl_total['End Time (s)']) / 2

    # Get values for flat extrapolation
    start_time = summary_df_excl_total['Start Time (s)'].iloc[0]
    end_time = summary_df_excl_total['End Time (s)'].iloc[-1]
    nox_start = summary_df_excl_total['NOx Emissions (g)'].iloc[0]
    nox_end = summary_df_excl_total['NOx Emissions (g)'].iloc[-1]
    co_start = summary_df_excl_total['CO Emissions (g)'].iloc[0]
    co_end = summary_df_excl_total['CO Emissions (g)'].iloc[-1]
    hc_start = summary_df_excl_total['HC Emissions (g)'].iloc[0]
    hc_end = summary_df_excl_total['HC Emissions (g)'].iloc[-1]

    # Construct extended x and y
    time_extended = [start_time] + summary_df_excl_total['Mid Time (s)'].tolist() + [end_time]
    nox_extended = [nox_start] + summary_df_excl_total['NOx Emissions (g)'].tolist() + [nox_end]
    co_extended = [co_start] + summary_df_excl_total['CO Emissions (g)'].tolist() + [co_end]
    hc_extended = [hc_start] + summary_df_excl_total['HC Emissions (g)'].tolist() + [hc_end]

    # Plot with filled area
    fig = go.Figure()


    fig.add_trace(go.Scatter(
        x=time_extended,
        y=nox_extended,
        mode='lines+markers',
        name='NOx Emitted (g)',
        line=dict(color='#E69F00'),
        marker=dict(color="#E69F00"),
        text=["Flat Start"] + phases.tolist() + ["Flat End"],
        hovertemplate="NOx Emitted: %{y:.2f} g<br>Time: %{x:.0f} s<br>Phase: %{text}<extra></extra>"
    ))

    fig.add_trace(go.Scatter(
        x=time_extended,
        y=co_extended,
        mode='lines+markers',
        name='CO Emitted (g)',
        line=dict(color='#56B4E9'),
        marker=dict(color="#56B4E9"),
        text=["Flat Start"] + phases.tolist() + ["Flat End"],
        hovertemplate="NOx Emitted: %{y:.2f} g<br>Time: %{x:.0f} s<br>Phase: %{text}<extra></extra>"
    ))

    fig.add_trace(go.Scatter(
        x=time_extended,
        y=hc_extended,
        mode='lines+markers',
        name='HC Emitted (g)',
        line=dict(color='#009E73'),
        marker=dict(color="#009E73"),
        text=["Flat Start"] + phases.tolist() + ["Flat End"],
        hovertemplate="NOx Emitted: %{y:.2f} g<br>Time: %{x:.0f} s<br>Phase: %{text}<extra></extra>"
    ))

    fig.update_layout(
        xaxis_title='Time (s)',
        yaxis_title='Fuel Flow (kg/s)',
        title='<b>Emissions (g) over Time (s)</b><br><sup>Midpoints used for phase-level Emissions; extended flat to full mission time</sup>',
        template='simple_white',
        showlegend=True,
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgrey',
            range=[0 , time_extended[-1]]
        ),
        yaxis=dict(
            type='log',
            title='Emissions (g)',
            showgrid=True,
            gridcolor='lightgrey',
            gridwidth=1,
            minor=dict(ticklen=1, showgrid=True)
        )
    )

    fig.show()