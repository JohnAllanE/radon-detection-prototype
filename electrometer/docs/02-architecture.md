# Architecture: electrometer front-end

**Status:** DRAFT 2, Phase 2 (architecture), 2026-10-20. Gate: the user approves the topology and block-level specs. Draft 2 records the user's answers to §8: topology and ranges approved, burden split, one source channel, Q-08 closed, coarse + fine DAC, two cells (D-05 to D-08). Items 3 and 6 are still open.
**Inputs:** requirements DRAFT 3 (`01-requirements.md`, confirmed by the user 2026-10-20, open questions carried here), decisions D-01 to D-04. Calculations: `sim/analytic/budget.py`, output in `sim/analytic/budget.out.txt`. Component classes only; parts are chosen in phase 3 (stock noted where it already matches).

## 1. Findings that change the plan

1. **The amplifier is not what limits 10 fA.** An ADA4530-1-class integrator resolves about 0.5–1 fA peak-to-peak in a 1 s integration, even with the 220 pF input capacitance of a zero-biased diode plus cables (budget §"Integrator current resolution"). The floor will be set by leakage, triboelectric charge, dielectric absorption and humidity. Effort goes into construction, cleaning, settling and the self-baseline (U-6), not into a better amplifier.
2. **Split rails are needed.** The ADA4530-1's input range runs from its negative rail to 1.5 V below its positive rail (ADA4530-1.pdf p3, p5), so a 0 V virtual ground needs a negative rail. Proposed ±5 V, which leaves a ±4 V usable output swing. That sets the ranges: **3.9 MΩ (1 µA full scale), 1 GΩ (4 nA full scale), and the 10 pF integrator (40 pC per ramp, up to about 4 nA)**.
3. **The mains frequency does not matter (Q-08).** Averaging or slope-fitting over multiples of 100 ms spans whole cycles of both 50 and 60 Hz, and a delta-sigma ADC with simultaneous 50/60 Hz rejection does the same for the resistor ranges.
4. **Self-test without a switch at the summing node.** A permanent 1 pF injection capacitor from a quiet DAC line replaces R-25's switchable reference capacitor and resistor. Held at 0 V it has no voltage across it and leaks nothing. Ramping its DAC line injects a known current (1 pF × 0.01–4 V/s = 10 fA to 4 pA), and a step injects a known charge (the power-up range check, D-03). This changes R-25 (§8).
5. **Burden at 1 µA.** Input protection needs a series resistor. 10 kΩ gives 40 µV burden at 4 nA but 10 mV at 1 µA. Proposed: burden ≤ 1 mV up to 4 nA and ≤ 10 mV on the 1 µA range. 10 mV is negligible against the node biases (20 V PD, ring). This changes R-01 (§8).
6. **The HV board must limit fault current.** A flashover from the tube to a diode node while the probe is on it can only be survived if the HV board's output has a series resistance. At 10 MΩ the fault current is 100 µA, easy to clamp. This is a new requirement on the radon HV board (§8).
7. **One source channel is enough (Q-03).** In the chamber, the real PD bias and ring supplies are used, selected by hand at the PicoBlade breakout (with a 0 V position for the femtoamp runs). The built-in source serves bench tests, bare boards and alternating-polarity resistance.
8. **Two cells (D-08).** Two 18650 cells in parallel give about 38 h with the source off and about 25 h with it on (budget §"Battery"; current draws `VERIFY`). That only just meets R-24 with the source on. The radio dominates.

## 2. System

The concept sketch is now the system diagram. Its values are updated to §3.1.

![Electrometer system, everything inside a grounded, light-tight cookie tin whose metal, the coax shields and the electrometer common are bonded to the detector board's 0 V at one point. Left, the chamber end: the chamber tube at +1 kV fed from the external HV board through an HV feedthrough with a lid interlock, and the detector board's back side. On channel 2 the probe is mated in the switched coaxial connector, so PD2's node goes to the probe and SMA coax while CSA2 idles at 0 V; channels 1, 3 and 4 stay on their CSAs. The PicoBlade carries PD bias, ring, TEST, ±4.5 V and GND; the ±50 V source drives the ring or PD bias through it, and a filtered pass-through brings in the MCU board and the HV board's PD bias. Middle, the electrometer head: input protection, then the guarded summing node on PTFE or in air, with a 1 pF injection capacitor from a quiet DAC. The feedback network between the summing node and the ADA4530-1-class op-amp output: a 3.9 MΩ branch (1 µA full scale) and a 1 GΩ branch (4 nA full scale), each switched by a manual T-switch on an off-board range panel (coax lines S, E1, E2), a 10 pF integrating capacitor that is always in, and an MCU-driven reset switch across it. Right, the control board: Vout to a 24-bit ADC, then the MCU, which auto-ranges by integration time, drives the reset, sets the source's level, polarity and slew, and reaches lab-gateway over ESP-NOW through an antenna outside the tin. Below, an inset shows a range branch switched off as a T-switch: Sa and Sb in series with their midpoint held at 0 V by Sc, so Sa has about 0 V across it; on the cheap panel Sa is an SPST and Sb/Sc an SPDT in separate bodies.](diagrams/switching-concept.svg)

![Power tree. A 1S2P Li-ion pack (two 18650 cells, 3.0 to 4.2 V) feeds a switch with fuse and cell protection, then three branches: a 3.3 V buck-boost for the digital rail (ESP32-S3, the ADC's digital side, the T/RH sensor); plus and minus 6.5 V converters at 1 MHz or above, shielded and far from the head, followed by plus and minus 5 V low-noise LDOs for the head (with local RC filters), the ADC and the DACs; and a plus and minus 60 V boost, switched on by the MCU only when the source is used, feeding the plus and minus 50 V source amplifier with its RC output filter and 100 µA limit. The charger connects only with the main switch off. Grounding notes: the analog common, the op-amp's + input, the guard, the coax shields, the head shield and the tin form one star point in the head; the digital ground joins it once at the ADC; the instrument floats on its battery and its only bond to the rest of the system is the probe shield at the detector board's 0 V; the boost and the radio are the noise sources, kept away from the head and shielded, with the boost off when unused and transmissions between integration windows.](diagrams/power-tree.svg)

Diagrams are generated by `diagrams/make_diagrams.py` (standard library; rerun `python3 electrometer/docs/diagrams/make_diagrams.py`).

## 3. Blocks

### 3.1 Head (the riskiest block)

A small board in its own non-ferrous shield box (aluminium), inside the tin, as close to the chamber end as the probe cable allows.

| Item | Spec (PROPOSED) | Class | Requirements |
|---|---|---|---|
| Input connector | SMA, PTFE insulation, shell to common | Panel SMA | R-11, R-31 |
| Input protection | 10 kΩ series resistor, then two low-leakage clamps from the summing node to common (about 0 V across them, so their leakage scales with Vos). Survives the HV board's fault current (≤ 100 µA at 1 kV through ≥ 10 MΩ, §8) | Thin-film R, rated for the pulse; low-leakage diodes or diode-connected JFETs (`VERIFY` leakage at mV) | R-10 |
| Summing node | Millimetres long: the op-amp's -IN pin, Cf, the reset switch, C_inj, the clamps and the S connector meet in air or on PTFE standoffs, inside a guard ring driven by the op-amp's guard pins (2, 7) | Construction | R-29, R-01 |
| Op-amp | ≤ 20 fA bias, guard buffer, ±5 V | Electrometer op-amp: ADA4530-1 (in the radon datasheets folder) | R-01 |
| Cf | 10 pF, always connected | C0G or PTFE/polystyrene; low dielectric absorption (`VERIFY` for 10 pF C0G) | R-01, R-02 |
| R1 | 3.9 MΩ, 1 µA full scale | Thin-film, ≤ 1 % | R-01, R-07 |
| R2 | 1 GΩ, 4 nA full scale | High-value glass or thick-film, low voltage coefficient; value calibrated (R-26), not trusted | R-01 |
| Range panel connectors | S, E1, E2: SMA, PTFE | Panel SMA | R-33 |
| Reset switch | T arrangement: Sa a reed relay with an electrostatically shielded coil (coil off while integrating), Sb/Sc a low-leakage analog SPDT; driven by the MCU | Reed relay + analog switch | R-01, R-02 |
| C_inj | 1 pF from a quiet DAC line, permanently connected; held at 0 V while measuring | C0G | R-25, R-26 (changed, §8) |
| Output to ADC | ±4 V scaled into the ADC's input range by a precision divider and buffer | Precision resistors, low-drift op-amp (OPA2186/OPA2192 in stock) | R-01 |
| Local supply filter | RC or LC per rail at the head | Passive | R-23 |

**Range plan** (budget §"Ranges"):

| Range | Covers | Offset before zeroing | Offset drift | Noise per 1 s reading |
|---|---|---|---|---|
| Integrator, 10 pF | 10 fA to about 4 nA (ramps of 10 ms or longer) | Zeroed against an open input | n/a | about 0.5–1 fA p-p (amplifier) |
| R2, 1 GΩ | about 4 pA to 4 nA, continuous | 40 fA max | 0.5 fA/K | 2.9 fA rms (thermal noise of R2) |
| R1, 3.9 MΩ | about 1 nA to 1 µA | 10 pA max | 0.13 pA/K | 46 fA rms |

**Stability:** with the worst-case 220 pF input, both resistor ranges have 87–90° of phase margin in a single-pole model (budget §"Loop stability"). Bandwidths are 4 kHz (R1) and 16 Hz (R2). S-01 checks this with the real model.

### 3.2 Range panel (off-board, D-03)

Cheap version first: per branch an SPST (Sa) and an SPDT (Sb/Sc), separate bodies, at any spacing, on a small metal panel at common. PTFE coax S, E1, E2 to the head, 30 cm or less (`VERIFY` against the capacitance in budget: 30 pF assumed). The power is off while ranges are changed. With no panel connected, the head runs integrate-only.

### 3.3 Readout and firmware measurement

| Item | Spec (PROPOSED) | Class | Requirements |
|---|---|---|---|
| ADC | 24-bit delta-sigma, ≥ 1 kSPS for slope fitting, a 20 SPS mode with simultaneous 50/60 Hz rejection; second channel reads the source output | 24-bit ΔΣ with mux (ADS1220 in stock, 8) | R-01, R-22 |
| Integrator readout | Sample Vout continuously; fit the slope over windows that are multiples of 100 ms; reset when \|Vout\| passes 3.5 V; discard a settle time after each reset; count resets for charge (R-02); flag overloads with a timestamp | Firmware | R-01, R-02, R-05, R-06 |
| Resistor-range readout | Average in the 20 SPS 50/60 Hz mode; zero against an open input at the start of a session | Firmware | R-01, R-07 |
| Power-up range check | C_inj step, decay time identifies the connected range (integrate: none; R2: 10 ms; R1: 40 µs) | Firmware | R-33 |
| Settling detection | Settled when the 60 s slope is below the noise floor | Firmware | R-13 |

### 3.4 Source (one channel)

| Item | Spec (PROPOSED) | Class | Requirements |
|---|---|---|---|
| DAC | Coarse + fine (D-07): both channels of the MCP4922, the fine channel attenuated so its full scale spans 4 coarse LSBs, summed at unity gain (MCP4922 datasheet §6.7, as on the microbalance). About 24 µV per step at the output; the firmware sets the coarse code, then trims the fine code against the readback, which makes the result monotonic and accurate despite the coarse DNL | MCP4922 (in stock) + low-noise reference (REF5040 in stock) + summing op-amp | R-08, R-21 |
| HV amplifier | ±50 V out from ±60 V rails, ≤ 1 mA quiescent, unity-gain stable, low 1/f noise | High-voltage op-amp, low power | R-08, R-24 |
| Output filter | Series R ≥ 100 kΩ then a film capacitor to common: limits current (≤ 100 µA at a short), sets the slew, and filters converter ripple | Passive | R-08, R-27 |
| Readback | Output sensed after the filter by a divider into the ADC | Precision divider | R-21 |
| ±60 V supply | Boost and inverter, enabled by the MCU only when the source is used | Small boost converter | R-24 |

Noise: the reference's 0.1–10 Hz noise times the amplifier's gain (about 20) is the main term and could reach the R-08 limit of 10 µV rms. The output RC only helps above its corner. This is S-02.

### 3.5 Control

| Item | Spec (PROPOSED) | Class | Requirements |
|---|---|---|---|
| MCU and radio | ESP32-S3 module with external-antenna connector, antenna on a bulkhead outside the tin | ESP32-S3-WROOM-1U (in stock, 1) | R-20, R-32 |
| Protocol | SCPI-style over ESP-NOW through lab-gateway; Keithley 6514/6517B names where they overlap | Firmware | R-20 |
| Radio scheduling | Transmit between integration windows | Firmware | R-23 |
| T/RH sensor | Digital, I²C, inside the tin away from the head | SHT4x class | R-17 |
| Reset driver | Reed coil driver, on only during a reset | Transistor | §3.1 |
| C_inj DAC | Drives C_inj: quiet, RC-filtered (which also smooths the 1 mV staircase into a ramp), held at 0 V while measuring. Its own part, since both MCP4922 channels go to the source | MCP4821 (in stock, 2), 12-bit, internal reference | R-25 |

### 3.6 Power and grounding

See the power-tree diagram. Two 18650 cells in parallel (D-08). They are charged externally, or by a charger that connects only with the main switch off, so nothing earths the instrument during a measurement. One star point in the head. The ±60 V boost and the radio are the noise sources: keep distance and shields, and turn the boost off when unused.

### 3.7 Tin and breakout

| Item | Spec (PROPOSED) | Requirements |
|---|---|---|
| PicoBlade breakout | Manual selectors: PD bias ∈ {HV board, source, 0 V}; ring ∈ {real ring supply, source, 0 V}; TEST ∈ {0 V, pulse generator}. Filtered pass-through in the tin wall | R-12, U-5 |
| HV feedthrough and interlock | HV board outside; lid switch disables the HV board and closes a bleeder to discharge the tube | R-09, R-28 |
| Gas, antenna | PTFE tubing through grommets; antenna bulkhead | R-15, R-32 |

## 4. Calculations

All in `sim/analytic/budget.py` (output `budget.out.txt`), with each input's source. What they don't capture:

- leakage of the real construction (PCB, PTFE, connectors, humidity);
- triboelectric and piezoelectric charge from handling;
- dielectric absorption of Cf and the board;
- reset-switch charge injection;
- converter and radio interference;
- the real op-amp model.

The cable capacitances, the zero-bias diode capacitance and all power draws are `VERIFY` assumptions.

## 5. Risks (simulate or measure first)

| # | Risk | Plan |
|---|---|---|
| 1 | Summing-node leakage and settling in the real construction | Build the head first and measure the self-baseline (U-6) before anything else |
| 2 | Murata SWF connector leakage and probe cable (Q-12) | Measure on the bare test board with the head (U-6); ask Murata for the approval sheet |
| 3 | Reset switch: charge injection, coil coupling, leakage | S-01 transient with a charge-injection estimate; bench test on the head |
| 4 | Source noise in 0.1–10 Hz (reference noise × gain) | S-02; choose a lower-noise reference or a higher output-filter time constant if needed |
| 5 | Converter and radio interference at the head | Layout distance and shields; boost off when unused; radio scheduling; measure radio on vs off (R-23) |
| 6 | Triboelectric settling after probe moves and range changes | Measure in U-6; sets the R-13 wait |
| 7 | Battery life with the source on (about 25 h on two cells, against 24 h) | Measure the real draws; a third parallel cell if needed (capacity only, same voltage) |

## 6. Simulations planned (phase 4)

- **S-01, head (SPICE):** loop stability on both resistor ranges with 100–220 pF input; integrator step and reset transient with an estimated reed-relay charge injection; the C_inj power-up range check. Verifies R-01 and R-33.
- **S-02, source (SPICE plus noise):** step response through the output filter; 0.1–10 Hz output noise from the reference, DAC and amplifier. Verifies R-08.
- **Analytic budget:** done (`budget.py`). Rerun when parts are chosen.

## 7. Candidate component classes (preview of phase 3)

| Block | Class | In stock |
|---|---|---|
| Electrometer op-amp | ≤ 20 fA, guard buffer | ADA4530-1 (datasheet pulled; not in stock) |
| ADC | 24-bit ΔΣ, 50/60 Hz rejection, ≥ 1 kSPS | ADS1220 (8) |
| MCU and radio | ESP32-S3, external antenna | ESP32-S3-WROOM-1U-N16R8 (1) |
| Reference | Low-noise 4.096 V | REF5040 (1) |
| DAC | Source: dual 12-bit as coarse + fine; C_inj: single 12-bit | MCP4922 (1), MCP4821 (2) |
| Buffers, divider driver | Low-drift precision op-amp | OPA2186 (8), OPA2192 (1) |
| HV op-amp, ±60 V boost, reed relay, analog SPDT, high-value resistor, T/RH sensor, switch connectors and probe | To select | No |

## 8. Questions and proposed requirement changes for the user

Answered 2026-10-20 (draft 2):

1. Topology and ranges: **approved** (±5 V rails; R1 3.9 MΩ, R2 1 GΩ, 10 pF integrator; T reset with a reed relay and an analog switch).
2. R-01 burden: **approved**, ≤ 1 mV up to 4 nA and ≤ 10 mV on the 1 µA range (D-05).
4. Q-03: **one source channel** (D-06).
5. Q-08: **closed**, not needed (D-06).
7. Source DAC: **MCP4922 as coarse + fine** (D-07). C_inj moves to an MCP4821.
8. Battery: **two 18650 cells** in parallel (D-08).

Still open (the user asked for clarification; answers given in conversation 2026-10-20):

3. **R-25 self-test:** replace the switchable reference capacitor and resistor with the permanent 1 pF C_inj (§1.4), and check the resistor ranges with an external "cal plug" on the probe. Why not a resistor fixed to the summing node: it adds its thermal noise current all the time (4 fA/√Hz at 1 GΩ, 0.4 fA/√Hz at 100 GΩ), and a source that is 10 mV off at "0 V" drives 10 pA (1 GΩ) or 100 fA (100 GΩ) into the node; disconnecting it needs a switch at the summing node, which this design avoids. C_inj has neither problem (budget §"cal plug").
6. **Radon HV-board requirement:** output series resistance ≥ 10 MΩ at the +1 kV output (`VERIFY` against the HV board's design), so that a tube flashover cannot draw more than about 100 µA from the multiplier's stored charge. No change to the detector board. It also protects the CSAs in service. The alternative, 10 MΩ at the electrometer input, gives 10 V burden at 1 µA and 40 mV at 4 nA (§1.5).
