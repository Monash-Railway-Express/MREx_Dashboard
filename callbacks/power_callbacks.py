from io import StringIO
from dash import Output, Input, State
from app import app
from callbacks.graph_callbacks import _get_time_range
from utils.data_loader import load_csv
import plotly.express as px
import plotly.io as pio
import pandas as pd

@app.callback(
    Output("energy-metric-graph", "figure"),
    Output("soc-graph", "figure"),
    Input("second-interval", "n_intervals"),
    Input("id-selector", "value"),
    Input("time-range-slider", "value"),
    Input("energy-metric-selector", "value"),
    State("dark-selector", "on"),
    State("log-string", "data"),
)
def update_energy_graphs(_, selected_ids, slider_range, metric, dark, log_string):
    if dark:
        template = "plotly_dark"
    else:
        template = None

    df = load_csv(log_string)

    # Time filtering
    start_dt, end_dt = _get_time_range(df, slider_range)
    df = df[(df["Timestamp"] >= start_dt) & (df["Timestamp"] <= end_dt)]

    if df.empty:
        return px.line(template=template), px.line(template=template)

    # --- LEFT GRAPH LOGIC ---
    if metric == "Current":
        df["ID"] = df["ID"].astype(str)
        df_metric = df[df["ID"] == "0x187"]   # FIXED

        if df_metric.empty:
            fig_energy = px.line(template=template)
        else:
            df_metric["Current"] = df_metric.apply(
                lambda row: decode_bytes(row, ["Data4", "Data5", "Data6", "Data7"], signed=True),
                axis=1
            )


            fig_energy = px.line(
                df_metric,
                x="Timestamp",
                y="Current",
                template=template,
            )

    elif metric == "Voltage":
        df["ID"] = df["ID"].astype(str)
        df_metric = df[df["ID"] == "0x187"]   # FIXED

        if df_metric.empty:
            fig_energy = px.line(template=template)
        else:
            df_metric["Voltage"] = df_metric.apply(
            lambda row: decode_bytes(row, ["Data2", "Data3"], signed=True),
            axis=1
        )


            fig_energy = px.line(
                df_metric,
                x="Timestamp",
                y="Voltage",
                template=template,
            )

    else:
        df["ID"] = df["ID"].astype(str)
        df_metric = df[df["ID"] == "0x387"]   # FIXED

        if df_metric.empty:
            fig_energy = px.line(template=template)
        else:
            df_metric["Power"] = df_metric.apply(
                lambda row: decode_bytes(row, ["Data4", "Data5", "Data6", "Data7"], signed=True),
                axis=1
            )


            fig_energy = px.line(
                df_metric,
                x="Timestamp",
                y="Power",
                template=template,
            )


    # --- RIGHT GRAPH: SOC ---
    df["ID"] = df["ID"].astype(str)
    df_soc = df[df["ID"] == "0x287"]

    if df_soc.empty:
        fig_soc = px.line(template=template)
    else:
        df_soc["SOC"] = df_soc.apply(
            lambda row: decode_bytes(row, ["Data2", "Data3"], signed=True),
            axis=1
        )


        fig_soc = px.line(
            df_soc,
            x="Timestamp",
            y="SOC",
            title="State of Charge (SOC)",
            template=template,
        )


    return fig_energy, fig_soc



def decode_bytes(row, cols, signed=False, endian="little"):
    """
    Generic decoder for CAN data bytes.
    
    cols   = list of column names, e.g. ["Data4", "Data5", "Data6", "Data7"]
    signed = True for 2's complement
    endian = "little" or "big"
    """

    # Clean and convert each byte
    bytes_list = []
    for col in cols:
        val = str(row[col]).replace("0x", "").strip()
        bytes_list.append(int(val, 16))

    # Combine into integer
    if endian == "little":
        raw = 0
        for i, b in enumerate(bytes_list):
            raw |= b << (8 * i)
    else:
        raw = 0
        for b in bytes_list:
            raw = (raw << 8) | b

    # Convert to signed if needed
    if signed:
        bit_len = 8 * len(cols)
        sign_bit = 1 << (bit_len - 1)
        full_range = 1 << bit_len

        if raw & sign_bit:
            raw -= full_range

    return raw



