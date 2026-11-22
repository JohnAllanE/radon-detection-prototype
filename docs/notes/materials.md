# Materials for a low-background alpha chamber

**Conclusion:**

- Inside or near the gas volume, prefer 304 or 316 stainless, PTFE, OFHC copper and clean ENIG. Use aluminium only where a surface can't see the die, or is covered.
- Avoid brass and any leaded alloy, Sn-Pb solder, and rubber, silicone or nitrile seals. Viton is the least bad O-ring elastomer.
- Why: lead carries Pb-210, whose daughter Po-210 emits at 5.30 MeV, the line this project separates from Rn-222 (`decay-chain-lines.md`). U and Th traces add alphas from 4 to 9 MeV. Elastomers pass or emanate radon.
- **The flange (the user's question): aluminium, not brass.** Sitting outside the inner chamber lowers the stakes but doesn't remove them: the flange face inside the O-ring shares the gas volume through the 1 mm gap and has a grazing line of sight to the die. With the PTFE washer covering that face either would do, but aluminium carries no lead and leaves no leaded chips.

**Relied on by:** R-11, R-30, R-39, R-54, A-23, A-24, A-29, D-25, standard-item choices.

## Working

### Why materials matter here

- Any alpha from a surface the die can see, or radon a material releases into the gas, adds counts the RAD7 transfer would not know about.
- Alpha range: a few centimetres in air at these energies, tens of µm in solids (`VERIFY`). So only surfaces with a line of sight to the die matter for direct alphas; a thin cover stops them. Radon from a material reaches the die anywhere the gas reaches.
- Surface contamination counts as much as bulk: radon progeny from room air plate out on every surface, and Pb-210 (22 years) stays (PNNL, [Pb-210 on copper surfaces](https://arxiv.org/abs/2003.06357)). Store parts sealed, clean before assembly.

### Materials

| Material | Use here | Concern | Verdict | Source |
|---|---|---|---|---|
| 304 or 316 stainless | Pipe, crosses, valves | Low U/Th in typical stock, but steel is screened case by case | Use: the chamber wall. Clean and possibly etch (A-23) | Screened in low-background programmes ([nEXO radioassay](https://arxiv.org/pdf/2604.15406)); values `VERIFY` |
| Aluminium (6061 and similar) | Flange, Part 2 chamber (R-46) | U and Th around 100 ppb in standard material, alpha-emitting surface; low-U/Th grades exist, 2–3 orders cleaner | Use where it can't see the die, or cover it | [Alpha emission from aluminium impurities](https://arxiv.org/pdf/1507.00607); [ultra-pure Al](https://jp4.journaldephysique.org/10.1051/jp4:1995708) |
| Brass, leaded alloys, lead solder | Fittings, flanges, nuts | Lead carries Pb-210, hence Po-210 alphas at 5.30 MeV. Leaded brass also sheds lead in machining | Avoid inside or near the volume | Pb-210 in lead as a background: [Pb-210 copper study and refs](https://arxiv.org/pdf/1707.06413); brass values `VERIFY` |
| OFHC copper | Small parts, shields | Pb-210 17–40 mBq/kg in bulk (XMASS samples); surface Pb-210 from radon exposure | Good; clean surfaces | [XMASS copper](https://arxiv.org/pdf/1707.06413), [PNNL](https://arxiv.org/abs/2003.06357) |
| PTFE | Washer, tubing, valve seats, filter membranes | Low emanation, a standard low-background plastic; cold-flows under load | Use | Low-background use: [Low Background Materials and Assay](https://arxiv.org/pdf/1311.3311), `VERIFY` values |
| Polypropylene | Syringe filter bodies (A-24) | Outside the chamber, upstream; R-30 allows it | Use upstream | R-30, D-25 amended |
| Viton (FKM) | Chamber O-rings | Lowest radon permeability of the common elastomers; a PTFE-encapsulated Viton O-ring measured below 1.2 atoms/min of radon | Use; PTFE-encapsulated if available | DRIFT-II, [radon emanation and mitigation](https://arxiv.org/pdf/1407.3938) |
| Nitrile (NBR) | | A nitrile door seal measured 7.2 atoms/min of radon | Avoid | DRIFT-II, same |
| Silicone | | High radon permeability (about 650 × 10⁻⁹ cm³(STP)·cm/(s·cm²·cmHg), an extrapolated estimate) | Avoid (R-30) | [US patent 5194158](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/5194158) |
| EPDM, butyl, natural rubber | | Natural rubber has the highest radon diffusion of the polymers listed (6.36 × 10⁻⁶ cm²/s); butyl lets noble gases through more than Kapton or nylon; EPDM: no data found | Avoid | Same patent; [noble-gas permeation](https://arxiv.org/pdf/0909.2610); EPDM `VERIFY` |
| Solder and flux exposed to the volume | Die attach area, board | Sn-Pb solder carries Pb-210; low-alpha solders exist for that reason. Flux residue is a leakage path | No solder on the chamber side; conductive epoxy for the die (A-03); clean (A-11) | Low-alpha solder: JEDEC JESD221 (`VERIFY`); flux: ADA4530-1.json p38 |
| FR4 and solder mask | The board's chamber face | Glass fibre and fillers carry K, U and Th at some level, not screened here | Acceptable: the die sits on it already. Keep the bare area small; ENIG copper is cleaner | `VERIFY`: no screening found |
| Desiccants | Gas train (A-24) | Molecular sieves emanate radon at levels unsuitable for sensitive work; Drierite (CaSO₄) not screened | Drierite upstream, behind the final filter (D-02); no molecular sieve in the chamber's path | [Low-radioactivity molecular sieves](https://arxiv.org/pdf/1910.02617); Drierite `VERIFY` |

### The flange in detail

- Its face between the pipe OD and the O-ring is inside the sealed volume, 1 mm above the board (A-23). From there, radon emanation (small area) and grazing alphas reach the die; the PTFE washer stops the alphas.
- Brass would put a Po-210 line on the one being measured; aluminium's U/Th alphas depend on the stock and are stopped by the washer.
- Practical (`VERIFY`): aluminium on stainless corrodes galvanically only with moisture, and the chamber is dry. Stainless on stainless galls, needing anti-seize near the volume.
