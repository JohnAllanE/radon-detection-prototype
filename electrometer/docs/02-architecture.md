# Electrometer front end: architecture

| | |
|---|---|
| Project | A battery-powered bench electrometer for the radon project's detector (CSA) boards: DC current from about 1 µA down to 10 fA, measured in situ in a grounded tin |
| This document | How the head, range panel, readout, source, control and power are built, and what they should do. Stock parts named where they fit. `VERIFY` marks an unconfirmed fact |
| State | Draft. Topology and ranges approved by the user, the rest awaits approval |
| Open questions | 4 |

## IDs from other documents

- Functions: R-01 DC current to 10 fA, R-02 charge, R-05 logging, R-07 DMM overlap, R-08 ±50 V source, R-10 survives faults, R-13 settling, R-17 T and RH, R-20 SCPI over ESP-NOW, R-21 records, R-25 range checks, R-26 calibration.
- Objectives: R-14 triboelectric pickup, R-23 radio disturbance, R-24 battery life, R-22 reading rate, R-34 build effort.
- Constraints: R-09 HV outside, R-15 the tin, R-27 SELV source, R-28 HV interlock, R-29 build, R-31 grounding, R-32 antenna outside, R-33 off-board range panel.
- Simulations: S-01 head (loop stability, integrator reset, range check), S-02 source (step and 0.1–10 Hz noise).
- Radon project: radon R-19 (HV ripple), radon R-60 (test port), radon A-21 (HV series resistance).

## Block diagram

![System diagram inside the grounded, light-tight tin. Left: the chamber at +1 kV, fed from the external HV board through an interlocked feedthrough, and the detector board's back, where the probe is mated on one channel's switch connector while the other channels stay on their CSAs. The PicoBlade breakout carries PD bias, ring, TEST, ±4.5 V and GND, and the ±50 V source can drive the ring or PD bias through it. Middle: the shielded head, with input protection, the guarded summing node, a 1 pF injection capacitor, the ADA4530-1-class op-amp, a 3.9 MΩ and a 1 GΩ branch each on a manual T-switch on the off-board panel, the 10 pF integrator always in, and an MCU-driven reset. Right: a 24-bit ADC and the MCU, which reaches lab-gateway over ESP-NOW through an antenna outside the tin. Inset: a branch switched off as a T-switch, Sa and Sb in series with their midpoint held at 0 V by Sc.](diagrams/switching-concept.svg)

![Power tree. A floating 1S2P Li-ion pack (two 18650 cells) feeds, through a switch, fuse and cell protection, a 3.3 V buck-boost for the digital side, ±6.5 V converters followed by ±5 V low-noise LDOs for the head, ADC and DACs, and a ±60 V boost for the ±50 V source, switched on only when used. The charger connects only with the main switch off. One star point in the head, digital ground joining it once at the ADC.](diagrams/power-tree.svg)

## Choices

| ID | Choice | Status | Serves | Why |
|---|---|---|---|---|
| A-01 | Transimpedance and integrator head around an ADA4530-1-class op-amp, + input at 0 V guard, ±5 V rails | firm | R-01 | Approved. Its input range needs a negative rail. [Floor](notes/amplifier-floor.md) |
| A-02 | Ranges: R1 3.9 MΩ (1 µA full scale), R2 1 GΩ (4 nA), 10 pF integrator always in | firm | R-01, R-07 | Approved. ±4 V swing sets them |
| A-03 | Range panel off the head board: T-switch per branch, PTFE coax S, E1, E2 at most 30 cm, cheap SPST plus SPDT panel first | firm | R-33 | D-03. Rotary panel later, same interface |
| A-04 | Reset switch as a T: Sa a reed relay with a shielded coil, off while integrating; Sb/Sc a low-leakage analog SPDT | firm | R-01, R-02 | Approved. Sa sees about 0 V |
| A-05 | Input protection: 10 kΩ series resistor, then low-leakage clamps from the summing node to common | firm | R-10, R-01 | D-05 burden split. [Protection](notes/input-protection.md) |
| A-06 | Self-test: permanent 1 pF $C_{inj}$ from an MCP4821, held at 0 V while measuring. Resistor ranges checked with an external cal plug | open | R-25, R-26 | Awaits the user. [Self-test](notes/self-test.md) |
| A-07 | Summing node millimetres long, in air or on PTFE standoffs, in a guard ring driven by the op-amp's guard pins (2, 7) | working | R-29, R-01 | Construction sets the floor |
| A-08 | Readout: 24-bit ΔΣ ADC (ADS1220), slope fits over multiples of 100 ms on the integrator, 20 SPS 50/60 Hz mode on the resistor ranges | working | R-01, R-22 | No need to know the mains frequency (D-06) |
| A-09 | One ±50 V source: MCP4922 coarse plus fine, REF5040, summing op-amp, HV amplifier from ±60 V, RC output filter, readback | firm | R-08, R-27 | D-06, D-07: about 24 µV steps, monotonic via readback |
| A-10 | Power: two 18650 cells in parallel (3.0–4.2 V), floating. Charger only with the main switch off | firm | R-24, R-31 | D-08 |
| A-11 | Rails: 3.3 V buck-boost, ±6.5 V converters at ≥ 1 MHz then ±5 V LDOs, ±60 V boost on only when the source is used | working | R-23, R-24 | Converters shielded and far from the head |
| A-12 | Control: ESP32-S3-WROOM-1U (in stock), antenna on a bulkhead outside the tin | working | R-20, R-32 | Q-14 open |
| A-13 | SCPI-style protocol over ESP-NOW through lab-gateway, Keithley 6514/6517B names where they overlap. Transmit between integration windows | working | R-20, R-23 | As the load-cell reader follows the SDM3055 |
| A-14 | T/RH: digital I²C sensor (SHT4x class) in the tin, away from the head | working | R-17 | — |
| A-15 | One star point in the head: common, op-amp + input, guard, coax shields, head shield, tin. Digital ground joins at the ADC | firm | R-31 | D-02. [Test connection](notes/test-connection.md) |
| A-16 | Head in its own non-ferrous (aluminium) shield box inside the tin, near the chamber end | working | R-15, R-23 | Short probe cable |
| A-17 | Power-up range check: a $C_{inj}$ step whose decay identifies the connected range | working | R-33 | D-03, no extra parts |
| A-18 | The radon HV board gets ≥ 10 MΩ output series resistance (radon A-21) | open | R-10 | Limits a flashover to about 100 µA |
| A-19 | PicoBlade breakout with manual selectors. PD bias: HV board, source or 0 V. Ring: its supply, source or 0 V. TEST: 0 V or pulse generator | working | R-12, R-08 | D-06. Filtered pass-through in the tin wall |
| A-20 | HV feedthrough with a lid switch that disables the HV board and closes a bleeder on the tube | working | R-09, R-28 | Interlock design open |

### Parts in stock and to select

- In stock: ADS1220 (8), ESP32-S3-WROOM-1U-N16R8 (1), REF5040 4.096 V (1), MCP4922 (1), MCP4821 (2), OPA2186 (8), OPA2192 (1).
- Not in stock: ADA4530-1 (datasheet pulled, Q-09 budget).
- To select: HV op-amp, ±60 V boost, reed relay and its coil driver transistor (on only during a reset), analog SPDT, high-value resistor, T/RH sensor, SWF receptacles and probe.

## Derived specs

Proposed numbers each requirement designs to are in [proposed targets](notes/proposed-targets.md), all working.

| Block | Spec | Value | Parent | Working |
|---|---|---|---|---|
| Head | Op-amp input bias | ≤ 20 fA, guard buffer | R-01 | ADA4530-1 class |
| Head | Burden | ≤ 1 mV up to 4 nA, ≤ 10 mV at 1 µA | R-01 | D-05 |
| Head | $C_f$ | 10 pF, C0G or PTFE/polystyrene, low dielectric absorption (`VERIFY` for C0G) | R-01, R-02 | — |
| Head | R1, R2 | 3.9 MΩ thin film ≤ 1 %. 1 GΩ glass or thick film, low voltage coefficient, calibrated (R-26) | R-01 | — |
| Head | Output to ADC | ±4 V scaled by a precision divider and buffer (OPA2186 or OPA2192, in stock) | R-01 | — |
| Readout | ADC rate | ≥ 1 kSPS for slope fitting, a 20 SPS 50/60 Hz mode, second channel reads the source | R-01, R-22 | — |
| Readout | Integrator reset | When \|Vout\| passes 3.5 V, then discard a settle time. Resets counted for charge (R-02) | R-01, R-02 | — |
| Readout | Settled | 60 s slope below the noise floor | R-13 | — |
| Source | Output filter | Series R ≥ 100 kΩ then a film capacitor: ≤ 100 µA into a short, sets the slew | R-08, R-27 | — |
| Source | HV amplifier | ±50 V from ±60 V rails, ≤ 1 mA quiescent, unity-gain stable, low 1/f noise | R-08, R-24 | — |
| Source | Noise | ≤ 10 µV rms in 0.1–10 Hz. Reference noise × gain (about 20) is the main term | R-08 | S-02 |

## Expected performance

| Quantity | Value | Set by | Known by |
|---|---|---|---|
| Integrator resolution, R-01 | about 0.5–1 fA p-p in 1 s | A-01 | Calculated: [floor](notes/amplifier-floor.md) |
| R2 range noise, R-01 | 2.9 fA rms per 1 s reading | A-02 | Calculated |
| R1 range noise | 46 fA rms per 1 s reading | A-02 | Calculated |
| Offset before zeroing | 40 fA (R2), 10 pA (R1) | A-01, A-02 | Calculated |
| Bandwidth, phase margin | 4 kHz and 87° (R1), 16 Hz and 90° (R2) | A-02 | Calculated, S-01 to confirm |
| Source step, R-08 | about 24 µV | A-09 | Calculated |
| Battery life, R-24 | about 38 h source off, about 25 h source on | A-10 | Calculated, draws `VERIFY` |

## Off-board connections

Counted from the head and control board. Conductor counts marked open wait for the pinouts.

| Item | Board connector | Keyed | Cable | Board edge | Conductors |
|---|---|---|---|---|---|
| Probe to the detector board | SMA on the head | Yes | Murata SWF probe, 100 or 300 mm | Head, chamber side | 2 (coax) |
| Range panel S, E1, E2 | SMA ×3, PTFE | Yes | PTFE coax ≤ 30 cm | Head | 6 |
| Head to control board | open | open | Shielded, inside the tin | open | open |
| Source to the PicoBlade breakout | open | open | Coax | Control board | 2 |
| Antenna | Module connector to a bulkhead | Yes | Coax pigtail | Control board | 1 cable |
| Battery charger | open | open | Charger lead, main switch off | Control board | 2 |
| Tin wall: HV feedthrough, interlock, filtered pass-through, gas grommets | — | — | Radon project's cables | Tin | open |
| **Total** | at least 7 | | | | at least 12, plus open items |

## Mechanics and assembly

| Aspect | Value | Status |
|---|---|---|
| Head | Small board in an aluminium shield box inside the tin | working |
| Control board | Inside the tin, battery beside it, antenna on a bulkhead | working |
| The tin | Grounded, light-tight, lid contact good. Size open | open |
| Chamber in the tin | On insulating standoffs, ≥ 10 mm from the tin (`VERIFY`, radon Q-12) | working |
| Range panel | Small metal panel at common, outside the head box | working |

Assembly:

1. Build the head first and measure the self-baseline (U-6) before anything else.
2. Fit the head box, control board, battery and range panel in the tin.
3. Fit the HV feedthrough, interlock, filtered pass-through, antenna bulkhead and gas grommets.
4. Mount the chamber on standoffs, tie down the probe cable.

## Risks

| # | Risk | Effect | Mitigation | Test first |
|---|---|---|---|---|
| 1 | Summing-node leakage and settling in the real construction | Floor above 10 fA | PTFE or air, cleaning | Build the head, measure U-6 |
| 2 | SWF connector leakage and the probe cable (Q-12) | Floor above 10 fA | Ask Murata | Measure on the bare test board (U-6) |
| 3 | Reset switch charge injection, coil coupling, leakage | Integrator errors | Shielded coil, T arrangement | S-01, then bench |
| 4 | Source noise in 0.1–10 Hz | Misses R-08 | Lower-noise reference, longer filter | S-02 |
| 5 | Converter and radio interference at the head | Misses R-23 | Distance, shields, boost off, scheduling | Radio on vs off |
| 6 | Triboelectric settling after probe moves and range changes | Long waits | Tie-down | Measure in U-6, sets the R-13 wait |
| 7 | Battery life with the source on, about 25 h against 24 h | Misses R-24 | A third parallel cell | Measure the draws |

## Open questions

1. A-06: accept $C_{inj}$ and an external cal plug in place of R-25's switched references?
2. A-18: does the radon HV board take ≥ 10 MΩ output series resistance?
3. Q-14: antenna on a bulkhead (working), or the control board outside the tin?
4. Power input: the bench power standard (GX12 2-pin) or the battery alone? The electrometer floats on its battery, and the standard notes it may need its own earth lug.

## Notes

- [Amplifier floor](notes/amplifier-floor.md): about 0.5–1 fA p-p from the amplifier, so construction sets the floor.
- [Self-test](notes/self-test.md): $C_{inj}$ gives 10 fA to 4 pA, no switch at the node.
- [Input protection](notes/input-protection.md): 10 kΩ and clamps, plus ≥ 10 MΩ at the HV board.
- [Proposed targets](notes/proposed-targets.md): the working numbers per requirement.
- Diagrams: `python3 electrometer/docs/diagrams/make_diagrams.py` (standard library).
