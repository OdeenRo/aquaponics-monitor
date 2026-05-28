# AQM MANIFEST
### Aquaponics Monitor — The Living Constitution
*Odeen Software · Agentic Project · Version 1.0*

> Acest document este "The Single Source of Truth" al proiectului **AQM (Aquaponics Monitor)**.
> Orice asistent AI are **obligația** să citească acest fișier la începutul oricărei sesiuni de lucru pe acest repository.
> Documentele din `docs/` sunt vii — dacă codul se schimbă, documentația se schimbă simultan.

---

## 1. Misiunea Proiectului

**AQM** nu este un simplu logger de date. Este un **sistem nervos digital** pentru un ecosistem biologic viu.

Un bazin de 9.600L cu 117 pești într-o seră din București nu poate fi monitorizat manual fără riscuri. O creștere de amoniu nedetectată timp de 4 ore poate ucide tot stocul. O cădere a oxigenului dizolvat sub 4 mg/L este o urgență biologică.

**Misiunea AQM:** să elimine incertitudinea și să înlocuiască inspecțiile manuale cu date în timp real, alerte automate și o interfață care arată starea sistemului dintr-o privire — de pe orice dispozitiv, de oriunde.

**Principiul director:** Dacă parametrii sunt în verde, fermierul doarme liniștit.

---

## 2. Consiliul Elders (Odeen Framework)

Acest proiect operează sub umbrela **Odeen Elders Framework** (`D:\Projects\Agentic\Odeen_Core`).

| Elder | Rol | Influență în AQM |
|---|---|---|
| **Scalex** — Grand Maester | Arhitect software | Definește arhitectura MQTT, modularitatea simulator↔ESP32, structura API |
| **Valon** — Master of Coin | Strateg business | Validează că fiecare feature aduce valoare reală (nu monitoring de dragul monitoring-ului) |
| **Arya** — Master of Faces | UI/UX | Dashboard minim, zero fricțiune, date critice la vedere fără scroll |
| **Sani** — Chief Implementer | Execuție & cod | Implementează, raportează în română, face glume la adresa bug-urilor |

**Constituția Odeen** (`D:\Projects\Agentic\Odeen_Core\Constitution\CONSTITUTION.md`) se aplică integral:
- Simplitate suverană — nicio abstractizare inutilă
- Async obligatoriu — MQTT + FastAPI sunt async by design
- Auto-documentare — codul vorbește, comentariile explică doar "de ce"

---

## 3. Structura Documentației (`docs/`)

Folderul `docs/` este sacru. Fiecare fișier are un rol unic și non-negociabil:

| Fișier | Rol | Echivalent TunsFlow |
|---|---|---|
| **`vision.md`** | De ce există AQM. Big picture, valoare, faze de evoluție. | `vision.md` |
| **`system_params.md`** | Sursa unică de adevăr pentru fizica sistemului: dimensiuni, volume, populație, calcule derivate. | *(specific AQM)* |
| **`data_flow.md`** | MQTT topics, format payload, model date senzori, praguri de alertă. | `data_structures.md` |
| **`use_cases.md`** | Scenariile de utilizare: monitoring normal, alerte, ciclare biologică, tranziție hardware. | `use_cases.md` |
| **`screens.md`** | Descrierea dashboard-ului: ce afișăm, cum, cu ce prioritate vizuală. | `screens.md` |
| **`technical_reference.md`** | ADRs (decizii de arhitectură), stack tehnic, ghid setup local + cloud. | `technical_reference.md` |
| **`PROJECT_CONTEXT.md`** | Scroll de onboarding sesiune: sistemul fizic, senzori, plan de faze. | *(specific AQM)* |

---

## 4. Regulile de Aur (Core Rules)

> [!WARNING]
> Aceste reguli se aplică la **orice** modificare de cod sau arhitectură.

### R-01 — Sincronizarea Datelor (Code = Docs)
De fiecare dată când se modifică:
- Structura unui payload MQTT → actualizezi **`docs/data_flow.md`**
- Pragurile de alertă (`ALERT_THRESHOLDS` din `backend/main.py`) → actualizezi tabelul din **`docs/data_flow.md`**
- Un topic MQTT nou → actualizezi **`docs/data_flow.md`** ȘI **`firmware/config.py`**

### R-02 — Sincronizarea UI
Orice modificare a dashboard-ului (`dashboard/app.py`) se reflectă în **`docs/screens.md`**.
Orice senzor nou adăugat apare în `LABELS` din dashboard **și** în `docs/data_flow.md` simultan.

### R-03 — Status Tags Obligatorii
Fiecare use case din `docs/use_cases.md` poartă un tag de status vizibil:
- `**Status:** Draft` — idee, nevalidată
- `**Status:** Ready for Dev` — specificat complet, gata de implementat
- `**Status:** Implemented` — în cod și testat

### R-04 — Simulator = Contract cu Hardware-ul
Simulatorul (`simulator/sensors.py`) este contractul de interfață cu ESP32.
**Niciodată** nu se modifică topicurile MQTT sau formatul payload fără a actualiza simultan:
1. `simulator/sensors.py`
2. `firmware/main.py` (publish) și `firmware/config.py`
3. `backend/main.py` (subscribe + parsing)
4. `docs/data_flow.md`

Dacă formatul se schimbă doar în simulator fără să updatezi firmware-ul, tranziția la hardware real va fi dureroasă. **Nu facem asta.**

### R-05 — Zero Alerte False (Alert Precision)
Orice modificare a pragurilor de alertă (`ALERT_THRESHOLDS`) trebuie validată față de datele biologice reale din `docs/data_flow.md` secțiunea "Parametri biologici normali".
Nu ajustăm praguri pentru a opri alertele — investigăm de ce se declanșează.

### R-06 — Secretele Rămân în `.env`
Niciodată token Telegram, credențiale Azure sau configurări sensibile în cod sau în git.
`.env.example` se actualizează de fiecare dată când o variabilă nouă este necesară.

---

## 5. Arhitectura de Bază (The Big Picture)

```
[Senzori fizici ESP32]          [Python Simulator]
         │                              │
         └──────────────┬───────────────┘
                        ↓ MQTT publish
              [Mosquitto MQTT Broker]
              (local Docker / Azure)
                        ↓ subscribe
              [Backend FastAPI + aiomqtt]
               ├── threshold checker
               ├── in-memory store
               └── Telegram alerts
                        ↓ REST API
              [Dashboard FastAPI + HTML/JS]
              (live sensor cards, 5s refresh)
```

**Principiu de izolare:** Backend-ul nu știe dacă datele vin de la un simulator sau de la un ESP32.
Înlocuirea unuia cu celălalt necesită zero modificări în backend sau dashboard.

---

## 6. Faze de Implementare

> Definiția completă (valoare + checklist + status) în **`docs/PROJECT_CONTEXT.md` — Secțiunea 8**.

| Fază | Descriere | Status |
|---|---|---|
| **Faza 1** | Simulator + arhitectură de bază (stack complet local) | ✅ Completă |
| **Faza 2** | Cloud deployment pe Azure (MQTT + Backend + Dashboard) | ⏳ Pending |
| **Faza 3** | Hardware real — ESP32 înlocuiește simulatorul | ⏳ Pending |
| **Faza 4** | Automatizare completă (control pompe, dozare pH) | ⏳ Viitor |

---

## 7. Protocolul de Start Sesiune

La începutul fiecărei sesiuni Claude Code:

1. **Citește** `AQM_MANIFEST.md` (acest fișier)
2. **Citește** `docs/PROJECT_CONTEXT.md` pentru statusul sistemului fizic
3. **Întreabă** dezvoltatorul ce s-a schimbat de la ultima sesiune (senzori sosiți, Docker instalat, etc.)
4. **Verifică** dacă există TODO-uri neîncheiate din sesiunea anterioară

**Prescurtare acceptată la start sesiune:**
> *"Citește AQM_MANIFEST.md și continuă de unde am rămas."*

---

*Semnat: Consiliul Elders Odeen — Scalex & Valon*
*Implementat de: Sani (Missandei), Chief Implementer*
*Director: Sabin*
