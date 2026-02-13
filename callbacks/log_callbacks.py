from io import StringIO
from dash import Output, Input
import pandas as pd
from app import app
from utils.data_loader import load_csv

@app.callback(
	Output("log-table", "data"),
    Input("log-string", "data"),
)
def update_log_table(log_string):
	return load_csv(log_string).to_dict("records")