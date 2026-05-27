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

### Greenhouse
- Metal tunnel with transparent film, ~18m × 6m
- Location: outdoor Bucharest

### Fish Tank
- Dimensions: 4m × 2m × 1.2m
- Volume: **9,600 L**
- Current population: **117 fish** (100 crucian carp 10-15cm + 15 common carp fry 10-15cm + 1 carp ~350g + 1 carp ~1kg)
- Cycling species: Carassius carassius

### Filtration System (outside greenhouse)
| Component | Volume | Role |
|---|---|---|
| Settling tank | ~1,000 L | First stage — sediment |
| Biofilter tank | ~500-700 L | Nitrifying bacteria |
| Aeration/pump tank | ~500 L | Oxygenation + water return |

### Grow Beds (inside greenhouse)
| Bed | Dimensions | Medium | Crops |
|---|---|---|---|
| Central | 1.875m × 12m × 0.3m | Hydroton | Tomatoes + cucumbers |
| Left lateral | 1.25m × 12m × 0.3m | Water (NFT) | TBD |
| Right lateral | 1.25m × 12m × 0.3m | Water (NFT) | TBD |

### Hydraulic System
- 3 pumps, total flow ~10,000 L/h
- Flow: Tank → Settling → Biofilter → Aeration → Beds → lateral return → Tank
- Well water (no chlorine)
- **Total system volume: ~14,500-15,000 L**

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

## 8. Implementation Plan

### Phase 1 – Simulator + Basic Architecture (CURRENT)
- [x] GitHub repository structure
- [x] Python simulator — generates realistic data for all sensors
- [x] Local MQTT Broker (Docker) for development
- [x] Python backend — MQTT subscribe, data processing
- [x] Telegram alerts — notifications on threshold breach
- [x] Simple web dashboard — real-time charts
- [ ] First commit + push to GitHub
- [ ] Docker Compose for local dev environment
- [ ] Test full stack end-to-end

### Phase 2 – Cloud Deployment
- [ ] MQTT Broker on Azure (Container Instance)
- [ ] Backend deployed on Azure
- [ ] Publicly accessible dashboard (fixed URL)
- [ ] CI/CD from GitHub Actions

### Phase 3 – Real Hardware
- [ ] MicroPython firmware on ESP32
- [ ] Physical sensor integration (DS18B20, DHT22, Atlas EZO-pH, EZO-DO)
- [ ] Replace simulator with real ESP32 — zero backend changes

### Phase 4 – Full Automation
- [ ] Pump control via relay (ESP32)
- [ ] Automatic pH dosing
- [ ] Automatic NH₄/NO₂ sensors

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
