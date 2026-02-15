from dash import html, dcc
from .header import header
from .selectors import selectors
from .time_graphs import time_graphs
from .agg_graphs import agg_graphs
from .power import energy_graphs
from .websocket import websocket
from .log_table import log_table

def main_layout(csv_files):
    return html.Div(
        id="page-container",
        children=[
            header(),
            selectors(csv_files),
            time_graphs(),
            agg_graphs(),
            energy_graphs(),
            log_table(),
            websocket(),
            dcc.Store(id="log-string"),
            dcc.Store(id="ws-connected"),
            dcc.Interval(id="second-interval", interval=1000),
        ],
    )
