# Aquaponics Monitor

Real-time monitoring system for a 9,600L aquaponics setup in Bucharest (~14,500L total system volume).

## Stack

- **Simulator**: Python — realistic sensor data via MQTT (bounded random walk + day/night cycle)
- **Broker**: Mosquitto 2.0 (Docker)
- **Backend**: FastAPI + aiomqtt — processes data, sends Telegram alerts
- **Dashboard**: FastAPI + vanilla HTML/JS — live sensor cards, 5s refresh
- **Firmware**: MicroPython on ESP32 (Phase 3)
- **Cloud**: Microsoft Azure (Phase 2)

## Quick Start

```powershell
# 1. Clone and set up environment
git clone https://github.com/OdeenRo/aquaponics-monitor
cd aquaponics-monitor
python -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt
cp .env.example .env   # fill in Telegram credentials

# 2. Start everything
.\start.ps1
```

Open `http://localhost:8001` — live sensor data appears within 10 seconds.

> **Note (Windows):** The backend must be started via `python run_backend.py`, not `uvicorn` directly.
> `start.ps1` handles this automatically. See `docs/runbook.md` for details.

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

## Documentation

| File | Contents |
|---|---|
| `docs/vision.md` | Why AQM exists, implementation phases |
| `docs/architecture.md` | ADRs, tech stack, MQTT contracts |
| `docs/runbook.md` | Setup, running services, troubleshooting |
| `docs/system_params.md` | Physical system parameters |
| `docs/data_flow.md` | MQTT payload format, alert thresholds |
