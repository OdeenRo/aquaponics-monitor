# Configuratie firmware APMF — fara secrete (merge pe GitHub)
# Secretele (WiFi, MQTT host) sunt in firmware/secrets.py (gitignored)

MQTT_CLIENT_ID = "esp32_apmf_01"
PUBLISH_INTERVAL_SEC = 10

# Pinii GPIO — senzori
PIN_DS18B20   = 5   # OneWire — temperatura apa — confirmat D5
PIN_DHT22     = 4   # temperatura + umiditate aer — confirmat D4
PIN_TRIG      = 13  # HC-SR04P nivel apa — trigger (D13, senzor de inlocuit)
PIN_ECHO      = 19  # HC-SR04P nivel apa — echo (D19, senzor de inlocuit)
PIN_YF_S201   = 18  # YF-S201 debit apa — confirmat D18

# Atlas Scientific EZO-pH (UART) — adaugat cand soseste kitul
PIN_UART_TX   = 17
PIN_UART_RX   = 16
