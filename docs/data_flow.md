# APMF: Fluxul de Date (Data Flow)

Acest document este sursa de adevăr pentru **toate datele care circulă prin sistem**: topicuri MQTT, format payload, model de date al senzorilor și pragurile de alertă.

> **Regula R-01 din Manifest:** Orice modificare în cod care afectează topicuri, payload sau praguri **trebuie** reflectată simultan în acest fișier.

---

## 1. Diagrama Fluxului de Date

```
[Senzor fizic / Simulator]
        │
        │  MQTT publish
        │  topic: aquaponics/sensors/<sensor>
        │  payload: JSON (vezi secțiunea 3)
        ↓
[Mosquitto MQTT Broker]
        │
        │  subscribe: aquaponics/sensors/#
        ↓
[Backend: mqtt_listener()]
        │
        ├──→ [latest_readings dict]  ──→ GET /sensors  ──→ [Dashboard]
        │
        └──→ [_check_thresholds()]
                    │
                    ├── OK → nimic
                    ├── WARNING → send_alert("WARNING") → [Telegram]
                    └── CRITICAL → send_alert("CRITICAL") → [Telegram]
```

---

## 2. Harta Topicurilor MQTT

| Topic MQTT | Cheie internă backend | Senzor fizic | Unitate | Locație |
|---|---|---|---|---|
| `aquaponics/sensors/ph` | `ph` | Atlas Scientific EZO-pH | pH | Bazin pești |
| `aquaponics/sensors/temperature/water` | `temperature_water` | DS18B20 | °C | Bazin pești |
| `aquaponics/sensors/temperature/air` | `temperature_air` | DHT22 | °C | Seră interior |
| `aquaponics/sensors/humidity` | `humidity` | DHT22 | % | Seră interior |
| `aquaponics/sensors/dissolved_oxygen` | `dissolved_oxygen` | Atlas Scientific EZO-DO | mg/L | Bazin pești |
| `aquaponics/sensors/ammonia` | `ammonia` | Atlas Scientific EZO-NH4 | mg/L | Bazin pești |
| `aquaponics/sensors/nitrite` | `nitrite` | *(calculat / viitor senzor)* | mg/L | Bazin pești |
| `aquaponics/sensors/nitrate` | `nitrate` | *(calculat / viitor senzor)* | mg/L | Bazin pești |
| `aquaponics/sensors/water_level` | `water_level` | HC-SR04 ultrasonic | cm | Bazin pești |
| `aquaponics/alerts` | *(publish de backend)* | N/A — generat de sistem | JSON | N/A |

---

## 3. Formatul Payload MQTT (Standard)

Toate mesajele publicate pe `aquaponics/sensors/#` respectă acest format JSON:

```json
{
  "sensor_id": "ph_main",
  "value": 7.10,
  "unit": "pH",
  "timestamp": "2026-05-27T10:30:00Z",
  "location": "fish_tank"
}
```

| Câmp | Tip | Descriere |
|---|---|---|
| `sensor_id` | string | Identificator unic al senzorului fizic (ex: `ph_main`, `temp_water_1`) |
| `value` | float | Valoarea măsurată |
| `unit` | string | Unitatea de măsură (`pH`, `°C`, `mg/L`, `%`, `cm`) |
| `timestamp` | string (ISO 8601 UTC) | Momentul măsurătorii, format `YYYY-MM-DDTHH:MM:SSZ` |
| `location` | string | Locul senzorului (`fish_tank`, `greenhouse`, `filter_tank`) |

### Sensor IDs Canonice

| Cheie topic | sensor_id | location |
|---|---|---|
| `ph` | `ph_main` | `fish_tank` |
| `temperature_water` | `temp_water_1` | `fish_tank` |
| `temperature_air` | `temp_air_1` | `greenhouse` |
| `humidity` | `dht22_1` | `greenhouse` |
| `dissolved_oxygen` | `do_main` | `fish_tank` |
| `ammonia` | `nh4_main` | `fish_tank` |
| `nitrite` | `no2_main` | `fish_tank` |
| `nitrate` | `no3_main` | `fish_tank` |
| `water_level` | `hcsr04_main` | `fish_tank` |

---

## 4. Pragurile de Alertă

Implementate în `backend/main.py` → `ALERT_THRESHOLDS`. Orice modificare acolo se reflectă în acest tabel.

| Parametru | Valoare optimă | ⚠️ WARNING | 🚨 CRITICAL |
|---|---|---|---|
| **pH** | 6.8 – 7.2 | < 6.5 sau > 7.8 | < 6.0 sau > 8.5 |
| **Temperatură apă** | 18 – 26 °C | < 15 °C sau > 28 °C | < 10 °C sau > 32 °C |
| **O₂ dizolvat** | > 6 mg/L | < 5 mg/L | < 4 mg/L |
| **Amoniu NH₄** | < 0.5 mg/L | > 1.0 mg/L | > 2.0 mg/L |
| **Nitriți NO₂** | < 0.5 mg/L | > 1.0 mg/L | > 2.0 mg/L |
| **Nitrați NO₃** | < 100 mg/L | > 200 mg/L | > 300 mg/L |
| **Temperatură aer seră** | 18 – 30 °C | > 35 °C | > 40 °C |
| **Umiditate aer seră** | 60 – 80 % | > 90 % | > 95 % |

> **Nota biologică:** În faza de ciclare (primele 4-6 săptămâni), NO₂ poate depăși temporar 1 mg/L fără pericol real. Pragurile de mai sus sunt pentru sistemul stabil post-ciclare. Considerăm dezactivarea alertelor NO₂/NH₄ pe durata ciclării — ADR-04.

---

## 5. Parametri Biologici Normali (Referință)

Valorile de mai jos reprezintă fereastra normală de operare a unui sistem acvaponic cu caraș și crap, folosite ca referință pentru calibrarea simulatorului și validarea alertelor.

| Parametru | Fereastra normală | Note |
|---|---|---|
| pH | 6.8 – 7.4 | Ușor acid favorizează plantele și bacteriile nitrificatoare |
| Temperatură apă | 18 – 24 °C | Carasul tolerează 4–30 °C, optim 18–24 |
| O₂ dizolvat | 6 – 9 mg/L | Sub 5 = stres, sub 4 = urgență |
| NH₄ (amoniu) | 0 – 0.3 mg/L | Sisteme mature mențin sub 0.1 mg/L |
| NO₂ (nitriți) | 0 – 0.3 mg/L | Toxic pentru pești, semnal de ciclare activă |
| NO₃ (nitrați) | 10 – 80 mg/L | Nutrient pentru plante; schimb parțial apă > 150 mg/L |
| Umiditate seră | 65 – 80 % | Peste 90% = risc botrytis pe roșii/castraveți |

---

## 6. Modelul de Date In-Memory (Backend)

Backend-ul menține un dicționar `latest_readings: dict[str, Any]` în memorie.

```python
latest_readings = {
    "ph": {
        "sensor_id": "ph_main",
        "value": 7.10,
        "unit": "pH",
        "timestamp": "2026-05-27T10:30:00Z",
        "location": "fish_tank"
    },
    "temperature_water": { ... },
    # ... restul senzorilor
}
```

**Limitare Faza 1:** Datele nu sunt persistate — la restart backend, istoricul se pierde.
**Faza 2:** Vom adăuga persistență (TimescaleDB sau InfluxDB pe Azure) — ADR va fi adăugat în `technical_reference.md`.
