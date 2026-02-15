import math
import csv
from datetime import datetime, timedelta

def encode_le_32bit_signed(value):
    """Return 4 bytes (little-endian) of a signed 32-bit integer."""
    if value < 0:
        value = (1 << 32) + value  # 2's complement

    b4 = value & 0xFF
    b5 = (value >> 8) & 0xFF
    b6 = (value >> 16) & 0xFF
    b7 = (value >> 24) & 0xFF

    return [f"0x{b4:02X}", f"0x{b5:02X}", f"0x{b6:02X}", f"0x{b7:02X}"]

# Generate 120-sample sine wave from -200 to +200
samples = 120
amplitude = 200
start_time = datetime(2025, 1, 1, 0, 0, 0)

rows = []
for i in range(samples):
    theta = (2 * math.pi * i) / samples
    value = int(amplitude * math.sin(theta))

    b4, b5, b6, b7 = encode_le_32bit_signed(value)

    timestamp = (start_time + timedelta(seconds=i)).strftime("%Y-%m-%d %H:%M:%S")

    rows.append([
        timestamp, "0x387", 8,
        "0x00", "0x00", "0x00", "0x00",
        b4, b5, b6, b7
    ])

# Write CSV
with open("sine_power_120.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Timestamp","ID","DLC","Data0","Data1","Data2","Data3","Data4","Data5","Data6","Data7"])
    writer.writerows(rows)

print("CSV generated: sine_power_120.csv")
