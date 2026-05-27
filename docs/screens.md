# AQM: Interfețele Grafice (Screens)

*"Un dashboard bun se citește în 3 secunde. Dacă ai nevoie de mai mult, e prea complicat." — Arya*

AQM are o singură interfață web: **Dashboard-ul de monitoring în timp real**.
Nu există login, nu există pagini multiple, nu există meniuri. Datele critice sunt imediat vizibile.

---

## 1. Dashboard Principal (Live Sensor Monitor)

**Fișier:** `dashboard/app.py`
**URL:** `http://localhost:8001/` (local) / `https://aqm.odeen.ro/` (Faza 2, Azure)

### 1.1. Header

```
┌─────────────────────────────────────────────────────────┐
│  Aquaponics Monitor                    Live sensor data  │
│  Last update: 10:45:32                                   │
└─────────────────────────────────────────────────────────┘
```

- Titlu fix, fără navigare
- Timestamp ultimului refresh (actualizat la fiecare 5 secunde)
- Dacă backend-ul e indisponibil: `"Backend unreachable"` în locul timestamp-ului

### 1.2. Grila de Carduri (Sensor Cards)

Layout: grid responsiv, `minmax(200px, 1fr)`, reflow automat pe mobile.

Fiecare card afișează un singur senzor:

```
┌──────────────────────┐
│  pH                  │  ← label (uppercase, gri)
│                      │
│  7.10                │  ← valoare (mare, colorată)
│  pH                  │  ← unitate (mic, gri)
│                      │
│  2026-05-27T10:45Z   │  ← timestamp (foarte mic, gri închis)
└──────────────────────┘
```

**Color coding al valorii (conform pragurilor din `docs/data_flow.md`):**

| Stare | Culoare valoare | Border card | Condiție |
|---|---|---|---|
| Normal | `#4fc3f7` (albastru) | `#1e3a4a` (subtil) | În fereastra optimă |
| Warning | `#f59e0b` (portocaliu) | `#f59e0b` | Prag WARNING depășit |
| Critical | `#ef4444` (roșu) | `#ef4444` | Prag CRITICAL depășit |
| No data | `#546e7a` (gri) | normal | Senzor offline / fără date |

**Ordinea cardurilor (de la critic la mai puțin critic):**

1. **pH** — parametrul cel mai sensibil biologic
2. **Dissolved O₂** — urgență maximă dacă scade
3. **Water Temp** — afectează metabolismul și oxigenul
4. **Ammonia NH₄** — toxic direct
5. **Nitrite NO₂** — toxic, semnal de ciclare
6. **Nitrate NO₃** — mai puțin urgent, nutrient plante
7. **Water Level** — pierdere de apă
8. **Air Temp** — condiții seră
9. **Humidity** — risc boli plante

### 1.3. Status Bar

O linie simplă sub header:
- Normal: `"Last update: HH:MM:SS"`
- Backend offline: `"Backend unreachable"` (roșu)

---

## 2. Comportament Refresh

- **Interval:** 5 secunde (fetch la `/api/sensors`)
- **Fără WebSocket în Faza 1** — polling simplu, suficient pentru datele biologice (schimbări lente)
- **Faza 2 / upgrade opțional:** WebSocket sau Server-Sent Events pentru actualizare instantanee

> **ADR:** Am ales polling 5s în loc de WebSocket pentru simplitate în Faza 1. Datele biologice nu se schimbă în sub 30 secunde în condiții normale. Revizuim în Faza 2 dacă latența devine problemă.

---

## 3. Experiența pe Mobile (Responsive)

Cardurile se reflow automat pe coloane mai puține pe ecrane mici.
Pe telefon (portrait): 2 coloane de carduri.
Fonturile sunt suficient de mari pentru a fi lizibile fără zoom.

**Principiu Arya:** Nu există funcționalitate "desktop only". Dashboard-ul trebuie să funcționeze pe telefonul fermierului în timp ce e în seră.

---

## 4. Ecrane Viitoare (Roadmap)

### 4.1. Alert History (Faza 2)
O secțiune colapsabilă sub grila de carduri, listând ultimele N alerte trimise:

```
┌─────────────────────────────────────────────────────────┐
│  🚨 CRITICAL  dissolved_oxygen  3.6 mg/L   10:32:01     │
│  ⚠️  WARNING   dissolved_oxygen  4.8 mg/L   10:28:45     │
│  ⚠️  WARNING   ph               7.9 pH      09:15:12     │
└─────────────────────────────────────────────────────────┘
```

Necesită: persistență date în backend (Faza 2).

### 4.2. Cycling Progress View (Faza 2)
Un grafic de tip line chart pentru NH₄, NO₂, NO₃ pe ultimele 7-30 zile.
Arată vizual progresia ciclării biologice.

Necesită: stocarea datelor istorice (TimescaleDB sau InfluxDB).

### 4.3. System Health Badge (Faza 2)
Un indicator global în header: `🟢 ALL SYSTEMS NORMAL` / `⚠️ 1 WARNING` / `🚨 CRITICAL`.
Calculat ca worst-case al tuturor parametrilor curenți.
