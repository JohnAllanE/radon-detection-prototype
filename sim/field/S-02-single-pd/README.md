# S-02: one photodiode per tube, tube inner diameter against top-copper bias

**Answer.** Build around **1-1/4 in schedule 40 pipe (ID 35.05 mm) with the top copper at $V_{top}$ = +200 V**. There, the field lines from 56 % of the gas volume end on the VTH2110's 5 × 5 mm active area (50–58 % between the die's side and diagonal sections). The interaction index $ID^2 f$ is 684 mm², 4.7 times the old four-die array's 145 mm² in the 3/4 in tube, with one die instead of four. A larger tube catches more volume but funnels a smaller share onto one die: 1-1/2 in gains only 7 % in index at 200 V while the share falls to 44 %. Raising $V_{top}$ helps every tube of 3/4 in and up (1-1/4 in: 41 % at 0 V, 56 % at 200 V, 76 % at 600 V), but above 200 V the copper's inner edge, 0.3 mm from the die, passes 1.2 kV/mm (2.6 kV/mm at 600 V, refined grid). Fields at the build point stay at or below about 1.0 kV/mm, against roughly 3 kV/mm for air (`VERIFY`). The NPT threads sit inside the flange, at +1 kV on both sides, with no field on them. Four tubes match the old array's 100 mm² of active silicon; one tube already beats its index.

| | |
|---|---|
| ID | S-02 |
| Addresses | A-29 (one detector per tube), the user's answers 1 and 6 of 2026-11-21 (tube sizes, top-copper bias, threads), R-39, R-47, R-75 |
| Method | S-01's axisymmetric (r, z) Laplace solver (`../S-01-chamber/field.py`), unchanged. The problem is linear: per tube, two unit fields (tube at 1 V, copper at 1 V) are solved and combined for each $V_{top}$. Field lines traced from 3,040 volume-weighted start points |
| Run | `.venv/bin/python sim/field/S-02-single-pd/run.py` (sweep, heatmaps, `summary.md`: about 4 minutes on the Intel Mac), then `points.py` (three points at h = 0.05 mm and both die sections, field-line plots: about 5 minutes). `run.py --plots` redraws from `sweep.json` |
| Outputs | `results/summary.md` (all 210 points), `results/sweep.json`, `results/points.json`, `results/run.out.txt`, `results/points.out.txt`, three SVG plots |

## Model

| Quantity | Value | Source |
|---|---|---|
| Tube IDs | 21 stainless pipe sizes, table below | ASME B36.19M via [Engineering ToolBox](https://www.engineeringtoolbox.com/ansi-stainless-steel-pipes-d_247.html), `VERIFY` against the standard |
| Tube and flange | One conductor at +1000 V: the pipe wall from the bore out, and the flange screwed on its thread, face flush with the pipe end | R-18 (`VERIFY` the final value); the user's answer 6 |
| Tube end above the board | 1.0 mm, set by the PTFE washer | `VERIFY` (A-23); as S-01 |
| Inner edge of the tube end | 0.5 mm radius | S-01's machining note; the user: rounded where reachable |
| Die | VTH2110, 5.67 × 5.67 × 0.30 mm, 5 × 5 mm active, at 0 V (CSA input) | VTH2110.json p1 |
| Die in the axisymmetric model | Disk of equal area (radius 3.20 mm) for the sweep; side (2.835 mm) and diagonal (4.01 mm) sections bound it at the three points | Claude's modelling choice |
| Active-area share | A landing at radius ρ counts by the share of the circle of radius ρ inside the 5 × 5 mm square (azimuthal average, as S-01's dead cross) | As S-01 |
| Top copper at $V_{top}$ | From 0.3 mm outside the die to 0.9 mm inside the bore | Detector-board note; S-01 point 5 |
| $V_{top}$ | 0, 20 (PD bias, A-04), 50, 100, 150, 200 (the HV board's 100–200 V transformer stage, A-20), 300, 400, 500, 600 V | Range chosen here: above 600 V the copper edge passes about 1.7 kV/mm at h = 0.1 mm |
| Tube length | 76 mm between two boards (A-23, R-05), so a symmetry plane at 38 mm; each detector serves 38 mm of tube | A-23 |
| Board | FR4 1.6 mm, εr 4.4, back copper 0 V | Typical, `VERIFY` |
| Grid | h = 0.1 mm for the sweep; 0.05 mm at the three points | S-01's grid study: fractions converge at 0.1 mm |

### Pipe sizes

Inner diameter = OD − 2 × wall. NPT thread height $0.8 \times$ pitch, from 18, 14 and 11.5 threads per inch (ASME B1.20.1, `VERIFY`).

| Nominal | OD (mm) | ID 80S (mm) | ID 40S (mm) | ID 10S (mm) | Thread height (mm) |
|---|---|---|---|---|---|
| 1/4 | 13.72 | 7.67 | 9.25 | 10.41 | 1.13 |
| 3/8 | 17.15 | 10.74 | 12.52 | 13.84 | 1.13 |
| 1/2 | 21.34 | 13.87 | 15.80 | 17.12 | 1.45 |
| 3/4 | 26.67 | 18.85 | 20.93 | 22.45 | 1.45 |
| 1 | 33.40 | 24.31 | 26.64 | 27.86 | 1.77 |
| 1-1/4 | 42.16 | 32.46 | 35.05 | 36.63 | 1.77 |
| 1-1/2 | 48.26 | 38.10 | 40.89 | 42.72 | 1.77 |

Schedule 10S is thin for a pipe thread: a 1.77 mm thread leaves 1.0 mm of a 1-1/4 in 10S wall. US Coast Guard rules forbid threading pipe thinner than standard weight ([46 CFR 56.30-20](https://www.ecfr.gov/current/title-46/chapter-I/subchapter-F/part-56/subpart-56.30/section-56.30-20)), which rules 10S out by that rule; whether threaded 10S fittings are sold is `VERIFY`. The 1/4 in sizes cannot hold the die: its corner (4.01 mm) plus clearance reaches past the copper's limit at 0.9 mm inside the bore.

## Checks

| Check | Result |
|---|---|
| Solver | S-01's analytic checks (coaxial cylinders 0.008 %, FR4 plates 0.6–1.1 %) still apply: the solver is the same file |
| Grid, three points | Active-area share at h = 0.1 and 0.05 mm: 77.9 / 78.1 %, 55.6 / 55.5 %, 68.8 / 68.7 %. Sharp-edge fields grow with refinement, as in S-01 (copper inner edge 577 → 853 V/mm at the build point) |
| Superposition | Two unit solves per tube combined linearly: exact for Laplace with fixed conductors |
| Square die | Side and diagonal sections bound the equal-area disk: 50.4–58.1 % at the build point (disk 55.5 %) |

## Results

![Heatmap of the interaction index per unit tube length, ID squared times the active-area share, over 21 pipe sizes and ten top-copper biases. It rises with tube size and with bias, from 24 square millimetres for 1/4 in schedule 80 to 1212 for 1-1/2 in schedule 10S at 600 V; the recommended 1-1/4 in schedule 40 at 200 V reads 684. Small tubes do not change with bias because they have no room for top copper.](results/heatmap-index.svg)

![Heatmap of the share of the gas volume whose field line ends on the active area. It peaks at 83 to 90 percent for 1/2 in to 3/4 in tubes and falls for larger tubes, 56 percent at the recommended point and 41 percent at 0 V there; for the smallest tubes it falls because most of a long narrow tube has no field.](results/heatmap-fraction.svg)

![Three half-sections with field lines. In today's 3/4 in tube at 20 V, most lines end on the die and those near the wall on the copper. In the 1-1/4 in tube at 200 V, the lines from the upper volume funnel onto the die and the lower outer third end on the copper. In the 1-1/2 in tube at 600 V the copper pushes more lines inward onto the die.](results/fieldlines-points.svg)

### Selected rows (h = 0.1 mm, $V_{top}$ = 200 V)

"Field-free" is the volume whose field line does not end within 200 mm of path: the middle of a long, narrow tube, where the board's field does not reach. Index per detector: the gas volume of 38 mm of tube times the share.

| Pipe | ID (mm) | To active area | To copper | Field-free | $ID^2 f$ (mm²) | Per detector (cm³) | Median transit (ms) |
|---|---|---|---|---|---|---|---|
| 1/2 40S | 15.80 | 83 % | 4 % | 8 % | 207 | 6.2 | 9.4 |
| 3/4 40S | 20.93 | 83 % | 11 % | 0.5 % | 362 | 10.8 | 9.1 |
| 1 40S | 26.64 | 73 % | 19 % | 0.1 % | 515 | 15.4 | 7.4 |
| 1-1/4 80S | 32.46 | 61 % | 29 % | 0 % | 643 | 19.2 | 6.9 |
| **1-1/4 40S** | **35.05** | **56 %** | **34 %** | **0 %** | **684** | **20.4** | **7.0** |
| 1-1/2 40S | 40.89 | 44 % | 45 % | 0 % | 733 | 21.9 | 7.3 |

Transit at a mobility of 2 cm²/(V·s) (`VERIFY`, as S-01).

### Fields at the three points (h = 0.05 mm, V/mm)

| Point | Die edge | Copper inner edge | Copper outer edge | Tube inner edge (0.5 mm radius) | Gap at the thread seam |
|---|---|---|---|---|---|
| 3/4 40S, 20 V | 284 | 126 | 805 | 1166 | 727 |
| **1-1/4 40S, 200 V** | **592** | **853** | **458** | **1014** | **724** |
| 1-1/2 40S, 600 V | 1608 | 2583 | 1425 | 886 | 722 |

Air breaks down at roughly 3 kV/mm at 1 atm in a uniform field (textbook value, `VERIFY`): a margin of about 3 at the build point, about 1.2 at the 600 V corner. Sharp edges are singular, so read these as the 50 µm grid's values.

### What it means

1. **Build point:** 1-1/4 in schedule 40, $V_{top}$ = +200 V. Its index is within 7 % of the largest schedule-40 tube's at 200 V and its share is 12 points higher. 200 V comes from the HV board's existing transformer stage (A-20) through an RC filter ([CSA rails](../../../docs/notes/csa-rails.md)), so no new supply.
2. **Index against share:** the share peaks at 83–90 % for 1/2 to 3/4 in tubes. Smaller tubes lose volume to the field-free middle (60 % of a 1/4 in schedule 80 tube); larger ones send more ions to the copper. The index ($ID^2 f$) still rises with size, but more slowly past 1-1/4 in: 1 → 1-1/4 in gains 33 %, 1-1/4 → 1-1/2 in gains 7 %.
3. **$V_{top}$:** no effect below 3/8 in schedule 40 (no room for copper). For 3/4 in and up, each 100 V adds about 1.5–7 points of share. 300–600 V would add up to 20 points at 1-1/4 in, at the cost of the copper-edge field (a question, `docs/questions/2026-11-21-single-pd.md`).
4. **Against the old array:** S-01's four dies in the 3/4 in tube put about 33 % of the gas volume on active silicon (99.5 % collected, 67 % of it on the dead cross): $ID^2 f \approx 21^2 \times 0.33 = 145$ mm². One die in today's 3/4 in tube at 20 V gives 341, in the 1-1/4 in tube at 200 V 684. Matching the old array's 100 mm² of active silicon takes four tubes; matching its index takes one.
5. **Threads (the user's answer 6):** the thread lies between the pipe and the flange, both at +1 kV: no field (0 V difference in the model). Its only contact with the gas is the seam at the pipe OD on the flange face, 3.56 mm out from the bore at 1-1/4 in schedule 40, in the 1 mm gap over the board, which has a uniform 0.72 kV/mm. A seam is a re-entrant corner, where the field is lower, not higher, if the face is machined flush and deburred. Covering it with the PTFE washer removes the gas gap there altogether.
6. **Leakage to watch:** 200 V on copper 0.3 mm from the die's contact puts a surface path straight into the CSA input. A 0 V guard trace in that gap (A-11's guard) takes the current; the clearance is a layout choice, simulate if it changes.

## Expected results (for the test plan)

| Measurement | Expected | From |
|---|---|---|
| Count rate, one die in a 1-1/4 in tube at 200 V, against the old four-die array in 3/4 in, same radon | About 4.7 times higher per tube | Point 4 |
| Count rate, $V_{top}$ 0 V against 200 V, same tube | About 1.4 times higher at 200 V (41 → 56 %) | Sweep |
| Leakage at the CSA input, $V_{top}$ on and off | No change with the guard trace | Point 6 |

## Not captured

- The square die in 3D: the equal-area disk and two sections only.
- Tube length: fixed at 76 mm between boards. A longer tube adds field-free volume in its middle; a manifold's cross fittings and gas ports are not modelled.
- Ion neutralisation, recoil, diffusion to the walls in the field-free middle, space charge, gas flow: as S-01.
- Surface charge on the bare FR4 and the PTFE washer; the PTFE washer's permittivity (modelled as gas).
- Breakdown itself and surface flashover: fields only.
