from io import StringIO
from dash import Output, Input
from app import app
from utils.data_loader import load_csv
import plotly.express as px
from datetime import datetime, timezone
import pandas as pd


@app.callback(
    Output("time-series-graph", "figure"),
    Output("occurrence-bar", "figure"),
    Input("log-string", "data"),
    Input("id-selector", "value"),
    Input("time-range-slider", "value"),
)
def update_graph(log_string, selected_ids, slider_range):
    """Update graphs based on file selection, IDs, and time range."""
    df = load_csv(log_string)
    df = df[df["ID"].isin(selected_ids)]

    # Determine time range
    start_dt, end_dt = _get_time_range(df, slider_range)

    # Filter by time range
    df = df[(df["Timestamp"] >= start_dt) & (df["Timestamp"] <= end_dt)]

    if df.empty:
        return {}, {}

    # Generate figures
    fig_time = _create_time_series_figure(df)
    fig_bar = _create_occurrence_figure(df)

    return fig_time, fig_bar


def _get_time_range(df, slider_range):
    """Extract time range from slider or use full range."""
    if not slider_range or not isinstance(slider_range, (list, tuple)) or len(slider_range) != 2:
        return df["Timestamp"].min(), df["Timestamp"].max()

    start_ms, end_ms = slider_range
    start_dt = pd.to_datetime(start_ms, unit='ms')  # Remove utc=True
    end_dt = pd.to_datetime(end_ms, unit='ms')      # Remove utc=True

    return start_dt, end_dt


def _create_time_series_figure(df):
    """Create scatter plot of messages over time."""
    fig = px.scatter(
        df,
        x="Timestamp",
        y="ID",
        color="ID",
        title="CAN Messages Over Time",
    )
    fig.update_xaxes(rangeslider_visible=True)

    return fig


def _create_occurrence_figure(df):
    """Create bar chart of message occurrences per ID."""
    counts = df["ID"].value_counts().reset_index(name="Count")

    fig = px.bar(
        counts,
        x="ID",
        y="Count",
        color="ID",
        title="Occurrences per ID",
        text="Count",
    )
    fig.update_traces(textposition="outside")

    return fig
