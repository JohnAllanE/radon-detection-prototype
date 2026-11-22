# Brief: radon detector, record the user's answers, field simulation, and write the open questions with context (2026-11-21)

For a fresh Claude session in this repo (`main`), home Intel Mac. The user answered part of the detector's open questions (requirements Q-xx) and of `docs/reviews/pass-1.md`'s questions on 2026-11-21. Their words, then what to do.

## The user's answers (verbatim, lightly trimmed)

Requirements questions:
- **Q4:** decide after first runs, but the target is to discriminate between the different members of the decay chain from radon.
- **Q12:** "I don't know what you mean by asking for the creepage and clearance rule, but my thought is to make the tube non-touchable by an insulated outer enclosure and an interlock. If the PDs also respond to ambient light, that could be a second check (inside must be dark enough); other approach welcome."
- **Q14:** a check source from a smoke alarm (Am-241), used tentatively until it can be measured in a RAD7 and used as a transfer standard. Read the kV by a divider; no HV probe on hand.
- **Q17:** unknown; open to suggestion; low cost first: this is preliminary work for a later funded effort.
- **Q2:** "What parameters would you like? It is not monitored."
- **Q8:** 8 channels; CAD 20 average per channel is the ceiling, CAD 10 preferred. If the best parts are out of reach at that average (even offset by the low-cost probe), limit them to 1–2 channels rather than 4 per probe, but proceed assuming 4 identical channels per probe; populating only a few channels at first is acceptable.
- **Q10:** high accuracy of the HV isn't needed: enough gradient for ions to flow. Reading it back is more important, and even that can wait for an HV probe bought in a funded effort.
- **Q13:** BGAs are out; every other package is acceptable; QFN at 0.5 mm pitch has been fine.

Pass-1 review questions:
- **1 (architecture review):** the user is satisfied the architecture is right as long as the requirements don't change: treat it as accepted.
- **4:** one MCU board handles all 8 CSA inputs; the peak-detect circuit is there so the MCU can handle closely spaced events.
- **6 (die-to-wall gap):** set up a 2D electric-field simulation with the surfaces at their voltages, to see the field lines; the spacing is arbitrary and can be whatever works. The simulation should also show whether a sloped surface at a moderate voltage, partly shielding the PCB, helps. The aim is field lines passing through the photodiodes.
- **The rest:** "I'm not equipped to answer them as written: do a larger write-up with context if they are necessary."

## Do

1. **Record the answers** in place: `docs/01-requirements.md` (each Q resolved, its requirement's status set: user answers are firm, targets the user leaves open stay working), `docs/02-architecture.md` (architecture accepted: the user's own choices firm; one MCU board for 8 inputs; the HV accuracy and readback position; the cost ceiling per channel as a constraint with the 1–2 premium channel fallback), `docs/decisions.md` (one entry for the answers), the review's questions (answers appended). For Q4, turn "discriminate the decay chain" into numbers with sources: the alpha energies of Po-218, Po-214 and Po-210 (and Rn-222 itself) from a cited nuclear-data source, and the energy resolution that separates them, against the R-09 100 keV target and the ENC budget's 4–14 keV. For Q14, Am-241's alpha energy and what a smoke-alarm source's activity typically is (cited), and how a resistive divider reads 1 kV safely (ratio, resistor voltage rating, creepage: link to Q12). For Q12, explain creepage and clearance in a sentence each and set the working rule from a cited standard (IEC 60664-1 or IPC-2221 for about 1 kV) as working, with the user's enclosure + interlock + darkness check as the touch-safety approach.
2. **2D electrostatic field simulation, S-01 or the next free S-number** in `sim/field/` (the workflow's place for field work): an axisymmetric (r, z) Laplace solution for the chamber tube at +1 kV (`VERIFY` the value in the requirements), the detector board and photodiodes at their bias, the board's ground and ring electrodes, the O-ring land and the gap from die corners to the wall (2.1–2.6 mm now, as a parameter), and the user's option of a sloped intermediate electrode at a moderate voltage. Show field lines and where ions starting in the gas volume end up (the field-line endpoints approximate ion paths at these speeds; say so). Python with numpy and matplotlib: this repo has no venv: create one per its `MACHINES.md` and the user's rules (uv at `~/.local/bin/uv`, `.python-version` 3.12.15, `requirements.txt`, wheels only; read `~/Documents/system-config/machines/README.md` first) and record it in `MACHINES.md`. A finite-difference relaxation on a grid is enough; mark the grid resolution's effect. Plots as SVG, a `README.md` in the simulation's folder per the workflow's simulation playbook (`$ELECTRONICS_TOOLS/pcb-design-workflow/phases/4-simulation.md`), results summary. Answer: does a field line from most of the gas volume end on a photodiode, how the gap and the sloped electrode change that, and the field strength at the board edge (for Q12's breakdown margin).
3. **Write the remaining open questions with context**, per the new rule in `$ELECTRONICS_TOOLS/pcb-design-workflow/PCB-WORKFLOW.md` ("Technical questions carry their context"; example: `~/Documents/Personal projects/fluorometer/docs/questions/2026-11-21-sink-loop.md`): `docs/questions/2026-11-21-detector.md` with, per question still open (including Q2 with the parameters you'd propose and why, and the review's questions 2, 3, 5, 7, 8), a small SVG diagram from a script beside it (house style, `$ELECTRONICS_TOOLS/diagrams/svgdiagram.py`), the finding in plain terms, the options and their costs, a recommendation, and a decision table at the end. Drop any question whose answer a simulation or a datasheet can settle: settle it instead and record it. Do the same for the electrometer's review questions (`electrometer/docs/reviews/pass-1.md`) in `electrometer/docs/questions/2026-11-21-electrometer.md`, unless the answers above already settle them.

## Rules

`PCB-WORKFLOW.md` standing instructions. Never invent a number: cite or mark `VERIFY`. Values a simulation determines are adopted without asking (the user's rule). Commit after each numbered step (`Radon: …`), this repo only, files by name; don't push. Update `RUN-LOG.md` in each commit. doclint 0 findings for the root and `electrometer/`. Render and look at every diagram (headless Chrome, light and dark).

## Report back

At most 300 words: what was recorded, the field simulation's answer (with the key numbers), the questions documents and how many questions each holds, the venv, the commits.
