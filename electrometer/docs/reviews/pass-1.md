# Electrometer front end: pass 1 review

| | |
|---|---|
| Pass | 1: a sketch of the head, range panel, source, control, power and the in-tin test |
| Date | 2026-11-20 |
| Covered | Intent (confirmed by the user), architecture draft 2 (topology and ranges approved, the rest awaiting approval), analytic budget. No simulation, no parts selected |
| Next pass | S-01 and S-02 simulations, part selection, measured power draws |

## Changed in earlier documents

| Document | What changed | Decision |
|---|---|---|
| Requirements | Rewritten to the contract, proposed numbers to a note, R-34 added | 2026-11-20: Requirements rewritten |
| Architecture | Choices A-01 to A-20, findings and answered questions to notes | 2026-11-20: Architecture rewritten |
| `CLAUDE.md` | Pass 1 status | 2026-11-20: Project CLAUDE.md |

## Revisit next pass

1. Architecture approval: A-06 ($C_{inj}$ self-test instead of R-25's switched references) and A-18 (≥ 10 MΩ at the radon HV board) are open, as the user left them.
2. A-01, A-11: ±5 V from ±6.5 V converters and LDOs. Converter noise at the head is risk 5, unmeasured. The ADA4530-1 is not in stock and unpriced (Q-09), and no fallback is named.
3. A-09: one source channel. S-02 checks the 0.1–10 Hz noise, with reference noise × 20 the main term against 10 µV rms.
4. A-10, R-24: about 25 h with the source on against 24 h proposed, every draw `VERIFY`, the radio dominant. `PROJECTS.md` still names the shelved 2S battery-pack for the electrometer, which D-08 (1S2P, internal) doesn't use.
5. A-12, R-20: control depends on lab-gateway, whose phase 3 is on hold, and on the gateway HAT's ESP-NOW bridge, still at the PCB stage. Nothing can command the electrometer yet.
6. Bench power standard: `PROJECTS.md` lists the electrometer as a box that follows it (GX12 input), but R-24 and R-31 need it floating on its battery during a measurement.
7. The diagram script keeps its own copy of the house style, not `svgdiagram.py`.

## Last mile

- **The tin:** size, lid contact and light-tightness open. Through it: HV feedthrough with lid interlock and bleeder, filtered PicoBlade pass-through, antenna bulkhead, two gas grommets.
- **Head shield box** (aluminium), range panel, probe tie-down and chamber standoffs: not designed.
- **Wires:** probe coax (2), range panel S, E1, E2 (6), source to breakout (2), charger (2), antenna coax: at least 12 conductors on 7 connectors. Head to control board and the tin's wall items are open.
- **Charger connection:** only with the main switch off. Connector not chosen.

## Questions for the user

1. A-06: $C_{inj}$ and an external cal plug for R-25? Working answer: yes.
2. A-18: ask the radon HV board for ≥ 10 MΩ? Working answer: yes.
3. Q-14: antenna on a bulkhead, or the control board outside? Working answer: bulkhead.
4. Power input: battery alone, or a GX12 2-pin from the bench standard? Working answer: battery inside, GX12 2-pin for charging only, with the main switch off.
5. Until the gateway carries ESP-NOW, a USB-serial console for head bring-up, disconnected for fA runs? Working answer: yes.
6. Q-09: budget for the ADA4530-1, the Murata probe and SWF receptacles? Working answer: one of each.
7. Q-04, Q-10, Q-12, Q-13, Q-15 stay open. Working answer: project HV board only, room-air RH, measure the SWF on the test board.

## Parts to order

No order planned.

| Part | Open items |
|---|---|
| ADA4530-1 | Q-09 budget, not in stock |
| Murata SWF probe and receptacles | Q-12 leakage, Q-13 space, part numbers |
| MCP4922, MCP4821, REF5040, ADS1220, OPA2186, ESP32-S3-WROOM-1U | In stock: none to order |
| HV op-amp, ±60 V boost, reed relay, analog SPDT, 1 GΩ resistor, T/RH sensor | Not selected |

## Answers

Written up with context: [questions](../questions/2026-11-21-electrometer.md). Question 2 is decided with the detector's A-21; question 7's Q-04, Q-10, Q-15 are settled there.
