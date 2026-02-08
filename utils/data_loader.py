import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGS_DIR = os.path.join(BASE_DIR, "Logs")

def list_csv_files():
    files = [f for f in os.listdir(LOGS_DIR) if f.lower().endswith(".csv")]
    return files[::-1]

def load_csv(filename):
    path = os.path.join(LOGS_DIR, filename)
    df = pd.read_csv(path, engine="python")
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    return df
