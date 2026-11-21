# The amplifier floor, the rails and the ranges

**Conclusion:** An ADA4530-1-class integrator resolves about 0.5–1 fA p-p in a 1 s integration even with 220 pF at the input, so the amplifier doesn't limit 10 fA: leakage, triboelectric charge, dielectric absorption and humidity do. Its input range forces split rails, ±5 V, which with a ±4 V usable swing sets the ranges.

**Relied on by:** A-01 (topology and rails), A-02 (ranges), A-08 (readout), R-01 (10 fA), R-07 (overlap), risks 1–6.

## Working

All from `sim/analytic/budget.py` (output `budget.out.txt`), each input with its source there.

### Split rails

- The ADA4530-1's input range runs from its negative rail to 1.5 V below its positive rail (ADA4530-1.pdf p3, p5). A 0 V virtual ground needs a negative rail.
- ±5 V leaves a ±4 V usable output swing.

### Ranges

| Range | Covers | Offset before zeroing | Offset drift | Noise per 1 s reading |
|---|---|---|---|---|
| Integrator, 10 pF | 10 fA to about 4 nA (ramps of 10 ms or longer, 40 pC per ramp) | Zeroed against an open input | — | about 0.5–1 fA p-p (amplifier) |
| R2, 1 GΩ | about 4 pA to 4 nA, continuous | 40 fA max | 0.5 fA/K | 2.9 fA rms (R2's thermal noise) |
| R1, 3.9 MΩ | about 1 nA to 1 µA | 10 pA max | 0.13 pA/K | 46 fA rms |

### Input capacitance

- PD bias on: 102 pF at the input, integrator noise gain 11.2. PD bias at 0 V (fA runs): 219 pF, noise gain 22.9.
- Assumed: diode 150 pF at 0 V (`VERIFY`, the curve stops at 20 V), probe cable and S coax 30 pF each (about 100 pF/m, `VERIFY`).

### Integrator resolution, op-amp limited

| Case | 1 s | 10 s |
|---|---|---|
| PD bias on | about 554 aA p-p | about 113 aA p-p |
| PD bias 0 V | about 973 aA p-p | about 138 aA p-p |

### Loop stability (single-pole model, worst-case input)

- R1: phase margin about 87°, signal bandwidth 4 kHz.
- R2: phase margin about 90°, signal bandwidth 16 Hz.
- S-01 checks this with the real model.

### Leakage at the summing node

Everything at the summing node (open Sa contacts, clamps, the reset switch's node side, $C_{inj}$'s line) has only $V_{os}$ across it, at most 40 µV: through 1 TΩ that is 40 aA. Its leakage scales with $V_{os}$, not with the 4 V output or the 50 V source.

### Mains frequency (Q-08)

A slope or average over a multiple of 100 ms spans whole cycles of 50 Hz (5) and 60 Hz (6). A delta-sigma ADC with simultaneous 50/60 Hz rejection does the same for the resistor ranges.

### Not captured by the budget

Leakage of the real construction (PCB, PTFE, connectors, humidity), triboelectric and piezoelectric charge, dielectric absorption of $C_f$ and the board, reset-switch charge injection, converter and radio interference, the real op-amp model. Cable capacitances, the zero-bias diode capacitance and all power draws are `VERIFY`.

## Sources

- `sim/analytic/budget.py`, `budget.out.txt`. `datasheets/ADA4530-1.pdf` p1, p3–p5 (parent repo).
