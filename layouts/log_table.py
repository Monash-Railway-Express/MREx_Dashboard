from dash import html, dash_table

def log_table():
    return html.Div(
        className="data-table",
        children=[
            dash_table.DataTable(
                id="log-table",
                fixed_rows={"headers": True}
            )
        ],
    )