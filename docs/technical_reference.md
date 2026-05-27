# AQM: Referință Tehnică

Acest document stochează **deciziile de arhitectură (ADRs)**, stack-ul tehnic ales și ghidul de configurare a mediului de development local.

---

## 1. Decizii de Arhitectură (ADRs)

### ADR-01: MQTT ca protocol de transport (vs. HTTP polling de pe ESP32)

- **Status:** `Acceptat`
- **Context:** ESP32-ul trebuie să trimită date din seră la backend. Alternativele sunt: HTTP POST direct, MQTT, WebSocket.
- **Decizie:** MQTT via broker Mosquitto.
- **Motive:**
  1. **Decuplare completă:** ESP32 nu știe că există un backend. Publică și uită. Dacă backend-ul repornește, nu pierde date în zbor (QoS 1).
  2. **Multiple consumatori:** Un singur publish poate fi consumat simultan de backend, dashboard (WebSocket) și orice altă componentă viitoare.
  3. **Eficiență pe hardware limitat:** MQTT e proiectat pentru IoT — overhead minim față de HTTP.
  4. **Simulator ↔ ESP32 interschimbabil:** Ambele publică MQTT identic. Backend-ul nu face diferența.
- **Consecințe:** Avem nevoie de un MQTT broker (Mosquitto). Adaugă o componentă de infrastructură, dar beneficiile depășesc complexitatea.

---

### ADR-02: Simulatorul ca "contract de interfață" cu hardware-ul

- **Status:** `Acceptat`
- **Context:** Hardware-ul (ESP32 + senzori) nu este disponibil în Faza 1. Trebuie să construim și să testăm backend-ul și dashboard-ul fără hardware real.
- **Decizie:** Simulatorul Python (`simulator/sensors.py`) implementează exact același protocol MQTT (topicuri + format payload) ca firmware-ul ESP32.
- **Motive:**
  1. Stack-ul complet poate fi testat și demonstrat fără hardware.
  2. Tranziția la hardware real = oprire simulator, pornire ESP32. Zero modificări altundeva.
  3. Simulatorul cu random walk biologic realist permite calibrarea pragurilor de alertă înainte ca hardware-ul să sosească.
- **Consecințe:** **Regula R-04 din Manifest** — orice schimbare de protocol MQTT trebuie aplicată simultan în simulator, firmware și backend.

---

### ADR-03: FastAPI pentru backend (vs. Flask, Django)

- **Status:** `Acceptat`
- **Context:** Backend-ul trebuie să ruleze un MQTT listener async în paralel cu un API HTTP.
- **Decizie:** FastAPI cu `asyncio` + `aiomqtt`.
- **Motive:**
  1. **Async nativ:** `aiomqtt` și FastAPI operează pe același event loop. Nu avem nevoie de threading sau multiprocessing.
  2. **Typing și validare:** Pydantic integrat, type hints obligatorii (Constituția Odeen).
  3. **Auto-documentare:** `/docs` generat automat — util pentru debugging în faza de dev.
- **Consecințe:** Dependență de `uvicorn` ca ASGI server. Standard în ecosistemul Python modern.

---

### ADR-04: Fără persistență în Faza 1 (in-memory store)

- **Status:** `Acceptat` *(revizuit în Faza 2)*
- **Context:** Faza 1 este focusată pe arhitectura de bază și validarea fluxului end-to-end.
- **Decizie:** Backend-ul stochează doar ultima valoare per senzor în memorie (`latest_readings` dict). La restart, istoricul se pierde.
- **Motive:**
  1. Zero complexitate de infrastructure în Faza 1 (fără DB, fără migrări).
  2. Dashboard-ul în Faza 1 are nevoie doar de valorile curente, nu de istoric.
  3. Ciclul de feedback (build → test → iterate) este mai rapid fără schema management.
- **Consecințe:** Nu există grafice de trend în Faza 1. Planul pentru Faza 2: adăugare TimescaleDB sau InfluxDB pe Azure. ADR separat va fi creat atunci.

---

### ADR-05: Docker pentru MQTT broker în development (vs. instalare nativă)

- **Status:** `Acceptat`
- **Context:** Mosquitto trebuie rulat local pentru development. Alternativa este instalare nativă pe Windows/Linux.
- **Decizie:** `docker run eclipse-mosquitto` cu configurația din `broker/mosquitto.conf`.
- **Motive:**
  1. Reproducibil pe orice mașină (home desktop + laptop Odeen).
  2. Izolat — nu poluează sistemul de operare.
  3. Comandă simplă, fără installer.
- **Consecințe:** Docker Desktop trebuie instalat. Porturile 1883 (MQTT) și 9001 (WebSocket) trebuie să fie libere.

---

### ADR-06: Alertele numai prin Telegram (vs. email, SMS, push)

- **Status:** `Acceptat`
- **Context:** Sistemul trebuie să notifice fermierul în timp real la depășirea pragurilor.
- **Decizie:** Telegram Bot API ca singurul canal de alerte în Faza 1.
- **Motive:**
  1. Sabin folosește Telegram — zero friction pentru utilizator.
  2. Telegram Bot API este gratuit, stabil și simplu de integrat (un singur HTTP POST).
  3. Mesajele sunt livrate instant pe mobile, cu notificare sonoră.
  4. Nu necesită server de email sau credențiale SMTP.
- **Consecințe:** Dacă Telegram este indisponibil, alertele se pierd silențios. Acceptabil în Faza 1. Faza 2 poate adăuga redundanță (email fallback).

---

## 2. Stack Tehnic

| Componentă | Tehnologie | Versiune | Justificare |
|---|---|---|---|
| Simulator | Python + aiomqtt | 3.11+ / 2.3.0 | Async MQTT publish, random walk biologic |
| MQTT Broker | Eclipse Mosquitto (Docker) | latest | Standard IoT, ușor de configurat |
| Backend | FastAPI + aiomqtt | 0.115 / 2.3.0 | Async nativ, ADR-03 |
| HTTP Client | httpx | 0.27.2 | Async, pentru Telegram API |
| Dashboard | FastAPI + Vanilla HTML/JS | — | Zero framework JS, Arya philosophy |
| Env management | python-dotenv | 1.0.1 | Secretele în `.env`, ADR-06 |
| Cloud | Microsoft Azure | — | Odeen Software infrastructure |
| CI/CD | GitHub Actions | — | Faza 2 |
| Firmware | MicroPython | 1.23+ | Singurul Python pe ESP32 |

---

## 3. Ghid Setup Local (Development)

### Cerințe preliminare
- Python 3.11+
- Docker Desktop instalat și pornit
- Git configurat cu acces la `github.com/OdeenRo`
- Telegram bot creat (via @BotFather) și chat ID cunoscut

### Pas 1: Clonare și configurare environment
```bash
git clone https://github.com/OdeenRo/aquaponics-monitor
cd aquaponics-monitor
cp .env.example .env
# Editează .env cu valorile tale reale
pip install -r requirements.txt
```

### Pas 2: Pornire MQTT Broker (Docker)
```bash
docker run -d --name aqm-mosquitto \
  -p 1883:1883 -p 9001:9001 \
  -v ${PWD}/broker/mosquitto.conf:/mosquitto/config/mosquitto.conf \
  eclipse-mosquitto
```

### Pas 3: Pornire Backend
```bash
uvicorn backend.main:app --port 8000 --reload
```
Verificare: `http://localhost:8000/health` → `{"status": "ok"}`

### Pas 4: Pornire Dashboard
```bash
uvicorn dashboard.app:app --port 8001 --reload
```
Verificare: `http://localhost:8001/` → dashboard cu carduri goale (—)

### Pas 5: Pornire Simulator
```bash
python -m simulator.sensors
```
La fiecare 10 secunde, datele apar în dashboard și în terminal.

### Verificare end-to-end
1. Terminal simulator: afișează readings → ✅
2. `http://localhost:8000/sensors` → JSON cu toate valorile → ✅
3. `http://localhost:8001/` → carduri cu valori actualizate → ✅
4. (opțional) Setează un prag mic în `.env` și verifică că primești alertă Telegram → ✅

---

## 4. Portabilitate Multi-Dispozitiv (`.env` pe două mașini)

Fișierul `.env` este în `.gitignore` și nu ajunge pe GitHub.
Soluție manuală pentru sincronizare între home desktop și laptop Odeen:
- Copiază `.env` manual sau folosește un secret manager (1Password, Bitwarden CLI).
- **Nu** folosi cloud sync (OneDrive, Google Drive) pentru fișiere cu tokeni.

> **TODO Faza 2:** Script de backup/restore `.env` similar cu `start_tunsflow.bat` din TunsFlow, salvând în `%USERPROFILE%\.aqm\.env`.
