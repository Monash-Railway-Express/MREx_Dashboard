from dash import Output, Input, Patch, no_update
from app import app
@app.callback(
    Output("page-container", "className"),
    Output("agg-time-series", "figure", allow_duplicate=True),
    Output("agg-bar", "figure", allow_duplicate=True),
    Output("time-series-graph", "figure", allow_duplicate=True),
    Output("occurrence-bar", "figure", allow_duplicate=True),
    Output("energy-metric-graph", "figure", allow_duplicate=True),
    Output("soc-graph", "figure", allow_duplicate=True),
    Input("dark-selector", "on"),
    prevent_initial_call=True
)
def update_theme(dark):
	if dark:
		className = "dark"
		template = "plotly_dark"
	else:
		className = ""
		template = None
	
	patch = Patch()
	patch["layout"]["template"] = template

	return className, patch, patch, patch, patch, patch, patch