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

| Status | Component | Preț | Link | Note |
|---|---|---|---|---|
| [x] | Breadboard 830p + 65 fire jumper | ~17 RON | [eMag](https://www.emag.ro/kit-breadboard-830-gauri-65-fire-modul-tensiune-alimentare-mb102-jh027/pd/DY1YP6BBM/) | Include și modul alimentare MB102 — 4.92/5 |
| [x] | Rezistențe 4.7kΩ (set 20 buc) | ~25 RON | [eMag](https://www.emag.ro/set-20-bucati-rezistenta-4-7k-kohm-carbon-film-rw25cf-0-25w-5-4700-rezistor-uni-ohm-rw25cf-4-7k/pd/DSGXYWYBM/) | Pull-up obligatoriu pentru DS18B20 |
| [ ] | Sursă alimentare 5V/2A USB-C | — | Orice încărcător telefon USB-C | ESP32-ul tău are USB-C |
| [ ] | Cutie aluminiu IP65, 80×125×58mm | 176 RON | [eMag](https://www.emag.ro/carcasa-aluminiu-80mmx125mmx58mm-ip65-combiplast-t131340/pd/DWTCN3YBM/) | IP65 confirmat, garnitură + suporturi PCB incluse — potrivită lângă bazin |
| [ ] | Cablu 4-conductor 10m+ | ~15 RON | eMag / magazin electric | Doar dacă ESP32-ul e departe de senzori (DS18B20 vin cu cablu 1m) |

### 🟢 Calibrare

> Kitul EZO-pH de la Atlas Scientific include deja soluțiile de calibrare (pH 4.01 + 7.01) și soluția KCl de depozitare. Nu e nevoie de comenzi separate.

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
| EZO-pH Kit (eztronics.nl) — include calibrare | €181 |
| Senzori eMag (ESP32, DS18B20, DHT22, HC-SR04P, YF-S201) | ~160 RON |
| Instalare (breadboard, rezistențe, cutie IP65) | ~218 RON |
| **Total Faza 3** | **~181€ + ~378 RON** |

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
