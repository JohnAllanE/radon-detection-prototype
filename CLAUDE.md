# Radon detection prototype

| | |
|---|---|
| Project | Alpha detection with silicon photodiodes: radon progeny in a 1 kV steel chamber (Part 1) and weld samples in rough vacuum (Part 2), premium against low-cost detector boards |
| Pass | 1, a sketch of the detector, MCU and HV boards and both chambers, ended by `docs/reviews/pass-1.md` |
| Activity | Pass 1 architecture accepted by the user, answers recorded. Field simulation S-01 and the questions with context under way. No hard stop near: no part is ready to order |
| Next for the user | Answer `docs/questions/2026-11-21-detector.md` and the electrometer's |
| Next for Claude | Pass 2: CSA ngspice model, hold-chain simulation, HV board architecture, prices and stock |
| Open `VERIFY` items | Notes, the architecture, `parts/selection.md` Open |

## Workflow

Follow `$ELECTRONICS_TOOLS/pcb-design-workflow/PCB-WORKFLOW.md`. Tier: full (analog, high voltage, vacuum).

`electrometer/` is a second project in this repo, with its own `CLAUDE.md` and local IDs. Here its IDs are written "electrometer R-xx".

## Rules

- Requirement IDs stay R-xx until the user decides to convert. R-57 to R-72 of the retired electrometer outline are not live (`docs/notes/electrometer-outline.md`).
- Instruments: Claude writes scripts and shows them, the user runs them. This includes the electrometer (Q-23).
- Effort goes into building and then measuring, not characterising everything in advance (D-13).
- Expected outcome of the comparison is "similar" (R-53). Don't add premium capability that won't show in the spectrum.

## Facts

- The user machines the chambers.
- Boards will be separate KiCad projects sharing one project-local library.
- Datasheet extracts are in `datasheets/<MPN>.json` (some PDFs committed, see `.gitignore`), pending migration to `$ELECTRONICS_TOOLS/component-data/`.
- Analytic budgets: `sim/analytic/enc_budget.py`. Diagrams: `python3 docs/diagrams/make_diagrams.py` (needs `ELECTRONICS_TOOLS`). Tool versions: `MACHINES.md`.
- History: `docs/decisions.md`. Background and calculations: `docs/notes/`. Run log for delegated work: `RUN-LOG.md`.
