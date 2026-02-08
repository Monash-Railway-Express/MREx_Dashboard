from dash import html, dcc

def agg_graphs():
    return html.Div(
        children=[
            html.Div(
                className="selector",
                children=[
                    html.Div("Select Aggregation Interval", className="menu-title"),
                    dcc.Dropdown(
                        id="agg-interval",
                        options=[
                            {"label": "1 Second", "value": "1s"},
                            {"label": "10 Seconds", "value": "10s"},
                            {"label": "1 Minute", "value": "1min"},
                        ],
                        value="1s",
                        clearable=False,
                        className="dropdown",
                    ),
                ],
            ),

            html.Div(
                className="graph-row",
                children=[
                    html.Div(dcc.Graph(id="agg-time-series", config={"displayModeBar": False}),
                             className="card"),
                    html.Div(dcc.Graph(id="agg-bar", config={"displayModeBar": False}),
                             className="card"),
                ],
            ),
        ]
    )
