import asyncio
import json
import os
import random
import math
import sys
from datetime import datetime, timezone

import aiomqtt
from dotenv import load_dotenv

# aiomqtt uses add_reader/add_writer which require SelectorEventLoop on Windows
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

load_dotenv()

MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))

# Publish interval in seconds
PUBLISH_INTERVAL = 10


class SensorState:
    """
    Tracks slow-drifting biological state so readings feel continuous,
    not random. Each sensor has a 'current' value that walks within
    its realistic range using bounded random walk.
    """

    def __init__(self) -> None:
        # Current system state — mid-cycle aquaponics (cycling active)
        self.ph = 7.1
        self.temp_water = 22.0
        self.temp_air = 24.0
        self.humidity = 72.0
        self.do = 7.2           # dissolved oxygen mg/L
        self.ammonia = 0.05     # low — nitrification active
        self.nitrite = 0.15     # elevated — active cycling
        self.nitrate = 0.075    # rising slowly
        self.water_level = 115.0  # cm, out of 120cm max

        # Slow drift counters (simulates day/night cycles)
        self._tick = 0

    def _walk(self, value: float, step: float, low: float, high: float) -> float:
        """Bounded random walk: nudge value by up to ±step, clamp to [low, high]."""
        delta = random.uniform(-step, step)
        return max(low, min(high, value + delta))

    def _day_temp_offset(self) -> float:
        """Sinusoidal day/night temperature swing ±3°C over 24h cycle."""
        hour_fraction = (self._tick * PUBLISH_INTERVAL) % 86400 / 86400
        return 3.0 * math.sin(2 * math.pi * hour_fraction - math.pi / 2)

    def tick(self) -> dict:
        self._tick += 1
        day_offset = self._day_temp_offset()

        self.ph = self._walk(self.ph, 0.02, 6.4, 8.0)
        self.temp_water = self._walk(self.temp_water + day_offset * 0.1, 0.1, 14.0, 30.0)
        self.temp_air = self._walk(self.temp_air + day_offset * 0.3, 0.2, 10.0, 38.0)
        self.humidity = self._walk(self.humidity, 0.5, 50.0, 98.0)
        self.do = self._walk(self.do, 0.05, 3.5, 12.0)

        # Cycling dynamics: ammonia gradually drops, nitrite peaks then drops,
        # nitrate accumulates slowly
        self.ammonia = self._walk(self.ammonia, 0.005, 0.0, 3.0)
        self.nitrite = self._walk(self.nitrite, 0.01, 0.0, 3.0)
        self.nitrate = max(0.0, self.nitrate + random.uniform(0.0, 0.002))  # slow accumulation
        self.water_level = self._walk(self.water_level, 0.2, 80.0, 120.0)

        return self._snapshot()

    def _snapshot(self) -> dict:
        return {
            "ph": round(self.ph, 3),
            "temperature_water": round(self.temp_water, 2),
            "temperature_air": round(self.temp_air, 2),
            "humidity": round(self.humidity, 1),
            "dissolved_oxygen": round(self.do, 2),
            "ammonia": round(self.ammonia, 4),
            "nitrite": round(self.nitrite, 4),
            "nitrate": round(self.nitrate, 4),
            "water_level": round(self.water_level, 1),
        }


SENSOR_METADATA: dict[str, dict] = {
    "ph":                {"topic": "ph",                  "sensor_id": "ph_main",      "unit": "pH",   "location": "fish_tank"},
    "temperature_water": {"topic": "temperature/water",   "sensor_id": "temp_water_1", "unit": "°C",   "location": "fish_tank"},
    "temperature_air":   {"topic": "temperature/air",     "sensor_id": "temp_air_1",   "unit": "°C",   "location": "greenhouse"},
    "humidity":          {"topic": "humidity",             "sensor_id": "dht22_1",      "unit": "%",    "location": "greenhouse"},
    "dissolved_oxygen":  {"topic": "dissolved_oxygen",    "sensor_id": "do_main",      "unit": "mg/L", "location": "fish_tank"},
    "ammonia":           {"topic": "ammonia",              "sensor_id": "nh4_main",     "unit": "mg/L", "location": "fish_tank"},
    "nitrite":           {"topic": "nitrite",              "sensor_id": "no2_main",     "unit": "mg/L", "location": "fish_tank"},
    "nitrate":           {"topic": "nitrate",              "sensor_id": "no3_main",     "unit": "mg/L", "location": "fish_tank"},
    "water_level":       {"topic": "water_level",         "sensor_id": "hcsr04_main",  "unit": "cm",   "location": "fish_tank"},
}


def _build_payload(sensor_key: str, value: float) -> bytes:
    meta = SENSOR_METADATA[sensor_key]
    payload = {
        "sensor_id": meta["sensor_id"],
        "value": value,
        "unit": meta["unit"],
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "location": meta["location"],
    }
    return json.dumps(payload).encode()


async def run_simulator() -> None:
    state = SensorState()
    print(f"[Simulator] Starting — publishing to {MQTT_HOST}:{MQTT_PORT} every {PUBLISH_INTERVAL}s")

    async with aiomqtt.Client(hostname=MQTT_HOST, port=MQTT_PORT) as client:
        while True:
            readings = state.tick()
            for sensor_key, value in readings.items():
                topic = f"aquaponics/sensors/{SENSOR_METADATA[sensor_key]['topic']}"
                payload = _build_payload(sensor_key, value)
                await client.publish(topic, payload)

            ts = datetime.now().strftime("%H:%M:%S")
            print(
                f"[{ts}] pH={readings['ph']} | "
                f"T_water={readings['temperature_water']}°C | "
                f"DO={readings['dissolved_oxygen']}mg/L | "
                f"NH4={readings['ammonia']} | "
                f"NO2={readings['nitrite']} | "
                f"NO3={readings['nitrate']}"
            )

            await asyncio.sleep(PUBLISH_INTERVAL)


if __name__ == "__main__":
    asyncio.run(run_simulator())
