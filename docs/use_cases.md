# AQM: Registrul Use Case-urilor

*"Un senzor care nu alertează la timp nu este un senzor — este un martor tăcut al unui dezastru."*

Acest document descrie scenariile principale prin care sistemul AQM aduce valoare reală.

---

## UC-01: Monitoring Normal (The Green Wall)

**Status:** Implemented

**Scop:** Vizualizarea în timp real a tuturor parametrilor sistemului acvaponic, astfel încât fermierul să confirme dintr-o privire că totul funcționează normal.

**Actor principal:** Fermierul (Sabin) — verificare pasivă, fără acțiune necesară

**Fluxul principal:**
1. **Publicare date:** Simulatorul (sau ESP32 în Faza 3) publică readings pe topicurile MQTT la fiecare 10-30 secunde.
2. **Procesare:** Backend-ul primește mesajele, le stochează în `latest_readings` și verifică pragurile — fără alertă.
3. **Vizualizare:** Dashboard-ul preia datele de la `/sensors` la fiecare 5 secunde și actualizează cardurile.
4. **Confirmare vizuală:** Toate cardurile sunt în culoarea normală (albastru). Fermierul vede: pH 7.1, O₂ 7.2 mg/L, Temp 22°C → sistemul e sănătos.

**Condiție de succes:** Toți senzorii afișează valori în fereastra optimă. Nicio alertă trimisă.

**Edge cases:**
- Un senzor nu mai publică (ESP32 offline) → cardul afișează `—` și timestamp vechi → UC-04.

---

## UC-02: Alertă la Depășire Prag (The Red Signal)

**Status:** Implemented

**Scop:** Notificarea imediată a fermierului când un parametru critic iese din fereastra acceptabilă, indiferent de oră sau locație.

**Actor principal:** Sistemul (automat) → Fermierul (reacționează)

**Fluxul WARNING:**
1. Backend primește o citire: `dissolved_oxygen = 4.8 mg/L` (sub pragul WARNING de 5.0).
2. `_check_thresholds()` detectează depășirea nivelului WARNING.
3. `send_alert("WARNING", "dissolved_oxygen", 4.8, "mg/L", 5.0)` este apelat.
4. Mesaj Telegram trimis: `⚠️ AQUAPONICS WARNING — dissolved_oxygen: 4.8 mg/L (prag: 5.0 mg/L)`.
5. Fermierul vede notificarea, verifică pompa de aerare.

**Fluxul CRITICAL:**
1. Backend primește: `dissolved_oxygen = 3.6 mg/L` (sub pragul CRITICAL de 4.0).
2. Mesaj Telegram: `🚨 AQUAPONICS CRITICAL — dissolved_oxygen: 3.6 mg/L (prag: 4.0 mg/L)`.
3. Fermierul intervine imediat (pornire pompă manuală, aerare suplimentară).

**Edge cases:**
- **Alert storm:** Dacă un parametru oscilează în jurul pragului, se pot trimite zeci de alerte pe minut.
  → **TODO Faza 1:** Implementare debounce/cooldown per parametru (ex: maxim 1 alertă per tip per 10 minute).
- **Telegram offline:** `send_alert()` folosește `httpx` async — dacă API-ul Telegram e indisponibil, eroarea este ignorată silențios (nu blochează procesarea).

---

## UC-03: Urmărirea Ciclării Biologice (The Nitrogen Watch)

**Status:** Ready for Dev

**Scop:** Monitorizarea progresului ciclării biologice a sistemului (procesul de stabilire a coloniilor de bacterii nitrificatoare), care durează 4-6 săptămâni de la pornire.

**Context biologic:**
Ciclul azotului în acvaponie: `NH₄ (amoniu)` → [*Nitrosomonas*] → `NO₂ (nitriți)` → [*Nitrobacter*] → `NO₃ (nitrați)`.
Ciclarea este completă când: NH₄ < 0.1 mg/L, NO₂ < 0.1 mg/L, NO₃ în creștere lentă.

**Status curent sistem (la pornire proiect, 2026-05-27):**
- NH₄: < 0.05 mg/L ✅ — Nitrosomonas active
- NO₂: 0.15 mg/L ✅ — Ciclare activă, Nitrobacter în curs
- NO₃: 0.075 mg/L ✅ — Nitrobacter produși confirmat

**Fluxul principal:**
1. Dashboard afișează cardurile NH₄, NO₂, NO₃ cu valorile curente.
2. Fermierul urmărește trendul zilnic: NO₂ ar trebui să crească, să atingă un vârf, apoi să scadă la < 0.1 mg/L.
3. Când NO₂ < 0.1 mg/L și NO₃ > 10 mg/L constant → ciclarea e completă.

**Deliverable viitor:** O vizualizare simplă de tip "grafic trend" pentru NH₄/NO₂/NO₃ în timp.
→ **Necesită:** persistență date (Faza 2) + chart library în dashboard.

---

## UC-04: Tranziția Simulator → Hardware Real (The Swap)

**Status:** Ready for Dev (execuție în Faza 3)

**Scop:** Înlocuirea simulatorului Python cu ESP32-ul fizic fără nicio modificare în backend sau dashboard. Acesta este testul de succes al arhitecturii din Faza 1.

**Actor principal:** Sabin (conectează hardware-ul)

**Condiții de succes (definite în Faza 1):**
- ESP32 publică pe aceleași topicuri MQTT cu același format payload
- Backend procesează datele ESP32 identic cu datele simulatorului
- Dashboard afișează datele reale fără nicio modificare de cod

**Fluxul de tranziție:**
1. Oprire simulator (`simulator/sensors.py`).
2. Flash firmware pe ESP32 (`firmware/main.py` + `firmware/config.py`).
3. Conectare senzori fizici la pinii definiți în `firmware/config.py`.
4. ESP32 pornit → se conectează la WiFi → se conectează la MQTT broker.
5. Backend și dashboard continuă să funcționeze identic.

**Verificare:** Dacă un parametru din dashboard se schimbă când pui mâna în apă (temperatura crește ușor), tranziția a reușit.

**Edge cases:**
- **Senzor calibrat greșit:** Valori aberante (pH = 2.0 sau 14.0) → CRITICAL alert. Recalibrare senzor Atlas EZO-pH.
- **ESP32 offline (WiFi picat):** Dashboard afișează ultimele valori cunoscute + timestamp vechi. Nu există alertă de "senzor offline" în Faza 3 — **TODO** pentru Faza 4.

---

## UC-05: Alertă Nivel Apă Scăzut (The Dry Tank)

**Status:** Draft

**Scop:** Detectarea pierderii de apă din sistem (evaporare accelerată, scurgere, oprire alimentare de la puț).

**Context:** Volumul total al sistemului este ~14.500-15.000L. Evaporarea normală în seră poate fi de 50-100L/zi. O pierdere bruscă de > 200L indică o problemă.

**Fluxul:**
1. Senzorul HC-SR04 măsoară distanța de la senzor la suprafața apei.
2. Backend convertește distanța în nivel (cm). Bazinul are 120cm adâncime.
3. Sub 80cm (33% din volum pierdut) → WARNING.
4. Sub 60cm → CRITICAL.

**Note:** Pragurile exacte depind de poziționarea senzorului. De calibrat după montare fizică.
