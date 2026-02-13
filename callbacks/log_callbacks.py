from dash import Output, Input
from app import app
from utils.data_loader import load_csv

@app.callback(
	Output("log-table", "data"),
    Input("file-selector", "value"),
)
def update_log_table(filename):
	return load_csv(filename).to_dict("records")