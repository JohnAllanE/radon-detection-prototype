# Brief: radon detector, the user's answers to the detector questions, and a single-detector field sweep (2026-11-21)

For a fresh Claude session in this repo (`main`), home Intel Mac. The user answered `docs/questions/2026-11-21-detector.md` on 2026-11-21. Record the answers, then run the new simulation.

## The user's answers

1. **Ions centre themselves (the S-01 finding).** The user's earlier assumption, more photodiode area to "cast a wide net", is undone by the field funnelling ions to the axis, where four packed dies meet at gaps and dead borders; economical 10 × 10 mm detectors weren't found. **New direction, to evaluate:** one detector per tube, centred on the axis; more area means more tubes in parallel, each with its own detector and CSA (a probe with one channel; the board need not be much smaller, only less on it). The alternative, a large board with several widely spaced detectors under an array of tubes, the user considers an assembly headache for little gain. Side effect: a premium probe no longer needs four premium op-amps; four tubes could even carry four different op-amp candidates.
   **Chamber construction (user):** 304 or 316 stainless NPT pipe and cross fittings (the user wrote "304/306ss": 306 is not a common grade, so take 316 and mark `VERIFY`), forming a manifold of tubes that is the interior volume, with one overall inlet and outlet. So tube inner diameters are limited to standard pipe sizes.
2. **ADA4817:** about CAD 13 (SOIC; the QFN is CAD 11): doable, at the top of the budget; the user prefers the SOIC for leakage. The LMP7721's 1.8–5.5 V supply is no concern: the driver board builds its rails. The user asks about a programmable low-noise rail: TI's LDO with output-setting resistor pins that could be switched by a shift register (that is the ANY-OUT family, TPS7A47 positive and TPS7A33 negative, `VERIFY`), or a buffer amplifier as the rail, and what is best practice at this performance level. Answer that in the architecture or a note, with sources: LDO noise and PSRR against the CSA's sensitivity, and whether a programmable rail is needed at all.
3. **The HV series resistor (A-21):** agreed as proposed.
4. **Q-02 (environment):** measurements inside the chamber air were agreed to be problematic, but ambient RH and temperature on the PCB, in room air, is fine; and an instrument of this calibre should carry whatever environmental sensors help compensate or track important factors. If there is an RH/T sensor with a tube (flow-through) interface, the inlet or outlet air can be piped through it during purge cycles: include it (candidates, cited).
5. **Q-17:** option (a), for now.
6. **Q-20 (chamber mechanics):** a mounting flange screwed onto the pipe threads, the end machined parallel; the chamber's edges rounded where reachable, but the threads are pointed: they sit outside the inner chamber, so check in the simulation that they are far enough from the field region to matter. O-ring in a machined triangular groove; a machined PTFE washer sets the O-ring compression.

## Do

1. **Record the answers** in the requirements, architecture (the single-detector-per-tube option as a proposal A-xx beside the current array, with its consequences: channels per probe, op-amp candidates per tube, the manifold), decisions, and the questions document's decision table. Settle item 2's rail question in a short note with sources. Item 4: candidate RH/T sensors, on-board and flow-through, cited.
2. **S-02: single-detector sweep**, in `sim/field/S-02-single-pd/`, reusing S-01's solver (`sim/field/S-01-chamber/field.py`), axisymmetric. Geometry: one detector (the VTH2110, 5.67 mm die, 5 mm active area; cite its extract) centred on the axis at the tube's end; the board's exposed top copper around it held at a bias V_top; the tube at its HV (as S-01); the threads and flange outside the inner chamber as the user describes, with their distance from the field region checked once. Sweep:
   - **Tube inner diameter:** the standard stainless pipe sizes the user could buy, 1/4" to 1-1/2" NPT, schedules 10, 40 and 80 where they exist (cite a pipe dimension table; list nominal size, schedule, ID).
   - **V_top:** from 0 V up to a value that pushes ions off the copper and onto the die, a range chosen and justified (at least 0 to +200 V, in about 10 steps; the PD's own bias as one point).
   For each pair compute the fraction of field lines from the gas volume that end on the active area, and the user's **interaction index**: interior volume times that fraction, with no units (state the tube length assumed: the index per unit length is ID² times the fraction, which ranks the same). Produce the **heatmap**, ID on one axis and V_top on the other, coloured by the index, plus the fraction alone as a second heatmap, and the field-line plots for three representative points. Also report: the field strength at the die edge and at the copper edge for the chosen points (breakdown margin), and how far the threads are from the field region.
   Interpret: which ID and V_top the user should build around, how the index trades against the fraction (a big tube catches more volume but funnels a smaller share onto one 5 mm die), and how many tubes in parallel match the old four-die array's area.
3. **Write any genuine trade-off left as a question** in the established format (`docs/questions/<date>-<topic>.md`: diagram, plain finding, options and costs, recommendation). Values the simulation settles are adopted, not asked.

## Rules

As in `docs/briefs/pass-1-answers.md`: the venv exists (numpy, scipy, matplotlib); never invent a number (cite or `VERIFY`); commit after each step, files by name, don't push; RUN-LOG.md in each commit; doclint 0; render and look at every plot (you can read images).

## Report back

At most 300 words: what was recorded, the rail answer, the RH/T candidates, the sweep's result (best ID and V_top, the index and fraction there, field margins), the heatmap paths, the commits, and any question left.
