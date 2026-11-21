# Candidates: HV generation

**Need:** about +1 kV, fixed, for the Part 1 chamber wall from a 48 V wall adapter, plus a regulated photodiode bias, without degrading the preamp noise floor and without a touchable HV part (R-18, R-19, R-20, R-22).

**Pick:** topology firm (D-11, D-20): 48 V into a PWM-driven PCB transformer (100–200 V), then a Walton (Cockcroft-Walton) multiplier to about 1 kV, with a divider feeding the PWM controller's feedback pin. No parts chosen: open.

**Relied on by:** A-20 (HV board), A-21 (output series resistance), A-22 (HV safety), R-18 to R-23, the electrometer's input protection (electrometer R-10).

## Candidates

The HV board has no design yet. The rows are approaches, not parts. Prices and stock open.

| Part | Maker | Price (CAD) | Stock or supplier | Package vs assembly | SPICE model | Lets the design | Costs the design |
|---|---|---|---|---|---|---|---|
| **PCB transformer + Walton multiplier** | own design | open | open | PCB up to the transformer, HV section point-to-point, potted after it works | open | The user's chosen construction, no surface leakage on the HV side | Transformer design, creepage rules (Q-12) |
| Wound transformer + multiplier | open | open | open | open | open | Proven magnetics | Not surveyed |
| Commercial HV DC-DC module | open | open | open | open | open | No magnetics or multiplier design | Not surveyed. Ripple and fixed output to check against R-19 |
| PWM controller with feedback pin | open | open | open | open | open | Regulation from the HV divider (D-20) | Not chosen |
| 48 V wall adapter | Mean Well | open | open | — | — | The user's choice (D-08) | Model not chosen |

Prices: none checked.

## What the pick sets

| Quantity | Value | From |
|---|---|---|
| Output | about +1 kV fixed, no adjustment | D-11 |
| Transformer secondary | 100–200 V | D-11, R-18 |
| Fault current into a diode node | about 100 µA with ≥ 10 MΩ output series resistance (working, A-21) | Electrometer architecture |
| Ripple limit | Not set: needs C(tube → input), measured with the bench gear | Electrometer requirements, R-19 |
| Load current, accuracy | open (Q-10, answer not recorded) | — |

## Sources

- Decisions D-11, D-20. Electrometer architecture (fault current), electrometer requirements (ripple coupling).
