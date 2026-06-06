# Configuratie firmware APMF — fara secrete (merge pe GitHub)
# Secretele (WiFi, MQTT host) sunt in firmware/secrets.py (gitignored)

MQTT_CLIENT_ID = "esp32_apmf_01"
PUBLISH_INTERVAL_SEC = 10

# Pinii GPIO — senzori
PIN_DS18B20   = 14  # OneWire — temperatura apa (DS18B20 x3 pe acelasi bus)
PIN_DHT22     = 4   # temperatura + umiditate aer (DHT22)
PIN_TRIG      = 5   # HC-SR04P nivel apa — trigger
PIN_ECHO      = 18  # HC-SR04P nivel apa — echo
PIN_YF_S201   = 19  # YF-S201 debit apa — interrupt

# Atlas Scientific EZO-pH (UART) — adaugat cand soseste kitul
PIN_UART_TX   = 17
PIN_UART_RX   = 16
