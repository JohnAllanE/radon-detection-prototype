# Candidates: peak-hold path and channel mux

**Need:** per channel, hold the shaped peak until the MCU converts it, with ≤ 80 pA total leakage on the hold node, a reset switch, and a 4:1 mux to the single-channel ADS8689 (R-13, A-16).

**Pick:** working: low-leakage diode (BAS116 candidate) into a 1 nF C0G or film $C_{hold}$, TI TMUX1101 reset, TLV9061-family driver and buffer, TI TMUX1104 mux.

**Relied on by:** A-16 (peak hold), A-17 (ADCs), R-13 (per-channel hold and reset), R-09 (droop and charge injection add to the resolution).

## Candidates

Prices and stock open (pass 2).

| Part | Maker | Price (CAD) | Stock or supplier | Package vs assembly | SPICE model | Lets the design | Costs the design |
|---|---|---|---|---|---|---|---|
| **TMUX1101** (reset) | TI | open | open | open | open | SPST, 3 pA leakage, −1.5 pC charge injection, listed for sample-and-hold | Logic polarity: TMUX1102 or TMUX1103 may suit the reset better (`VERIFY`) |
| TMUX1102, TMUX1103 | TI | open | open | Same family | open | Other logic polarity | Not pulled |
| **TMUX1104** (mux) | TI | open | open | open | open | 4:1, 3 pA, 1.5 pC | Signals GND to VDD only: positive peaks only |
| **BAS116** (diode) | open | open | open | open | open | Low-leakage diode | Not pulled. Leakage must be ≪ 80 pA (`VERIFY`) |
| Other low-leakage diodes | — | open | open | open | open | Alternates | Not surveyed |
| **1 nF $C_{hold}$**, C0G or film | — | open | open | open | — | 80 pA budget at 0.03 % droop | Droop and dielectric absorption `VERIFY`. 220 pF tightens the budget to about 15 pA |

Prices: none checked. The hold buffer and peak-detector op-amps are in [TLV90xx assessment](tlv90xx-assessment.md).

## What the pick sets

| Quantity | Value | From |
|---|---|---|
| Hold-node leakage budget | ≤ 80 pA total for 0.4 mV droop over 5 ms | [Signal levels](signal-levels.md) |
| Known contributors | TMUX1101 3 pA, TLV9001 bias ±5 pA typical (TLV9061 0.5 pA) | TMUX1101.json p1, TLV9001.json p17 |
| Reset charge injection | about 1.5 mV after reset into 1 nF: absorbed in the baseline | TMUX1101.json p1 |
| Supplies | TMUX1104, TMUX1101 are 5.5 V parts, on the +5 V rail | Datasheets |

## Sources

- `datasheets/TMUX1101.json` p1, `TMUX1104.json` p1, `TLV9001.json` p17. None yet in component-data (it has TMUX1108, TMUX1219, TMUX6104 and others).
