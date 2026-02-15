from dash import Output, Input, State
import pandas as pd
from app import app
from callbacks.graph_callbacks import _get_time_range
from utils.data_loader import load_csv
from utils.translator import translate_row

@app.callback(
    Output("log-table", "data"),
    Input("second-interval", "n_intervals"),
    Input("id-selector", "value"),
    Input("time-range-slider", "value"),
    Input("table-selector", "on"),
    State("log-string", "data"),
)
def update_log_table(_, selected_ids, slider_range, translated, log_string):
    """Update log table based on file selection, IDs, and time range."""
    df = load_csv(log_string)
    df = df[df["ID"].isin(selected_ids)]

    # Determine time range
    start_dt, end_dt = _get_time_range(df, slider_range)

    # Filter by time range
    df = df[(df["Timestamp"] >= start_dt) & (df["Timestamp"] <= end_dt)]
    
    if translated:
        df = pd.DataFrame(data=[translate_row(
            row.Timestamp,
            row.ID,
            row.DLC,
            [row.Data0, row.Data1, row.Data2, row.Data3, row.Data4, row.Data5, row.Data6, row.Data7,],
        ) for row in df.itertuples()])

    return df.reset_index().to_dict("records")