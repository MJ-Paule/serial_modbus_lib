# serial_modbus_lib

`serial_modbus_lib` ist eine kleine Hilfsbibliothek zur Initialisierung serieller Verbindungen mittels `pyserial` auf Basis einer JSON-Konfiguration. Sie ist als leichtgewichtiger Baustein für Modbus-over-Serial Setups in Tests und Beispielprojekten gedacht.

Kurz: Features
- Lädt serielle Konfigurationen aus JSON-Dateien
- Erzeugt fertig konfigurierte `serial.Serial`-Instanzen
- Sucht serielle Schnittstellen anhand von Geräte-Serialnummern
- Kleine, erweiterbare API für Entwicklungs- und Testzwecke

Voraussetzungen
- Python 3.10 oder neuer empfohlen
- `pyserial` (in `pyproject.toml` als Abhängigkeit angegeben)

Installation (Entwicklung)
1. Virtuelle Umgebung anlegen und aktivieren (empfohlen):

   python -m venv .venv
   source .venv/bin/activate

2. Abhängigkeiten installieren:

   pip install -e .

   Alternativ nur `pyserial` direkt installieren:

   pip install pyserial

Schnellstart / Nutzung

1. Beispiel `config.json` (wichtig: `relay_board.allowed_serials` wird zur Port-Erkennung genutzt):

```json
{
  "serial": {
    "baudrate": 19200,
    "bytesize": 8,
    "parity": "N",
    "stopbits": 1,
    "timeout": 1
  },
  "relay_board": {
    "allowed_serials": ["ABCD1234", "EFGH5678"]
  }
}
```

2. Beispielcode (korrekter Import via Paketoberfläche):

```python
from pathlib import Path
from serial_modbus_lib import load_config, create_serial_con

config = load_config(Path('config.json'))
ser = create_serial_con(config)

# Beispiel: einfache Schreib-/Lese-Operation (je nach Protokoll)
ser.write(b'\x01\x03\x00\x00\x00\x01')
data = ser.read(128)
print(data)

# Verbindung schließen
ser.close()
```

Wichtige Hinweise zur Konfiguration
- Die Config muss die Sektionen `serial` und `relay_board` enthalten.
- `serial` benötigt die Keys: `baudrate`, `bytesize`, `parity`, `stopbits`, `timeout`.
- `relay_board.allowed_serials` ist eine Liste von Seriennummern (Strings), die zur Auswahl des Geräts verwendet wird.

Tests
- Tests im Gesamtprojekt mit `pytest` ausführen (z. B. aus Projekt-Root):

  pytest -q

Fehlerbehandlung & Troubleshooting
- Fehlende Sektionen oder Parameter: Es wird ein `ValueError` geworfen.
- Kein passendes Gerät gefunden: `RuntimeError` mit Liste der gesuchten Seriennummern.
- Gerät nicht sichtbar: Prüfe Systemlogs (`dmesg`), verfügbare Ports (`ls /dev/tty*`) und Benutzerberechtigungen.

Weiterentwicklung
- Ideen: Modbus-spezifische Wrapper, Retry-Logik, erweitertes Logging und Timeouts.

Contributing
- Fork → Feature-Branch → Commit → Pull Request. Änderungen mit Tests beschreiben.

Lizenz
- Im Repo ist keine Lizenzdatei enthalten; bitte bei Bedarf eine passende Lizenz ergänzen.

