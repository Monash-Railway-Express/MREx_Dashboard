from dash import html, dcc
import dash_daq as daq
# Assuming load_csv is a function that loads your CSV and is already defined or imported
# from your_data_loading_module import load_csv  

def selectors(csv_files):
    return html.Div(
        children=[
            # Dark theme selector
            daq.BooleanSwitch(
                id="dark-selector",
                label="Dark?",
            ),

            # File selector
            html.H1("Select log source"),

            html.Div(
                className="file-menu-container",
                children=[
                    html.Div(
                        className="file-menu",
                        children=[
                            html.Div("Logs folder", className="menu-title"),
                            dcc.Dropdown(
                                id="folder-selector",
                                options=[{"label": f, "value": f} for f in csv_files],
                                value=csv_files[0] if csv_files else None,
                                clearable=False,
                                className="dropdown",
                            ),
                        ],
                    ),

                    html.Div(
                        className="file-menu",
                        children=[
                            html.Div("Local device", className="menu-title"),
                            dcc.Upload(
                                id="local-selector",
                                className="dnd",
                                children=[
                                    "Drag and drop or ",
                                    dcc.Button("Select file")
                                ],
                            ),
                            html.P(id="local-filepath"),
                        ],
                    ),
                    
                    html.Div(
                        className="file-menu",
                        children=[
                            html.Div("Remote server", className="menu-title"),
                            dcc.Dropdown(
                                id="remote-selector",
                                clearable=False,
                                className="dropdown",
                            ),
                        ],
                    ),

                    html.Div(
                        className="file-menu",
                        children=[
                            html.Div("Remote feed", className="menu-title"),
                            dcc.Button(
                                id="ws-selector",
                                children=["Connect to WebSocket"],
                            ),
                            html.P(id="ws-status"),
                        ],
                    ),
                ]
            ),

            html.Hr(),

            # ID selector
            html.Div(
                className="selector",
                children=[
                    html.Div("Select IDs", className="menu-title"),
                    dcc.Dropdown(id="id-selector", multi=True, className="dropdown"),
                ],
            ),

            # Time inputs (start + end)
            html.Div(
                className="time-row",
                children=[
                    html.Div(
                        className="selector",
                        children=[
                            html.Div("Start Time", className="menu-title"),
                            dcc.Input(id="start-time", type="text", className="time-input", readOnly=True)
                        ],
                    ),

                    html.Div(
                        className="selector",
                        children=[
                            html.Div("End Time", className="menu-title"),
                            dcc.Input(id="end-time", type="text", className="time-input", readOnly=True),
                        ],
                    ),
                ],
            ),


            html.Div(
                className="time-range-container",
                children=[
                    html.Div("Select Time Range", className="menu-title"),
                    html.Div(
                        dcc.RangeSlider(
                            id="time-range-slider",
                            min=0,
                            max=1,
                            value=[0, 1],
                            step=1000,
                            tooltip={"placement": "bottom", "always_visible": False},
                            allowCross=False,
                            updatemode="drag",
                        ),
                        className="slider-wrapper"
                    ),
                ],
            )

        ]
    )


