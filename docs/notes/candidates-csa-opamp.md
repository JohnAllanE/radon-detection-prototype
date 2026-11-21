# Candidates: CSA op-amp

**Need:** the charge-sensitive preamp's op-amp on each detector board: lowest series noise into about 35 pF, stable with $C_f$ = 1 pF, ±4.5 V rails (R-09, R-10, A-05). Low-cost variant on one standard SOIC-8 footprint, premium free to use guard pins.

**Pick:** Texas Instruments OPA140 for the low-cost board, working (D-17). LMP7721 for the premium board, working and awaiting the user's approval (D-18): it differs by leakage control and guarding, not by noise.

**Relied on by:** A-06 (low-cost CSA), A-07 (premium CSA), R-09 (energy resolution), R-10 (low-cost footprint), R-53 (similar readings), R-60 (stable at noise gain 1 with the diode unplugged).

## Candidates

Prices and stock are open (pass 2). The user's estimates: general op-amps about $4, dedicated premium parts about $12, LMP7721 $8.40 each. None checked.

| Part | Maker | Price (CAD) | Stock or supplier | Package vs assembly | SPICE model | Lets the design | Costs the design |
|---|---|---|---|---|---|---|---|
| **OPA140** | TI | open (user: about $4) | open | SOIC-8, pins 1, 5, 8 NC: fits | open | 5.1 nV/√Hz, 11 MHz, 0.5 pA, 6.9–7.4 keV at 4 µs | 17 pF input, 1.7 µs rise: needs τ ≥ 4 µs |
| OPA656 | TI | open | open | SOIC-8, same footprint | open | 6.0 nV/√Hz, 230 MHz, 3 pF input, unity-gain stable | 6.0–6.5 keV at 4 µs, no better than OPA140 |
| OPA657 | TI | open | open | SOIC-8, same footprint | open | 4.8 nV/√Hz, 1600 MHz, 5.1–5.7 keV at 4 µs | Decompensated: may oscillate with the diode unplugged (R-60, `VERIFY`) |
| TL071-class | various | open | open | SOIC-8 | open | Cheapest tier | Not pulled. Noise unknown |
| **LMP7721** | TI | open (user: $8.40) | open | SOIC-8, non-standard pinout: own footprint | open | 3 fA bias, NC pins separate the inputs for guarding (LMP7721.json p3), 17 MHz | 6.5 nV/√Hz: 6.8–7.3 keV at 4 µs, no noise gain over OPA140 |
| ADA4817-1 | ADI | open (user: expensive) | open | SOIC-8, FB pin next to −IN, hand-solderable | open | 4.0 nV/√Hz, 1.4 pF, 410 MHz: about 4 keV at 4 µs | 19 mA per amplifier, about 0.7 W per board: heats the diode side |
| ADA4530-1 | ADI | open (user: expensive) | open | SOIC-8, guard pins both sides | open | 20 fA, built-in guard buffer | 14 nV/√Hz, 2 MHz, 8 pF: about 15 keV at 4 µs. Kept for the electrometer |

Prices: none checked. Exchange rate: not applicable yet.

### What the premium board can test

- The leakage idea (LMP7721, ADA4530-1: fA bias, guard pins) is invisible while the diode's own dark current (0.15–2 nA) is about 10⁴ times larger than 3–20 fA. Only board surface leakage could matter.
- The noise idea (ADA4817-1, about 4 against 7 keV at 4 µs) is the one with a visible effect on peak width, at a power and price cost.
- So ADA4817-1 gives the information-rich answer and LMP7721 the affordable one. The cheapest informative step is one or two ADA4817-1 on a single-channel test, not eight.
- Expected outcome: both boards measure similar spectra. Differences show in baseline leakage and drift (R-52), not peak widths.

### The two variants

| | Low-cost | Premium |
|---|---|---|
| Layout | Guard by trace only | Guard on the NC pins, tighter keep-out |
| Passives | Standard C0G and thick film | Low-leakage $C_f$ and $R_f$ |
| Purpose | How cheap the amplifier can be | What extra leakage control or noise buys |

## What the pick sets

| Quantity | Value | From |
|---|---|---|
| Electronic resolution, OPA140, τ = 4 µs | 6.9–7.4 keV FWHM | `sim/analytic/enc_budget.out.txt` |
| Electronic resolution, LMP7721, τ = 4 µs | 6.8–7.3 keV FWHM ($C_{in}$ assumed 5 pF) | Same |
| CSA rise, OPA140 | about 1.7 µs | Same |
| Minimum shaping time with OPA140 | 4 µs | [Noise budget](noise-budget.md) |

## Sources

- `datasheets/OPA140.json` p7, `OPA656.json` p5, `OPA657.json`, `LMP7721.json` p3, `ADA4817-1.json` p1, p4, `ADA4530-1.json` (to migrate to component-data, which has none of these yet).
- [Noise budget](noise-budget.md), [JFET and module noise](jfet-and-module-noise.md).
