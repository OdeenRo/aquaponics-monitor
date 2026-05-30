# APMF — Project Manifest

## Proiectul
Sistem de monitorizare în timp real pentru o instalație acvaponică de 9,600L din București — 117 pești, 3 trepte de filtrare, paturi de cultură. Scopul: fermierul doarme liniștit pentru că datele îl trezesc ele, nu inspecția manuală.
**Limbă:** română | **Ton:** informal, direct

---

## Elders Framework
| Elder | Rol | Influență în APMF |
|---|---|---|
| **Scalex** | Arhitect software | Arhitectura MQTT, modularitate simulator↔ESP32 |
| **Valon** | Strateg business | Fiecare feature aduce valoare reală fermierului |
| **Arya** | UI/UX | Dashboard citibil în 3 secunde, zero scroll |
| **Sani** | Implementare (AI) | Execuție, raportare în română, glume la bug-uri |

---

## Reguli Esențiale
1. **Sincronizare cod ↔ docs** — schimbi payload MQTT → actualizezi `docs/architecture.md` și `firmware/config.py` simultan
2. **Simulator = contract ESP32** — topicurile și formatul payload sunt identice; niciodată nu le schimbi doar într-un singur loc
3. **Secretele în `.env`** — niciodată token Telegram, credențiale Azure sau config sensibil în cod sau git
4. **Zero alerte false** — nu ajustezi pragurile ca să oprești alertele; investighezi de ce se declanșează

---

## Harta Docs
| Fișier | Întrebarea la care răspunde |
|---|---|
| `docs/vision.md` | De ce există APMF? (misiune, utilizator, faze) |
| `docs/architecture.md` | Cum e construit tehnic? (ADRs, stack, convenții, contracte MQTT) |
| `docs/runbook.md` | Cum îl pornesc / deployez? |
| `docs/system_params.md` | Care sunt parametrii fizici ai instalației? |
| `docs/data_flow.md` | Care sunt topicurile MQTT, payload-urile și pragurile de alertă? |
| `docs/screens.md` | Cum arată dashboard-ul? |
| `docs/use_cases.md` | Care sunt scenariile de utilizare? |
| `docs/hardware.md` | Ce hardware trebuie cumpărat? (lista Faza 3 cu checkboxuri) |

---

## Protocol de Start Sesiune
1. Citește `MANIFEST.md` (acest fișier)
2. Întreabă ce s-a schimbat de la ultima sesiune (senzori sosiți, Docker instalat, etc.)
3. Continuă de unde s-a rămas
