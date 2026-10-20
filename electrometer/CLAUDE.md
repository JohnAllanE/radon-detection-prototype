# Electrometer front-end (test equipment)

Bench electrometer for the radon project's detector (CSA) boards: DC current from 10 fA up to a small overlap with the DMM (about 1 µA), with optional charge and capacitance modes (D-01), plus a built-in ±50 V source. Tested in situ: the built chamber, its detector board and the electrometer in a grounded tin, with one probe cable moved between Murata switch connectors on the board (D-02). Battery powered, controlled over ESP-NOW through `lab-gateway`. Requirements: `docs/01-requirements.md`.

It lives inside the radon project until built (radon R-50), then moves to `$ELECTRONICS_TOOLS/bench-test-gear/`. Keep this folder self-contained: requirement, question and decision IDs here are local, and radon-project IDs are always written "radon R-xx".

## Workflow

Follow `$ELECTRONICS_TOOLS/pcb-design-workflow/PCB-WORKFLOW.md`, as the parent project does.

**Current phase:** 2 (architecture), `docs/02-architecture.md`. Gate: the user approves the topology and block-level specs. Phase 1 confirmed 2026-10-20.

## Project-specific facts

- The bench gear resolves nothing below about 1 nA (SDM3055 200 µA range; DP2031 readback 1 µA).
- Instrument rules apply to this board as to the SCPI instruments: Claude writes scripts and shows them; the user runs them (radon Q-23).
- Electrometer op-amp candidate: ADA4530-1 (datasheet extract in the parent project's `datasheets/`; choice confirmed in phase 3).
