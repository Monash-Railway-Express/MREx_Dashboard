from dash_extensions import WebSocket

def websocket():
    return WebSocket(id="ws", url="ws://10.0.0.1/ws")