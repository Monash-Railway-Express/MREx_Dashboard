from dash import html
from .header import header
from .selectors import selectors
from .time_graphs import time_graphs
from .agg_graphs import agg_graphs
from .power import energy_graphs

def main_layout(csv_files):
    return html.Div(
        className="page-container",
        children=[
            header(),
            selectors(csv_files),
            time_graphs(),
            agg_graphs(),
            energy_graphs(),

        ],
    )
