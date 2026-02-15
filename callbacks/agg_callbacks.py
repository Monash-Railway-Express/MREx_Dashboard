from dash import Output, Input, State
from app import app
from utils.data_loader import load_csv
import plotly.express as px
import plotly.io as pio
import pandas as pd

pio.templates.default = "plotly"


@app.callback(
    Output("agg-time-series", "figure"),
    Output("agg-bar", "figure"),
    Input("second-interval", "n_intervals"),
    Input("id-selector", "value"),
    Input("time-range-slider", "value"),
    Input("agg-interval", "value"),
    State("dark-selector", "on"),
    State("log-string", "data"),
)
def update_aggregated_graphs(_, selected_ids, slider_range, agg_interval, dark, log_string):
    if dark:
        template = "plotly_dark"
    else:
        template = None

    df = load_csv(log_string)
    df = df[df["ID"].isin(selected_ids)]

    # Filter by time range using timestamps, not indices
    start_dt, end_dt = _get_time_range(df, slider_range)
    df = df[(df["Timestamp"] >= start_dt) & (df["Timestamp"] <= end_dt)]

    if df.empty:
        return px.line(template=template), px.bar(template=template)

    df = df.set_index("Timestamp")
    agg_counts = (
        df.groupby("ID")
          .resample(agg_interval, include_groups=False)
          .size()
          .reset_index(name="Count")
    )

    if agg_counts.empty:
        return px.line(template=template), px.bar(template=template)
    
    fig_time = px.line(
        agg_counts,
        x="Timestamp",
        y="Count",
        color="ID",
        title=f"Messages per {agg_interval}",
        template=template,
    )

    totals = agg_counts.groupby("ID")["Count"].mean().reset_index()
    fig_bar = px.bar(
        totals,
        x="ID",
        y="Count",
        color="ID",
        title=f"Average Messages per ID ({agg_interval})",
        text="Count",
        template=template,
    )
    fig_bar.update_traces(textposition="outside")

    return fig_time, fig_bar


def _get_time_range(df, slider_range):
    """Extract time range from slider or use full range."""
    if not slider_range or not isinstance(slider_range, (list, tuple)) or len(slider_range) != 2:
        return df["Timestamp"].min(), df["Timestamp"].max()

    start_ms, end_ms = slider_range
    start_dt = pd.to_datetime(start_ms, unit='ms')
    end_dt = pd.to_datetime(end_ms, unit='ms')


    return start_dt, end_dt
    return start_dt, end_dt
