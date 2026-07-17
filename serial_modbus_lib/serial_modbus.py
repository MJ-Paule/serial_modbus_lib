import serial
import yaml
import logging

_LOG = logging.getLogger(__name__)

from pathlib import Path
from serial.tools import list_ports


#Load configuration from YAML file
def load_config(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:

        _LOG.debug(f"Config loaded from {path}")
        
        return yaml.safe_load(f)


#Find right Port for serial connection based on allowed serial numbers
def find_port_by_serials(allowed_serials: list[str]) -> str:
    
    devices = [
        p for p in list_ports.comports()
        if p.serial_number in allowed_serials
    ]
    
    if not devices:
        raise RuntimeError(f"No serial COM device found: {allowed_serials}")
    
    devices.sort(key=lambda p: p.device)  # Sort by device name for consistency
   
    _LOG.info("Found %d machting ports: %s", len(devices), [d.device for d in devices])
     
    _LOG.info(
        "Used Serial Port: %s",
        devices[0].device
    )

    return devices[0].device



#Mapp serial config from YAML to pyserial constants
def create_serial_con(config: dict) -> serial.Serial:
    if "serial" not in config or "relay_board" not in config:
        raise ValueError("Config Failure: 'serial' or 'relay_board' not in config")
    
    serial_cfg = config["serial"]
    allowed_serials = set(config["relay_board"]["allowed_serials"])
    
    port = find_port_by_serials(allowed_serials)

    required_keys = ["baudrate", "bytesize", "parity", "stopbits", "timeout"]
    
    for key in required_keys:
        if key not in serial_cfg:
            raise ValueError(f"Config Failure: '{key}' missing")

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

    # Create serial connection
    try:
        ser = serial.Serial(
            port = port,
            baudrate = serial_cfg["baudrate"],
            bytesize = bytesize_map[serial_cfg["bytesize"]],
            parity = parity_map[serial_cfg["parity"]],
            stopbits = stopbits_map[serial_cfg["stopbits"]],
            timeout = serial_cfg["timeout"]
        )
        _LOG.debug("Serial connection initialized on port %s", port)
        return ser
    
    except serial.SerialException:
        _LOG.exception("Failed to open serial connection: %s", port)
        raise

