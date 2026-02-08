from dash import html, dcc, Input, Output
# Assuming load_csv is a function that loads your CSV and is already defined or imported
# from your_data_loading_module import load_csv  

def selectors(csv_files):
    return html.Div(
        children=[
            # File selector
            html.Div(
                className="file-menu",
                children=[
                    html.Div("Select CSV File", className="menu-title"),
                    dcc.Dropdown(
                        id="file-selector",
                        options=[{"label": f, "value": f} for f in csv_files],
                        value=csv_files[0] if csv_files else None,
                        clearable=False,
                        className="dropdown",
                    ),
                ],
            ),

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
                        ),
                        className="slider-wrapper"
                    ),
                ],
            )

        ]
    )


