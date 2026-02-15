from dash import html, dash_table
import dash_daq as daq

def log_table():
    return html.Div(
        className="data-table",
        children=[
            daq.BooleanSwitch(
                id="table-selector",
                label="Translation?"
            ),
            dash_table.DataTable(
                id="log-table",
                sort_action="native",
            ),
        ],
    )