import dht, machine, network, time, json
from umqtt.simple import MQTTClient
from secrets import WIFI_NETWORKS, MQTT_HOST, MQTT_PORT
from config import MQTT_CLIENT_ID, PUBLISH_INTERVAL_SEC, PIN_DHT22


def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    for ssid, password in WIFI_NETWORKS:
        print("WiFi: conectare la", ssid)
        wlan.connect(ssid, password)
        for _ in range(20):
            if wlan.isconnected():
                print("WiFi OK:", wlan.ifconfig()[0])
                return wlan
            time.sleep(0.5)
        wlan.disconnect()
    print("WiFi FAIL - nicio retea disponibila")
    return None


def publish_reading(client, topic, sensor_id, value, unit, location):
    payload = json.dumps({
        "sensor_id": sensor_id,
        "value": round(value, 2),
        "unit": unit,
        "location": location,
        "timestamp": "2026-01-01T00:00:00Z",
    }).encode()
    client.publish("aquaponics/sensors/" + topic, payload)


wlan = connect_wifi()
if not wlan:
    raise RuntimeError("WiFi indisponibil")

client = MQTTClient(MQTT_CLIENT_ID, MQTT_HOST, MQTT_PORT, keepalive=60)
client.connect()
print("MQTT OK ->", MQTT_HOST)

sensor = dht.DHT22(machine.Pin(PIN_DHT22))
print("Start — publish la fiecare", PUBLISH_INTERVAL_SEC, "secunde")

while True:
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        publish_reading(client, "temperature/air", "temp_air_1", temp, "C", "greenhouse")
        publish_reading(client, "humidity", "dht22_1", hum, "%", "greenhouse")
        print("Publicat:", temp, "C |", hum, "%")
    except Exception as e:
        print("Eroare senzor:", e)
    time.sleep(PUBLISH_INTERVAL_SEC)
