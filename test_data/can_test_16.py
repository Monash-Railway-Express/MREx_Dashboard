import math
import csv
from datetime import datetime, timedelta

def encode_le_16bit_signed(value):
    """Return 2 bytes (little-endian) of a signed 16-bit integer."""
    if value < 0:
        value = (1 << 16) + value  # 2's complement

    b2 = value & 0xFF
    b3 = (value >> 8) & 0xFF

    return [f"0x{b2:02X}", f"0x{b3:02X}"]

# Generate 120-sample sine wave from -200 to +200
samples = 120
amplitude = 200
start_time = datetime(2025, 1, 1, 0, 0, 0)

rows = []
for i in range(samples):
    theta = (2 * math.pi * i) / samples
    value = int(amplitude * math.sin(theta))

    b2, b3 = encode_le_16bit_signed(value)

    timestamp = (start_time + timedelta(seconds=i)).strftime("%Y-%m-%d %H:%M:%S")

    rows.append([
        timestamp, "0x187", 8,
        "0x00", "0x00", b2, b3,  # Data2, Data3 hold the 16-bit value
        "0x00", "0x00", "0x00", "0x00"
    ])

# Write CSV
with open("sine_voltage_120.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Timestamp","ID","DLC","Data0","Data1","Data2","Data3","Data4","Data5","Data6","Data7"])
    writer.writerows(rows)

print("CSV generated: sine_voltage_120.csv")
