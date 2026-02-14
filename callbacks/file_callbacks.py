import os
import base64
from dash import State, ctx, Input, Output
import pandas as pd
from app import app
from utils.data_loader import load_csv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGS_DIR = os.path.join(BASE_DIR, "Logs")

@app.callback(
    Output("log-string", "data"),
    Output("ws-connected", "data"),
    Input("folder-selector", "value"),
    Input("local-selector", "contents"),
    Input("remote-selector", "n_clicks"),
    State("ws", "message"),
)
def update_log_string(filename, contents, _, message):
    if ctx.triggered_id == "local-selector":
        _, content_string = contents.split(",")
        log_string = base64.b64decode(content_string).decode("utf-8")
        return log_string, False
    elif ctx.triggered_id == "remote-selector":
        return f"Timestamp,ID,DLC,Data0,Data1,Data2,Data3,Data4,Data5,Data6,Data7\n{message["data"]}\n", True
    else:
        if not filename:
            return "", False
        
        path = os.path.join(LOGS_DIR, filename)
        
        with open(path, "r") as file:
            log_string = file.read()

        return log_string, False

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
