# Electrometer front end (test equipment)

| | |
|---|---|
| Project | A battery-powered bench electrometer for the radon detector boards: DC current from about 1 µA down to 10 fA, in situ in a grounded tin, ±50 V source, ESP-NOW control |
| Pass | 1, a sketch of the head, range panel, source, control and power, ended by `docs/reviews/pass-1.md` |
| Activity | Pass 1: requirements confirmed by the user, architecture awaiting approval. No hard stop near |
| Next for the user | Approve the architecture (A-06 self-test, A-18 HV series resistance). Answer the pass 1 review's questions |
| Next for Claude | Pass 2: S-01 head and S-02 source simulations, part selection, the battery budget with real draws |
| Open `VERIFY` items | The notes, the architecture, `docs/notes/proposed-targets.md` |

## Workflow

Follow `$ELECTRONICS_TOOLS/pcb-design-workflow/PCB-WORKFLOW.md`. Tier: full (femtoamp analog, HV nearby).

## Rules

- Keep this folder self-contained: requirement, question, decision and choice IDs are local. Radon-project IDs are always written "radon R-xx" (the parent project is the repo root).
- It lives in the radon repo until built (radon R-50), then moves to `$ELECTRONICS_TOOLS/bench-test-gear/`.
- Instrument rules apply to this board as to the SCPI instruments: Claude writes scripts and shows them, the user runs them (radon Q-23).

## Facts

- The bench gear resolves nothing below about 1 nA (SDM3055 200 µA range, DP2031 readback 1 µA).
- Control goes through `lab-gateway` over ESP-NOW. The homelab gateway is on hold before its phase 3, and the gateway HAT with the ESP-NOW bridge is still being designed.
- Electrometer op-amp candidate: ADA4530-1, datasheet extract in the parent repo's `datasheets/`.
- Budgets: `sim/analytic/budget.py` (standard library). Diagrams: `python3 electrometer/docs/diagrams/make_diagrams.py`. Tool versions: the repo root's `MACHINES.md`.
- History: `docs/decisions.md`. Background and calculations: `docs/notes/`.
