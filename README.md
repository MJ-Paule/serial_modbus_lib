# serial_modbus_lib

`serial_modbus_lib` ist eine kleine Hilfsbibliothek zur Erstellung einer seriellen Verbindung mit `pyserial` auf Basis einer JSON-Konfiguration.

## Funktionen

- `load_config(path: Path) -> dict`
  - Lädt Konfigurationen aus einer JSON-Datei.
- `create_serial_con(config: dict) -> serial.Serial`
  - Erzeugt eine `serial.Serial`-Instanz aus der geladenen Konfiguration.

## Installation

1. Python 3.8+ installieren.
2. Abhängigkeiten installieren:

```bash
python -m pip install pyserial
```

> Hinweis: Im aktuellen `pyproject.toml` sind noch keine Abhängigkeiten eingetragen. Mindestens `pyserial` wird für den Betrieb benötigt.

## Projektstruktur

- `serial_modbus_lib/serial.py`
  - Enthält die Kernfunktionen für Konfigurationslade- und Verbindungsaufbau.
- `pyproject.toml`
  - Projektmetadaten.

## Nutzung

1. Erstelle eine JSON-Konfigurationsdatei, z. B. `config.json`:

```json
{
  "serial": {
    "port": "/dev/ttyUSB0",
    "baudrate": 19200,
    "bytesize": 8,
    "parity": "N",
    "stopbits": 1,
    "timeout": 1
  }
}
```

2. Verwende die Bibliothek in deinem Python-Skript:

```python
from pathlib import Path
from serial_modbus_lib.serial import load_config, create_serial_con

config_path = Path("config.json")
config = load_config(config_path)
serial_connection = create_serial_con(config)

print(serial_connection)
```

## JSON-Konfiguration

Die Konfiguration muss den Schlüssel `serial` enthalten und folgende Einträge bereitstellen:

- `port`: Serieller Port, z. B. `/dev/ttyUSB0` oder `COM3`
- `baudrate`: Baudrate als Ganzzahl
- `bytesize`: Anzahl der Datenbits (`5`, `6`, `7`, `8`)
- `parity`: Parität als String (`N`, `E`, `O`)
- `stopbits`: Anzahl der Stopbits (`1`, `2`)
- `timeout`: Timeout in Sekunden

## Fehlerbehandlung

- Es wird `ValueError` ausgelöst, wenn die `serial`-Sektion fehlt oder erforderliche Parameter nicht vorhanden sind.

## Hinweise

- Diese Bibliothek stellt derzeit nur eine Konfigurations-basierte Initialisierung bereit.
- Anpassungen für Modbus-spezifische Protokolle oder zusätzliche `pyserial`-Optionen können direkt in `serial_modbus_lib/serial.py` vorgenommen werden.
