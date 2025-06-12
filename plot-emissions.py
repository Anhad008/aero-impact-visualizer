import plotly.graph_objects as go
import pandas as pd

def plot_bar_summary(summary_df):
    phases = summary_df["Phase"]
    co_emm = summary_df["CO emissions (g)"]
    nox_emm = summary_df["NOx emissions (g)"]
    hc_emm = summary_df["HC emissions (g)"]

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
