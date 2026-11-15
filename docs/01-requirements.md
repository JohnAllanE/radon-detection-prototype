# Requirements: radon detection prototype

**Status:** DRAFT 2, Phase 1 (requirements). Not yet confirmed by the user.
**Started:** 2026-10-12. **Revised:** 2026-10-12 after the user's answers to Q-01 to Q-19.
**Legend:** `TBD (Q-xx)` means the target depends on an open question in §6. `VERIFY` means not yet checked against a source. `PROPOSED` means Claude's suggestion for the user to accept or change. Decisions are recorded in `decisions.md` (D-xx).

## 1. Purpose and scope

Build a two-part prototype for measuring alpha particles with silicon photodiodes:

- **Part 1: radon in air.** Sample gas passes through a filter, desiccant column and second filter into a small stainless-steel chamber. Chamber walls are held at about +1 kV so that positively charged radon-progeny ions (Po-218 and Po-214) are drawn onto the photodiodes.
- **Part 2: weld-sample alpha detection in rough vacuum.** The same detector board, with weld samples placed close to the detectors for direct alpha strikes. No HV, no ion steering. The aim is to find contamination that would matter for low-background scientific apparatus.

In each chamber, two detector boards run side by side (one premium, one low-cost) so the comparison is made on the same radiation field. **The comparison metric is whether the low-cost board gives similar information: event type and event frequency, i.e. the same radiation readings.** A low-cost design that works could later be used in large numbers (the user mentions ~100 detectors in parallel).

Electronics in scope: detector board (two variants), MCU board, HV board, plus a test electrometer front-end (§4.7). Mechanical in scope: both chambers, gas train, board mounting and feedthroughs (D-04). Pump and valves are operated manually and are outside the electronics (D-12).

```mermaid
flowchart LR
  PD["4x silicon photodiode"] --> CSA["4x charge-sensitive preamp\n(detector board: premium / low-cost)"]
  CSA -- board-to-board connector --> MCU["MCU board:\nshaping, peak-hold, comparator trigger,\nmux, ADC, microcontroller"]
  HV["HV board\n48 V -> PCB transformer -> Walton multiplier"] -- "~1 kV" --> WALLS["Part 1 chamber walls"]
  HV -- "regulated PD bias" --> PD
  MCU -- "USB / ESP-NOW" --> HOST["Host"]
```

### Part 1 gas train (D-01 to D-03)

```mermaid
flowchart LR
  IN["Sample gas\n(air / N2 control)"] --> F1["Inlet filter"] --> D["Desiccant column"] --> F2["Final filter"] --> V1["Ball valve\n(SS + PTFE)"] --> CH["Chamber: 304 SS tube ~16 mm ID,\nwalls ~+1 kV, 2 detector boards ~3 in apart"] --> V2["Ball valve\n(SS + PTFE)"] --> P["Diaphragm pump"] --> EX["Exhaust"]
```

## 2. Boards

| Board | Function | Variants / qty |
|---|---|---|
| Detector | 4x silicon photodiodes (5 mm active) in a square + 4x charge-sensitive preamps; pressure boundary of the chamber (O-ring sealed); 2 layers | **Premium** and **low-cost**; one of each per chamber, so 4 boards total |
| MCU | Pulse shaping, peak-hold, comparator trigger, channel mux, ADC, microcontroller (USB, ESP-NOW option) | 1, external to the chambers |
| HV | 48 V in; 100–200 V via PCB transformer; Walton multiplier to ~1 kV; regulated PD bias | 1; fixed output, no adjustment |
| Electrometer front-end (test equipment) | Pico-amp leakage and capacitance measurements of bare and populated boards | 1, may move to the test-gear repo later |

Power: wall adapters only (48 V and 5 V).

## 3. Reference facts and preliminary estimates

Numbers marked `VERIFY` are standard figures or recalled values that must be checked against a source before they drive a design decision.

**Physics**
- Si pair-creation energy is about 3.6 eV per pair, so a 6 MeV alpha releases about 1.7 × 10⁶ pairs (about 270 fC). `VERIFY` in phase 2.
- Alpha energies in MeV (`VERIFY` against ENSDF): Po-218 6.00; Po-214 7.69; Po-210 5.30 (from long-lived Pb-210, half-life about 22 y, so it accumulates on surfaces and shows up as background); thoron chain Po-216 6.78 and Po-212 8.78, Bi-212 6.05 (36 %).
- Self-contamination: Pb-210 and Po-210 deposited by previous air runs stay on the photodiode and chamber. That is the reason for the N₂ control run (D-05).
- Rough vacuum energy loss (`VERIFY`): a 5.5 MeV alpha loses roughly 1 MeV per cm of air at atmospheric pressure, so about 10 keV per cm at 10 mbar. Over the 5–10 mm sample gap (D-19) the loss is about 100 keV at 100 mbar, 10 keV at 10 mbar, 1 keV at 1 mbar and about 10 eV at 10⁻² mbar, so anything at or below about 1–10 mbar is enough for R-09. The Edwards E2M8 reaches 1×10⁻³ mbar (D-24), about four orders of magnitude of margin.

**Sensitivity of the Part 1 chamber (preliminary, assumptions in bold, `VERIFY` all)**
- Volume of a 21–22 mm bore tube (D-22), boards 76 mm apart: π × 1.05² × 7.6 ≈ 26 cm³ (21 mm) to π × 1.1² × 7.6 ≈ 29 cm³ (22 mm).
- At 100 Bq/m³ (0.1 Bq/L, a typical indoor level) the tube holds 0.1 × 0.026 ≈ 2.6 mBq of radon, which is about 9.5 radon decays per hour (about 10.4 at 22 mm).
- Each decay can give two alphas (Po-218, later Po-214). **If the overall collection and detection efficiency is 10–25 % per alpha**, the whole chamber sees roughly 2–5 counts/hour at 100 Bq/m³ and 0.2–0.5 counts/hour at 10 Bq/m³ (outdoor level). The efficiency is a guess and is the thing the field simulation must tell us.
- Consequence: for a 10 % statistical uncertainty (100 counts), indoor air takes of order days and outdoor air weeks. That fits the user's "hours/days, week+ for calibration" plan, but it makes the chamber a low-sensitivity instrument at ambient levels and a good one at mine levels (higher radon). It is not a blocker for the detector comparison, which compares boards against each other, but it sets expectations.

**Water load on the desiccant** (for the later characterisation, not a design driver, D-13)
- Saturated vapour density of air at 20 °C is about 17.3 g/m³, so 50 % RH holds about 8.65 g/m³. At 1 L/min (0.06 m³/h) that is 0.52 g/h, about 12.5 g per day. If the desiccant takes up about 10 % of its weight (`VERIFY` for the chosen product), that is about 125 g per day of continuous running. The N₂ control is already dry.
- Commercial radon monitors dry the sample and ask for low humidity at the detector (Durridge RAD7 uses a calcium sulfate desiccant, roughly 1 L/min; `VERIFY` from its manual) because water vapour reduces the fraction of Po-218 that stays charged.

**Parts** (part-specific facts live in `02-architecture.md`)
- Photodiode: area, capacitance, dark current, rated bias (the user recalls 20 V as an option), which electrode faces the window. All `VERIFY`. The electrode polarity matters for ion steering, see R-47.
- ADC: a multi-channel 24-bit delta-sigma part and a 16-bit SAR part are the candidates (R-16). Input range, channel count and single-ended behaviour are `VERIFY`.
- **ADC resolution vs detector resolution (PROPOSED view):** a 16-bit ADC over 0–9 MeV has about 0.14 keV per code. Even 12 bits is about 2 keV per code. The photodiode and preamp resolution will be tens of keV, so ADC bits are not the limit; noise, droop and charge injection in the peak-hold are.

## 4. Requirements

IDs are provisional until the user confirms. Verification: **S** = simulation, **T** = test, **I** = inspection.

### 4.1 System

| ID | Statement | Target | Verify |
|---|---|---|---|
| R-01 | Part 1 detects alphas from radon progeny collected on the photodiode surface from a flowing or static sample | Sensitivity not specified. Expected levels: typical surface-level indoor/outdoor and underground-mine air. See §3 estimate | T |
| R-02 | Part 1 works with ambient air; bottled N₂ (semi-dry) is used as a control to check self-contamination between runs | Air and N₂ only | T |
| R-03 | Part 2 detects alphas from weld samples held close to the detectors in rough vacuum | ≤ 1 mbar target, ≤ 10 mbar acceptable (§3); E2M8 ultimate 1×10⁻³ mbar (D-24). Sample–detector 5–10 mm (D-19) | T |
| R-04 | One detector board design serves Part 1 and Part 2 | n/a | I, T |
| R-05 | In each chamber, one premium and one low-cost board run simultaneously, in the same field, about 3 in (76 mm) apart (Part 1) | Same arrangement in Part 2 | T |
| R-53 | Comparison metric: low-cost board reports similar event types and event frequency to the premium board | Quantitative criterion TBD (Q-07) | T |
| R-52 | Stable operation for long runs: hours to days regular, a week or more for calibration. Gain, baseline and leakage drift are within limits | Drift limits TBD, derived from R-09 | T |

### 4.2 Detector board (both variants)

| ID | Statement | Target | Verify |
|---|---|---|---|
| R-06 | Four silicon photodiodes (5 mm active, 5.67 mm die) in a 2×2 array, each with its own charge-sensitive preamp | 4 channels, about 11.8 mm per side with 0.5 mm gaps, fits a 21–22 mm bore (R-39) | I |
| R-07 | Premium and low-cost variants share connector, pinout and mechanical interface so either can plug into the MCU board | Same | I |
| R-08 | Energy range covered | Radon chain 6.0–7.7 MeV; weld contamination may need roughly 4–9 MeV (Th/U chains) (Q-05) | S, T |
| R-09 | Energy resolution (FWHM) | PROPOSED ≤ 100 keV at ~5.5 MeV: separates Po-210 / Po-218 / Po-214 easily. Telling Bi-212 6.05, Rn-220 6.29 and Po-216 6.78 apart for thoron or weld work needs about this or better | S, T |
| R-10 | Low-cost variant uses standard footprints and general-purpose parts (the user estimates ~$4 vs ~$12 per amplifier), with no use of NC pins for guard or feedback. Premium variant may use dedicated CSP parts and their guard/feedback pins | Cost per channel TBD (Q-08) | I |
| R-11 | Works in vacuum (Part 2) and in the Part 1 gas: only the photodiode side is exposed; part choices avoid outgassing | Per R-03 | I, T |
| R-12 | Per-channel gain and noise are matched or characterised so channels can be compared | TBD | T |
| R-54 | The board is the pressure boundary: O-ring sealed to the chamber, photodiodes inside, back side at atmosphere with the connectors | Leak rate TBD; vias and board material are leak paths to check (Q-20) | I, T |
| R-55 | Two-layer board (lowest interlayer capacitance, simple circuit) | 2 layers | I |
| R-60 | Non-destructive test port per CSA input (electrometer R-19, D-02): a Murata SWF-type switched coaxial connector on the back side, in series between the diode node and the CSA input, shell on the 0 V guard ring; Ctest on the diode side. A populated, cleaned board is measured without soldering and goes into service after 1–2 mating cycles per connector. A dedicated bare-board test board uses the same footprints | SWF 2.5 × 2.5 mm, 100 cycles rated; fit on the ≤ 20 mm board (electrometer Q-13); CSA op-amp stable at noise gain 1 while its diode is disconnected | I, T |

### 4.3 MCU board

| ID | Statement | Target | Verify |
|---|---|---|---|
| R-13 | Per channel: pulse shaper, peak-hold (sample-and-hold) and a comparator. A comparator trigger interrupts the MCU, which routes that channel's held peak to the ADC, samples it, then clears only that channel | 4 channels; shaping time TBD (Q-04) | S, T |
| R-14 | Handles the expected event rate without losing events on other channels while one is converting | PROPOSED: no loss up to 100 events/s total (calibration source), far above radon rates; pile-up on one channel is detected and flagged | S, T |
| R-15 | Reports event energy code, channel and timestamp to the host over USB; ESP-NOW (PCB antenna) kept as a possible option | Microcontroller with native USB and a radio | T |
| R-16 | ADC choice by merit. A 24-bit delta-sigma ADC (in stock) is the default; a 16-bit SAR with mux is the alternative. A selectable high-resolution/high-rate path is optional | Options compared in phase 2; single-ended inputs are probably adequate for ground-referenced unipolar pulses | S |
| R-17 | The MCU board reads no chamber sensors (T, RH, pressure, flow) and applies no compensation (D-06) | None | I |
| R-56 | Board is external to the chambers; 2-layer if possible, 4 if needed | n/a | I |

### 4.4 HV board

| ID | Statement | Target | Verify |
|---|---|---|---|
| R-18 | Generates about +1 kV for the Part 1 chamber wall from a 48 V wall-adapter supply, via PCB transformer (100–200 V) and Walton multiplier. Fixed output | Load current, accuracy TBD (Q-10) | S, T |
| R-19 | Output ripple and switching noise do not degrade the preamp noise floor | Limit derived from R-09 | S, T |
| R-20 | Regulated photodiode bias | Per the photodiode datasheet (user recalls 20 V option, `VERIFY`); noise TBD | S, T |
| R-21 | HV construction: PCB for the low-voltage and transformer part; the high-voltage section built point-to-point (Manhattan or in-air) to avoid PCB surface leakage; epoxy-potted (vacuum and pressure pot) only after it is shown to work | Creepage/clearance margins TBD (Q-12) | I, T |
| R-22 | Nothing at HV is user-touchable. This includes the +1 kV chamber tube | Enclosure or insulation TBD (Q-12) | I |
| R-23 | HV output can be checked by the user (divider or test point) | TBD | T |

### 4.5 Interfaces, environment, build

| ID | Statement | Target | Verify |
|---|---|---|---|
| R-24 | Detector → MCU connection uses a small board-to-board wire connector (family and pitch in architecture §3) | Pin count and signals TBD in phase 2 | I |
| R-25 | Power inputs: 48 V wall adapter (HV board) and 5 V wall adapter (other boards) | Rail details TBD | I |
| R-27 | Operating environment | Lab ambient; range TBD (Q-02) | T |
| R-28 | Prototype build: hand-assembled, 2-layer detector board | Smallest package, fab house TBD (Q-13) | I |

### 4.6 Mechanical and gas path

| ID | Statement | Target | Verify |
|---|---|---|---|
| R-29 | Part 1 gas train in the order of D-02, with a manual SS/PTFE ball valve on the chamber inlet and outlet | As drawn | I |
| R-30 | Everything upstream of the chamber avoids outgassing and radon-permeable materials (no silicone, rubber or PVC tubing). Tubing is PTFE | Calcium sulfate (indicating) desiccant is preferred; sourcing outstanding (Q-17) | I |
| R-31 | Closing both valves seals the chamber, so it can run static | Hold time TBD | T |
| R-32 | Gas-tightness: with the pump downstream the chamber is below ambient, so leaks draw in unfiltered, undried air | Characterise after build (D-13) | T |
| R-33 | Flow, pressure drop, desiccant service interval | Characterise after build (D-13) | T |
| R-34 | Humidity is measured at the outlet during purge with a manual sensor. No sensor is placed in the chamber or on the detector board (see §7) | Manual | I |
| R-37 | Filters remove aerosols and radon progeny from incoming gas, and stop desiccant dust | One standard filter for every gas port, PROPOSED in D-25; part selection open (Q-17) | T |
| R-38 | No conductive path from the +1 kV chamber to valves, tubing, pump or mounts: insulating PTFE gas-line sections between chamber and valves; creepage and clearance around the board's O-ring land and the photodiode corners | Distances TBD (Q-12) | I, S |
| R-39 | Chamber: 304 SS tube, walls at HV, four photodiodes on the detector board. **Decided 2026-10-12 (D-22): 3/4 in NPS pipe, bore 21–22 mm after grinding and lapping, possibly etched to remove contamination.** The photodiode die is 5.67 mm square: a 2×2 array with 0.5 mm gaps has a 16.75 mm diagonal, leaving about 2.1 mm (21 mm bore) to 2.6 mm (22 mm bore) from die corner to the wall. Uniform-field Paschen estimate for 2.1 mm at 100 mbar is about 1.46 kV (`VERIFY`; corners are worse), so R-43 still applies | Gap to wall confirmed by the field simulation; bore tolerance and etch recorded in the mechanical drawing | S, I |
| R-40 | Feedthroughs: detector signals pass through the board itself, which seals to the chamber. HV connects to the tube. Part 2 vacuum ports are standard | Details TBD (Q-18, Q-20) | I, T |
| R-41 | Pump vibration and drive noise (the pump is operated manually, outside the electronics) do not degrade the noise floor | Measured with the pump running | T |
| R-43 | HV is not applied to the chamber when it is below ambient pressure (inlet valve closed with pump running, or any pump-down). Procedure first; an optional hardware interlock decided in phase 2 | Claude's rough Paschen estimate (`VERIFY` in phase 2): a ~1 mm gap, such as a photodiode corner to the wall, can approach 1 kV near 100 mbar; the ~8 mm gaps are safe down to about 15 mbar | I |
| R-44 | Detector board mounts at each end of the tube with the photodiodes facing the sample volume; HV-side clearances per R-38 | Mount design TBD (Q-20) | I, S |
| R-46 | Part 2: custom aluminum chamber with gaskets, an NW25 port for the Edwards E2M8 two-stage rotary vane pump (D-24), an SS/PTFE ball valve, board O-ring sealed with its back at atmosphere. Weld samples close to the detectors | Pressure per R-03; gasket (Q-21), sample holder (Q-22) | I, T |
| R-57 | Part 2: pump oil does not reach the weld samples or the photodiodes. Pump only to a few ×10⁻² to 10⁻¹ mbar, not to ultimate (oil vapour backstreams in molecular flow); a foreline trap (activated alumina or molecular sieve) between chamber and pump; the chamber valve closed before the pump is stopped; venting with dry N₂ through the chamber inlet, never back through the pump line. The PTFE membrane filter (D-25) stops oil mist and particles but not oil vapour | Trap type and part TBD | I, T |
| R-58 | Part 2: counting can be done with the chamber sealed and the pump off, to remove pump vibration, motor EMI (R-41) and backstreaming. The allowed run length is set by the leak-up rate measured on the built chamber, up to about 1–10 mbar (R-03) | Leak-up rate measured after build (D-13) | T |
| R-59 | Part 2: a vacuum gauge (Pirani or similar) on an NW25 tee reads the chamber pressure | Gauge part TBD | I |
| R-47 | Photodiode surfaces are surrounded by exposed ENIG with a bias to push ions onto the photodiodes. Sign, magnitude and source decided by simulation. **Claude's view:** the ring should be slightly *positive* relative to the photodiode front surface (positive ions are repelled from it and steered to the diode). The source should be filtered or regulated, not raw 48 V, because noise on the ring couples capacitively into the preamp input | Set by simulation | S, T |

### 4.7 Test instrumentation and board characterisation

| ID | Statement | Target | Verify |
|---|---|---|---|
| R-48 | Bare-board characterisation before assembly: leakage between the input pad, guard and ring; interlayer and node capacitance | Limits from the preamp noise budget (phase 2) | T |
| R-49 | Populated-board characterisation: input leakage, input capacitance, gain via charge injection | TBD | T |
| R-50 | Electrometer front-end board (premium electrometer IC, switchable capacitors, reed relays, external wireless MCU over ESP-NOW, R-67) controlled by test scripts through the host-side ESP-NOW bridge API (future). Until built, this section lives in this project; afterwards it is factored out into the test-gear repo | Requirements in `electrometer/docs/01-requirements.md` (DRAFT 1, 2026-10-20) | I, T |
| R-51 | Alpha source and HV measurement method | TBD (Q-14) | T |

#### Electrometer outline (PROPOSED, 2026-10-13)

**Scope.** Leakage is the core job and the only one the physics needs: board leakage currents add shot noise and baseline offset to the preamp input. Two additions to "leakage only", both from the same hardware: (a) the photodiode's own reverse current versus bias on populated boards (the largest DC current on the board, and it screens diodes and tracks drift for R-52), and (b) node capacitance, already in D-15, R-48 and R-49, via a charge step into the switchable reference capacitors. Not electrometer jobs: gain calibration by charge injection (R-49, uses a pulse generator) and any kV measurement (R-51).

**Node pairs to test** (bare board, then populated, per R-48 and R-49):

| Path | Why it matters |
|---|---|
| CSA input pad ↔ guard | Guard only works if its leakage to the input is far below the diode dark current |
| CSA input pad ↔ ENIG ring | The ring carries a bias (R-47); leakage here is a DC load on the input and a noise path |
| CSA input pad ↔ GND, PD bias, other layer | Surface and through-board paths on the critical node |
| Input pad ↔ neighbouring channel input | Crosstalk and charge sharing between channels |
| Via ↔ via and ↔ plane near the sealed vias (R-54) | Sealed, filled vias are a new construction, so leakage there is untested |
| Photodiode reverse current vs bias, in the dark | Compares the 8 diodes, screens bad chips, baseline for drift |

| ID | Statement | Target | Verify |
|---|---|---|---|
| R-57 | Measure DC current between any two nodes of a board with a stated voltage applied, at the voltages used in operation: PD bias (default 20 V, specified at 20 V and 40 V, breakdown above 100 V) and the ring bias (TBD) | Source up to 50 V PROPOSED; who supplies it is Q-27 | T |
| R-58 | Current range and resolution | PROPOSED 10 fA resolution after averaging, 100 µA full scale (decided 2026-10-13, so the top range overlaps the bench DMM, R-72; revisit if size becomes a problem). Diode dark current is 0.15–2 nA. The physics only needs about 1 pA: board leakage at 1 % of typical diode dark current is about 1.5 pA. The extra decade or two is margin to see contamination trends. Q-28 | T |
| R-59 | Fixture: guarded contacts to the board pads, shielded enclosure, PTFE or air insulation, no hand contact during a measurement. Fixture leakage with open contacts is at least 10× below the lowest board value measured, and is recorded each session | Fixture design TBD (Q-31) | I, T |
| R-60 | Settling: leakage at fA–pA levels takes seconds to minutes to settle (dielectric absorption, board capacitance). Scripts record the current-versus-time trace after each voltage step and report the value at a stated delay, not a single reading | Delay TBD from first measurements | T |
| R-61 | Each measurement record stores the board ID and state (bare, populated, cleaned, baked), date, and temperature and RH read by the in-box sensor (R-68) at the start and end of the measurement. Surface leakage depends on humidity and flux residue (architecture §3), so repeats before and after clean and bake are expected | n/a | I |
| R-62 | Capacitance mode: node capacitance from a charge step into switchable reference capacitors | PROPOSED range 0.1–100 pF, resolution 0.1 pF. The nominal 1 pF feedback capacitor has 0.1–0.3 pF of board stray (architecture §2.2), so about 0.1 pF is what is useful. Q-30 | T |
| R-63 | The input survives a charged capacitor, ESD and a wrong connection without a change in leakage afterwards. Source limit and input protection TBD | Protection parts must not add leakage | T |
| R-64 | Self-test and verification: known high-value resistors (1 GΩ to 100 GΩ class) and a known capacitor check each range before a session; offset current checked with the input open | Tolerance TBD. The bench DMM can verify only the top ranges (R-72); trust at fA ranges rests on the ratio chain and capacitor ramp, so it is limited | T |
| R-65 | Data over the user's API as a stream of timestamped samples with range, source voltage and state attached; Claude writes the scripts and the user runs them (Q-23) | n/a | T |
| R-66 | Shielded enclosure: the front-end, board contacts and DUT sit inside a closed conductive enclosure (a tin is acceptable if the lid makes good contact) against electrostatic, mains and RF pickup. Cable and fixture are mechanically fixed to limit triboelectric and microphonic currents | Enclosure and lid contact TBD; check by comparing open-input offset with the lid open and closed | I, T |
| R-67 | Three boards and one enclosure. (1) Front-end board inside the enclosure: electrometer IC, feedback resistors and capacitors, relays, board contacts, an I²C I/O expander for relay and sensor control, and a gain stage (R-70). No MCU inside; an MCU is acceptable there only if asleep with clocks stopped during a measurement. (2) Environmental sensor board inside, sensor elements exposed and very near the board under test (R-68). (3) External board: ESP32 and radio, supply, two removable 18650 cells in series, no onboard charger, ADC. The enclosure blocks the radio, and MCU heat and radio bursts would shift and disturb a fA input. Link: short shielded cable through filtered feedthroughs (R-71) | Power inside the enclosure TBD, minimised (relay coils are the main load, R-69); heating checked by logging in-box temperature | I, T |
| R-68 | An RH/T sensor sits inside the enclosure next to the board and is powered down during a measurement (its I²C lines are a noise path). It is read before and after each measurement. Optional dry-N₂ or desiccant-dried atmosphere in the enclosure for runs that represent detector conditions; room air is the worst case | Sensor and accuracy TBD (Q-32) | T |
| R-69 | Relays and ranging. Reed relays (open-contact insulation about 10¹²–10¹⁴ Ω, `VERIFY` per part) on every node that touches the CSA-style input; ordinary EM latching relays or analog switches only after the first stage, where leakage does not matter. Range selection: one feedback resistor and one feedback capacitor at a time, about 10 relays in all (about 5 resistor values from 10 kΩ to 100 GΩ for the 100 µA to fA span, 2–3 capacitors, zero/reset, input select; post-first-stage gain fills the decades between). Capacitance mode may combine reference capacitors in a few steps only, because each added reed puts open-contact leakage on the input. De-energised state is safe (input protected). Few coils energised at once, placed away from the input node, since coils need holding power of tens of mW (`VERIFY`). Latching reed relays are an option if found (`VERIFY`) | Part choice and relay count in phase 2 | I, T |
| R-70 | Signal level at the enclosure wall: a 10 fA current through a 100 GΩ feedback resistor is only 1 mV, so the front-end includes a gain stage and a differential output pair before the signal crosses the wall, or the ADC moves inside (decision in phase 2; PROPOSED: gain stage inside, ADC outside) | Level at the wall TBD, volts-scale PROPOSED | S, T |
| R-71 | Enclosure link: shielded panel-mount jack with the cable shield bonded 360° to the wall; Ethernet-style twisted pairs for power, I²C, and the analog output; cable about 1 m or less. Because it looks like Ethernet, it must not be able to meet a network or PoE switch: label it or use a keyed connector (e.g. M12) | Connector TBD (Q-35) | I |
| R-72 | Calibration. (1) Top ranges against the bench DMM (Siglent SDM3055, lowest current range 200 µA, about 1 nA resolution, accuracy about 0.1 % of reading plus 0.05 % of range, `VERIFY` from its manual): at 100 µA the DMM is good to about 0.15 %, at 10 µA about 1 %, at 1 µA only about 10 %. (2) Voltage across a measured resistor, I = V/R, using the DMM as voltmeter and as ohmmeter up to about 100 MΩ. (3) A ratio chain: the same current into adjacent ranges gives each feedback resistor relative to the last, from 100 MΩ up to 100 GΩ. (4) Capacitor ramp for the fA decades: I = C dV/dt with C of 1–100 pF checked on an LCR meter; also calibrates integrating and capacitance mode. Source: the SDG2122X ramp or DC output behind a divider and filter, or a battery-fed source for the lowest ranges. (5) Open-input offset every session (R-64). (6) Optional outside tie-in: a borrowed SMU or an accredited certificate for one or two resistor standards | Target accuracy about 5–10 % PROPOSED, because the aim is comparing boards on the same instrument, so repeatability and offset matter more than absolute accuracy. Check at more than one voltage and temperature for resistor coefficients | T |

## 5. Assumptions
- `PCB-WORKFLOW.md` applies (prototype boards, local inventory is a source of parts).
- The chamber is machined by the user; effort goes into building and then measuring, not into characterising everything in advance (D-13).
- Boards are separate KiCad projects sharing one project-local library.
- The electrometer is not SCPI. Until told otherwise, Claude will treat it like the bench instruments: write the script, show it, and have the user run it (Q-23).

## 6. Open questions

Resolved by the user on 2026-10-12: Q-01, Q-02, Q-08, Q-09, Q-10, Q-13, Q-16, Q-18 (partly), Q-19. See `decisions.md`.

- **Q-03** Resolved (2026-10-16): pump is an Edwards E2M8, ultimate 1×10⁻³ mbar (D-24); distance 5–10 mm (D-19). The pressure actually reached and the leak-up rate are measured with the gauge (R-59) after build. HV is not used in Part 2, so only the Part 1 pressure case (R-43) remains.
- **Q-04** Target sensitivity, and shaping time. The user does not know the target; decide after the first runs, or set a placeholder?
- **Q-05** Alphas of interest: radon chain, thoron chain, and the weld-contamination energy range? (Accept R-09 proposal?)
- **Q-06** Accept R-14 proposal (100 events/s total)? Expected weld-sample rates unknown.
- **Q-07** A quantitative "similar enough" criterion for R-53 (e.g. counts within X % over N days, peak positions within Y keV).
- **Q-11** Confirm the photodiode bias from the datasheet (needs pulling) and the electrode polarity.
- **Q-12** Creepage and clearance rule for 1 kV (to be proposed in phase 2: IEC 60664-1 or IPC-2221 tables, `VERIFY`), and how the +1 kV tube is made non-touchable.
- **Q-14** Alpha check source (e.g. Am-241)? Method of reading 1 kV (HV probe or divider)? Existing instrument limits to be checked in `instruments.json` in the test-plan phase.
- **Q-15** Suppliers and the path/format of `parts/inventory.csv`. Desiccant sourcing is outstanding.
- **Q-17** Remaining gas-train details are deferred to after the build (D-13). Desiccant availability to check.
- **Q-20** Detector board layout: are the preamps on the atmosphere side of the board (short vias from each photodiode) or on the chamber side? Board outline and O-ring land diameter. Are plated vias acceptable as the seal at rough vacuum?
- **Q-21** Gasket material for Part 2. Claude's input: Viton (FKM) is fine for a prototype. For low-background work the concerns are radon emanation and permeation, and U/Th in fillers; indium wire, PTFE or FEP-encapsulated O-rings are the usual lower-background choices, and screening a lot is the proper check (`VERIFY`).
- **Q-22** Weld sample size, holder, and distance to the detectors in Part 2.
- **Q-23** Confirm that the electrometer should be treated like the SCPI instruments (Claude does not operate it).

## 6b. Status after the user's second set of answers (2026-10-12)

- **Q-03 resolved:** sample-to-detector 5–10 mm; mid-level rotary pump (specs to come); purge with N₂ first to remove free radon, then pump down. HV is not used on the vacuum side. Pump pressure still to be read from its spec or a gauge.
- **Q-05, Q-06 accepted** (R-09, R-14 proposals). Radon in air is the primary target; the module PCB is fixed for it, and weld testing is best-effort (D-21).
- **Q-07 resolved as "LLM best effort"** (no metric until much more data; D-17).
- **Q-11 answered from the datasheet:** specs are at 20 V and 40 V reverse bias; breakdown > 100 V; no recommended operating point; polarity not stated. Default 20 V (architecture §3). The user's recollection of "20 V as an option" matches.
- **Q-12, Q-14:** kV tube enclosed in an outer touch-safe enclosure, trained staff only, possible NC discharge interlock; HV divider feeds the PWM controller; fire-alarm-type standards suggested (D-20). Still `VERIFY`.
- **Q-20 resolved:** preamps on the atmosphere side, filled and capped ENIG vias, circular board, O-ring size from the mechanical design; fallback is a vacuum-rated bulkhead connector with both sides under separate vacuum.
- **Q-21 resolved:** Viton, with "consider lower-background materials in future revisions".
- **Q-22 resolved:** coupons about 15 × 30 mm; vacuum chamber is a 50 mm ID cylinder (R-46).
- **Q-23 resolved:** the electrometer is scripted over the user's API that cascades to ESP-NOW; it streams data as events arrive. Treated like the bench instruments (Claude does not operate it).
- **Q-15, Q-17 unknown yet.**
- **New open questions:** **Q-24** ring bias sign: Claude's view is slightly positive relative to the diode front (to be confirmed by simulation and the diode polarity). **Q-25 resolved (D-22):** 21–22 mm bore. **Q-26** how to attach the four chips (wire bond vs conductive epoxy, ask the diode manufacturer about carriers; architecture §3).
- **Electrometer questions (2026-10-13, §4.7 outline):** **Q-27** does the electrometer also source the test voltage (source-measure style), or is an external supply used with the electrometer as an ammeter at ground? **Q-28** 10 fA to 100 µA (R-58) accepted 2026-10-13; revisit if the relay count or physical size becomes a problem. **Q-29** is leakage at 1 kV (across the O-ring land and board edge nearest the tube) in scope? Claude's view: no, it needs a kV source and a different instrument, and the HV divider (D-20) already reads the tube. **Q-30** is capacitance mode in scope, or leakage only? **Q-31** how are boards contacted: pogo-pin fixture or probes, and how many boards per session (4 plus spares)? **Q-32** RH/T sensor choice and whether the enclosure is purged with dry N₂ or just holds desiccant. **Q-33** is the front-end powered from a battery inside the enclosure (swapping needs the lid opened, but it is quiet and isolated) or fed through the feedthrough from the outside part (filtered)? Claude's view: feed it through the feedthrough from a battery or linear supply outside, so the lid stays closed during runs. **Q-34** confirm reed relays on the input-node paths and EM latching or analog switches elsewhere (R-69), and the relay count of about 10. **Q-35** link connector: shielded RJ45 with a label, or a keyed connector such as M12? **Q-36** where in this project is a measurement above about 1 µA needed (diode forward current, bias-line faults, HV board load)? This sets whether 100 µA is worth its size. **Q-37** the SDM3055 manual: confirm the DCI accuracy and resolution on 200 µA, and whether the user wants outside calibration (R-72 item 6).

## 7. Notes on the answers

- **RH sensor on the detector board:** Claude recommends not putting one in the chamber. It is a ~15 cm³ volume, so a sensor body, its adsorbed water and any outgassing are large relative to it, it sits next to a 1 kV wall, and its I²C lines would be a noise path into the preamps. Use the outlet sensor during purge, as the user suggests.
- **Single-ended vs differential:** the held peaks are ground-referenced unipolar pulses, so four single-ended inputs are adequate. Differential helps for common-mode noise, which the layout and shielding should handle first.
- **Why the high-rate ADC may be unnecessary:** radon counts are ~1/hour in this chamber. Even a 2 ms conversion allows ~500/s. A fast path matters only for calibration with a strong source.

## 8. Verification coverage
Filled in at phase 4b (every `R-xx` mapped to S-xx, a `tests/NN-*` folder, or inspection).
