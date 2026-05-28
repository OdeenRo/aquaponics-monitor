# AQM: Runbook Operațional

---

## 1. Cerințe Preliminare

| Cerință | Verificare |
|---|---|
| Python 3.12+ | `python --version` |
| Docker Desktop (pornit) | `docker ps` |
| Git | `git --version` |
| Node.js + npm (pentru tunel local) | `node --version` |
| Telegram bot creat via @BotFather | token + chat ID în `.env` |

---

## 2. Setup Inițial (prima dată)

```powershell
git clone https://github.com/OdeenRo/aquaponics-monitor
cd aquaponics-monitor

# Creează și activează venv
python -m venv .venv

# Instalează dependențele
.\.venv\Scripts\pip install -r requirements.txt

# Configurează .env
cp .env.example .env
# Editează .env cu valorile reale (Telegram token, chat ID)
```

---

## 3. Pornire Servicii (Development)

### Varianta rapidă — tot dintr-o comandă

```powershell
.\start.ps1
```

Deschide 4 ferestre PowerShell: broker (Docker) + backend + dashboard + simulator.

---

### Varianta manuală — serviciu cu serviciu

**1. MQTT Broker**
```powershell
docker compose up -d broker
# Verificare: docker ps → aqm-broker running
```

**2. Backend** *(important: folosește `run_backend.py`, nu `uvicorn` direct)*
```powershell
.\.venv\Scripts\python run_backend.py
# Verificare: http://localhost:8000/health → {"status": "ok"}
```

> **De ce `run_backend.py`?** Pe Windows, uvicorn setează implicit `ProactorEventLoop`
> care e incompatibil cu `aiomqtt`. `run_backend.py` setează `WindowsSelectorEventLoopPolicy`
> înainte ca uvicorn să creeze event loop-ul. Vezi ADR-03 în `architecture.md`.

**3. Dashboard**
```powershell
.\.venv\Scripts\uvicorn dashboard.app:app --port 8001
# Verificare: http://localhost:8001 → dashboard cu carduri
```

**4. Simulator**
```powershell
.\.venv\Scripts\python -m simulator.sensors
# Publică date la fiecare 10s; le vezi în terminal și în dashboard
```

---

## 4. Verificare End-to-End

```powershell
# Toți senzorii live (9 chei)
Invoke-WebRequest -Uri http://localhost:8000/sensors -UseBasicParsing | Select-Object -ExpandProperty Content

# Dashboard proxy funcțional
Invoke-WebRequest -Uri http://localhost:8001/api/sensors -UseBasicParsing | Select-Object StatusCode
```

Rezultat așteptat: JSON cu `ph`, `temperature_water`, `dissolved_oxygen`, etc.

---

## 5. Tunel Local (acces din internet)

Expune dashboardul cu un URL fix pentru colegi sau demonstrații:

```powershell
npx localtunnel --port 8001 --subdomain aqm-fuior
# URL: https://aqm-fuior.loca.lt
```

La prima accesare, utilizatorii văd o pagină de confirmare localtunnel (buton "Click to Continue") — normal, măsură anti-bot.

---

## 6. Oprire Servicii

```powershell
# Oprire broker Docker
docker compose stop broker

# Procesele Python (backend, dashboard, simulator) — închide ferestrele PowerShell
# sau:
Get-Process python | Stop-Process -Force
```

---

## 7. Portabilitate Multi-Dispozitiv

Fișierul `.env` este în `.gitignore` și **nu** ajunge pe GitHub.

Pentru sincronizare între home desktop și laptop Odeen:
- Copiază `.env` manual între mașini
- Sau folosește un secret manager (1Password, Bitwarden CLI)
- **Nu** folosi cloud sync (OneDrive, Google Drive) pentru fișiere cu tokeni

---

## 8. Troubleshooting

| Simptom | Cauză probabilă | Fix |
|---|---|---|
| `MqttError: Operation timed out` | Broker Docker nu e pornit | `docker compose up -d broker` |
| `NotImplementedError: add_reader` | Backend pornit cu `uvicorn` direct în loc de `run_backend.py` | Folosește `python run_backend.py` |
| `/sensors` returnează `{}` | Simulatorul nu e pornit sau nu s-a conectat | Pornește `python -m simulator.sensors`, așteaptă 10s |
| Dashboard arată `Backend unreachable` | Backend-ul nu e pornit sau e pe alt port | Verifică `http://localhost:8000/health` |
| `docker: command not found` | Docker Desktop nu e pornit | Pornește Docker Desktop din system tray |
