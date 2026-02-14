from dash import Input, Output, State
from app import app

# Client-side callback for performance on frequent WebSocket messages
app.clientside_callback(
    """function (message, current_log, connected) {
        if (!message || !connected) {
            return dash_clientside.no_update;
        }
		
        return current_log + message.data + "\\n";
    }
    """,
    Output("log-string", "data", allow_duplicate=True),
    Input("ws", "message"),
	State("log-string", "data"),
	State("ws-connected", "data"),
	prevent_initial_call=True,
)

@app.callback(
	Output("remote-selector", "disabled"),
	Input("ws", "state"),
)
def check_ws_state(state):
	if (state["readyState"] == 1): # WebSocket.OPEN
		return False
	else:
		return True