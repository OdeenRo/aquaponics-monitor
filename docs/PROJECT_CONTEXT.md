# Aquaponics Monitor – Project Context

> This file provides the complete project context for Claude Code.
> At the start of each working session: **"Read PROJECT_CONTEXT.md and continue from where we left off."**

---

## 1. About the Developer

- **Background:** Former C++ developer (20-year break), recently familiar with Python
- **Current Role:** Principal Partner / CEO at Odeen Software (~70 employees)
- **Work Style:** Agentic development — Claude proposes and executes, developer reviews and approves
- **Key Principle:** Understand everything being built — no black boxes
- **Language:** Communication in Romanian
- **Setup:** Home desktop + office laptop (Odeen Software)
- **Elders Framework:** `D:\Projects\Agentic\Odeen_Core` — Scalex, Valon, Arya, Sani

---

## 2. Physical System Description

> Dimensiuni, volume, populație pești și calcule derivate: vezi **[`docs/system_params.md`](system_params.md)**

Sumar rapid:
- Seră: **12m × 6m × ~3.5m**
- Bazin: **4m × 2m × 1.2m = 9,600 L**, 117 pești, ~5–10 kg biomasă
- Filtrare (exterior): ~2,000–2,200 L (decantare + biofiltru + aerare)
- Paturi cultură: 52.5 m² total (hydroton central + NFT lateral ×2)
- **Volum total sistem: ~14,500–15,000 L**, ciclu complet ~1.5h

---

## 3. Biological System Status

| Parameter | Measured Value | Status |
|---|---|---|
| NH₄⁺ (ammonium) | < 0.05 mg/L | ✅ Excellent |
| NO₂⁻ (nitrites) | 0.15 mg/L | ✅ Active cycling |
| NO₃⁻ (nitrates) | 0.075 mg/L | ✅ Nitrobacter active |
| pH | Not tested electronically | ⚠️ |
| O₂ dissolved | Not yet monitored | ⚠️ |

**Conclusion:** Biological cycling has started naturally, system more advanced than expected.
**Estimated cycling completion:** 2-3 weeks from project start (2026-05-27).

---

## 4. Planned Sensors

| Sensor | Model | Location | Priority | Status |
|---|---|---|---|---|
| Water pH | Atlas Scientific EZO-pH | Fish tank | Critical | To order |
| Water temperature | DS18B20 (×3) | Tank + beds | Critical | To order |
| Dissolved oxygen | Atlas Scientific EZO-DO | Fish tank | High | To order |
| Air temp/humidity | DHT22 (×2) | Greenhouse interior | High | To order |
| Water level | HC-SR04 ultrasonic | Fish tank | Medium | To order |
| NH₄/NO₂ | Atlas Scientific EZO-NH4 | Fish tank | Phase 3 | Future |
| Water flow | YF-S201 | Pump pipes | Medium | To order |

**Microcontroller:** ESP32 with MicroPython
**Protocol:** MQTT

---

## 5. Software Architecture

```
[ESP32 / Simulator]
       ↓ MQTT publish (topic: aquaponics/sensors/#)
[MQTT Broker - Mosquitto on Azure]
       ↓
[Python Backend - processing + alerts]
       ↓                    ↓
[Web Dashboard]      [Telegram Bot - alerts]
```

### Tech Stack
| Component | Technology |
|---|---|
| ESP32 Firmware | MicroPython |
| Sensor Simulator | Python |
| MQTT Broker | Mosquitto (Docker on Azure) |
| Backend | Python + FastAPI |
| Dashboard | FastAPI + HTML/JS |
| Alerts | Telegram Bot API |
| Cloud | Microsoft Azure (Odeen Software) |
| Source Control | GitHub (Odeen Software) |
| IDE | VS Code + Claude Code |

---

## 6. Repository Structure

```
aquaponics-monitor/
├── simulator/
│   ├── __init__.py
│   └── sensors.py          # realistic simulated data generation
├── broker/
│   └── mosquitto.conf      # MQTT broker configuration
├── backend/
│   ├── __init__.py
│   ├── main.py             # FastAPI app + MQTT subscriber
│   └── alerts.py           # Telegram alert logic
├── dashboard/
│   ├── __init__.py
│   └── app.py              # real-time web interface
├── firmware/
│   ├── main.py             # MicroPython ESP32 code
│   └── config.py           # WiFi, MQTT, pin configuration
├── docs/
│   └── PROJECT_CONTEXT.md  # this file
├── .env.example            # required environment variables
├── requirements.txt        # Python dependencies
└── README.md
```

---

## 7. Alert Thresholds

| Parameter | Optimal | WARNING Alert | CRITICAL Alert |
|---|---|---|---|
| pH | 6.8 – 7.2 | < 6.5 or > 7.8 | < 6.0 or > 8.5 |
| Water temperature | 18 – 26°C | < 15°C or > 28°C | < 10°C or > 32°C |
| NH₄ (ammonia) | < 0.5 mg/L | > 1 mg/L | > 2 mg/L |
| NO₂ (nitrites) | < 0.5 mg/L | > 1 mg/L | > 2 mg/L |
| NO₃ (nitrates) | < 100 mg/L | > 200 mg/L | > 300 mg/L |
| O₂ dissolved | > 6 mg/L | < 5 mg/L | < 4 mg/L |
| Greenhouse air humidity | 60 – 80% | > 90% | > 95% |
| Greenhouse air temperature | 18 – 30°C | > 35°C | > 40°C |

---

## 8. Faze de Implementare *(sursa unică — referențiat din MANIFEST și vision.md)*

### Faza 1 — Simulator + Arhitectură de Bază ✅ Completă *(2026-05-28)*

**Valoare:** Arhitectura validată end-to-end fără hardware. Stack demonstrabil, praguri calibrate, dashboard funcțional.

- [x] Structură repository GitHub
- [x] Simulator Python — date realiste pentru toți senzorii (bounded random walk + ciclu zi/noapte)
- [x] MQTT Broker local (Docker — Mosquitto 2.0)
- [x] Backend Python — MQTT subscribe, procesare date, in-memory store
- [x] Alerte Telegram — cod complet, necesită credențiale în `.env`
- [x] Dashboard web — carduri senzori live, refresh 5s
- [x] Commit + push GitHub (`OdeenRo/aquaponics-monitor`)
- [x] Docker Compose pentru mediul local de dev
- [x] Test stack end-to-end — 9 senzori live verificați

---

### Faza 2 — Cloud Deployment Azure ⏳ Pending

**Valoare:** Sistem accesibil de oriunde, URL fix, monitorizare de la birou sau din mașină.

- [ ] MQTT Broker pe Azure (Container Instance)
- [ ] Backend deployed pe Azure
- [ ] Dashboard public cu URL fix
- [ ] CI/CD din GitHub Actions

---

### Faza 3 — Hardware Real ⏳ Pending

**Valoare:** Date reale în loc de simulate. Zero modificări în backend sau dashboard — acesta e succesul arhitectural al Fazei 1.

- [ ] Firmware MicroPython pe ESP32
- [ ] Integrare senzori fizici (DS18B20, DHT22, Atlas EZO-pH, EZO-DO)
- [ ] Înlocuire simulator cu ESP32 real

---

### Faza 4 — Automatizare Completă ⏳ Viitor

**Valoare:** Fermierul devine observator, nu operator. Intervențiile manuale dispar.

- [ ] Control pompe via releu (ESP32)
- [ ] Dozare automată pH
- [ ] Senzori automatici NH₄/NO₂

---

## 9. Code Conventions

- **Language:** Python 3.11+
- **Style:** PEP8, type hints mandatory
- **MQTT topics:**
  - `aquaponics/sensors/ph`
  - `aquaponics/sensors/temperature/water`
  - `aquaponics/sensors/temperature/air`
  - `aquaponics/sensors/humidity`
  - `aquaponics/sensors/dissolved_oxygen`
  - `aquaponics/sensors/ammonia`
  - `aquaponics/sensors/nitrite`
  - `aquaponics/sensors/nitrate`
  - `aquaponics/sensors/water_level`
  - `aquaponics/alerts`
- **MQTT message format:** JSON
  ```json
  {
    "sensor_id": "ph_main",
    "value": 7.1,
    "unit": "pH",
    "timestamp": "2026-05-27T10:30:00Z",
    "location": "fish_tank"
  }
  ```
- **Environment variables:** all secrets in `.env`, never in code

---

## 10. How to Continue the Session

At the start of each Claude Code session:
1. Open `docs/PROJECT_CONTEXT.md`
2. Say: **"Read PROJECT_CONTEXT.md and continue from where we left off"**
3. Mention what changed since the last session (e.g., "installed Docker", "sensors arrived")
