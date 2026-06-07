import dht, machine, network, ntptime, onewire, ds18x20, time, json
from umqtt.simple import MQTTClient
from secrets import WIFI_NETWORKS, MQTT_HOST, MQTT_PORT
from config import MQTT_CLIENT_ID, PUBLISH_INTERVAL_SEC, PIN_DHT22, PIN_DS18B20, PIN_YF_S201


def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(False)
    time.sleep(0.5)
    wlan.active(True)
    time.sleep(0.5)
    for ssid, password in WIFI_NETWORKS:
        print("WiFi: conectare la", ssid)
        wlan.connect(ssid, password)
        for _ in range(40):          # 20 secunde timeout
            if wlan.isconnected():
                print("WiFi OK:", wlan.ifconfig()[0])
                return wlan
            time.sleep(0.5)
        wlan.disconnect()
        time.sleep(1)
    print("WiFi FAIL - nicio retea disponibila")
    return None


def now_iso():
    t = time.gmtime()
    return "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5])


def publish_reading(client, topic, sensor_id, value, unit, location):
    payload = json.dumps({
        "sensor_id": sensor_id,
        "value": round(value, 2),
        "unit": unit,
        "location": location,
        "timestamp": now_iso(),
    }).encode()
    client.publish("aquaponics/sensors/" + topic, payload)


wlan = connect_wifi()
if not wlan:
    raise RuntimeError("WiFi indisponibil")

try:
    ntptime.settime()
    print("NTP sync OK")
except Exception as e:
    print("NTP FAIL (continuam cu ora incorecta):", e)

client = MQTTClient(MQTT_CLIENT_ID, MQTT_HOST, MQTT_PORT, keepalive=60)
client.connect()
print("MQTT OK ->", MQTT_HOST)

dht_sensor = dht.DHT22(machine.Pin(PIN_DHT22))
ow = onewire.OneWire(machine.Pin(PIN_DS18B20))
ds = ds18x20.DS18X20(ow)
ds_roms = ds.scan()
print("DS18B20 senzori gasiti:", len(ds_roms))

# YF-S201 — debit apa
flow_count = 0
def flow_pulse(pin):
    global flow_count
    flow_count += 1

flow_pin = machine.Pin(PIN_YF_S201, machine.Pin.IN, machine.Pin.PULL_UP)
flow_pin.irq(trigger=machine.Pin.IRQ_RISING, handler=flow_pulse)
print("YF-S201 activ pe GPIO", PIN_YF_S201)
print("Start — publish la fiecare", PUBLISH_INTERVAL_SEC, "secunde")

while True:
    try:
        dht_sensor.measure()
        publish_reading(client, "temperature/air", "temp_air_1", dht_sensor.temperature(), "C", "greenhouse")
        publish_reading(client, "humidity", "dht22_1", dht_sensor.humidity(), "%", "greenhouse")
        print("DHT22:", dht_sensor.temperature(), "C |", dht_sensor.humidity(), "%")
    except Exception as e:
        print("Eroare DHT22:", e)

    if ds_roms:
        try:
            ds.convert_temp()
            time.sleep_ms(750)
            for i, rom in enumerate(ds_roms):
                t = ds.read_temp(rom)
                sensor_id = "temp_water_" + str(i + 1)
                publish_reading(client, "temperature/water", sensor_id, t, "C", "fish_tank")
                print("DS18B20:", t, "C")
        except Exception as e:
            print("Eroare DS18B20:", e)

    # Debit apa — calcul pe intervalul de publicare
    pulses = flow_count
    flow_count = 0
    flow_lpm = round((pulses / PUBLISH_INTERVAL_SEC) / 7.5, 2)
    publish_reading(client, "water_flow", "yf_s201_main", flow_lpm, "L/min", "pump_pipe")
    print("YF-S201:", pulses, "pulsuri ->", flow_lpm, "L/min")

    time.sleep(PUBLISH_INTERVAL_SEC)
