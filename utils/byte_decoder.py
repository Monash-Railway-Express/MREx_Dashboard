def decode_bytes(row, cols, signed=False, endian="little"):
    """
    Generic decoder for CAN data bytes.
    
    cols   = list of column names, e.g. ["Data4", "Data5", "Data6", "Data7"]
    signed = True for 2's complement
    endian = "little" or "big"
    """

    # Clean and convert each byte
    bytes_list = []
    for col in cols:
        val = str(row[col]).replace("0x", "").strip()
        bytes_list.append(int(val, 16))

    # Combine into integer
    if endian == "little":
        raw = 0
        for i, b in enumerate(bytes_list):
            raw |= b << (8 * i)
    else:
        raw = 0
        for b in bytes_list:
            raw = (raw << 8) | b

    # Convert to signed if needed
    if signed:
        bit_len = 8 * len(cols)
        sign_bit = 1 << (bit_len - 1)
        full_range = 1 << bit_len

        if raw & sign_bit:
            raw -= full_range

    return raw