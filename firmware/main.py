import time
import json
import network
import machine
from umqtt.simple import MQTTClient
from config import (
    WIFI_SSID, WIFI_PASSWORD,
    MQTT_HOST, MQTT_PORT, MQTT_CLIENT_ID,
    PUBLISH_INTERVAL_SEC,
)


def connect_wifi() -> None:
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    while not wlan.isconnected():
        time.sleep(0.5)


def publish(client: MQTTClient, topic: str, sensor_id: str, value: float, unit: str, location: str) -> None:
    payload = json.dumps({
        "sensor_id": sensor_id,
        "value": value,
        "unit": unit,
        "timestamp": "2000-01-01T00:00:00Z",  # replace with NTP time when available
        "location": location,
    })
    client.publish(f"aquaponics/sensors/{topic}", payload)


def main() -> None:
    connect_wifi()

    client = MQTTClient(MQTT_CLIENT_ID, MQTT_HOST, MQTT_PORT)
    client.connect()

    while True:
        # TODO: read real sensor values here
        # publish(client, "ph", "ph_main", ph_value, "pH", "fish_tank")
        # publish(client, "temperature/water", "temp_water_main", temp_value, "°C", "fish_tank")
        time.sleep(PUBLISH_INTERVAL_SEC)


main()
