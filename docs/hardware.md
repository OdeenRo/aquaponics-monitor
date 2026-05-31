# APMF: Hardware & Lista de Cumpărături

> Sursa unică pentru echipamentele fizice necesare Fazei 3 (hardware real).
> Bifează pe măsură ce echipamentele sunt comandate/primite/instalate.

---

## Senzori și Microcontroller (Faza 3)

### 🔴 Critici — fără astea nu pornești

| Status | Component | Model | Qty | Preț | Link |
|---|---|---|---|---|---|
| [x] | Microcontroller | Placa ESP32, 30 pini, USB-C | 1 | ~50 RON | [eMag](https://www.emag.ro/placa-esp32-cu-esp-wroom-32-30-pini-usb-tip-c-3874784221589/pd/D0JH59YBM/) |
| [ ] | Senzor pH apă | Atlas Scientific EZO-pH Kit (KIT-101P) | 1 | €181 | [eztronics.nl](https://www.eztronics.nl/webshop3/) |
| [x] | Senzor temperatură apă | DS18B20 waterproof inox, cablu 1m (set 3) | 1 set | ~47 RON | [eMag](https://www.emag.ro/set-de-3-senzori-de-temperatura-digitali-ds18b20-din-otel-inoxidabil-impermeabili-cablu-de-1-m-interval-de-masurare-55-125-et000004/pd/D5R0HR3BM/) |
| [x] | Senzor temp + umiditate aer | DHT22 AM2302 | 2 | ~26 RON/buc | [eMag](https://www.emag.ro/senzor-de-temperatura-si-umiditate-am2302-dht22-ai142-s271/pd/DXSFYMMBM/) |
| [x] | Senzor nivel apă | HC-SR04**P** (3.3V!) | 1 | ~21 RON | [eMag](https://www.emag.ro/senzor-ultrasonic-de-masurare-distanta-hc-sr04p-dc-3-5-5v-bmx636/pd/DTM2K83BM/) |
| [x] | Senzor debit apă | YF-S201 G1/2 (Robofun) | 1 | ~40 RON | [eMag](https://www.emag.ro/senzor-debit-apa-robofun-yf-s201-g1-2-1-30l-min-00004036/pd/DVYWPYYBM/) |

### 🟡 Necesari pentru instalare

| Status | Component | Note |
|---|---|---|
| [ ] | Cablu 4-conductor 10m+ | DS18B20 e la distanță de ESP32 |
| [ ] | Rezistență 4.7kΩ (×5) | Pull-up obligatoriu pentru DS18B20 |
| [ ] | Breadboard + jumper wires | Prototipare inițială |
| [ ] | Sursă alimentare 5V/2A | USB sau adaptor |
| [ ] | Cutie waterproof IP65 | Pentru ESP32 lângă bazin |

### 🟢 Calibrare (de la Hydroponika.ro — mai rapid local)

| Status | Component | Preț est. | Note |
|---|---|---|---|
| [ ] | Soluții calibrare pH (4.01 + 7.01) | ~50 RON | Obligatorii pentru EZO-pH |
| [ ] | Soluție KCl depozitare sondă pH | ~83 RON | Prelungește viața sondei |

---

## Bioindicator (opțional, recomandat)

| Status | Component | Note |
|---|---|---|
| [ ] | Vas plastic 80-100L | Troc separat pentru lintița de apă |
| [ ] | Lintița de apă (*Lemna minor*) | Bioindicator NH₄/NO₃ — izolată de pești |
| [ ] | Panou LED mic (12-24V) | Iluminare fixă deasupra vasului |

---

## Buget estimat

| Categorie | Estimat |
|---|---|
| EZO-pH Kit (eztronics.nl) | €181 |
| Senzori eMag (ESP32, DS18B20, DHT22, HC-SR04P, YF-S201) | ~160 RON |
| Instalare (cabluri, rezistențe, cutie) | ~30€ |
| Calibrare (hydroponika.ro) | ~133 RON |
| **Total Faza 3** | **~211€ + ~293 RON** |

---

## Note pentru Tyron

- **Atlas Scientific** — comandă **kit-urile complete**, nu doar chip-urile. Kit-ul include sonda, soluțiile de calibrare și carrier board-ul.
- **DS18B20** — ia waterproof (cu cablu), nu varianta bare metal.
- **DHT22** — nu DHT11, sensibilitate mai bună la umiditate.
- **YF-S201** — debit apă, detectează instant oprirea pompelor (risc major pentru pești).

---

## Faza 4 — Senzori viitori (nu acum)

| Component | Model | Preț est. | Motiv amânare |
|---|---|---|---|
| **Senzor O₂ dizolvat** | Atlas Scientific EZO-DO Kit (KIT-103DX) | €411 | DO acoperit indirect: YF-S201 (oprire pompă = criza principală) + DS18B20 (temp >26°C = risc). Carașul tolerează bine DO scăzut. De reevaluat după 3-6 luni de funcționare reală. [eztronics.nl](https://www.eztronics.nl/webshop3/) |
| Senzor amoniu | Atlas Scientific EZO-NH3 | ~500€ | Înlocuit cu test manual săptămânal (kit API) |
| Senzor nitriti/nitrati | — | ~400€+ | Idem |
