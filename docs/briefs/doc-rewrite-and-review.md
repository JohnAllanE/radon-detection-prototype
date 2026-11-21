# Brief: radon detection prototype, documents to the contract, then a review of where each design stands

For a fresh Claude session in this repo (`~/Documents/GBC projects/XLZD/radon-detection-prototype`, branch `main`, home Intel Mac), 2026-11-20. Written by the coordinating session at the user's request: "update the radon detector project to the new docs and review", delegated.

## What this repo holds

Two designs, written in October 2026 under the old phase-and-gate workflow, before the document contract existed:

1. **The radon detection prototype** (root `docs/`): detector boards (premium and low-cost CSA), MCU board, HV board, two chambers. Requirements DRAFT 2 (6,100 words), architecture DRAFT 1 (5,400 words, "gate not passed, the user has not reviewed it"), `parts/selection.md`, `decisions.md`, `sim/analytic/enc_budget.py`.
2. **The electrometer front end** (`electrometer/`): bench test equipment for the detector boards, self-contained, with its own IDs. Requirements DRAFT 3 (5,350 words, confirmed by the user 2026-10-20), architecture DRAFT 2 (3,200 words, awaiting the user's approval), `decisions.md`, `sim/analytic/budget.py`, SVG diagrams from `docs/diagrams/make_diagrams.py`. It moves to electronics-tools `bench-test-gear/` once built.

Treat them as two projects for the rewrite and give each its own review.

## Read first, in this order

1. Both `CLAUDE.md` files, then `RUN-LOG.md` (keep it updated after every document).
2. `$ELECTRONICS_TOOLS/reviews/2026-11-20-process-review/README.md` (section 1) and `brief-3-project-doc-rewrite.md`: this brief is brief 3 applied here, plus a review per design.
3. `$ELECTRONICS_TOOLS/pcb-design-workflow/PCB-WORKFLOW.md`, `DOCUMENTS.md`, `templates/`, `phases/1-requirements.md`, `phases/2-architecture.md` ("The last mile").
4. Finished examples: the fluorometer on electronics-tools branch `fluorometer` (`git -C "$ELECTRONICS_TOOLS" show fluorometer:bench-test-gear/fluorometer/docs/01-requirements.md`, also `02-architecture.md`, `CLAUDE.md`, `docs/reviews/pass-1.md`, `docs/notes/candidates-adc.md`; don't switch that repo's branch) and kitchen-scale v2 at `~/Documents/Personal projects/home-server/kitchen-scale/v2/` (its `docs/notes/candidates-*.md` are the surveys the user likes).
5. This repo's documents, all of them.

## Part 1: rewrite, one design at a time (the detector first, then the electrometer)

Follow brief 3's "Do", "Check" and "Report back", with these specifics:

- **IDs.** Keep `R-xx` as the requirement IDs (the workflow says projects that started with `R-xx` keep them until the user decides to convert). Keep `D-xx` decision IDs and `Q-xx` questions where they are cited. Every ID defined in the old documents survives somewhere: the document, a note, or `decisions.md`. The electrometer's IDs are local to its folder, and radon IDs are written "radon R-xx" there, as now.
- **Status column.** Give every requirement, choice and part the contract's firm / working / open status. "Confirmed by the user" rows are firm; `PROPOSED` rows are working; `TBD (Q-xx)` rows are open with the question in the pass review. Drop the `PROPOSED` and `TBD` legend.
- **Passes, not phases.** The detector's work so far is pass 1 with its architecture unreviewed; the electrometer's is pass 1 with requirements confirmed and the architecture awaiting approval. Say so in each `CLAUDE.md` status block (from `templates/project-CLAUDE.md`). The root `CLAUDE.md` is eight words now: make it the detector project's `CLAUDE.md`, and say that `electrometer/` is a second project with its own.
- **Diagrams.** The root documents hold Mermaid diagrams in code fences (requirements 4, architecture 2). Convert each to an SVG drawn by a new `docs/diagrams/make_diagrams.py` with `$ELECTRONICS_TOOLS/diagrams/svgdiagram.py`, following `$ELECTRONICS_TOOLS/readme.MD` "Diagrams" and the electrometer's existing script as the pattern. Formulas in LaTeX.
- **Candidate surveys.** `parts/selection.md` is a candidate table across every block, with no price or stock checks. Split the parts that shape the design into `docs/notes/candidates-<role>.md` (CSA op-amp, photodiode, ADC, mux and hold path, HV generation, MCU) from `templates/candidates.md`, stating what relies on each; rewrite `parts/selection.md` to the template. Don't look up prices or stock now: mark them open and list it as pass-2 work. Never invent a number.
- **Datasheets.** This repo keeps datasheet JSONs and some PDFs in `datasheets/`, where the workflow (`PCB-WORKFLOW.md` §2) puts them in the shared store `$ELECTRONICS_TOOLS/component-data/`. Don't move them: the shared repo changes only on its `main`, by the reviewer. Cite them as they are and list in the run log which parts should migrate (which already exist in `component-data/`, which are new).
- **Lint.** `python3 "$ELECTRONICS_TOOLS/pcb-design-workflow/tools/doclint.py" <project folder>` for the root and for `electrometer/`, to 0 findings; a `<!-- doclint-allow: <kind> — <reason> -->` line only where a finding is right to keep, each listed in the report.
- **Environment.** `sim/analytic/*.py` are the repo's runtime. If they need only the standard library, say so in a new root `MACHINES.md` (short: Shared section, this Mac's section from `uname -m` x86_64, macOS 13.7.8, the python used; leave the work Mac as "known so far"). If they import anything else, add `requirements.txt` and `.python-version` (3.12.15) per the user's Python rules and record the venv; read `~/Documents/system-config/machines/README.md` before installing anything (wheels only, uv at `~/.local/bin/uv`).

## Part 2: review where each design stands

Write `docs/reviews/pass-1.md` and `electrometer/docs/reviews/pass-1.md` from `templates/pass-review.md` (at most 600 words each, records): what pass 1 produced, what Part 1 changed, what to revisit in pass 2, the last mile (chambers, feedthroughs, board mounting, the cookie-tin test setup, cables and connectors: count every off-board wire), questions for the user, and open items against parts that would be ordered. Base "revisit" on each design's own open points: for the detector, the unreviewed architecture, the anode-side question of the VTH2110, the energy-resolution budget, the hold-node leakage `VERIFY` items, the HV board's fault-current limit; for the electrometer, the architecture approval, the ±5 V rails and the ADA4530-1 choice, the one source channel, the battery budget, and its dependence on the lab gateway for ESP-NOW (check `$ELECTRONICS_TOOLS/homelab/` for the gateway's current state and the bench power standard in `bench-test-gear/PROJECTS.md`: the electrometer is listed there as a bench-gear box that follows the standard). Don't start pass 2.

## Rules

- `PCB-WORKFLOW.md` "Standing instructions" apply. Never invent a number; mark unknowns `VERIFY`. Lose no fact: every number with a unit in the old documents survives, checked by script.
- **Commit** after each document (messages `Radon: …` or `Electrometer: …`), in this repo only. **Do not push.** Don't edit anything under `$ELECTRONICS_TOOLS` or `~/Documents/system-config`; list needed shared changes in the run log.
- Don't touch `sim/` results or `datasheets/`.
- Scratch scripts go in the session's scratchpad.

## Report back

At most 300 words: per document, words before and after and where the removed material went; the ID and number check results; the `VERIFY` items whose current truth was unclear; the datasheets to migrate; the commits; the questions for the user, per design.
