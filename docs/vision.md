# AQM: Viziunea Sistemului

## 1. Context și Problemă

O seră de 12m × 6m în București adăpostește un ecosistem acvaponic complex: un bazin de 9.600L cu 117 pești, trei trepte de filtrare biologică și paturi de cultură cu o suprafață totală de ~40m².

Ecosistemul este **viu și fragil**. Parametrii apei se pot deteriora în ore, nu în zile:
- O pompa oprită noaptea → oxigenul dizolvat scade sub 4 mg/L → pești morți dimineața
- Ciclarea biologică nemonitorizată → vârf de amoniu nedetectat → toxicitate acută
- pH în afara ferestrei 6.5–7.8 → bacteriile nitrificatoare mor → colaps biologic în 48h

**Problema:** Fără monitorizare continuă, singurul sistem de alertă este inspecția manuală — care nu funcționează noaptea, în weekend sau când fermierul este la birou.

---

## 2. Misiunea AQM

**AQM transformă un ecosistem biologic opac într-un sistem transparent și alertat.**

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

## 4. Valoarea pe Faze

> Definiția completă a fazelor (valoare + checklist + status curent) se află în **[`docs/PROJECT_CONTEXT.md` — Secțiunea 8](PROJECT_CONTEXT.md)**.

| Fază | Valoare principală | Status |
|---|---|---|
| **Faza 1** — Simulator + arhitectură locală | Stack demonstrabil, arhitectură validată fără hardware | ✅ Completă |
| **Faza 2** — Cloud Azure | Acces remote permanent, URL fix | ⏳ Pending |
| **Faza 3** — Hardware real ESP32 | Date reale, zero modificări arhitectură | ⏳ Pending |
| **Faza 4** — Automatizare completă | Fermierul devine observator, nu operator | ⏳ Viitor |

---

## 5. Ce NU este AQM

- **Nu este un ERP agricol** — nu gestionăm stocuri, vânzări sau recoltare
- **Nu este un sistem SCADA industrial** — nu avem nevoie de redundanță de nivel enterprise
- **Nu este un proiect IoT generic** — arhitectura este specifică acvaponiei, nu universală
- **Nu are UI complex** — un dashboard cu carduri și alerte, nimic mai mult în Faza 1
