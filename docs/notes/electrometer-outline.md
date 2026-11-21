# Electrometer outline (retired, replaced by `electrometer/`)

**Conclusion:** The first electrometer outline (requirements section 4.7, R-57 to R-72 of that section) is replaced by the electrometer's own documents in `electrometer/`, confirmed by the user. Its IDs are retired: R-57 to R-60 also name detector requirements, and only the detector meanings are live.

**Relied on by:** nothing live. R-48 to R-50 (board characterisation, the electrometer) point to `electrometer/docs/01-requirements.md`.

## Working

### Scope as first proposed

- Leakage first (it adds shot noise and offset at the preamp input), plus photodiode reverse current versus bias and node capacitance from the same hardware.
- Not electrometer jobs: gain calibration by charge injection (R-49) and kV measurement (R-51).

### Node pairs to test

| Path | Why it matters |
|---|---|
| CSA input pad ↔ guard | Guard works only if this is far below dark current |
| CSA input pad ↔ ENIG ring | The ring carries a bias (R-47): a DC load and a noise path |
| Input pad ↔ GND, PD bias, other layer | Surface and through-board paths on the critical node |
| Input pad ↔ neighbouring input | Crosstalk and charge sharing |
| Via ↔ via and plane near the sealed vias (R-54) | Filled, sealed vias are a new construction |
| PD reverse current vs bias, dark | Screens the 8 diodes, drift baseline |

### Outline requirements (retired IDs)

| Old ID | Outline | Now |
|---|---|---|
| R-57 | DC current between two nodes at operating voltages: PD bias default 20 V, specified at 20 V and 40 V, breakdown above 100 V. Source up to 50 V | Electrometer R-01, R-08 |
| R-58 | 10 fA resolution after averaging, 100 µA full scale. Dark current 0.15–2 nA. Physics needs about 1 pA: leakage at 1 % of typical dark current is about 1.5 pA | 10 fA to 1 µA (electrometer D-01) |
| R-59 | Guarded fixture, shielded, PTFE or air. Fixture leakage at least 10× below the lowest board value, recorded each session | Probe and switch connectors (electrometer D-02) |
| R-60 | Settling: fA–pA leakage takes seconds to minutes. Record I(t) after each step | Electrometer R-05, R-13 |
| R-61 | Records carry board ID and state, date, T and RH | Electrometer R-21 |
| R-62 | Capacitance 0.1–100 pF, 0.1 pF resolution. The 1 pF feedback capacitor has 0.1–0.3 pF of board stray | Electrometer R-03, optional |
| R-63 | Input survives faults | Electrometer R-10 |
| R-64 | Self-test with 1 GΩ to 100 GΩ class resistors and a known capacitor. Offset with the input open | Electrometer R-25 |
| R-65 | Timestamped samples over the user's API (Q-23) | Electrometer R-20 |
| R-66 | Closed conductive enclosure, a tin with good lid contact | The tin (electrometer R-15) |
| R-67 | Three boards: front end inside, sensor board inside, external ESP32 board with two 18650 cells in series. Shielded cable through filtered feedthroughs | Battery-powered head and control in the tin, antenna outside (electrometer R-24, R-32, D-08) |
| R-68 | RH/T sensor in the enclosure, off during a measurement | Electrometer R-17 |
| R-69 | Reed relays (open-contact insulation about 10¹²–10¹⁴ Ω, `VERIFY`) on input paths, about 10 relays: about 5 resistors from 10 kΩ to 100 GΩ, 2–3 capacitors. Coils need tens of mW (`VERIFY`) | Matrix dropped, manual T-switch panel (electrometer D-02, D-03) |
| R-70 | 10 fA through 100 GΩ is only 1 mV, so gain before the wall | ADC in the tin (electrometer architecture) |
| R-71 | Shielded twisted-pair link, about 1 m or less, keyed so it can't meet a network switch | No wired link (electrometer R-32) |
| R-72 | Calibration chain, below | Electrometer R-07, R-26 |

### Calibration chain as first proposed (R-72)

- Top ranges against the SDM3055 (lowest current range 200 µA, about 1 nA resolution, about 0.1 % of reading plus 0.05 % of range, `VERIFY`): good to about 0.15 % at 100 µA, about 1 % at 10 µA, only about 10 % at 1 µA.
- I = V/R across a measured resistor, the DMM as ohmmeter up to about 100 MΩ.
- A ratio chain between adjacent ranges, 100 MΩ up to 100 GΩ.
- Capacitor ramp, I = C dV/dt with C of 1–100 pF checked on an LCR meter, from the SDG2122X or a battery-fed source.
- Open-input offset every session, optionally an outside SMU or resistor certificate.
- Target accuracy about 5–10 %, since boards are compared on one instrument.

## Sources

- Requirements DRAFT 2 section 4.7, in git history before the contract rewrite.
- `electrometer/docs/01-requirements.md`, `electrometer/docs/decisions.md`.
