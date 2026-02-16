from io import StringIO
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGS_DIR = os.path.join(BASE_DIR, "Logs")

def list_csv_files():
    files = [f for f in os.listdir(LOGS_DIR) if f.lower().endswith(".csv")]
    return files[::-1]

def load_csv(log_string):
    try:
        df = pd.read_csv(StringIO(log_string), engine="python")
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])
        return df
    except:
        return pd.DataFrame(columns=["Timestamp", "ID", "DLC", "Data0", "Data1", "Data2", "Data3", "Data4", "Data5", "Data6", "Data7"])
