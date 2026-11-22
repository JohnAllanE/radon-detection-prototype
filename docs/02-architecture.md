# Radon detection prototype: architecture

| | |
|---|---|
| Project | Alpha detection with silicon photodiodes: radon progeny in air (Part 1) and weld samples in rough vacuum (Part 2), comparing a premium and a low-cost detector board |
| This document | How the detector board, MCU board, HV board and chambers are built, and what they should do. `VERIFY` marks an unconfirmed fact. Simulated: the chamber field (S-01) |
| State | Accepted by the user while the requirements hold. Claude's choices working until simulated or tested |
| Open questions | 6 |

## IDs from other documents

- Functions: R-01 Part 1 radon progeny, R-03 Part 2 weld samples, R-13 per-channel hold, R-15 reports to the host, R-18 about +1 kV, R-20 PD bias, R-47 ion-steering ring, R-49 populated-board tests, R-60 test port.
- Objectives: R-53 similar readings, R-09 resolution (100 keV), R-14 event rate (100 events/s), R-52 drift, R-73 build effort.
- Constraints: R-06 four diodes, R-10 low-cost footprint, R-74 cost per channel, R-28 no BGA, R-22 no touchable HV, R-24 board-to-board connector, R-25 wall adapters, R-39 21–22 mm bore, R-43 no HV below ambient, R-54 board is the seal, R-55 two layers.
- Electrometer IDs are written "electrometer R-xx".

## Block diagram

![System block diagram. Two detector boards per chamber (four photodiodes and four CSAs each) cable to the MCU board, which shapes, holds, digitises and reports to the host over USB and supplies ±4.5 V. The HV board, from a 48 V adapter, supplies about +1 kV to the Part 1 walls and the photodiode bias. A 5 V adapter powers the MCU board.](diagrams/system-block.svg)

![Per-channel signal chain. Photodiode, CSA with test charge and filtered bias, then over the PicoBlade to the MCU board: pole-zero and gain, shaper, comparator interrupting the ESP32-S3, and peak detector with reset and hold buffer. The hold goes to the ADS1220 directly and through a 4:1 mux to the ADS8689 or the ESP32-S3 ADC.](diagrams/signal-chain.svg)

## Choices

| ID | Choice | Status | Serves | Why |
|---|---|---|---|---|
| A-01 | Detector board: circular two-layer PCB, the pressure boundary. Diodes on the chamber side, CSAs and connector on the atmosphere side, signals through filled, capped ENIG vias | firm | R-54, R-55, R-40 | The user's answer to Q-20. [Detector board](notes/detector-board.md) |
| A-02 | Four Excelitas VTH2110 chips, 2×2, 0.5 mm gaps | firm | R-06 | The user's part. [Survey](notes/candidates-photodiode.md) |
| A-03 | Chip mounting: conductive-epoxy die attach plus a wire to the 0.4 mm top pad, bonded or epoxied | open | R-06 | Electrode polarity unknown (Q-11). Q-26 |
| A-04 | PD bias 20 V from the HV board, a per-board RC filter, a resistor per diode | working | R-20, R-09 | Specified at 20 V. Fully depleted for alphas |
| A-05 | CSA: + input at 0 V, ±4.5 V rails, $C_f$ = 1 pF C0G with $R_f$ = 100 MΩ, output series R | working | R-09, R-13 | 44.3 mV/MeV. [Signal levels](notes/signal-levels.md) |
| A-06 | Low-cost CSA op-amp: OPA140 on a standard SOIC-8 with pins 1, 5, 8 unconnected | working | R-10, R-09 | 6.9–7.4 keV at 4 µs. [Survey](notes/candidates-csa-opamp.md) |
| A-07 | Premium CSA op-amp: LMP7721, guard on its NC pins, own footprint | working | R-10, R-53, R-74 | Awaits the user (D-18). Leakage control, not noise. Over R-74: 1–2 channels only |
| A-08 | Test charge: about 1 pF C0G per channel from a common TEST line | working | R-49 | Gain calibration is mandatory: stray makes the nominal gain wrong |
| A-09 | Test port: Murata SWF switched coax per CSA input on the back, shell on the 0 V guard ring, $C_{test}$ on the diode side | firm | R-60 | Electrometer D-02. Stable-at-unity CSA needed |
| A-10 | Ion-steering ring: exposed ENIG out to about 9.6 mm radius, on the filtered +20 V PD bias. No sloped electrode | working | R-47 | S-01: 95–99 % of ions reach the dies unaided |
| A-11 | Input guarding and cleaning: 0 V guard trace, RMA flux, ultrasonic IPA clean, 125 °C bake, gloves | working | R-48, R-52 | Flux residue is a leakage path (ADA4530-1.json p38) |
| A-12 | Detector-to-MCU connector: Molex PicoBlade-style, 14 pins proposed | working | R-24, R-07 | Pin count ≤ 15 `VERIFY` |
| A-13 | MCU board analog chain on one filtered +5 V rail, TLV906x family, baseline 0.2–0.3 V | working | R-13, D-23 | TLV90xx can't take ±4.5 V. [TLV90xx](notes/tlv90xx-assessment.md) |
| A-14 | Shaper: AC-coupled pole-zero and gain stage (inverting or non-inverting by jumper), then CR-RC^n, τ = 4 µs, footprints for 2–10 µs | working | R-09, R-14 | Low rates allow long shaping. Q-04 |
| A-15 | Trigger: TLV9061 as comparator with hysteresis, TLV3201 as footprint alternate, threshold from filtered PWM or DAC | working | R-13 | The held peak makes µs delay harmless |
| A-16 | Peak hold: TLV906x driver, low-leakage diode, 1 nF $C_{hold}$, TMUX1101 reset, TLV906x buffer | working | R-13, R-09 | 80 pA leakage budget. [Survey](notes/candidates-mux-hold.md) |
| A-17 | ADCs: ADS1220 on the holds, a mux into ADS8689, jumper to the ESP32-S3 ADC. Eight holds: two ADS1220 (4 inputs each, ADS1220.json p1), an 8:1 mux | firm | R-16, R-14 | The user's choice (D-16). Mux part open. [Survey](notes/candidates-adc.md) |
| A-18 | MCU: ESP32-S3-WROOM-1, PCB antenna, USB data, ESP-NOW option | firm | R-15 | The user's choice (D-08). [Survey](notes/candidates-mcu.md) |
| A-27 | One MCU board per chamber takes all eight CSA inputs. Peak holds handle closely spaced events | firm | R-13, R-14, R-73 | The user (review question 4) |
| A-19 | MCU board power: 5 V adapter, a 3.3 V LDO (not chosen) and an LM27762 for ±4.5 V to the detector boards only | working | R-25 | LM27762 noise and PSRR `VERIFY` |
| A-20 | HV board: 48 V, PWM-driven PCB transformer to 100–200 V, Walton multiplier, divider feedback. Point-to-point HV section, potted later. No accuracy target | firm | R-18, R-21 | D-11, D-20, Q-10. [Survey](notes/candidates-hv-generation.md) |
| A-28 | HV readback: the feedback divider (about 1000:1, before the series resistor) tapped to an MCU ADC and a test point | working | R-23 | [Readback](notes/hv-spacing-and-readback.md) |
| A-21 | HV output series resistance ≥ 10 MΩ, limiting a tube flashover to about 100 µA | open | R-22, electrometer R-10 | Asked by the electrometer, awaits the user |
| A-22 | HV safety: tube in an insulated outer enclosure with a lid interlock (PWM enable off, NC discharge), trained staff only, no HV below ambient | firm | R-22, R-43 | D-20, Q-12. Darkness check optional: [HV spacing](notes/hv-spacing-and-readback.md) |
| A-23 | Part 1 chamber: 304 SS 3/4 in NPS pipe ground and lapped to 21–22 mm, possibly etched. A board at each end, 76 mm apart | firm | R-39, R-44, R-05 | D-22 |
| A-24 | Gas train per D-02, PTFE tubing and insulating sections, Drierite desiccant, one PTFE membrane filter type | working | R-29, R-30, R-37, R-38 | D-13. Filter D-25 awaits the user. [Gas train](notes/gas-train.md) |
| A-25 | Part 2: aluminium chamber, Viton, E2M8 on NW25 with a foreline trap, Pirani gauge on an NW25 tee | working | R-46, R-57, R-59 | D-24. [Part 2](notes/part2-vacuum.md) |
| A-26 | Event firmware: on a trigger, wait the peaking time, convert that channel, reset it only. A pulse counter flags pile-up | working | R-13, R-14 | [Signal levels](notes/signal-levels.md) |

## Derived specs

| Block | Spec | Value | Parent | Working |
|---|---|---|---|---|
| CSA | Decay time $R_f C_f$ | 100 µs | R-13 | Pole-zero cancels the 4 % undershoot |
| CSA | Output offset from dark current | 15–200 mV | R-13 | AC-coupled on the MCU board |
| Shaper | Gain per stage (1 MHz part) | ≤ 5 | R-09 | GBW at 100–200 kHz |
| Chain | System gain | 150 mV/MeV nominal | R-08 | 8.78 MeV about 1.3 V |
| Hold | Total hold-node leakage | ≤ 80 pA | R-09 | 0.4 mV droop over 5 ms |
| Trigger | Threshold | about 5σ of baseline noise, near 15 keV | R-13 | [Noise budget](notes/noise-budget.md) |
| PD bias filter | RC | about 1 MΩ, about 100 nF, to simulate | R-19 | [Detector board](notes/detector-board.md) |
| Part 2 | Pressure | ≤ 1 mbar target, ≤ 10 mbar acceptable. Pump to a few ×10⁻² to 10⁻¹ mbar | R-03, R-57 | [Physics](notes/physics-reference.md) |
| HV | Ripple at the tube | open: needs C(tube → input) | R-19 | Electrometer requirements |

## Expected performance

| Quantity | Value | Set by | Known by |
|---|---|---|---|
| Electronic resolution, R-09 | 6.9–7.4 keV FWHM (OPA140, 4 µs), about 4 keV (ADA4817-1) | A-06, A-14 | Calculated: [noise budget](notes/noise-budget.md) |
| Peak width, R-09 | tens of keV, set by dead layer and straggling | A-02 | Estimated |
| ADC resolution | 0.52 keV per code (ADS8689), sub-eV (ADS1220) | A-17 | Calculated: [signal levels](notes/signal-levels.md) |
| Offset before calibration | 2.7–11 keV (TLV9001 offset) | A-13 | Calculated |
| Count rate at 100 Bq/m³, R-01 | about 2–5 counts/hour per chamber, about 16 % per alpha | A-23, A-10 | Simulated collection: S-01, `sim/field/` |
| Dead time per event, R-14 | tens of µs (ADS8689), about 0.5 ms (ADS1220) | A-17 | Datasheet |

## Off-board connections

Per Part 1 chamber with its two detector boards and one MCU board (A-27). Pin assignments are open.

| Item | Board connector | Keyed | Cable | Board edge | Conductors |
|---|---|---|---|---|---|
| Detector board to MCU board, ×2 | PicoBlade-style, 14-pin | Yes | Ribbon or loose wires, length open | Back side, edge open | 28 |
| HV to the chamber tube | open | open | HV wire | HV board, outside | 1 |
| HV return | open | open | open | HV board | 1 `VERIFY` |
| PD bias and ring bias, HV board to MCU board | open | open | open | open | open |
| 48 V adapter to HV board | open | open | Adapter lead | HV board | 2 |
| 5 V adapter to MCU board | open | open | Adapter lead | MCU board | 2 |
| USB to host | USB | Yes | USB cable | MCU board | 1 cable |
| TEST pulse input | open | open | Coax | MCU board | 2 `VERIFY` |
| **Total** | at least 5 | | | | at least 36 conductors, plus the USB cable |

## Mechanics and assembly

| Aspect | Value | Status |
|---|---|---|
| Detector board outline | Circular, covers the 21–22 mm bore and O-ring land. Diameter from the mechanical design | open |
| O-ring land and size | From the mechanical design (Q-20) | open |
| Mounting | A board at each end of the tube, O-ring sealed | firm |
| Tallest part, chamber side | VTH2110 chips, exposed | firm |
| Tallest part, atmosphere side | Connector or SWF ports, height open | open |
| MCU board, HV board | Outside the chambers. Enclosures open | open |
| HV enclosure | Touch-safe outer enclosure around the +1 kV tube (D-20) | working |

![Part 1 gas train: sample gas, inlet filter, desiccant, final filter, inlet ball valve, chamber, outlet ball valve, outlet filter, diaphragm pump, exhaust.](diagrams/gas-train.svg)

Assembly, from populated boards to a running chamber:

1. Mount and wire the four chips on each detector board (A-03), clean and bake (A-11).
2. Measure leakage through the SWF ports with the electrometer (R-48, R-49).
3. Seal a board to each end of the tube with O-rings, the chamber in its touch-safe enclosure.
4. Connect PTFE gas lines with insulating sections, then valves, filters and pump.
5. Cable both boards to the MCU board, the HV board to the tube, the adapters, and USB.

## Risks

| # | Risk | Effect | Mitigation | Test first |
|---|---|---|---|---|
| 1 | Tube end edges at about 1.5 kV/mm (S-01), die corner 0.3–0.7 kV/mm | Discharge below ambient | R-43, 0.5 mm edge radius on the tube ends | Done: S-01 |
| 2 | Diode polarity unknown | Wrong bias, pulse and steering polarity | Measure before layout | DMM diode test on a spare chip |
| 3 | CSA stability and gain with $C_f$ = 1 pF and stray, 33 pF plus $C_{in}$ at the input | Oscillation, wrong gain | Test charge | ngspice AC and noise, then test charge |
| 4 | Ring bias couples noise into the input | Wider peaks | Filtered source | Simulate the coupling capacitance |
| 5 | Hold leakage and charge injection beyond 80 pA | Droop, offset | Smaller or better parts | Simulate the hold chain, measure a node |
| 6 | Charge-pump and ESP32 noise on the analog rails | Wider peaks | LC and LDO post-filter | Rail noise measurement |
| 7 | Plated vias as a rough-vacuum seal | Leak | Bulkhead fallback (Q-20) | Leak test a bare board on the Part 2 chamber |
| 8 | Hand bonding to a 0.4 mm pad | Yield | Carrier option | Practice on spare chips |
| 9 | TLV9061 peak detector driving $C_{hold}$ | Instability, error | Smaller $C_{hold}$ | ngspice transient with the real model |
| 10 | Baseline offset and TLV90xx offset, ±0.3 to ±1.6 mV, 2–11 keV | Drift (R-52) | Per-channel baseline in firmware | Drift over a week |
| 11 | ADA4817-1 power, 0.7 W per board, if chosen | Heats the diode side | Choose it for one channel only | Thermal check |

## Open questions

1. Q-11: which VTH2110 electrode is on top? Measure a spare chip.
2. Ions land mostly where the four dies meet (S-01): [questions](questions/2026-11-21-detector.md).
3. Q-26: bond or epoxy the chips, and ask Excelitas about carriers?
4. Q-20 remainder: board outline and O-ring land diameter.
5. Q-15: suppliers. `$ELECTRONICS_TOOLS/inventory/stock.csv` now replaces the planned `parts/inventory.csv`.
6. D-16 to D-18, ADA4817-1, OPA657: [questions](questions/2026-11-21-detector.md).

Settled since: the die-corner gap and Q-24 (S-01), one MCU board per chamber (A-27).

## Notes

- Design: [detector board](notes/detector-board.md) (measure the diode polarity first), [signal levels](notes/signal-levels.md), [noise budget](notes/noise-budget.md) (4–14 keV from the electronics), [JFET and module noise](notes/jfet-and-module-noise.md), [TLV90xx assessment](notes/tlv90xx-assessment.md), [HV spacing and readback](notes/hv-spacing-and-readback.md), [decay-chain lines](notes/decay-chain-lines.md).
- Candidate surveys: [photodiode](notes/candidates-photodiode.md), [CSA op-amp](notes/candidates-csa-opamp.md), [ADC](notes/candidates-adc.md), [hold and mux](notes/candidates-mux-hold.md), [MCU](notes/candidates-mcu.md), [HV generation](notes/candidates-hv-generation.md).
- Requirements notes: [physics](notes/physics-reference.md), [chamber](notes/chamber-sensitivity.md), [gas train](notes/gas-train.md), [Part 2](notes/part2-vacuum.md).
