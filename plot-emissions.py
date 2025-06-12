import plotly.graph_objects as go
import pandas as pd

def plot_bar_summary(summary_df):
    phases = summary_df["Phase"]
    co_emm = summary_df["CO emissions (g)"]
    nox_emm = summary_df["NOx emissions (g)"]
    hc_emm = summary_df["HC emissions (g)"]

    fig = go.Figure([
        go.Bar(name='HC emissions', x=phases, y=hc_emm),
        go.Bar(name='NOx emissions', x=phases, y=nox_emm),
        go.Bar(name='CO emissions', x=phases, y=co_emm)
    ])

    fig.update_layout(barmode='group', yaxis_type='log')
    fig.show()
