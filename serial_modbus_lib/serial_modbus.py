import serial
import json
import logging

_LOG = logging.getLogger(__name__)

from pathlib import Path


#Load configuration from JSON file
def load_config(path: Path) -> dict:
    with open(path, "r") as f:
        return json.load(f)


#Mapp serial config from JSON to pyserial constants
def create_serial_con(config: dict) -> serial.Serial:
    if "serial" not in config:
        raise ValueError("Config Fehler: 'serial' fehlt")
    
    serial_cfg = config["serial"]
    
    required_keys = ["port", "baudrate", "bytesize", "parity", "stopbits", "timeout"]
    
    for key in required_keys:
        if key not in serial_cfg:
            raise ValueError(f"Config Fehler: '{key}' fehlt")

    #Mapping
    bytesize_map = {
        5: serial.FIVEBITS,
        6: serial.SIXBITS,
        7: serial.SEVENBITS,
        8: serial.EIGHTBITS
    }

    parity_map = {
        "N": serial.PARITY_NONE,
        "E": serial.PARITY_EVEN,
        "O": serial.PARITY_ODD,
    }
    
    stopbits_map = {
        1: serial.STOPBITS_ONE,
        2: serial.STOPBITS_TWO
    }

    ser = serial.Serial(
        port = serial_cfg["port"],
        baudrate = serial_cfg["baudrate"],
        bytesize = bytesize_map[serial_cfg["bytesize"]],
        parity = parity_map[serial_cfg["parity"]],
        stopbits = stopbits_map[serial_cfg["stopbits"]],
        timeout = serial_cfg["timeout"]
    )

    return ser
    
