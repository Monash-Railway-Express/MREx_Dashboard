import os
import base64
from dash import State, ctx, Input, Output, no_update
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
    Output("id-selector", "options", allow_duplicate=True),
    Output("id-selector", "value", allow_duplicate=True),
    Input("ws-connected", "data"),
    prevent_initial_call=True,
)
def reset_id_selector(ws_connected):
    if (ws_connected):
        return [], []
    else:
        return no_update

@app.callback(
    Output("id-selector", "options"),
    Output("id-selector", "value"),
    Output("time-range-slider", "min"),
    Output("time-range-slider", "max"),
    Output("time-range-slider", "value"),
    Output("time-range-slider", "marks"),
    Input("log-string", "data"),
    State("ws-connected", "data"),
    State("id-selector", "options"),
    State("id-selector", "value"),
    State("time-range-slider", "max"),
    State("time-range-slider", "value"),
)
def update_id_selector(log_string, ws_connected, previous_ids, previous_selected_ids, previous_max_time, previous_selected_times):
    df = load_csv(log_string)
    ids = sorted(df["ID"].unique())

    # Convert timestamps to POSIX seconds
    start_ts = df["Timestamp"].min().value // 10**6   # to milliseconds
    end_ts = df["Timestamp"].max().value // 10**6


    marks = {
        start_ts: df["Timestamp"].min().strftime("%H:%M:%S"),
        end_ts: df["Timestamp"].max().strftime("%H:%M:%S"),
    }

    if ws_connected:
        if (len(previous_ids) == len(previous_selected_ids)):
            selected_ids = ids
        else:
            selected_ids = no_update

        if (previous_selected_times[1] == previous_max_time):
            selected_times = [previous_selected_times[0], end_ts]
        else:
            selected_times = no_update
    else:
        selected_ids = ids
        selected_times = [start_ts, end_ts]

    return (
        [{"label": i, "value": i} for i in ids],
        selected_ids,
        start_ts,
        end_ts,
        selected_times,
        marks,
    )
