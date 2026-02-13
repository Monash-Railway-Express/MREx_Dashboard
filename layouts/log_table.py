from dash import dash_table

def log_table():
    return dash_table.DataTable(
        id="log-table",
    )
