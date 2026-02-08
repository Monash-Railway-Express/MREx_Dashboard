from dash import html, dcc

def energy_graphs():
    return html.Div(
        className="graph-row",
        children=[
            html.Div(
                className="card",
                children=[
                    dcc.Dropdown(
                        id="energy-metric-selector",
                        options=[
                            {"label": "Current", "value": "Current"},
                            {"label": "Voltage", "value": "Voltage"},
                            {"label": "Power", "value": "Power"},
                        ],
                        value="Current",
                        clearable=False,
                        className="dropdown"
                    ),
                    dcc.Graph(id="energy-metric-graph", config={"displayModeBar": False}),
                ],
            ),
            html.Div(
                dcc.Graph(id="soc-graph", config={"displayModeBar": False}),
                className="card",
            ),
        ],
    )
