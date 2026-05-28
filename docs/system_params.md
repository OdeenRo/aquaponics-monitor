# AQM: Parametrii Fizici ai Sistemului

> Sursa unică de adevăr pentru toate dimensiunile, volumele și caracteristicile fizice ale instalației.
> Orice prag de alertă, calibrare de simulator sau calcul de densitate **pornește de aici**.

---

## 1. Sera

| Parametru | Valoare |
|---|---|
| Tip | Tunel metalic cu folie transparentă |
| Lungime | 12 m |
| Lățime | 6 m |
| Înălțime (la coamă) | ~3.5 m |
| Suprafață la sol | 72 m² |
| Locație | Exterior, București |

---

## 2. Bazinul de Pești

| Parametru | Valoare |
|---|---|
| Dimensiuni | 4 m × 2 m × 1.2 m |
| Volum | **9,600 L** |
| Număr pești | **117** |
| Biomasă estimată | ~5–10 kg |
| Densitate | ~0.5–1 kg/m³ *(optim acvaponic: < 5 kg/m³)* |

### Populație curentă

| Specie | Cantitate | Dimensiune |
|---|---|---|
| Caras (Carassius carassius) | 100 | 10–15 cm |
| Crap puiet (Cyprinus carpio) | 15 | 10–15 cm |
| Crap adult | 1 | ~350 g |
| Crap adult | 1 | ~1 kg |

---

## 3. Sistemul de Filtrare *(în exterior, lângă seră)*

| Componentă | Volum estimat | Rol |
|---|---|---|
| Bazin decantare | ~1,000 L | Prima treaptă — sediment grosier |
| Bazin biofiltru | ~500–700 L | Bacterii nitrificatoare (Nitrosomonas + Nitrobacter) |
| Bazin aerare/pompare | ~500 L | Oxigenare + retur apă în bazin |
| **Total filtrare** | **~2,000–2,200 L** | |

---

## 4. Paturi de Cultură *(în seră)*

| Pat | Dimensiuni | Suprafață | Mediu | Culturi planificate |
|---|---|---|---|---|
| Central | 1.875 m × 12 m × 0.3 m | 22.5 m² | Hydroton | Roșii + castraveți |
| Lateral stânga | 1.25 m × 12 m × 0.3 m | 15 m² | NFT (apă) | TBD |
| Lateral dreapta | 1.25 m × 12 m × 0.3 m | 15 m² | NFT (apă) | TBD |
| **Total** | | **52.5 m²** | | |

---

## 5. Sistemul Hidraulic

| Parametru | Valoare |
|---|---|
| Pompe | 3 pompe submersibile |
| Debit total | ~10,000 L/h |
| Circuit | Bazin → Decantare → Biofiltru → Aerare → Paturi → retur lateral → Bazin |
| Sursă apă | Fântână (fără clor) |

---

## 6. Volume și Calcule Derivate

| Metric | Valoare | Notă |
|---|---|---|
| **Volum total sistem** | ~14,500–15,000 L | Bazin + filtrare + paturi + conducte |
| **Timp ciclu complet** | ~1.5 h | Volum total / debit pompe |
| **Schimburi apă/zi** | ~16 x | Debit 10,000 L/h × 24h / 15,000 L |
| **Raport apă/biomasă** | ~1,500–3,000 L/kg | Indicator de sănătate sistem |

---

## 7. Relevanță pentru Simulator și Praguri de Alertă

- **Volumul 9,600 L** justifică inertia termică mare — temperatura apei se schimbă lent (~0.1–0.2°C/tick de 10s în simulator)
- **Ciclul de 1.5h** înseamnă că un vârf de amoniu din biofiltru ajunge în bazin în max 90 min — justifică intervalul de alertă critic
- **Densitate mică (< 1 kg/m³)** permite o fereastră biologică mai largă; sistemul e robust la variații moderate
- **Sursa fântână** (fără clor, pH natural 7.0–7.5, fier posibil) — pH-ul de bază al apei proaspete e în intervalul optim
