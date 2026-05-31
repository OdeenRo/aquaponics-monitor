# APMF: Hardware & Lista de Cumpărături

> Sursa unică pentru echipamentele fizice necesare Fazei 3 (hardware real).
> Bifează pe măsură ce echipamentele sunt comandate/primite/instalate.

---

## Senzori și Microcontroller (Faza 3)

### 🔴 Critici — fără astea nu pornești

| Status | Component | Model | Qty | Preț | Link |
|---|---|---|---|---|---|
| [ ] | Microcontroller | Placa ESP32, 30 pini, USB-C | 1 | ~50 RON | [eMag](https://www.emag.ro/placa-esp32-cu-esp-wroom-32-30-pini-usb-tip-c-3874784221589/pd/D0JH59YBM/) |
| [ ] | Senzor pH apă | Atlas Scientific EZO-pH Kit | 1 | ~165€ | [atlasscientific.com](https://atlas-scientific.com/kits/ph-kit/) |
| [ ] | Senzor temperatură apă | DS18B20 waterproof inox (set 5) | 1 set | ~80 RON | [eMag](https://www.emag.ro/set-5-senzori-de-temperatura-ds18b20-waterproof-inox-6x50mm-negru-fg711k0225-07151-426/pd/DX34DF3BM/) |
| [ ] | Senzor O₂ dizolvat | Atlas Scientific EZO-DO Kit | 1 | ~200€ | [atlasscientific.com](https://atlas-scientific.com/kits/dissolved-oxygen-kit/) |
| [ ] | Senzor temp + umiditate aer | DHT22 AM2302 | 2 | ~26 RON/buc | [eMag](https://www.emag.ro/senzor-de-temperatura-si-umiditate-am2302-dht22-ai142-s271/pd/DXSFYMMBM/) ⚠️ stoc limitat |
| [ ] | Senzor nivel apă | HC-SR04**P** (3.3V!) | 1 | ~21 RON | [eMag](https://www.emag.ro/senzor-ultrasonic-de-masurare-distanta-hc-sr04p-dc-3-5-5v-bmx636/pd/DTM2K83BM/) |
| [ ] | Senzor debit apă | YF-S201 G1/2 (Robofun) | 1 | ~40 RON | [eMag](https://www.emag.ro/senzor-debit-apa-robofun-yf-s201-g1-2-1-30l-min-00004036/pd/DVYWPYYBM/) |

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
| Senzori critici (Atlas Scientific) | ~380€ |
| Senzori simpli + ESP32 (AliExpress) | ~60€ |
| Instalare (cabluri, rezistențe, cutie) | ~30€ |
| Calibrare (hydroponika.ro) | ~40 RON |
| **Total Faza 3** | **~470€ + 40 RON** |

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
| Senzor amoniu | Atlas Scientific EZO-NH3 | ~500€ | Prea scump; înlocuit cu test manual săptămânal |
| Senzor nitriti/nitrati | — | ~400€+ | Idem |
