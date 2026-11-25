# Radon detection prototype

| | |
|---|---|
| Project | Alpha detection with silicon photodiodes: radon progeny in a 1 kV chamber (Part 1), weld samples in rough vacuum (Part 2). Four single-diode probes, different preamps, one four-channel MCU board |
| Pass | 1, a sketch of the detector, MCU and HV boards and both chambers, ended by `docs/reviews/pass-1.md` |
| Activity | Pass 1 accepted. Field simulations S-01 to S-03 done. Four-probe plan, on-probe test pulse and scope outputs recorded. No hard stop near |
| Next for the user | Sketch the thin-plate seal; confirm R-47 (0 V board). |
| Next for Claude | Pass 2: CSA ngspice models (four types, JFET pair stability), test-pulse and monitor parts, hold chain, HV board, prices and stock |
| Open `VERIFY` items | Notes, the architecture, `parts/selection.md` Open |

## Workflow

Follow `$ELECTRONICS_TOOLS/pcb-design-workflow/PCB-WORKFLOW.md`. Tier: full (analog, high voltage, vacuum).

`electrometer/` is a second project in this repo, with its own `CLAUDE.md` and local IDs. Here its IDs are written "electrometer R-xx".

## Rules

- Requirement IDs stay R-xx until the user decides to convert. R-57 to R-72 of the retired electrometer outline are not live (`docs/notes/electrometer-outline.md`).
- Instruments: Claude writes scripts and shows them, the user runs them. This includes the electrometer (Q-23).
- Effort goes into building and then measuring, not characterising everything in advance (D-13).
- Expected outcome of the comparison is "similar" (R-53). Don't add premium capability that won't show in the spectrum or the test-pulse width.

## Facts

- The user machines the chambers.
- Boards will be separate KiCad projects sharing one project-local library.
- Datasheet extracts are in `datasheets/<MPN>.json` (some PDFs committed, see `.gitignore`), pending migration to `$ELECTRONICS_TOOLS/component-data/`.
- Analytic budgets: `sim/analytic/enc_budget.py`. Diagrams: `python3 docs/diagrams/make_diagrams.py` (needs `ELECTRONICS_TOOLS`). Tool versions: `MACHINES.md`.
- History: `docs/decisions.md`. Background and calculations: `docs/notes/`. Papers and manuals: `docs/references/` (only CC-licensed PDFs committed). Run log for delegated work: `RUN-LOG.md`.
