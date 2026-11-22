# Electrometer front end: requirements
<!-- doclint-allow: words — an R-xx project: 34 requirements keep their IDs (PCB-WORKFLOW.md) until the user decides whether to convert and merge them into F/O/C items -->

| | |
|---|---|
| Project | A battery-powered bench electrometer for the radon project's detector (CSA) boards: DC current from about 1 µA down to 10 fA, measured in situ in a grounded tin |
| This document | Purpose, scope and the R-xx requirements as functions, objectives and constraints. IDs are local. Radon-project IDs are written "radon R-xx". `VERIFY` marks an unconfirmed fact |
| State | Approved by the user. Numbers proposed since are working, in the architecture |
| Open questions | 4 |

## Purpose

- Measure the small DC currents on the detector boards that the bench gear can't reach, so parasitic leakage can be told apart from the photodiode signal (D-01).
- Complement the bench DMM: a small overlap with its lowest current range, then down to 10 fA. Nothing on the bench resolves below about 1 nA, and the dark current is 0.15 nA typical.
- Test the 1 kV paths in situ, on a built chamber, since only the real thing includes them meaningfully (D-02).
- Built inside the radon project, then moved to `$ELECTRONICS_TOOLS/bench-test-gear/` (radon R-50, the electrometer project).

## Scope

### In scope

- Leakage characterisation of bare and populated detector boards (radon R-48, R-49)
- The electrometer head, control board, range panel and built-in source
- The in-tin test arrangement: the tin, its pass-throughs, the probe cable
- Requirements it places on the detector board (R-19) and on the radon HV board
- Optional charge and capacitance modes, kept only if almost free (D-01)

### Out of scope

- AC impedance (LCR), pulse-height spectroscopy and CSA pulse-gain calibration (the electrometer only supplies a measured $C_{test}$)
- Generating HV: the 1 kV comes from outside (R-09)
- A switching matrix (D-02): nodes are selected by moving the probe
- Currents above 1 µA (the DMM), and metrology-grade absolute accuracy: comparisons matter more
- The chamber's ion current as a radon measurement

## Functions

| ID | Function | Status | Source | Verification |
|---|---|---|---|---|
| R-01 | Measures DC current with the node held at virtual ground, from 1 µA full scale down to 10 fA. The primary function | firm | User (D-01, Q-02) | Test |
| R-02 | Optional: measures charge on the integrator, counting resets for slow charge and logging fast charge as a timestamped overload | firm | User (D-01, D-04) | Test |
| R-03 | Optional, needs R-02: measures guarded capacitance by charge transfer with small steps, for bare boards (U-2) and absolute $C_{test}$ (U-3) | firm | User (D-01) | Test |
| R-04 | Measures resistance from V/I, including alternating polarity to reject soak currents and offsets | firm | User | Test |
| R-05 | Logs time-stamped I(t) and Q(t) after a source step, 10 ms to 24 h per run | firm | User | Test |
| R-06 | Optional: detects and time-stamps charge steps (micro-discharges) in charge mode | firm | User | Test |
| R-07 | Overlaps the bench DMM for cross-checks, 100 nA to 1 µA read by both | firm | User (D-01) | Test |
| R-08 | Provides one bipolar programmable source, ±50 V, for bias, steps and alternating polarity | firm | User (D-06) | Simulation, test |
| R-10 | Survives a flashover from the 1 kV tube to a diode node under the probe, and a mis-routed ±50 V, without lasting change in leakage or offset | firm | User | Simulation, test |
| R-11 | Selects the node by hand: one probe cable moved between the detector board's switch connectors, tin open and HV off | firm | User (D-02) | Inspection, test |
| R-12 | No node floats during a measurement. TEST is held at 0 V for DC measurements | firm | User | Inspection |
| R-13 | Waits until a reading has settled after a probe move or source step, and logs the wait | firm | User | Test |
| R-17 | Logs temperature and RH inside the tin with every reading | firm | User | Inspection, test |
| R-18 | Optional dry-N₂ purge of the tin itself | firm | User | Inspection |
| R-20 | Is controlled by SCPI-style text over ESP-NOW through `lab-gateway`, scripted from the user's API, and streams readings | firm | User (radon Q-23) | Test |
| R-21 | Each record carries timestamp, function, range, value, source level, probed channel and board, confirmed range, PD bias and ring state, T, RH and flags | firm | User | Inspection |
| R-25 | Checks each range before a session: input zero, and a known reference | firm | User | Test |
| R-26 | Calibrates against the bench gear: a ramp into a known capacitor, the source against the SDM3055, the R-07 overlap. Constants stored on the instrument | firm | User | Test |

### R-01

Burden ≤ 1 mV up to 4 nA and ≤ 10 mV on the 1 µA range (D-05, firm). Noise and accuracy targets are working: [proposed targets](notes/proposed-targets.md).

## Objectives

Ranked in table order (working).

| ID | Objective | Status | Scoring |
|---|---|---|---|
| R-14 | Triboelectric pickup from normal handling: lower is better | firm | Good enough: ≤ 50 fA (U-6) |
| R-23 | Disturbance from the radio and digital activity: lower is better | firm | Good enough: radio on vs off differs by less than the R-01 noise floor |
| R-24 | Battery life: longer is better | working | ≥ 24 h of logging proposed. Measured draws against D-08 |
| R-22 | Reading rate: higher is better | working | Proposed values in the architecture |
| R-34 | Build and assembly effort after the boards are populated: lower is better | working | Off-board connections and conductors in the architecture |

## Constraints

| ID | Constraint | Status | Source | Verification |
|---|---|---|---|---|
| R-09 | HV never passes through the electrometer: the radon HV board, outside the tin, feeds the tube through an HV feedthrough. ≤ 1.1 kV | firm | User | Inspection |
| R-15 | Everything sits in a grounded metal tin: chamber, detector boards, head and control board, with pass-throughs for HV, gas, the PicoBlade lines and the antenna | firm | User (D-02) | Inspection |
| R-16 | The tin is dark: stray light on a diode stays within the noise floor | firm | Physics | Test: lights on vs off |
| R-19 | On the detector board (feeds radon R-60, the test port): a guarded switched coaxial connector per CSA input, shell on the 0 V guard ring, $C_{test}$ on the diode side | firm | User (D-02) | Inspection, test |
| R-27 | The built-in source stays in the SELV range and is current-limited, ≤ 100 µA | firm | Safety | Inspection, test |
| R-28 | A lid interlock disables and discharges the external HV. HV-present shown outside. HV off before the probe moves | firm | Safety (radon R-22, D-20) | Inspection, test |
| R-29 | Hand-assembled. Input node on PTFE standoffs or in air, guarded, board washed after assembly | firm | User | Inspection |
| R-30 | Portable to the test-gear repo: no dependency on radon paths except its use cases | firm | User | Inspection |
| R-31 | Single-point grounding: coax shield is common and guard, one bond to the detector board's 0 V, tin bonded to common, HV return separate | firm | User (D-02) | Inspection, test |
| R-32 | The radio antenna is outside the tin | firm | Physics: the tin blocks 2.4 GHz | Test: link holds with the tin closed |
| R-33 | Ranges set on an off-board panel by the operator as the script instructs, power off, no position sensing. No panel means integrate-only | firm | User (D-03) | Inspection, test |

## Open questions

With context and recommendations: [questions](questions/2026-11-21-electrometer.md).

1. Q-09: budget for the ADA4530-1, the Murata probe and the SWF receptacles.
2. Q-14: antenna on a bulkhead (working), or the control board outside the tin?
3. Q-12: SWF leakage and probe life: `DECIDE AT TEST`, on the bare test board.
4. Q-13: space on the detector board's back: `DECIDE AT` detector layout.

Settled: Q-04 (project HV board only), Q-10 (RH logged by R-17, purge `DECIDE AT TEST`), Q-15 (bare laminate; the detector's +20 V ring catches tube leakage), decisions "Questions settled by the detector answers and S-01".

## Notes

- [Use cases](notes/use-cases.md): U-1 to U-6, U-5 in the tin is primary.
- [Expected magnitudes](notes/expected-magnitudes.md): parasitics from fA to nA, so measured. fA runs at PD bias 0 V.
- [Bench gear](notes/bench-gear-coverage.md): the DMM and a powered CSA reach about 1 pA in situ. Bare boards and absolute $C_{test}$ need the electrometer.
- [Test connection](notes/test-connection.md): SWF switch connectors, single-point grounding, a floating instrument.
- [Answered questions](notes/user-answers.md): Q-01 to Q-11 and the architecture draft's questions.
- [Proposed targets](notes/proposed-targets.md): Claude's working numbers for each requirement, for the user to make firm.
