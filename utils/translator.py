# Sheet https://docs.google.com/spreadsheets/d/1OaXG5B06xnvpNkGQIkrtbM_n-pCCqvnd99yezD7YYoQ/edit?usp=sharing
from utils.byte_decoder import decode_bytes


emcy_message = {

}

object_dictionary = {
    0x2000: {
        0x00: "Current",
        0x01: "Voltage",
        0x02: "State of charge",
    },
}

pdo_entries = {
    0x187: [(0x2000, 0x00, 32, True), (0x2000, 0x01, 16, True), (0x2000, 0x02, 16, True)],
}

node_name = {
    1: "Motor Controller",
    2: "Brakes",
    3: "Driver Control",
    4: "Lights",
    5: "Audio",
    6: "Sensor System",
    7: "Battery",
    8: "CAN Logger",
    9: "Driver Screen"
}

# Spec https://github.com/Monash-Railway-Express/CAN_MREx
nmt_state = {
    0x01: "Operational",
    0x02: "Stopped",
    0x80: "Pre-operational",
    0x81: "Reset node",
    0x82: "Reset communication",
}

emcy_priority = {
    0: "Major",
    1: "Minor",
}

emcy_type = {
    0x00: "CAN MREx fault",
    0x01: "Motor fault",
    0x02: "Brake fault",
    0x03: "Battery fault",
}

def translate_row(timestamp, id, dlc_int, data):
    translated = {
        "Timestamp": timestamp
    }

    id_int = intify(id)

    data = data[:dlc_int]
    data_int = []
    for datum in data:
        data_int.append(intify(datum))

    if id_int == 0x000:
        translated["Function"] = "NMT"
        translated["Node ID"] = data_int[1]
        translated["Node"] = node_name[translated["Node ID"]]
        try:
            translated["Data"] = nmt_state[data_int[0]]
        except KeyError:
            translated["Data"] = f"Unknown state {data[0]}"

    elif 0x080 <= id_int and id_int <= 0x0FF:
        translated["Function"] = "EMCY"
        translated["Node ID"] = id_int - 0x080
        translated["Node"] = node_name[translated["Node ID"]]
        try:
            translated["Data"] = f"{emcy_priority[data_int[0]]} at node {data_int[1]}: {emcy_message[concatify(data_int[5:1:-1])]}"
        except KeyError:
            translated["Data"] = f"Unknown emergency priority {data[0]} at node {data_int[1]}: message {data[2:6]}"

    elif 0x180 <= id_int and id_int <= 0x57F:
        translated["Function"] = "PDO"
        translated["Node ID"] = id_int % 0x80
        translated["Node"] = node_name[translated["Node ID"]]
        # Assuming object data boundaries are on byte boundaries - reflects a CAN MREX implementation assumption
        try:
            translated["Data"] = "| "
            current_byte = 0
            for index, subindex, bits, signed in reversed(pdo_entries[id_int]):
                upper_byte = current_byte + (bits // 8)
                cols = [i for i in range(current_byte, upper_byte, 1)]
                raw = decode_bytes(data, cols, signed)
                try:
                    translated["Data"] += f"{object_dictionary[index][subindex]}: {raw} | "
                except KeyError:
                    translated["Data"] += f"Unknown object index {index} subindex {subindex}: {raw} | "
                current_byte = upper_byte
        except KeyError:
            translated["Data"] = f"Unmapped PDO COB-ID {id} data {data}"

    elif 0x580 <= id_int and id_int <= 0x5FF:
        translated["Function"] = "SDO Tx"
        translated["Node ID"] = id_int - 0x580
        translated["Node"] = node_name[translated["Node ID"]]
        try:
            translated["Data"] = f"{object_dictionary[concatify([data_int[2], data_int[1]])][data_int[3]]}: "
        except KeyError:
            translated["Data"] = f"Unknown object index {data[1:3]} subindex {data[3]}: "
        
        if data_int[0] == 0x60:
            translated["Data"] += "Write confirmation"
        elif data_int[0] in [0x4F, 0x4B, 0x43]:
            translated["Data"] += hexify(concatify(data_int[7:3:-1])) ## check little-endianness
        else:
            translated["Data"] += f"Unknown command {data[0]} data {data[4:]}"

    elif 0x600 <= id_int and id_int <= 0x67F:
        translated["Function"] = "SDO Rx"
        translated["Node ID"] = id_int - 0x600
        translated["Node"] = node_name[translated["Node ID"]]
        try:
            translated["Data"] = f"{object_dictionary[concatify([data_int[2], data_int[1]])][data_int[3]]}: "
        except KeyError:
            translated["Data"] = f"Unknown object index {data[1:3]} subindex {data[3]}: "
        
        if data_int[0] in [0x2F, 0x2B, 0x23]:
            translated["Data"] += hexify(concatify(data_int[7:3:-1])) ## check little-endianness
        elif data_int[0] == 0x40:
            translated["Data"] += "Read request"
        else:
            translated["Data"] += f"Unknown command {data[0]} data {data[4:]}"

    elif 0x700 <= id_int and id_int <= 0x77F:
        translated["Function"] = "Hearbeat"
        translated["Node ID"] = id_int - 0x700
        translated["Node"] = node_name[translated["Node ID"]]
        try:
            translated["Data"] = nmt_state[data_int[0]]
        except KeyError:
            translated["Data"] = f"Unknown state {data[0]}"

    else:
        translated["Function"] = "Unknown"

    return translated

def intify(hex_string):
    if hex_string == "" or not isinstance(hex_string, str):
        return 0

    return int(hex_string, 16)

def concatify(data_int):
    result = 0
    for i, datum_int in enumerate(reversed(data_int)):
        result += datum_int * 16**(i*2)
    return result

def hexify(number):
    return f"0x{number:X}"