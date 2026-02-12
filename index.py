import os
from app import app
from layouts.main_layout import main_layout

logs_dir = os.path.join(os.path.dirname(__file__), "Logs")
csv_files = [f for f in os.listdir(logs_dir) if f.lower().endswith(".csv")][::-1]

app.layout = main_layout(csv_files)

# Import callbacks (they auto-register)
import callbacks.file_callbacks
import callbacks.graph_callbacks
import callbacks.agg_callbacks
import callbacks.time_callbacks
import callbacks.power_callbacks
import callbacks.ws_callbacks


if __name__ == "__main__":
    app.run(debug=True)
