# Requirements: electrometer front-end (test equipment)

**Status:** DRAFT 3, Phase 1 (requirements), 2026-10-20. **Confirmed by the user 2026-10-20** (phase-1 gate); the open questions in §7 are carried into phase 2 (`02-architecture.md` §8). Draft 2 made DC current the primary function (D-01). Draft 3 makes the in-chamber test in a grounded tin the primary validation, replaces the switching matrix with one probe cable moved between per-channel switch connectors, and sets the grounding scheme (D-02).
**Parent:** radon detection prototype, `docs/01-requirements.md` §4.7 (radon R-48 to R-50). This board lives here until it is built, then moves to `electronics-tools/bench-test-gear/` (radon R-50), so this folder is self-contained.
**IDs:** `R-xx`, `Q-xx`, `U-xx` and `D-xx` in this folder are local to the electrometer. Requirements of the radon project are always written as "radon R-xx".
**Legend:** `VERIFY` means not yet checked against a source. `PROPOSED` means Claude's suggestion for the user to accept or change. `TBD (Q-xx)` depends on an open question in §7.

## 1. Purpose

Measure the small DC currents on the detector (CSA) boards that the bench gear cannot reach, so that parasitic leakage can be separated from the photodiode signal. It complements the bench DMM: a small overlap with the DMM's lowest current range, then down to 10 fA (D-01). The DMM's lowest current range is 200 µA with about 1 nA resolution (SDM3055, `instruments.json`), and the PSU reads back to 1 µA. Nothing on the bench resolves below 1 nA, and the photodiode's own dark current is only 0.15 nA typical. Capacitance is mainly left to the bench gear (§2). Charge and capacitance are an optional mode here, kept only if they come almost free with the current topology (R-02, R-03).

The board is biased by sources that the project itself applies, and each can push current or charge into the CSA input node:

| Source | Level | Path into the input node |
|---|---|---|
| Photodiode reverse bias | 20 V default, 40 V option (VTH2110.json p1) | Diode dark current (the wanted baseline), and board surface leakage from the bias net |
| Ring bias on the exposed ENIG around the diodes (radon R-47) | Slightly positive, value from field simulation | Surface leakage across the top face; capacitive coupling of ring noise |
| Chamber wall | About +1 kV, ~2.1–2.6 mm from the die corners (radon R-39) | Surface and bulk leakage from the O-ring land; capacitive coupling of HV ripple (radon R-19); micro-discharges |
| Radon-progeny ions steered onto the diodes | Function of the field | Ionisation current in the gas (estimated in §3, it is tiny) |

What "working" means: for each of these paths, the electrometer can say how much DC current reaches the input node, with enough resolution to show that it is small compared with the dark current, or to show that it isn't. Capacitive coupling of noise (ripple, ring bias) is measured mostly with the bench gear (§2).

**How it is tested (D-02).** The real thing is the only meaningful test of the 1 kV paths: a built Part 1 chamber with its detector board(s) attached, the electrometer beside it, all inside a grounded metal enclosure (a "cookie tin") that is also the shield and the dark box. The HV board stays outside and feeds the tube through an HV feedthrough. Each CSA input has a switched coaxial test connector on the back of the board; one probe cable is moved between them by hand with the tin open and HV off. The bench version of the same arrangement, with a dedicated sacrificial board, is used to find causes.

## 2. Use cases

| ID | Use case | DUT state | Main measurements |
|---|---|---|---|
| U-5 | **Primary validation: in-chamber parasitics, in the tin.** Board on a built Part 1 chamber, walls at +1 kV from the real HV board, ring bias on, air vs N₂, pump on vs off (radon R-41). Current into each input node, PD bias at 0 V for the fA runs (§3), PD bias on for the in-service picture; charge steps from micro-discharges | Populated board, mounted on the chamber; probe on one channel's switch connector (R-19) | DC current vs condition, charge steps |
| U-1 | **Bare-board leakage map** on a dedicated test board with the same footprints (R-19). Input node against guard, ring, PD bias, TEST, ground at 10–50 V; the O-ring land at 1 kV, either on the chamber or with a metal ring pressed on it as a tube stand-in | Bare PCB, cleaned; sacrificial, so wires may also be soldered to it | I(t) after a step, R by alternating polarity |
| U-2 | *Optional (D-01).* **Bare-board capacitance matrix.** Coupling between the input node and every other node, especially Cf stray, ring → input, O-ring land (tube) → input. On populated boards the bench-gear method in §2 does this instead | Bare test board | Guarded cross-capacitance, fF |
| U-3 | **Populated board before service.** Input-node leakage per channel with the CSA, Cf, Rf and Ctest fitted. *Optional:* each channel's Ctest measured, so the charge-injection calibration (radon R-49) uses a measured value rather than the ±0.25 pF tolerance of a 1 pF part. One or two mating cycles per connector, no soldering (R-19) | Populated, cleaned, in the tin | Leakage; optionally capacitance |
| U-4 | **Photodiode dark current** vs bias (0–40 V) and temperature, on the board, in the dark | Diodes fitted, probe on the channel | I–V, I–T |
| U-6 | **Self-baseline.** Probe unmated and parked, tin closed, cables flexed, radio on vs off; probe on an unpopulated connector footprint of the test board | No DUT | Noise floor, triboelectric pickup, offsets, connector leakage |

**Concept sketch (for discussion; topology is decided in phase 2).** Diagrams are SVGs generated by `diagrams/make_diagrams.py` (standard library only; edit it and rerun `python3 electrometer/docs/diagrams/make_diagrams.py`).

![Electrometer concept, everything inside a grounded, light-tight cookie tin whose metal, the coax shields and the electrometer common are bonded to the detector board's 0 V at one point. Left, the chamber end: the chamber tube at +1 kV, fed from the external HV board outside the tin through an HV feedthrough with a lid interlock, and the detector board (20 mm or less), back side shown. On channel 2, photodiode PD2's node goes into a switched coaxial connector (Murata SWF type); with the probe mated, the node goes to the probe and SMA coax, and CSA2, now disconnected, idles at 0 V. Channels 1, 3 and 4 have their connectors unmated, so each node stays on its CSA. The PicoBlade connector carries PD bias, ring, TEST, ±4.5 V and GND; the electrometer's ±50 V source drives the ring (or PD bias) through it, and a filtered pass-through in the tin wall brings in the MCU board and the PD bias. Middle, the electrometer head: input protection, then the summing node, which is millimetres long, on PTFE or in air, and guarded. The feedback network sits between the summing node and the op-amp output (ADA4530-1 candidate, non-inverting input at 0 V guard): a 10 MΩ branch (1 µA full scale) and a 1 GΩ branch (10 nA full scale), each switched by a manual T-switch on an off-board range panel (coax lines S, E1, E2), set by the operator as the script instructs; a 10 pF integrating capacitor that is always in; and a reset switch across it driven by the MCU. Right, the control board: Vout goes to a 24-bit ADC and then the MCU, which auto-ranges by integration time, drives the reset, sets the source's level, polarity and slew, and reaches lab-gateway over ESP-NOW through an antenna mounted outside the tin. Below the tin, an inset shows one range branch switched off as a T-switch: two series switches Sa and Sb between the summing node and the element, with Sc tying their midpoint to 0 V, so Sa has about 0 V across it and leaks nothing into the input while Sb's leakage goes to 0 V through Sc. On the cheap panel, Sa is an SPST and Sb/Sc an SPDT in separate bodies (one DPDT would put Vout next to the summing node inside one body); a later rotary panel does the same with separate wafers. The reset switch needs the same arrangement.](diagrams/switching-concept.svg)

**Measurement procedure, in outline.** HV off and discharged (interlock) → open the tin → move the probe to the next switch connector → close the tin, re-purge if the run needs dry gas → script waits for settling (R-13) → HV and biases on → measure. The script asks the operator which channel the probe is on and logs it (R-21).

**Grounding and shielding (R-31).**

| Point | Connects to |
|---|---|
| Probe/coax centre conductor | The CSA input node through the switch connector; held at virtual ground by the electrometer |
| Coax shield, electrometer end | Electrometer analog common (0 V): the op-amp's + input, the head's shield box, the source's reference |
| Coax shield, board end | The switch connector's shell, soldered to the detector board's 0 V guard ring around the input node (same net as GND and the CSA's + input) |
| The tin | Electrometer common, bonded once |
| Single bond point | Electrometer common meets the rest of the system **only** at the detector board's 0 V, through the coax shield. The detector board's GND also reaches mains earth through the MCU board, USB and the PC, so the electrometer must float (battery, ESP-NOW; R-24) or there is a ground loop, and its millivolts appear between the guard and the input |
| HV return | The HV board's own wiring, never a coax shield |

No separate driven guard is needed: the measured node sits at virtual ground (burden ≤ 1 mV), so the common is the guard potential and the coax shield is the guard up to the connector.

**Already possible with the bench gear (to avoid over-building):** on a populated, powered board the CSA is itself a transimpedance amplifier for DC, with Rf = 100 MΩ (radon `docs/02-architecture.md` §3). A leakage current I shifts the CSA output by I × 100 MΩ, so 1 pA gives 100 µV, which the SDM3055 resolves on its 200 mV range. Reading the output with HV on and off cancels the op-amp offset, so in-situ leakage down to roughly 1 pA is measurable today (`VERIFY`: limited by the CSA op-amp's offset drift and Rf tolerance). The electrometer is needed for everything below that, and for bare boards.

**Capacitance with the bench gear:**

- *Two-terminal values from about 100 pF up* (diode junction, decoupling, cables): the SDM3055 capacitance function. Its lowest range is 2 nF with about 1 pF resolution (`VERIFY` against the SDM3055 datasheet; `instruments.json` only lists "capacitance"). It cannot guard, so it reads everything between its two leads, including lead capacitance and each node's path to ground in series.
- *fF coupling into an input node on a populated, powered board:* the CSA is a charge amplifier, so step the suspect node (ring, PD bias, tube) with the SDG2122X and read the output step on the scope: C_x = Cf × ΔV_out / ΔV_step. Doing the same through the test-charge input gives C_x / Ctest directly, so Cf cancels, but the absolute value is only as good as Ctest's tolerance (±25 % for a 1 pF ±0.25 pF part, adequate for setting a ripple limit). This is the measurement behind radon R-19.
- *Not covered by the bench gear:* fF coupling on a **bare** board (U-2), and an absolute Ctest value (U-3). These are the only reasons to keep R-02 and R-03.

## 3. Expected magnitudes (what the instrument has to resolve)

These set the ranges in §4. The arithmetic is shown so it can be checked; inputs marked `VERIFY` are textbook or recalled values.

**Reference levels at the input node**

- Photodiode dark current: 0.15 nA typical, 2 nA max at 20 V; 5 nA max at 40 V (VTH2110.json p1, p3).
- CSA op-amp input bias: OPA140 0.5 pA typical (parts/selection.md); LMP7721 3 fA; ADA4530-1 20 fA max (ADA4530-1.json p1).
- Charge scale: a 6 MeV alpha gives about 270 fC (requirements §3), so **1 fC ≈ 22 keV**. The resolution target is 100 keV FWHM (radon R-09).

**Parasitic paths**

| Effect | Estimate | Consequence for the instrument |
|---|---|---|
| **Dark current drift masks fA parasitics when the diode is biased** | Dark current roughly doubles every ~8 °C (`VERIFY`), i.e. about 9 %/K: at 150 pA that is **13 pA per kelvin**. Resolving 10 fA on top of it needs about 1 mK of temperature stability | fA runs on a populated board use **PD bias at 0 V** (no dark current; the diode is then just a capacitance and a shunt resistance at 0 V across it), then ring bias and HV are applied one at a time. With PD bias on, read differences (HV on vs off) at the pA level, with temperature logged (U-5) |
| Surface leakage, 20 V across a 0.25 mm × 20 mm gap | R = ρs × 0.25/20. For ρs = 10¹⁵ down to 10¹² Ω/□ (`VERIFY`: clean vs humid or contaminated FR-4): R = 1.25×10¹³ to 1.25×10¹⁰ Ω, so **1.6 pA to 1.6 nA** | Range spans fA to nA; it depends on cleaning and RH, which is why it is measured rather than computed |
| Surface leakage, 1 kV across a 2 mm × 70 mm path (O-ring land around a 22 mm bore) | 0.029 □: **35 pA (10¹⁵ Ω/□) to 35 nA (10¹² Ω/□)** | Most of it should land on a guard or ground, not on the input. The residual into the input node is the number that matters (U-1, U-5) |
| HV ripple coupled through C(tube → input) | Charge per ripple swing = C × ΔV. Example: 50 fF × 0.1 V = 5 fC ≈ **110 keV**, already above the resolution target | **The HV ripple limit (radon R-19) cannot be set without this capacitance.** On populated boards it is measured with the siggen, scope and CSA (§2); on bare boards only with R-03 |
| Ring-bias noise through C(ring → input) | Same arithmetic. For a 10 keV contribution, C × V_noise ≤ 0.45 fC, e.g. ≤ 1 mV in the shaper band if C = 0.45 pF | Same: measure C(ring → input) |
| Ionisation of the chamber gas | Radon at 100 Bq/m³ in 26 cm³: 2.6 mBq × up to 3 alphas × 1.6×10⁵ pairs (5.5 MeV / 34 eV per pair, `VERIFY`) × 1.6×10⁻¹⁹ C = **0.2 fA**; mine air (×100): 20 fA. Background gamma/cosmic ionisation of ~10 pairs/cm³/s (`VERIFY`): 0.04 fA | Negligible at ambient. **Exception:** an alpha check source in the gas (e.g. 37 kBq Am-241, half the alphas into the gas) gives about 0.5 nA of ion current, which the +1 kV field distributes over the diodes, ring and wall |
| Stray light on a bare diode | Responsivity 0.74 A/W peak (VTH2110.json p3): **1 fW gives 0.7 fA**, 1 nW gives 0.7 nA | The tin must be light-tight with no indicator LEDs inside. FR-4 passes some light, so the board's back side counts |
| Dielectric absorption after a voltage step | Soak currents that decay over seconds to hours and can exceed the steady leakage by orders of magnitude (`VERIFY` for FR-4) | Time-stamped I(t) logging and an alternating-polarity method |
| Cable motion and vibration (triboelectric) | pA for ordinary coax, tens of fA for low-noise cable (`VERIFY`) | Probe cable fixed inside the tin; the pump-on case (radon R-41) is itself a measurement |
| Micro-discharges at 1 kV | Charge bursts from fC upward; look like events to the CSA | Optional step detection in charge mode (R-06) |

## 4. Requirements

Verification: **S** = simulation, **T** = test, **I** = inspection.

### 4.1 Measurement functions

| ID | Statement | Target | Verify |
|---|---|---|---|
| R-01 | DC current, with the measured node held at virtual ground (as the CSA input is). **The primary function (D-01)** | ±1 µA full scale (overlap, R-07) down to **10 fA (user target)**. PROPOSED to meet it: noise ≤ 10 fA p-p over 60 s at 1 s per reading on the lowest range; burden ≤ 1 mV up to 4 nA and ≤ 10 mV on the 1 µA range (D-05); accuracy ±2 % of reading above 1 pA after zeroing | T |
| R-02 | *Optional (D-01, D-04):* charge, as a firmware mode on the 10 pF integrator. Slowly arriving charge is counted through resets (each reset dumps a known charge), so its range is not limited by the capacitor; a charge arriving faster than a reset (above about 100 pC at once) is logged as an overload, not measured | PROPOSED: 1 fC resolution over a 1 s window; overloads timestamped | T |
| R-03 | *Optional (D-01), needs R-02:* capacitance by charge transfer with small steps (about ±1 V; 33 pF × 1 V = 33 pC fits the 10 pF integrator), guarded cross-capacitance between a source node and the measured node with all other nodes held at 0 V. For bare boards (U-2) and absolute Ctest (U-3) | PROPOSED: 1 fF to 100 pF at a 1 V step (charge ≤ 100 pC; larger C needs a proportionally smaller step); resolution 1 fF; accuracy ±(1 % + 2 fF) | T |
| R-04 | Resistance from V/I, including the alternating-polarity method to reject soak currents and offsets | PROPOSED: up to 10¹⁵ Ω at 50 V (50 fA), ±10 % | T |
| R-05 | Time-stamped I(t) and Q(t) logging after a source step, for soak and settling studies | 10 ms to 24 h per run | T |
| R-06 | Optional: in charge mode, detect and time-stamp charge steps (micro-discharges) | PROPOSED: steps ≥ 50 fC (≈ 1.1 MeV equivalent), 1 ms timing | T |
| R-07 | Range overlap with the bench DMM for cross-checks | 100 nA to 1 µA read by both. The SDM3055 200 µA range resolves 1 nA, so below 100 nA it has fewer than 100 counts and is not a useful reference (`VERIFY` its low-range accuracy) | T |

### 4.2 Sources

| ID | Statement | Target | Verify |
|---|---|---|---|
| R-08 | Built-in bipolar programmable voltage source for bias, steps and alternating polarity. In the chamber it drives the ring (or PD bias) through the PicoBlade breakout | PROPOSED: ±50 V, 10 mV steps, current limit ≤ 100 µA, noise ≤ 10 µV rms in 0.1–10 Hz (100 pF × 10 µV at 1 Hz moves only 6 fA), controlled slew so a step does not overload the input. One channel (D-06): in the chamber the real PD bias and ring supplies are selected at the breakout | S, T |
| R-09 | External HV: the project HV board, outside the tin, feeds the chamber tube through an HV feedthrough in the tin wall. For bench tests of the bare board, a metal ring pressed on the O-ring land stands in for the tube. HV never passes through the electrometer | ≤ 1.1 kV; supply choice Q-04 | I |
| R-10 | Input protection: the input survives a flashover from the 1 kV tube to a diode node while the probe is on it, and a mis-routed ±50 V, without lasting change in leakage or offset | Survives; the zero and noise floor (R-01) re-checked after a deliberate test (`VERIFY` the energy available from the HV board's output capacitance) | S, T |

### 4.3 Connection to the DUT (D-02)

| ID | Statement | Target | Verify |
|---|---|---|---|
| R-11 | Node selection by hand: **one probe cable**, a Murata SWF-series probe with an SMA end (e.g. MXHS83QE3000, 300 mm, or MXHS83QE1000, 100 mm), moved between the per-channel switch connectors (R-19) with the tin open and HV off. No switching matrix | 4 input nodes per board; the script records which one (R-21) | I, T |
| R-12 | No node floats during a measurement. Unmated connectors leave each input node on its CSA; PD bias, ring, TEST and GND come through the PicoBlade breakout from the real supplies or the source (R-08); TEST is held at 0 V for DC measurements | Checked in the test plan for each configuration | I |
| R-13 | Settling after the probe is moved or a source is stepped: the script waits until the reading has settled and logs the wait, rather than using a fixed delay. Opening the tin changes the RH; a dry-gas run re-purges first | PROPOSED: settled when the 60 s slope is below the R-01 noise floor; longer settling is a DUT soak effect and is logged, not hidden | T |
| R-14 | The probe cable is tied down and strain-relieved inside the tin. Murata warns that cable stress on a mated probe can unmate it, damage the connector or peel its electrodes off the board ([Murata SWF](https://www.murata.com/en-global/products/connector/switchconnector/overview/lineup/swf)) | Triboelectric pickup from normal handling ≤ 50 fA (U-6) | I, T |
| R-31 | Grounding and shielding as in the §2 table: coax shield = electrometer common = guard; single bond to the detector board's 0 V at the connector shell; tin bonded to common; electrometer floats; HV return separate | n/a | I, T |

### 4.4 Enclosure and environment

| ID | Statement | Target | Verify |
|---|---|---|---|
| R-15 | **The tin:** a grounded metal enclosure holding the built chamber, its detector board(s), the electrometer head and control board. Pass-throughs: HV feedthrough (R-09), PTFE gas lines through grommets (pump outside), filtered pass-through for the PicoBlade lines to the MCU board and HV board, antenna bulkhead (R-32). The tube sits on insulating standoffs; the back of the detector board is reachable with the probe while the chamber is assembled | Tube to tin clearance PROPOSED ≥ 10 mm (`VERIFY` against the clearance rule chosen for radon Q-12) | I |
| R-16 | Darkness | Stray light ≤ 1 fW on a diode (≤ 1 fA, §3). Check: diode at 20 V, tin closed, room lights on vs off, difference within the noise floor | T |
| R-17 | Temperature and RH inside the tin logged with every reading. Temperature matters most when PD bias is on (§3) | PROPOSED: ±0.5 °C accuracy, 0.01 °C resolution; ±3 % RH | I, T |
| R-18 | Optional dry-N₂ purge of the tin itself (the chamber already has its own N₂ supply, radon D-05), to separate humidity-driven surface leakage on the board's back | Inlet and outlet | I |
| R-19 | **Requirement on the detector board (feeds radon R-60):** each CSA input node has a non-destructive, guarded test port on the back side: a Murata SWF-type switched coaxial connector in series between the diode node and the CSA input. Unmated, it connects diode to CSA; with the probe in, it routes the diode node to the probe and disconnects the CSA. Its shell is soldered to the 0 V guard ring around the input node. Ctest sits on the diode side, so the electrometer can measure it. No soldering on an input node after the board is cleaned. The dedicated bare-board test board uses the same footprints | SWF: 2.5 × 2.5 × 1.4 mm, rated 100 mating cycles with a Murata probe, 30 Vrms ([Murata SWF](https://www.murata.com/en-global/products/connector/switchconnector/overview/lineup/swf)). Service boards see 1–2 cycles per connector. Leakage not published (Q-12) | I, T |

The open switch contact sits between the diode node (held at virtual ground by the electrometer) and the CSA input (idling at 0 V), so it has about 0 V across it, and the connector body likewise has about 0 V from centre to shell in service and under test. Its leakage should therefore be small whatever the plastic; U-6 measures it. With its diode disconnected, the measured channel's CSA becomes a follower of its 0 V input through Rf, so the other channels can keep running, **provided** the CSA op-amp is stable at a noise gain of 1. OPA140 and OPA656 are unity-gain stable; a decompensated part such as OPA657 relies on the diode capacitance and may oscillate (`VERIFY` for the chosen parts; otherwise turn the rails off while measuring).

### 4.5 Control, data and power

| ID | Statement | Target | Verify |
|---|---|---|---|
| R-20 | Control by SCPI-style text over ESP-NOW through `lab-gateway`, scripted from the user's API (radon Q-23). Streams readings as they are taken | PROPOSED: command names follow the Keithley 6514/6517B where they overlap, as the load-cell reader follows the SDM3055 | T |
| R-21 | Each record carries: timestamp, function, range, value, source level, probed channel and board (entered by the operator), range setting as instructed and confirmed (R-33), PD bias and ring state, T, RH, and flags (overload, range change, settling, HV present) | n/a | I |
| R-22 | Reading rate | PROPOSED: 1–10 readings/s with integration over whole mains cycles (Q-08); up to 1 kS/s in charge-step mode (R-06) | T |
| R-23 | Radio and digital activity do not disturb readings | Radio on vs off differs by less than the R-01 noise floor; transmissions scheduled between integration windows if needed | T |
| R-24 | Power: battery, so the electrometer floats and the only bond to the rest of the system is the coax shield (R-31) | Resolved (D-02). Battery life PROPOSED ≥ 24 h of logging (R-05); two 18650 cells in parallel, about 25 h with the source on (D-08) | I, T |
| R-32 | The tin blocks 2.4 GHz, so the radio antenna is outside it: an ESP32 module with an external-antenna connector and a bulkhead antenna, or the control board outside with a shielded cable to the head (Q-14) | ESP-NOW link holds with the tin closed | T |

### 4.6 Calibration and self-test

| ID | Statement | Target | Verify |
|---|---|---|---|
| R-25 | Built-in checks: input zero (open), a switchable reference capacitor and a reference high-value resistor, to check each range before a session | Pass/fail against stored values | T |
| R-26 | Calibration traceable to the bench gear: current from a ramp into a known capacitor (SDG2122X ramp, I = C·dV/dt; e.g. 1 V/s into 10 pF gives 10 pA), source voltage against the SDM3055, overlap per R-07. Constants stored on the instrument | Procedure in the test plan (phase 4b). The reference capacitor's value is the accuracy limit (`VERIFY` part tolerance) | T |

### 4.7 Safety and build

| ID | Statement | Target | Verify |
|---|---|---|---|
| R-27 | The built-in source stays in the SELV range and is current-limited | ≤ 60 V DC (`VERIFY` limit against IEC 61010-1), ≤ 100 µA | I, T |
| R-28 | HV at the tin: lid interlock that disables and discharges the external HV when the tin opens; HV-present indication outside; HV off and discharged before the probe is moved. Follows the project's HV rules (radon R-22, D-20) | Interlock design in phase 2 | I, T |
| R-33 | Range selection on an **off-board panel** (D-03): feedback resistors and the 10 pF integrator stay on the head board; the panel holds the T-switches and connects by PTFE coax lines S (summing node), E1, E2 (resistor free ends), shields at 0 V. The same interface takes a cheap panel (SPST + SPDT per branch, separate bodies) or a rotary panel later; with no panel the head runs integrate-only. Ranges are changed with the power off. **No position sensing:** the script tells the operator the setting and the operator confirms it before power-on. Optional firmware check at power-up: a reference-capacitor charge step whose decay identifies the connected range (R-25) | Script prompt and confirmation logged with each run; S coax ≤ 30 cm PROPOSED (`VERIFY` against the phase-2 capacitance budget) | I, T |
| R-29 | Build: hand-assembled; the input node on PTFE standoffs or in air, guarded; board washed after assembly; the premium electrometer op-amp is the ADA4530-1 candidate already pulled (parts/selection.md; part choice confirmed in phase 3) | 2 or 4 layers | I |
| R-30 | Portable to the test-gear repo: no dependency on radon-project paths except this use-case document | n/a | I |

## 5. Out of scope

- AC impedance (LCR), pulse-height spectroscopy (the MCU board does that), and pulse-gain calibration of the CSA (pulse generator and scope; the electrometer only supplies the measured Ctest).
- Generating HV. The 1 kV comes from outside (R-09).
- A switching matrix (dropped in D-02): nodes are selected by moving the probe.
- Currents above 1 µA (use the DMM) and metrology-grade absolute accuracy. The radon project needs comparisons between nodes, boards and conditions more than absolute numbers.
- The radon chamber's ion current as a radon measurement: at 0.2 fA it is far below the alpha-counting method (§3).

## 6. Assumptions

- `PCB-WORKFLOW.md` applies, including the instrument rules: Claude writes scripts, shows them, and the user runs them (radon Q-23).
- Lab ambient; RH not controlled unless a purge (R-18) is used.
- One electrometer and one probe cable are built or bought. Detector boards go into service after one or two test cycles per connector.

## 7. Open questions

- **Q-01** Resolved (2026-10-20, D-02): U-5 in the tin is the primary validation; the bench test diagnoses.
- **Q-02** Resolved (2026-10-20, D-01): target 10 fA. Consequence: PTFE or in-air input node, guarded range switching, careful cleaning.
- **Q-03** (Resolved, D-06: one channel.) Built-in source: one ±50 V channel, or two (PD bias and ring bias at the same time)? Or use the HV board's regulated PD bias for the second?
- **Q-04** 1 kV: the project HV board (fixed output), or also an adjustable lab HV supply and an HV probe for leakage vs voltage curves?
- **Q-05** Resolved (2026-10-20, D-02): Murata SWF switch connectors per input, one probe cable.
- **Q-06** Resolved (2026-10-20, D-02): no matrix; four inputs per board via the probe; other nets through the PicoBlade.
- **Q-07** Resolved (2026-10-20, D-02): battery.
- **Q-08** (Closed, D-06: not needed; integration over multiples of 100 ms rejects both.) Mains frequency in the lab (50 or 60 Hz).
- **Q-09** Budget for the premium parts: ADA4530-1 (one; your earlier note says it is very expensive), the Murata probe (price not checked), SWF receptacles (low cost per the user).
- **Q-10** Typical lab RH, and whether a tin purge (R-18) is wanted.
- **Q-11** Resolved (2026-10-20, D-04): no 1 nF charge range. Charge and capacitance stay optional firmware modes on the 10 pF integrator (reset counting for slow charge, steps of about ±1 V for capacitance); a large fast charge is logged as a timestamped overload.
- **Q-12** Murata SWF leakage and probe life: neither the receptacle's insulation resistance nor the probe's own cycle life is published; only the receptacle's 100 cycles with a probe. Ask Murata for the approval sheet, and measure the connector on the test board (U-6) before relying on it at 10 fA.
- **Q-13** Space and access: four 2.5 × 2.5 mm SWF connectors with guard rings, plus the CSAs, on the back of a ≤ 20 mm board; and room for the probe with the chamber assembled in the tin.
- **Q-14** Radio: ESP32 module with an external antenna on a bulkhead (PROPOSED), or the control board outside the tin?
- **Q-15** Detector board: is the O-ring land copper or bare laminate? Is a 0 V ring just inside it wanted, to catch surface leakage from the tube? It changes the field near the diodes, so the field simulation decides.

## 8. Verification coverage

Filled in at phase 4b.
