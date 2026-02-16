from dash import Input, Output
from app import app
import datetime

@app.callback(
    Output("start-time", "value"),
    Output("end-time", "value"),
    Input("time-range-slider", "value"),
)
def display_times(slider_range):
    if not slider_range or len(slider_range) != 2:
        return "", ""

    start_ms, end_ms = slider_range
    try:
        start_dt = datetime.datetime.fromtimestamp(start_ms / 1000)
        end_dt = datetime.datetime.fromtimestamp(end_ms / 1000)
        return (
            start_dt.strftime("%H:%M:%S"),
            end_dt.strftime("%H:%M:%S"),
        )
    except:
        return "", ""
