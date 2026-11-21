# Run log: radon detection prototype (detector and electrometer)

Kept per the shared rules for long or delegated work. A new session reads this first, then `docs/briefs/`.

## Goal

Rewrite both designs' documents to the document contract (brief: `docs/briefs/doc-rewrite-and-review.md`, Part 1), then a pass-1 review for each (Part 2).

## Standing instructions

- Commit after each document; don't push (the reviewer does). This repo only.
- Shared-repo changes (component-data migration, PROJECTS.md) are listed below, not made.

## Done

- 2026-11-20: repo level with GitHub at 12943f4 (last work 2026-11-15). Brief and this log written by the coordinating session.
- 2026-11-20: detector requirements to the contract, 0d583d5 (6,103 → 1,580 words; 5 numbers carried to the architecture commit: 0.14 keV, 100 cycles, 2.5 mm, 20 mm, 200 V).

## Running

- Part 1, detector: architecture next (with candidate notes and diagrams). Fact-check script: scratchpad `factcheck.py` (IDs and numbers with units against commit ea7fd29).

## Next

- Part 1, detector documents; Part 1, electrometer documents; Part 2 reviews.

## Decisions made while the user was away

- Detector R-xx kept and sorted into functions, objectives and constraints; new R-73 (build effort). Words allowance on the requirements (55 rows).
- Electrometer outline (old requirements 4.7, R-57 to R-72, Q-27 to Q-37) retired to a note: it reused R-57 to R-60.
- Q-02, Q-08, Q-10, Q-13 reopened: listed as answered, but no answer was recorded.

## Shared-repo changes for the reviewer

- (none yet)

## Waiting on the user

- (from the reviews' questions)
