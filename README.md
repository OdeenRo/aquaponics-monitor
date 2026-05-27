# Aquaponics Monitor

Real-time monitoring system for a 14,500L aquaponics setup in Bucharest.

## Stack

- **Simulator**: Python — realistic sensor data via MQTT
- **Broker**: Mosquitto (Docker)
- **Backend**: FastAPI + aiomqtt — processes data, sends Telegram alerts
- **Dashboard**: FastAPI + vanilla HTML/JS — live sensor cards
- **Firmware**: MicroPython on ESP32 (Phase 3)
- **Cloud**: Microsoft Azure

## Quick Start

```bash
# 1. Copy env file and fill in your values
cp .env.example .env

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start MQTT broker (Docker)
docker run -d --name mosquitto -p 1883:1883 -p 9001:9001 \
  -v $(pwd)/broker/mosquitto.conf:/mosquitto/config/mosquitto.conf \
  eclipse-mosquitto

# 4. Start backend
uvicorn backend.main:app --port 8000 --reload

# 5. Start dashboard
uvicorn dashboard.app:app --port 8001 --reload

# 6. Start simulator
python -m simulator.sensors
```

## Sensor Topics (MQTT)

| Topic | Unit |
|---|---|
| `aquaponics/sensors/ph` | pH |
| `aquaponics/sensors/temperature/water` | °C |
| `aquaponics/sensors/temperature/air` | °C |
| `aquaponics/sensors/humidity` | % |
| `aquaponics/sensors/dissolved_oxygen` | mg/L |
| `aquaponics/sensors/ammonia` | mg/L |
| `aquaponics/sensors/nitrite` | mg/L |
| `aquaponics/sensors/nitrate` | mg/L |
| `aquaponics/sensors/water_level` | cm |

## Alert Thresholds

See `docs/PROJECT_CONTEXT.md` section 7.
