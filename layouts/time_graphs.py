from dash import html, dcc

def time_graphs():
    return html.Div(
        className="graph-row",
        children=[
            html.Div(dcc.Graph(id="time-series-graph", config={"displayModeBar": False}),
                     className="card"),
            html.Div(dcc.Graph(id="occurrence-bar", config={"displayModeBar": False}),
                     className="card"),
        ],
    )
