import asyncio
import json
import os
import sys
from datetime import datetime
from typing import Any

import aiomqtt
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

# aiomqtt uses add_reader/add_writer which require SelectorEventLoop on Windows
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from backend.alerts import send_alert

app = FastAPI(title="APMF API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))

# Latest sensor readings (in-memory store for now)
latest_readings: dict[str, Any] = {}

ALERT_THRESHOLDS = {
    "ph": {"warning_low": 6.5, "warning_high": 7.8, "critical_low": 6.0, "critical_high": 8.5, "unit": "pH"},
    "temperature_water": {"warning_low": 15.0, "warning_high": 28.0, "critical_low": 10.0, "critical_high": 32.0, "unit": "°C"},
    "temperature_air": {"warning_low": None, "warning_high": 35.0, "critical_low": None, "critical_high": 40.0, "unit": "°C"},
    "dissolved_oxygen": {"warning_low": 5.0, "warning_high": None, "critical_low": 4.0, "critical_high": None, "unit": "mg/L"},
    "ammonia": {"warning_low": None, "warning_high": 1.0, "critical_low": None, "critical_high": 2.0, "unit": "mg/L"},
    "nitrite": {"warning_low": None, "warning_high": 1.0, "critical_low": None, "critical_high": 2.0, "unit": "mg/L"},
    "nitrate": {"warning_low": None, "warning_high": 200.0, "critical_low": None, "critical_high": 300.0, "unit": "mg/L"},
    "humidity": {"warning_low": None, "warning_high": 90.0, "critical_low": None, "critical_high": 95.0, "unit": "%"},
}


def _extract_sensor_key(topic: str) -> str:
    # aquaponics/sensors/ph -> ph
    # aquaponics/sensors/temperature/water -> temperature_water
    parts = topic.split("/")[2:]
    return "_".join(parts)


async def _check_thresholds(sensor_key: str, value: float) -> None:
    thresholds = ALERT_THRESHOLDS.get(sensor_key)
    if not thresholds:
        return

    unit = thresholds["unit"]

    if thresholds["critical_high"] and value >= thresholds["critical_high"]:
        await send_alert("CRITICAL", sensor_key, value, unit, thresholds["critical_high"])
    elif thresholds["critical_low"] and value <= thresholds["critical_low"]:
        await send_alert("CRITICAL", sensor_key, value, unit, thresholds["critical_low"])
    elif thresholds["warning_high"] and value >= thresholds["warning_high"]:
        await send_alert("WARNING", sensor_key, value, unit, thresholds["warning_high"])
    elif thresholds["warning_low"] and value <= thresholds["warning_low"]:
        await send_alert("WARNING", sensor_key, value, unit, thresholds["warning_low"])


async def mqtt_listener() -> None:
    async with aiomqtt.Client(hostname=MQTT_HOST, port=MQTT_PORT) as client:
        await client.subscribe("aquaponics/sensors/#")
        async for message in client.messages:
            try:
                payload = json.loads(message.payload.decode())
                topic = str(message.topic)
                sensor_key = _extract_sensor_key(topic)
                latest_readings[sensor_key] = payload
                await _check_thresholds(sensor_key, payload["value"])
            except (json.JSONDecodeError, KeyError):
                pass


@app.on_event("startup")
async def startup() -> None:
    asyncio.create_task(mqtt_listener())


@app.get("/sensors")
async def get_sensors() -> dict[str, Any]:
    return latest_readings


@app.get("/sensors/{sensor_key}")
async def get_sensor(sensor_key: str) -> Any:
    return latest_readings.get(sensor_key, {})


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}
