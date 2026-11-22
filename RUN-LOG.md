# Run log: radon detection prototype (detector and electrometer)

Kept per the shared rules for long or delegated work. A new session reads this first, then `docs/briefs/`.

## Goal

- 2026-11-21: the user's answers, the 2D field simulation, and the open questions written with context (brief: `docs/briefs/pass-1-answers.md`).

Rewrite both designs' documents to the document contract (brief: `docs/briefs/doc-rewrite-and-review.md`, Part 1), then a pass-1 review for each (Part 2).

## Standing instructions

- Commit after each document; don't push (the reviewer does). This repo only.
- Shared-repo changes (component-data migration, PROJECTS.md) are listed below, not made.

## Done

- 2026-11-20: repo level with GitHub at 12943f4 (last work 2026-11-15). Brief and this log written by the coordinating session.
- 2026-11-20: detector requirements to the contract, 0d583d5 (6,103 → 1,580 words; 5 numbers carried to the architecture commit: 0.14 keV, 100 cycles, 2.5 mm, 20 mm, 200 V).
- 2026-11-20: detector architecture, a2658a8 (5,427 → about 1,990 words; 11 notes, 6 candidate surveys, 3 SVGs from the Mermaid blocks). Part selection, 0e323ec. MACHINES.md, 60db0d0. CLAUDE.md, a2d70f6. Detector check: all IDs and numbers present (one false positive, the heading "2.4 Why").
- 2026-11-20: electrometer requirements, 303daf6 (4,896 → 1,336 doclint words). Architecture, be8f48b (2,882 → 1,870). CLAUDE.md, d0982aa. All IDs and numbers present.
- 2026-11-20: pass 1 reviews for both designs, 1d6dab5 and 10bcf6f. doclint 0 findings for the root and `electrometer/` (one `words` allowance on each requirements file).
- 2026-11-21 step 3: questions with context, detector (6, plus OPA657 settled from its datasheet and the LMP7721 1.8–5.5 V supply found) and electrometer (5; Q-04, Q-10, Q-15 settled). Diagrams rendered light and dark. doclint 0 for the root and `electrometer/`.
- 2026-11-21 step 2: S-01 field simulation (`sim/field/S-01-chamber/`), `.venv` built (numpy 2.5.5, scipy 1.18.1, matplotlib 3.11.2), architecture A-10 and risk 1, decisions entry. 95–99 % of ions reach the dies, about two-thirds where the dies meet, peak 1.5 kV/mm at the tube edge.
- 2026-11-21 step 1: the user's answers recorded (requirements R-74, R-75, architecture A-27, A-28, decisions, review, notes `decay-chain-lines.md` and `hv-spacing-and-readback.md` with NuDat and NRC sources). doclint 0.

## Running

- Nothing running. The 2026-11-21 brief is complete (steps 1–3 committed); nothing pushed.

## Next

- The user answers `docs/questions/2026-11-21-detector.md` (6) and `electrometer/docs/questions/2026-11-21-electrometer.md` (5). Then pass 2.

## Decisions made while the user was away

- Detector R-xx kept and sorted into functions, objectives and constraints; new R-73 (build effort). Words allowance on the requirements (55 rows).
- Electrometer outline (old requirements 4.7, R-57 to R-72, Q-27 to Q-37) retired to a note: it reused R-57 to R-60.
- Q-02, Q-08, Q-10, Q-13 reopened: listed as answered, but no answer was recorded.
- Architecture choice IDs A-01 to A-26 introduced (the old draft had none). A-21 (HV series resistance ≥ 10 MΩ) open, from the electrometer.
- New architecture question 9: one MCU board per detector board, or one eight-channel board (the chain is drawn for four channels).
- Quantities in parts/selection.md assume 4 detector boards.
- Electrometer diagram script left on its own style copy (not svgdiagram.py): rewriting it risks the drawings; pass-2 item.

## Shared-repo changes for the reviewer

- Migrate `datasheets/*.json` (and PDFs) to `$ELECTRONICS_TOOLS/component-data/`, adding an `evaluations` entry for this project. Already there: ADS1220, ADS8689, TLV3201 (merge evaluations). Close relatives there: ESP32-S3-WROOM-1U-N16R8 (this repo has the -1 module), TLV9002 (this repo has TLV9001). New: ADA4530-1, ADA4817-1, CR-110-R2.1, ESP32-S3-WROOM-1, LM27762, LMP7721, OPA140, OPA656, OPA657, TLV9001, TLV9061, TMUX1101, TMUX1104, VTH2110 (VTH2110, ADA4530-1, ADA4817-1 PDFs have no stable download).
- `bench-test-gear/PROJECTS.md`: radon entry's status can say documents rewritten and pass 1 reviewed (both designs).

## Waiting on the user

- Detector (`docs/reviews/pass-1.md`): architecture review, D-16 to D-18 and an ADA4817-1 test, OPA657 tier, MCU boards per detector board, the unrecorded Q-02/Q-08/Q-10/Q-13 answers, the die-to-wall gap, A-21 HV series resistance, R-xx conversion.
- Electrometer (`electrometer/docs/reviews/pass-1.md`): A-06 self-test, A-18, Q-14 antenna, battery vs GX12 input, USB console for bring-up until the gateway carries ESP-NOW, Q-09 budget.
