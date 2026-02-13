import os
from dash import Input, Output
import pandas as pd
from app import app
from utils.data_loader import load_csv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGS_DIR = os.path.join(BASE_DIR, "Logs")

@app.callback(
    Output("log-string", "data"),
    Input("file-selector", "value"),
)
def update_log_string(filename):
    if not filename:
        return ""
    
    path = os.path.join(LOGS_DIR, filename)
    
    with open(path, "r") as file:
        log_string = file.read()

    return log_string

@app.callback(
    Output("id-selector", "options"),
    Output("id-selector", "value"),
    Output("time-range-slider", "min"),
    Output("time-range-slider", "max"),
    Output("time-range-slider", "value"),
    Output("time-range-slider", "marks"),
    Input("log-string", "data"),
)
def update_id_selector(log_string):
    df = load_csv(log_string)
    ids = sorted(df["ID"].unique())

    # Convert timestamps to POSIX seconds
    start_ts = df["Timestamp"].min().value // 10**6   # to milliseconds
    end_ts = df["Timestamp"].max().value // 10**6


    marks = {
        start_ts: df["Timestamp"].min().strftime("%H:%M:%S"),
        end_ts: df["Timestamp"].max().strftime("%H:%M:%S"),
    }


    return (
        [{"label": i, "value": i} for i in ids],
        ids,
        start_ts,
        end_ts,
        [start_ts, end_ts],
        marks,
    )
