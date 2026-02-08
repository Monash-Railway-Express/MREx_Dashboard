from dash import Input, Output
from app import app
from utils.data_loader import load_csv

@app.callback(
    Output("id-selector", "options"),
    Output("id-selector", "value"),
    Output("time-range-slider", "min"),
    Output("time-range-slider", "max"),
    Output("time-range-slider", "value"),
    Output("time-range-slider", "marks"),
    Input("file-selector", "value"),
)
def update_id_selector(filename):
    if not filename:
        return [], [], 0, 0, [0, 0], {}

    df = load_csv(filename)
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
