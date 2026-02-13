from io import StringIO
from dash import Output, Input
import pandas as pd
from app import app
from callbacks.graph_callbacks import _get_time_range
from utils.data_loader import load_csv

@app.callback(
    Output("log-table", "data"),
    Input("log-string", "data"),
    Input("id-selector", "value"),
    Input("time-range-slider", "value"),
)
def update_log_table(log_string, selected_ids, slider_range):
    """Update log table based on file selection, IDs, and time range."""
    df = load_csv(log_string)
    df = df[df["ID"].isin(selected_ids)]

    # Determine time range
    start_dt, end_dt = _get_time_range(df, slider_range)

    # Filter by time range
    df = df[(df["Timestamp"] >= start_dt) & (df["Timestamp"] <= end_dt)]
    
    return df.to_dict("records")