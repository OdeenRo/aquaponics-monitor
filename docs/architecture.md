# AQM: Arhitectura Tehnică

---

## 1. Diagrama Arhitecturală

```
[Senzori fizici ESP32]          [Python Simulator]
         │                              │
         └──────────────┬───────────────┘
                        ↓ MQTT publish (aquaponics/sensors/#)
              [Mosquitto MQTT Broker]
              (local Docker / Azure)
                        ↓ subscribe
              [Backend FastAPI + aiomqtt]
               ├── threshold checker → [Telegram Bot]
               ├── in-memory store (Faza 1)
               └── REST API /sensors
                        ↓ HTTP proxy
              [Dashboard FastAPI + HTML/JS]
              (carduri live, refresh 5s)
```

**Principiu de izolare:** Backend-ul nu știe dacă datele vin de la simulator sau ESP32.
Înlocuirea unuia cu celălalt necesită zero modificări în backend sau dashboard.

---

## 2. Stack Tehnic

| Componentă | Tehnologie | Versiune | Justificare |
|---|---|---|---|
| Simulator | Python + aiomqtt | 3.12 / 2.3.0 | Async MQTT publish, random walk biologic |
| MQTT Broker | Eclipse Mosquitto (Docker) | 2.0 | Standard IoT, ușor de configurat |
| Backend | FastAPI + aiomqtt | 0.115 / 2.3.0 | Async nativ — ADR-03 |
| HTTP Client | httpx | 0.27.2 | Async, pentru Telegram API și proxy dashboard |
| Dashboard | FastAPI + Vanilla HTML/JS | — | Zero framework JS — filozofia Arya |
| Env management | python-dotenv | 1.0.1 | Secretele în `.env` |
| Cloud | Microsoft Azure | — | Odeen Software infrastructure (Faza 2) |
| CI/CD | GitHub Actions | — | Faza 2 |
| Firmware | MicroPython | 1.23+ | Singurul Python pe ESP32 |

---

## 3. Decizii de Arhitectură (ADRs)

### ADR-01: MQTT ca protocol de transport

- **Status:** Acceptat
- **Context:** ESP32-ul trebuie să trimită date din seră la backend.
- **Decizie:** MQTT via broker Mosquitto, nu HTTP polling.
- **Motive:**
  1. Decuplare completă — ESP32 publică și uită; backend-ul poate reporni fără pierderi (QoS 1)
  2. Multiple consumatori simultan (backend + dashboard WebSocket + viitoare componente)
  3. Overhead minim pe hardware limitat
  4. Simulator și ESP32 identice din perspectiva backend-ului
- **Consecințe:** Nevoie de MQTT broker ca infrastructură suplimentară.

---

### ADR-02: Simulatorul ca contract de interfață cu hardware-ul

- **Status:** Acceptat
- **Context:** Hardware-ul (ESP32 + senzori) nu este disponibil în Faza 1.
- **Decizie:** `simulator/sensors.py` implementează exact același protocol MQTT ca firmware-ul ESP32 — topicuri identice, format payload identic.
- **Motive:**
  1. Stack complet testabil și demonstrabil fără hardware
  2. Tranziția la hardware = oprire simulator, pornire ESP32. Zero modificări altundeva.
  3. Random walk biologic realist → calibrare praguri de alertă înainte ca hardware-ul să sosească
- **Consecințe:** Orice schimbare de protocol MQTT se aplică simultan în simulator, firmware și backend (vezi Regula R-01 din `CLAUDE.md`).

---

### ADR-03: FastAPI + aiomqtt pentru backend

- **Status:** Acceptat
- **Context:** Backend-ul trebuie să ruleze un MQTT listener async în paralel cu un API HTTP.
- **Decizie:** FastAPI cu `asyncio` + `aiomqtt`.
- **Motive:**
  1. Async nativ — `aiomqtt` și FastAPI operează pe același event loop, fără threading
  2. Pydantic integrat, type hints obligatorii
  3. `/docs` generat automat — util pentru debugging
- **Consecințe:** Pe Windows, uvicorn folosește `ProactorEventLoop` incompatibil cu `aiomqtt`. Fix: `run_backend.py` setează `WindowsSelectorEventLoopPolicy` înainte de pornirea uvicorn (vezi `runbook.md`).

---

### ADR-04: Fără persistență în Faza 1 (in-memory store)

- **Status:** Acceptat, revizuit în Faza 2
- **Context:** Faza 1 validează arhitectura end-to-end, nu are nevoie de istoric.
- **Decizie:** `latest_readings: dict` în backend — doar ultima valoare per senzor. La restart, se pierde.
- **Motive:** Zero infrastructură de DB în Faza 1; dashboard-ul are nevoie doar de valorile curente.
- **Consecințe:** Nu există grafice de trend în Faza 1. Faza 2: TimescaleDB sau InfluxDB pe Azure.

---

### ADR-05: Docker pentru MQTT broker în development

- **Status:** Acceptat
- **Decizie:** `docker compose up -d broker` cu config din `broker/mosquitto.conf`.
- **Motive:** Reproducibil pe orice mașină, izolat, fără installer nativ.
- **Consecințe:** Docker Desktop trebuie instalat. Porturile 1883 (MQTT) și 9001 (WebSocket) libere.

---

### ADR-06: Telegram ca singurul canal de alerte în Faza 1

- **Status:** Acceptat
- **Decizie:** Telegram Bot API — un singur HTTP POST per alertă.
- **Motive:** Sabin folosește Telegram; gratuit, stabil, notificare instant pe mobile; fără SMTP.
- **Consecințe:** Dacă Telegram e indisponibil, alertele se pierd silențios. Acceptabil în Faza 1. Faza 2 poate adăuga email fallback.

---

## 4. Contracte de Interfață MQTT

### Topicuri

| Senzor | Topic | Senzor ID |
|---|---|---|
| pH | `aquaponics/sensors/ph` | `ph_main` |
| Temperatură apă | `aquaponics/sensors/temperature/water` | `temp_water_1` |
| Temperatură aer | `aquaponics/sensors/temperature/air` | `temp_air_1` |
| Umiditate | `aquaponics/sensors/humidity` | `dht22_1` |
| Oxigen dizolvat | `aquaponics/sensors/dissolved_oxygen` | `do_main` |
| Amoniu | `aquaponics/sensors/ammonia` | `nh4_main` |
| Nitriti | `aquaponics/sensors/nitrite` | `no2_main` |
| Nitrati | `aquaponics/sensors/nitrate` | `no3_main` |
| Nivel apă | `aquaponics/sensors/water_level` | `hcsr04_main` |
| Alerte | `aquaponics/alerts` | — |

### Format Payload

```json
{
  "sensor_id": "ph_main",
  "value": 7.1,
  "unit": "pH",
  "timestamp": "2026-05-28T10:30:00Z",
  "location": "fish_tank"
}
```

---

## 5. Convenții de Cod

- **Limbaj:** Python 3.12+
- **Stil:** PEP8, type hints obligatorii pe toate funcțiile publice
- **Async:** obligatoriu pentru orice I/O (MQTT, HTTP, filesystem)
- **Secretele:** exclusiv în `.env` via `python-dotenv`, niciodată hardcodate
- **Comentarii:** doar WHY, niciodată WHAT (codul vorbește singur)
