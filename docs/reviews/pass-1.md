# Radon detection prototype: pass 1 review

| | |
|---|---|
| Pass | 1: a sketch of the detector, MCU and HV boards and both chambers |
| Date | 2026-11-20 |
| Covered | Intent, candidate parts, architecture (unreviewed), analytic ENC budget. No simulation or schematic |
| Next pass | CSA and hold-chain simulation, the HV board's architecture, prices and stock |

## Changed in earlier documents

| Document | What changed | Decision |
|---|---|---|
| Requirements | Rewritten to the contract, R-xx kept, R-73 added, Q-02, Q-08, Q-10, Q-13 reopened | 2026-11-20: Requirements rewritten |
| Requirements 4.7 | Electrometer outline retired to a note. Its R-57 to R-60 clashed with live IDs | 2026-11-20: The first electrometer outline is retired |
| Architecture | Choices A-01 to A-26, Mermaid to SVG, budgets to notes | 2026-11-20: Architecture rewritten |
| Part selection | One row per function, six candidate surveys | 2026-11-20: Part selection to the template |
| `CLAUDE.md`, `MACHINES.md` | Pass 1 status | 2026-11-20: Project CLAUDE.md |

## Revisit next pass

1. Architecture: not reviewed by the user. A-xx stay working until then, except the user's own choices.
2. Q-11, A-03, A-04, A-10: which VTH2110 face is the anode. It sets bias, pulse and ring polarity and which pad is the CSA input. A DMM diode test on a spare chip, before any layout.
3. R-09: the electronics give 4–14 keV against 100 keV, from a model without 1/f noise or CR-RC^n. An ngspice `.noise` run, and a dead-layer and straggling estimate from NIST ASTAR, decide whether the premium board can show anything (R-53).
4. A-16: hold-node leakage `VERIFY`s (BAS116, TLV906x maximum bias, $C_{hold}$ absorption, TMUX1101 polarity) against 80 pA. Simulate the hold chain (risks 5, 9).
5. A-20, A-21: the HV board has topology only. Its fault-current limit (≥ 10 MΩ, from the electrometer) and the ripple limit (R-19, needs C(tube → input)) come first.
6. Architecture question 9: one MCU board per detector board, or one eight-channel board.
7. Detector board outline: the electrometer quotes "≤ 20 mm", but it must cover a 21–22 mm bore and O-ring land.

## Last mile

- **Part 1 chamber:** tube end mounts, O-ring land, board clamping, insulating standoffs, PTFE insulating sections: not designed (Q-20).
- **Touch-safe enclosure** around the +1 kV tube and an HV feedthrough to it (A-22): not designed.
- **Part 2 chamber:** 50 mm ID body, NW25 port and tee, sample holder, foreline trap: not designed.
- **Cookie-tin test setup:** in the electrometer's review. The detector board carries the SWF ports and breakout lines.
- **Wires per chamber:** two 14-pin PicoBlade cables (28), HV and return (2), two adapter leads (4), TEST (2), USB: at least 36 conductors and 5 connectors. PD bias and ring routing from the HV board is open.
- **MCU and HV board enclosures:** none yet.

## Questions for the user

1. Review the architecture? Working answer: A-xx as written.
2. Accept D-16 to D-18, and buy one or two ADA4817-1 for a single-channel noise test? Working answer: LMP7721 premium, no ADA4817-1.
3. OPA657 as a third tier? Working answer: no.
4. One MCU board per detector board? Working answer: yes, four channels each.
5. Answers to Q-02, Q-08, Q-10, Q-13, never recorded? Working answer: lab ambient, no cost target, load current open, hand assembly.
6. Is a 2.1–2.6 mm die-to-wall gap acceptable? Working answer: yes, with R-43.
7. The HV board's ≥ 10 MΩ series resistance (A-21)? Working answer: yes.
8. Convert R-xx to F/O/C? Working answer: keep R-xx.

## Parts to order

No order planned: prices, stock and suppliers are unchecked.

| Part | Open items |
|---|---|
| VTH2110 | Lead time, no alternate, polarity (Q-11) |
| OPA140, LMP7721 | D-18 approval, price |
| TLV9062/9064, TLV9061 | Pinouts |
| TMUX1101, TMUX1104, BAS116, $C_{hold}$ | Leakage, reset polarity |
| ADS8689, ESP32-S3-WROOM-1 | MCU-board count, module variant |
| LM27762 | Noise and PSRR |
| PicoBlade, SWF | Circuit count, part number |
| HV parts | No design |
