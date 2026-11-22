# Answered questions (requirements Q-01 to Q-37)

**Conclusion:** The user's answers that set the requirements, by question. Questions still open are in the requirements' and architecture's Open questions. Q-27 to Q-37 were about the electrometer outline and are answered by the electrometer's own documents.

**Relied on by:** every R-xx whose source is the user. Decisions D-01 to D-25 record the choices.

## Working

### Answered in the user's first set of answers

Q-01, Q-02, Q-08, Q-09, Q-10, Q-13, Q-16, Q-18 (partly) and Q-19 were answered with D-01 to D-21. The answers to Q-02, Q-08, Q-10 and Q-13 were not written down; the user answered them again on 2026-11-21 (third set, below).

### Answered in the second set

| Q | Answer |
|---|---|
| Q-03 | Sample-to-detector 5–10 mm (D-19). Pump: Edwards E2M8, ultimate 1×10⁻³ mbar (D-24). Pressure reached and leak-up rate measured with the gauge (R-59) after build. No HV in Part 2, so only Part 1's pressure case (R-43) remains |
| Q-05, Q-06 | R-09 and R-14 accepted. Radon in air is the primary target. The detector module PCB is fixed for it, and weld testing is best effort (D-21) |
| Q-07 | "LLM best effort": no quantitative metric until there is much more data (D-17) |
| Q-11 | From the datasheet: specified at 20 V and 40 V reverse bias, breakdown > 100 V, no recommended operating point, polarity not stated. Default 20 V. The user's recollection of 20 V matches. Polarity stays open |
| Q-12, Q-14 | kV tube in an outer touch-safe enclosure, trained staff only, possible NC discharge interlock. HV divider feeds the PWM controller. Fire-alarm-type standards suggested (D-20). Still `VERIFY` |
| Q-20 | Preamps on the atmosphere side, filled and capped ENIG vias, circular board, O-ring size from the mechanical design. Fallback: a vacuum-rated bulkhead connector with both sides under separate vacuum |
| Q-21 | Viton, with lower-background materials considered in later revisions |
| Q-22 | Coupons about 15 × 30 mm. Vacuum chamber a 50 mm ID cylinder (R-46) |
| Q-23 | The electrometer is scripted over the user's API, which cascades to ESP-NOW, and streams data as events arrive. Treated like the bench instruments: Claude writes scripts, the user runs them |
| Q-25 | 21–22 mm bore (D-22) |

### Answered in the third set (2026-11-21)

| Q | Answer |
|---|---|
| Q-02 | The lab is not monitored. "What parameters would you like?": proposed in the [questions](../questions/2026-11-21-detector.md) |
| Q-04 | Decide after the first runs; the target is to tell the members of the radon decay chain apart ([decay-chain lines](decay-chain-lines.md)) |
| Q-08 | Eight channels. CAD 20 average per channel is the ceiling, CAD 10 preferred. Best parts on 1–2 channels if they don't fit; assume four identical channels per board; partial population acceptable (R-74) |
| Q-10 | HV accuracy not needed: enough gradient for ions to flow. Reading it back matters more, and can wait for an HV probe in a funded effort (R-18, R-23) |
| Q-12 | An insulated outer enclosure and an interlock make the tube untouchable; a darkness check by the photodiodes is a possible second check; other approaches welcome ([HV spacing](hv-spacing-and-readback.md)) |
| Q-13 | No BGA; any other package; QFN at 0.5 mm pitch has been fine (R-28) |
| Q-14 | A smoke-alarm Am-241 source, tentative until measured in a RAD7 and used as a transfer standard. The kV read by a divider; no HV probe on hand (R-51) |
| Q-17 | Unknown; open to suggestion; low cost first: this is preliminary work for a later funded effort |

### Electrometer outline questions (Q-27 to Q-37)

Asked about the electrometer outline ([electrometer outline](electrometer-outline.md)), all answered by the electrometer's requirements (confirmed by the user) and decisions:

| Q | Question | Where it landed |
|---|---|---|
| Q-27 | Does the electrometer source the test voltage? | Yes: built-in ±50 V source (electrometer R-08, D-06) |
| Q-28 | 10 fA to 100 µA accepted, revisit if size grows | Full scale now 1 µA, overlapping the DMM (electrometer D-01) |
| Q-29 | Leakage at 1 kV in scope? | Yes, in situ in the tin with the real HV board (electrometer D-02, U-1, U-5) |
| Q-30 | Capacitance mode in scope? | Optional, kept only if almost free (electrometer D-01) |
| Q-31 | Pogo pins or probes, boards per session | One probe cable, switch connectors on the board (electrometer D-02) |
| Q-32 | RH/T sensor, N₂ or desiccant | Sensor in the tin (electrometer R-17), purge optional (electrometer Q-10) |
| Q-33 | Front end on an inside battery or fed from outside? | Battery, floating (electrometer D-02, D-08) |
| Q-34 | Reed relays on input paths, about 10 relays | Matrix dropped (electrometer D-02) |
| Q-35 | Shielded RJ45 or M12 link? | No wired link: ESP-NOW with the antenna outside the tin (electrometer R-32) |
| Q-36 | Where above 1 µA is needed | Above 1 µA is the DMM's job (electrometer D-01) |
| Q-37 | SDM3055 DCI accuracy and resolution, outside calibration | Still `VERIFY` (electrometer R-07) |

## Sources

- Requirements DRAFT 2 sections 6 and 6b, in git history before the contract rewrite.
- Decisions D-01 to D-25. Electrometer decisions D-01 to D-08.
