from dash import Input, Output
from app import app

# Client-side callback for performance on frequent WebSocket messages
app.clientside_callback(
    """function(message) {
        if (!message) {
            return "";
        }
        return message.data;
    }
    """,
    Output("feed", "children"),
    Input("ws", "message")
)