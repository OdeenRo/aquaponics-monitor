# APMF: Viziunea Sistemului

## 1. Context și Problemă

O seră de 12m × 6m în București adăpostește un ecosistem acvaponic complex: un bazin de 9.600L cu 117 pești, trei trepte de filtrare biologică și paturi de cultură cu o suprafață totală de ~40m².

Ecosistemul este **viu și fragil**. Parametrii apei se pot deteriora în ore, nu în zile:
- O pompa oprită noaptea → oxigenul dizolvat scade sub 4 mg/L → pești morți dimineața
- Ciclarea biologică nemonitorizată → vârf de amoniu nedetectat → toxicitate acută
- pH în afara ferestrei 6.5–7.8 → bacteriile nitrificatoare mor → colaps biologic în 48h

**Problema:** Fără monitorizare continuă, singurul sistem de alertă este inspecția manuală — care nu funcționează noaptea, în weekend sau când fermierul este la birou.

---

## 2. Misiunea APMF

**APMF transformă un ecosistem biologic opac într-un sistem transparent și alertat.**

Obiective concrete:
1. **Vizibilitate 24/7** — orice parametru critic este vizibil de pe orice dispozitiv, în timp real
2. **Alerte proactive** — notificare Telegram în secunde de la depășirea unui prag, nu după ce e prea târziu
3. **Istoric și tendințe** — datele stocate permit identificarea pattern-urilor (ciclare, sezonalitate, corelații)
4. **Zero-downtime la tranziția hardware** — simulatorul și ESP32-ul sunt interschimbabile; arhitectura nu se schimbă

---

## 3. Utilizatorul Principal

**Sabin** — fermier urban, CEO Odeen Software, lucrează de acasă și de la birou.

Nevoi concrete:
- Să vadă dintr-o privire dacă totul e în regulă (verde = ok, roșu = acționează)
- Să primească alertă pe Telegram dacă ceva iese din parametri, indiferent de oră
- Să nu fie nevoit să intre în seră pentru a citi parametrii

**Principiu Arya aplicat:** Dashboard-ul trebuie să fie citibil în 3 secunde. Dacă necesită scroll sau interpretare, e prea complicat.

---

## 4. Faze de Implementare

### Faza 1 — Simulator + Arhitectură de Bază ✅ Completă *(2026-05-28)*

**Valoare:** Arhitectura validată end-to-end fără hardware. Stack demonstrabil, praguri calibrate, dashboard funcțional.

- [x] Structură repository GitHub
- [x] Simulator Python — date realiste (bounded random walk + ciclu zi/noapte)
- [x] MQTT Broker local (Docker — Mosquitto 2.0)
- [x] Backend Python — MQTT subscribe, procesare, in-memory store
- [x] Alerte Telegram — cod complet, necesită credențiale în `.env`
- [x] Dashboard web — carduri senzori live, refresh 5s
- [x] Commit + push GitHub (`OdeenRo/aquaponics-monitor`)
- [x] Docker Compose pentru mediul local de dev
- [x] Test stack end-to-end — 9 senzori live verificați

---

### Faza 2 — Cloud Deployment Azure ✅ Completă *(2026-05-30)*

**Valoare:** Sistem accesibil de oriunde, URL fix, monitorizare de la birou sau din mașină.

- [x] MQTT Broker pe Azure — Docker container pe VM `apmf-vm` (germanywestcentral)
- [x] Backend deployed pe Azure — Docker container, `restart: unless-stopped`
- [x] IP static — `20.113.134.32` (nu se schimbă la repornire VM)
- [x] Dashboard public — `http://20.113.134.32`
- [x] CI/CD GitHub Actions — orice push pe `main` deployează automat via Azure CLI + Service Principal

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

## 5. Ce NU este APMF

- **Nu este un ERP agricol** — nu gestionăm stocuri, vânzări sau recoltare
- **Nu este un sistem SCADA industrial** — nu avem nevoie de redundanță de nivel enterprise
- **Nu este un proiect IoT generic** — arhitectura este specifică acvaponiei, nu universală
- **Nu are UI complex** — un dashboard cu carduri și alerte, nimic mai mult în Faza 1
