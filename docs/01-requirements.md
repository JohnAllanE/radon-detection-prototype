# Radon detection prototype: requirements
<!-- doclint-allow: words — an R-xx project: 55 requirements keep their IDs (PCB-WORKFLOW.md) until the user decides whether to convert and merge them into F/O/C items -->

| | |
|---|---|
| Project | Alpha detection with silicon photodiodes: radon progeny in air (Part 1) and weld samples in rough vacuum (Part 2), comparing a premium and a low-cost detector board |
| This document | Purpose, scope, and the R-xx requirements sorted into functions, objectives and constraints. `VERIFY` marks an unconfirmed fact |
| State | Draft. The user's latest answers recorded: Q-04, Q-08, Q-10, Q-12, Q-13, Q-14 resolved |
| Open questions | 2 |

## Purpose

- Measure alpha particles from radon progeny in air (Part 1) and from weld samples that would matter for low-background scientific apparatus (Part 2).
- Find out whether a low-cost detector board gives the same radiation readings as a premium one: event type and event frequency, on the same radiation field.
- A low-cost design that works could later be used in large numbers (the user mentions ~100 detectors in parallel).

## Scope

### In scope

- Detector board, premium and low-cost variants: one of each per chamber, 4 boards in all
- MCU board and HV board
- Both chambers, the Part 1 gas train, board mounting and feedthroughs: mechanics is part of the project (D-04)
- Test requirements on the boards for the electrometer, which is a separate project in `electrometer/`

### Out of scope

- Operating the pump and valves: manual, outside the electronics (D-12)
- Chamber sensors and compensation for pressure, temperature or humidity (D-06)
- Gases other than air and N₂ (D-05)
- HV in Part 2

## Functions

| ID | Function | Status | Source | Verification |
|---|---|---|---|---|
| R-01 | Part 1 detects alphas from radon progeny collected on the photodiode surface, from a flowing or static sample | firm | User | Test |
| R-02 | Part 1 runs on ambient air, with bottled N₂ as the control for self-contamination between runs | firm | User (D-05) | Test |
| R-03 | Part 2 detects alphas from weld samples held close to the detectors in rough vacuum | firm | User (D-10, D-19) | Test |
| R-04 | One detector board design serves Part 1 and Part 2 | firm | User | Inspection, test |
| R-05 | Each chamber runs one premium and one low-cost board at once in the same field, about 3 in (76 mm) apart in Part 1 | firm | User (D-07) | Test |
| R-12 | Channel gain and noise are matched or characterised, so channels can be compared | working | Claude | Test |
| R-13 | Each channel is shaped, held at its peak and triggers by itself. The MCU converts the triggered channel, then clears only that one | firm | User | Simulation, test |
| R-15 | Reports each event's energy code, channel and timestamp to the host | firm | User (D-08) | Test |
| R-18 | Supplies a fixed high voltage, about +1 kV, to the Part 1 chamber wall. No accuracy target: enough field for ions to drift. Load: ion and leakage current | firm | User (D-11, Q-10) | Simulation, test |
| R-20 | Supplies a regulated photodiode bias | firm | User (D-11) | Simulation, test |
| R-23 | The HV output can be read back, which matters more than accuracy: a divider tap now, an HV probe in a later funded effort | firm | User (Q-10, Q-14) | Test |
| R-31 | Closing both valves seals the Part 1 chamber, so it can run static | firm | User (D-03) | Test |
| R-34 | Humidity is measured at the outlet during the purge, with a manual sensor | firm | User (D-06) | Inspection |
| R-37 | Filters remove aerosols and radon progeny from incoming gas and stop desiccant dust | firm | User (D-02) | Test |
| R-47 | A biased exposed ring around the photodiodes steers ions onto them | firm | User (D-09) | Simulation, test |
| R-48 | Bare boards can be characterised before assembly: leakage between input pad, guard and ring, and node capacitance | firm | User (D-15) | Test |
| R-49 | Populated boards can be characterised: input leakage, input capacitance, gain by charge injection | firm | User (D-15) | Test |
| R-50 | An electrometer front end measures board leakage, built as its own project (`electrometer/`), moving to the test-gear repo once built | firm | User (D-15) | Inspection, test |
| R-51 | An alpha check source exists: a smoke-alarm Am-241 source, tentative until a RAD7 measurement makes it a transfer standard. The kV is read by a divider | firm | User (Q-14) | Test |
| R-58 | Part 2 can count with the chamber sealed and the pump off | working | Claude (D-24) | Test |
| R-59 | Part 2 reads the chamber pressure with a vacuum gauge | working | Claude (D-24) | Inspection |
| R-60 | Each CSA input has a non-destructive test port, so a populated, cleaned board is measured without soldering | firm | User (electrometer D-02) | Inspection, test |

## Objectives

Ranked in table order (Claude's ranking, working).

| ID | Objective | Status | Scoring |
|---|---|---|---|
| R-53 | Low-cost board's event types and frequencies match the premium board's: closer is better | firm | No quantitative criterion until there is much more data (Q-07, D-17) |
| R-09 | Energy resolution (FWHM): lower is better. The aim is to tell the radon chain's members apart (Q-04) | firm | Good enough: 100 keV at about 5.5 MeV (D-21), which separates the closest pair, Po-210 and Rn-222 (185 keV apart). Shaping time after the first runs |
| R-08 | Energy range: the radon chain is required, wider is better | firm | Radon chain 6.0–7.7 MeV required. Weld work, roughly 4–9 MeV, best effort (D-21) |
| R-14 | Events handled without loss on other channels while one converts: more is better | firm | Good enough: 100 events/s total. Pile-up on one channel detected and flagged (D-21) |
| R-52 | Gain, baseline and leakage drift over long runs (hours to days, a week or more for calibration): lower is better | working | Limits derived from R-09 in the architecture |
| R-73 | Build and assembly effort after the boards are populated: lower is better | working | Off-board connections and conductors in the architecture: fewer is better |

## Constraints

| ID | Constraint | Status | Source | Verification |
|---|---|---|---|---|
| R-06 | Four silicon photodiodes (5 mm active, 5.67 mm die) in a 2×2 array, each with its own charge-sensitive preamp. Eight identical channels per chamber, partial population acceptable at first | firm | User (D-09, Q-08) | Inspection |
| R-07 | Both variants share connector, pinout and mechanical interface | firm | User | Inspection |
| R-10 | Low-cost: one standard single 8-pin op-amp footprint, general-purpose parts, no NC pins for guard or feedback. Premium may use dedicated parts and their guard pins | firm | User (D-17) | Inspection |
| R-74 | Cost: CAD 20 average per channel at most, CAD 10 preferred. Best parts that don't fit go on 1–2 channels per premium board, not all four | firm | User (Q-08) | Inspection of the priced BOM |
| R-11 | Works in vacuum and in the Part 1 gas: only the photodiode side is exposed, and parts avoid outgassing | firm | User | Inspection, test |
| R-54 | The detector board is the pressure boundary: O-ring sealed, photodiodes inside, back at atmosphere with the connectors | firm | User (Q-20) | Inspection, test |
| R-55 | Detector board: two layers | firm | User (D-14) | Inspection |
| R-56 | MCU board outside the chambers, two layers if possible, four if needed | firm | User (D-14) | Inspection |
| R-16 | ADC chosen on merit. The in-stock 24-bit delta-sigma part and a 16-bit SAR are both fitted | firm | User (D-16) | Simulation |
| R-17 | The MCU board reads no chamber sensors and applies no compensation | firm | User (D-06) | Inspection |
| R-19 | HV ripple and switching noise do not degrade the preamp noise floor | firm | Physics, R-09 | Simulation, test |
| R-21 | HV built on a PCB up to the transformer, point-to-point beyond it, potted only after it works | firm | User (D-11) | Inspection, test |
| R-22 | Nothing at HV is user-touchable, including the +1 kV chamber tube: an insulated outer enclosure with an interlock | firm | Safety (D-20), user (Q-12) | Inspection, test |
| R-24 | Detector to MCU board through a small board-to-board wire connector | firm | User | Inspection |
| R-25 | Wall adapters only: 48 V for the HV board, 5 V for the other boards | firm | User (D-08) | Inspection |
| R-27 | Lab ambient environment, not monitored | working | User (Q-02). What to record per run is proposed in the questions | Test |
| R-28 | Hand-assembled prototype. No BGA; any other package, QFN at 0.5 mm pitch included | firm | User (Q-13) | Inspection |
| R-29 | Part 1 gas train in the order of D-02, with a manual SS/PTFE ball valve on the chamber inlet and outlet | firm | User (D-02, D-03) | Inspection |
| R-30 | Nothing upstream of the chamber outgasses or passes radon: no silicone, rubber or PVC. PTFE tubing | firm | User (D-13) | Inspection |
| R-32 | The pump is downstream, so the chamber runs below ambient. Gas-tightness is characterised after build | firm | User (D-01, D-13) | Test |
| R-33 | Flow, pressure drop and desiccant service interval are characterised after build, not designed to | firm | User (D-13) | Test |
| R-38 | No conductive path from the +1 kV chamber to valves, tubing, pump or mounts. Creepage and clearance at the O-ring land and photodiode corners | firm | Safety | Inspection, simulation |
| R-75 | Spacing from +1 kV: 5.0 mm on bare board surfaces (IPC-2221 B2, `VERIFY`). Inside the chamber, from the field simulation | working | Claude (Q-12) | Inspection, simulation |
| R-39 | Part 1 chamber: 304 SS, 3/4 in NPS pipe, bore 21–22 mm, walls at HV | firm | User (D-22) | Simulation, inspection |
| R-40 | Detector signals pass through the board itself. HV connects to the tube. Part 2 ports are standard | firm | User | Inspection, test |
| R-41 | Pump vibration and drive noise do not degrade the noise floor | firm | User (D-01) | Test with the pump running |
| R-43 | HV is not applied to the chamber below ambient pressure. Procedure first, a hardware interlock optional | working | Claude: Paschen estimate | Inspection |
| R-44 | A detector board at each end of the tube, photodiodes facing the sample volume | firm | User | Inspection, simulation |
| R-46 | Part 2: custom aluminium chamber, 50 mm ID, Viton gaskets, NW25 port for the E2M8, SS/PTFE valve, board sealed as in Part 1 | firm | User (D-10, D-19, D-24) | Inspection, test |
| R-57 | Part 2: pump oil does not reach the weld samples or the photodiodes | working | Claude (D-24) | Inspection, test |

## Open questions

With their context and Claude's proposals: [questions with context](questions/2026-11-21-detector.md).

1. Q-02: which lab conditions to record for R-27. The lab is not monitored.
2. Q-17: desiccant and filter sourcing (D-25): low cost first.

Resolved by the user's latest answers: Q-04 (target set, shaping time after first runs), Q-08 (R-74), Q-10 (R-18, R-23), Q-12 (R-22, R-38), Q-13 (R-28), Q-14 (R-51).

## Notes

- [Answered questions](notes/user-answers.md): the user's answers to Q-01 to Q-37.
- [Decay-chain lines](notes/decay-chain-lines.md): Po-210 to Rn-222 is the closest pair, 185 keV; the smoke-alarm Am-241 source.
- [HV spacing and readback](notes/hv-spacing-and-readback.md): creepage and clearance, 5.0 mm at 1 kV, the divider before the series resistor.
- [Physics reference](notes/physics-reference.md): 44.3 fC per MeV, alpha lines, and why 1–10 mbar is enough for Part 2.
- [Chamber sensitivity](notes/chamber-sensitivity.md): 2–5 counts/hour at 100 Bq/m³, days per 100 counts indoors.
- [Gas train](notes/gas-train.md): about 12.5 g of water a day into the desiccant at 1 L/min. No humidity sensor in the chamber.
- [Part 2 vacuum](notes/part2-vacuum.md): pump to 10⁻² to 10⁻¹ mbar, trap the foreline, count sealed.
- [Electrometer outline](notes/electrometer-outline.md): the first outline, retired. Its R-57 to R-72 are replaced by `electrometer/`.
