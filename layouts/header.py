from dash import html

def header():
    return html.Div(
        className="header-container",
        children=[
            html.Img(src="/assets/MREx_logo.png", className="header-image"),
            html.Div(
                className="header-text",
                children=[
                    html.H1("CAN Bus Dashboard", className="header-title"),
                    html.P("Explore CAN messages over time and analyze",
                           className="header-description"),
                ],
            ),
        ],
    )
