from dash import html
from dash_extensions import WebSocket

def websocket():
    return html.Div(
        children=[
            WebSocket(id="ws", url="ws://10.0.0.1/ws"),
            html.Div(id="feed")
        ],
    )