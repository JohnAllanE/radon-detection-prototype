# Decisions

Short dated entries: decision, alternatives considered, reason. Don't re-open an entry without saying why.

## 2026-10-12

**D-01 Pump on the chamber outlet; generic diaphragm pump.**
Reason (user): offgassing products from the pump must not reach the chamber, so the pump sits downstream. Alternatives not discussed.
Consequence noted by Claude: the chamber runs slightly below ambient, so any leak draws in unfiltered, undried room air (R-32). Pump vibration and drive noise are a possible microphonic and EMI source for the preamps (R-41).

**D-02 Gas train order.**
Inlet filter → desiccant column → final filter → chamber inlet valve → chamber → chamber outlet valve → pump. The final filter catches desiccant dust and any progeny formed in the column.

**D-03 Chamber isolation valves.**
Manual ball valves (stainless steel body, PTFE seats) on the chamber inlet and outlet.
Consequence noted by Claude: a metal valve body touching a chamber wall at +1 kV would put HV on the gas lines. See R-38.

**D-04 Mechanical design is part of this project's requirements,** because mechanical and electrical choices are interlinked (HV isolation, microphonics, feedthroughs, board mounting).

**D-05 Gases: ambient air, and semi-dry bottled N₂ as a control** to check self-contamination between runs. No other gases.

**D-06 No compensation and no chamber sensors on the MCU board.** The MCU board is external to the chambers and reads no T, RH, pressure or flow. Pressure/T/RH coefficients are not investigated. Manual sensors are used as needed; RH is measured at the outlet during N₂ purge. Alternative considered: an RH sensor on the detector board in the chamber; rejected on Claude's advice (tiny volume, sensor may disturb ion behaviour, noise path).

**D-07 Detector comparison arrangement.** One premium and one low-cost detector board in each chamber (about 3 in apart in Part 1, similar in Part 2). Success metric: the low-cost board gives similar event types and frequencies.

**D-08 MCU board:** ESP32-S3 over USB, with ESP-NOW (PCB antenna) as a possible later option. Powered from wall adapters (Mean Well 48 V and 5 V).

**D-09 Chamber geometry (Part 1):** 304 SS tube, ~16 mm ID, walls at +1 kV. Four 5 mm photodiodes in a 10–12 mm square on the detector board; exposed ENIG around the diodes with a bias to steer ions onto them (to be settled by simulation). Claude flagged that a 12 mm square does not fit comfortably in 16 mm (R-39).

**D-10 Part 2 (vacuum):** custom aluminum chamber with gaskets, standard port for a single-stage rotary pump, SS/PTFE ball valve. Rough vacuum, pressure not yet known. HV not used. The detector board is O-ring sealed to the chamber with its back side at atmosphere. Weld samples close to the detectors.

**D-11 HV board:** fixed output from a Mean Well 48 V supply, no adjustment. PD bias per VTH2110 datasheet (user recalls 20 V as an option, to verify). Construction: PCB up to the transformer, Manhattan or in-air from the transformer to the output, epoxy-potted (vacuum and pressure) after it is shown to work.

**D-12 Pump and valves are operated manually** by the user on-site and are outside the electronics design.

**D-13 Gas-train quantities** (flow, pressure drop, leak rate, desiccant life) are not design drivers. They are characterised after the build. Drierite is the preferred desiccant (sourcing to check); PTFE tubing.

**D-14 Board stackup:** detector board 2-layer (lowest interlayer capacitance, simple circuit); MCU board 2-layer if possible, 4-layer if needed.

**D-16 ADC strategy (user, 2026-10-12):** populate both ADS1220 (24-bit, 2 kSPS, in stock) and ADS8689 (16-bit, 100 kSPS, single-channel, needs an external mux) on the MCU board, plus an option to route the mux output to the ESP32-S3's internal ADC for a low-resolution, high-rate path. Reason: low risk, and event rates are low. Claude's note: ADC bits are not the limiting factor (architecture §2.2).

**D-17 Low-cost board constraint (user):** the low-cost detector board uses a standard single 8-pin op-amp footprint so many parts can be swapped to explore the BOM cost. Claude picks a best-effort low-cost amplifier ("LLM best effort"; the real answer needs much more data). Default OPA140; swap candidates OPA656, OPA657.

**D-18 Premium variant (Claude proposal, awaiting approval; revised 2026-10-12):** LMP7721 (user reports $8.40 each) with a guard-friendly footprint is the default premium candidate. It differs from the low-cost board by leakage control and layout, not by expected noise. ADA4817-1 (lowest noise, FB pin) and ADA4530-1 (guard buffer, 20 fA) are expensive per the user and unpriced here; ADA4530-1 is reserved for the electrometer front end (D-15). See architecture §3.

**D-19 Mechanical facts from the user's answers (2026-10-12):** sample-to-detector distance 5–10 mm; weld coupons about 15 mm wide × 30 mm tall; vacuum chamber is a cylinder of 50 mm ID; mid-level rotary pump (specs to follow); N₂ purge first, then pump down, to remove free radon; HV not used on the vacuum side; viton gaskets accepted. Lower-background materials to be considered in future revisions.

**D-20 HV safety:** the kV tube is shielded by air and an outer enclosure that is touch-safe, used only by trained technical staff. A normally-closed interlock path that shorts stored energy through a fast-discharge path is a possible addition. HV return divider feeds the PWM controller feedback (dedicated PWM driver with feedback pin). Fire-alarm-type standards are a candidate for the safety rules (to verify in phase 2 of the HV board).

**D-21 Radon-chain targets accepted (user):** R-09 (FWHM ≤ 100 keV at about 5.5 MeV) and R-14 (no loss up to 100 events/s total). The scope is airborne radon first: the detector module PCB is fixed for airborne radon, and the weld testing is "doing what we can with it".

**D-15 Test electrometer:** an electrometer front-end (premium IC, switchable capacitors, reed relays, ESP32 over ESP-NOW, controlled through a Raspberry Pi ESP-NOW bridge API) will be built to measure leakage and capacitance of bare and populated boards. Documented in this project (requirements §4.7) until it exists, then factored out to the test-gear repo.

**D-22 Chamber bore (user, 2026-10-12):** 3/4 in NPS pipe, bore ground and lapped to about 21–22 mm, possibly etched to remove the user's own contamination. Replaces the 16 mm ID assumption (D-09), which could not hold four 5.67 mm dies.

**D-23 Op-amp standard (user, 2026-10-12):** the user's designs prefer TLV900x (TLV90xx) op-amps wherever possible, but not at the expense of specifications. Applied to the MCU board's shaping, peak-detect, hold-buffer and comparator stages. Claude's assessment from the datasheets (architecture §2.5): TLV9001 (1 MHz) is adequate for the shaper but marginal for the peak detector and hold buffer; the TLV9061 family (10 MHz, 0.5 pA bias, 100 Ω output impedance) fits those stages and stays within the standard. The detector board's CSA does not use TLV90xx (too noisy). TLV90xx is rated 1.8–5.5 V (absolute maximum 7 V for TLV9001, 6 V for TLV9061), so the MCU board analog chain runs on a single +5 V rail with a baseline offset, not on the ±4.5 V rails.

## 2026-10-16

**D-24 Part 2 pump: Edwards E2M8 (user).** Claude read the specs from the Edwards instruction manual (E2M2–E2M12, Table 3): two-stage oil-sealed rotary vane; maximum displacement 9.5 m³/h at 50 Hz (11.4 at 60 Hz); Pneurop pumping speed 8.2 m³/h (about 2.3 L/s); ultimate 1×10⁻³ mbar total (2.5×10⁻⁴ partial) without gas ballast, 3×10⁻² mbar with full gas ballast; maximum water-vapour inlet pressure 15 mbar; NW25 inlet; about 0.55 L Ultragrade 19 oil; the oil distribution valve prevents suck-back on stop only with the gas ballast closed. This corrects "single-stage" in D-10. Claude's assessment: suitable with a wide margin, since about 1–10 mbar is enough for a 5–10 mm gap (requirements §3). The risks are oil backstreaming onto the samples and pump vibration, not pressure; handled by R-57, R-58 and R-59. Use gas ballast only on the first pump-down from humid air or the N₂ purge.

**D-25 Standard gas filter (Claude proposal, awaiting approval).** One filter type at every gas port: the Part 1 inlet filter, the Part 1 final filter after the desiccant, the Part 1 chamber outlet (catches diaphragm-pump wear particles; it does not stop pump outgassing vapour, which D-01 handles by placing the pump downstream), and the Part 2 chamber-to-pump line. The type is a hydrophobic PTFE membrane, about 0.2 µm, in a housing that is vacuum-rated, has the membrane supported against flow in both directions (Part 2 vents back through it), and has a stainless steel or PFA/PTFE body with the same end fittings everywhere. Alternative considered: a different filter per position. Reason: one spare part, one fitting set, materials consistent with R-30. Limits: on the vacuum side a membrane stops oil mist and particles but not oil vapour, so R-57's trap and operating practice are still needed. It also lowers conductance in molecular flow, which costs pump-down time but not usable pressure (R-03). Part selection is open (Q-17).

## 2026-11-20: Requirements rewritten to the document contract

- **Decision (Claude, from the brief, user away):** `01-requirements.md` keeps every R-xx ID and sorts the rows into functions, objectives and constraints, each with a status: user-confirmed rows firm, Claude's proposals working, TBD rows open. Non-firm numbers, physics, the count-rate estimate, the gas-train working, Part 2 vacuum practice and the answered questions move to `docs/notes/`. Part-level detail (the SWF test port, the ring sign, ADC input mode) moves to the architecture. New R-73: build and assembly effort.
- **Alternatives:** convert to F/O/C IDs (the user's call, not taken).
- **Reason:** the document contract; the old draft was 6,100 words.
- **Affects:** all R-xx; Q-02, Q-08, Q-10, Q-13 reopened because their answers were never recorded.
- **Replaces:** none.

## 2026-11-20: The first electrometer outline is retired

- **Decision (Claude, user away):** requirements section 4.7 (the electrometer outline, R-57 to R-72 of that section, Q-27 to Q-37) moves to `docs/notes/electrometer-outline.md` as a record. The electrometer's own requirements, confirmed by the user, replace it. The outline reused R-57 to R-60, which also name detector requirements (Part 2 oil, sealed counting, gauge, test port): only the detector meanings are live.
- **Alternatives:** renumber the outline's IDs.
- **Reason:** nothing cites the outline's IDs, and the electrometer has its own local IDs.
- **Affects:** R-48 to R-50, R-57 to R-60.
- **Replaces:** D-15 in part (the electrometer is documented in `electrometer/`, not requirements section 4.7).

## 2026-11-20: Architecture rewritten to the document contract

- **Decision (Claude, from the brief, user away):** `02-architecture.md` now holds choices A-01 to A-26 with a status, derived specs, expected performance, off-board connections, mechanics and ranked risks. The HV board and chambers get choice rows from D-11, D-20 to D-25. Derivations, the noise and gain budgets, the TLV90xx assessment, the JFET discussion and the detector-board detail move to notes. Part facts move to six candidate surveys. The three Mermaid diagrams become SVGs from `docs/diagrams/make_diagrams.py`.
- **Alternatives:** keep the numbered draft with its findings section.
- **Reason:** the document contract; the old draft was 5,400 words.
- **Affects:** A-01 to A-26; the electrometer's HV fault-current request becomes A-21, open.
- **Replaces:** none.

## 2026-11-20: Part selection to the template, candidate surveys split out

- **Decision (Claude, from the brief, user away):** `parts/selection.md` lists one row per function with a status, quantity and stock. Quantities assume four detector boards. The comparison of candidates moves to six `docs/notes/candidates-<role>.md` surveys. Prices and stock stay unchecked and are pass-2 work. Datasheet JSONs stay in `datasheets/` until the reviewer migrates them.
- **Alternatives:** keep the single candidate table.
- **Reason:** the document contract and templates.
- **Affects:** A-02 to A-20.
- **Replaces:** none.

## 2026-11-20: Project CLAUDE.md to the template; passes replace phases

- **Decision (Claude, from the brief):** the root `CLAUDE.md` becomes the detector project's, tier full, with `electrometer/` named as a second project. The work since 2026-10-12 (requirements draft 2, architecture draft 1, candidate parts) is pass 1, with the architecture not yet reviewed by the user, ended by `docs/reviews/pass-1.md`. `MACHINES.md` added at the root: every script is standard library only.
- **Alternatives:** keep the phase numbering and its gates.
- **Reason:** the workflow's passes and document contract (`PCB-WORKFLOW.md`).
- **Affects:** none (process only).
- **Replaces:** none.

## 2026-11-21: The user's answers to the pass 1 questions

- **Decision (user, recorded by Claude):** the architecture is accepted as long as the requirements don't change. Q-04: the target is to tell the radon chain's members apart; shaping time after the first runs. Q-08: eight channels per chamber, CAD 20 average per channel at most, CAD 10 preferred; premium parts on 1–2 channels if they don't fit, four identical channels assumed, partial population acceptable (R-74). Q-10: HV accuracy not needed, readback more important, an HV probe later (R-18, R-23). Q-12: an insulated outer enclosure with an interlock, a darkness check as a possible second check (R-22). Q-13: no BGA, QFN at 0.5 mm pitch fine (R-28). Q-14: a smoke-alarm Am-241 check source, transferred from a RAD7 later; the kV read by a divider (R-51). Q-02: the lab is not monitored. Q-17: open to suggestion, low cost first. One MCU board per chamber takes all eight inputs (A-27). The die-to-wall gap goes to a field simulation (S-01).
- **Claude's working additions:** IPC-2221 B2, 5.0 mm at 1 kV, as the bare-board spacing rule (`VERIFY`); the readback divider sits before the ≥ 10 MΩ series resistor and is the feedback divider's tap; the darkness check proves the chamber is closed, not that the enclosure is shut. R-09's 100 keV separates Po-210 and Rn-222 (185 keV apart, NuDat). Notes: `decay-chain-lines.md`, `hv-spacing-and-readback.md`.
- **Alternatives:** one MCU board per detector board (the old drawing), an HV probe now.
- **Reason:** the user's answers of 2026-11-21 (`docs/briefs/pass-1-answers.md`).
- **Affects:** R-06, R-09, R-18, R-22, R-23, R-27, R-28, R-38, R-51, new R-74; A-07, A-17, A-20, A-22, new A-27.
- **Replaces:** the working answers in the pass 1 review's questions 1, 4 and 5 (Q-08, Q-10, Q-13).

## 2026-11-21: Chamber field simulation S-01 adopted

- **Decision (Claude, from the simulation; the user's rule adopts simulated values):** the 2.1–2.6 mm die-to-wall gap is accepted. The ring (A-10) is tied to the filtered +20 V PD bias (Q-24: slightly positive). No sloped electrode. Both edges of each tube end get about a 0.5 mm radius. Inside the chamber, peak field replaces the 5.0 mm surface rule (R-75).
- **Alternatives:** a sloped electrode at +300 to +700 V (takes 4–9 % of the ions); a +100 V ring rail (1.6 points more, not worth a rail); a 22 mm bore (no gain in collection).
- **Reason:** S-01 (`sim/field/S-01-chamber/`): 95–99 % of field lines from the gas end on the dies unaided; peak field about 1.5 kV/mm at the sharp tube edge, 1.2 kV/mm rounded, against roughly 3 kV/mm for air at 1 atm (`VERIFY`).
- **Affects:** A-10, R-38, R-43, R-47, R-75, risk 1, `chamber-sensitivity.md` (about 16 % per alpha). New finding for the user: about two-thirds of the ions land where the four dies meet.
- **Replaces:** none.

## 2026-11-21: No OPA657 tier; LMP7721 supply range

- **Decision (Claude, from the datasheets):** OPA657 is not a third CSA tier: its minimum stable gain is about 7 (OPA657.json), and the CSA must be stable at a noise gain of 1 with the test port open (R-60, electrometer R-19). Found on the way: the LMP7721 is a 1.8–5.5 V part (LMP7721.json p5), so it can't sit on the ±4.5 V CSA rails; the premium board needs a local ±2.5 V pair (questions 2026-11-21, question 2).
- **Alternatives:** OPA657 with a compensation network (not worth it for an invisible noise gain).
- **Reason:** review question 3; the user asked for a write-up only where needed.
- **Affects:** A-06, A-07, D-17's swap list (OPA656 stays), D-18.
- **Replaces:** none.

## 2026-11-21: The user's answers to the detector questions

- **Decision (user, recorded by Claude):** (1) The ions centre themselves (S-01), so four packed dies lose much of what they catch: evaluate one detector per tube, centred, with more area from more tubes in parallel in a manifold of 304 or 316 stainless NPT pipe and cross fittings (316 assumed for the user's "306", `VERIFY`), one inlet and one outlet; proposal A-29, simulated in S-02. A board with several widely spaced detectors under a tube array is rejected as an assembly headache. (2) ADA4817-1 at about CAD 13 in SOIC (preferred for leakage) is doable; the LMP7721's supply range is no concern. (3) A-21 agreed: ≥ 10 MΩ after the divider. (4) Q-02: ambient T and RH on the board in room air, other environmental sensors as useful, a flow-through RH/T sensor on the purge air if one exists (R-76, A-30). (5) Q-17 option (a): PTFE-membrane syringe filters in polypropylene, Drierite column; D-25's stainless or PFA body requirement is dropped for Part 1. (6) Q-20: flange screwed onto the pipe thread, end machined parallel, edges rounded where reachable, O-ring in a triangular groove with a PTFE washer setting compression; the threads' distance from the field checked in S-02.
- **Claude's additions:** a programmable CSA rail is not needed ([CSA rails](notes/csa-rails.md)): fixed LDO and RC per board, ANY-OUT parts strapped if used. Sensor candidates: SHT45 and a barometer on the board, SHT45-AD1F in a flow cell on the outlet.
- **Alternatives:** the 2×2 array with a centre electrode (question 1 option (b)); stainless filter housings (Q-17 (b)); a programmable rail.
- **Reason:** the user's answers of 2026-11-21 (`docs/briefs/single-pd-sweep.md`).
- **Affects:** R-17, R-27, R-34, R-39, R-54, new R-76; A-07, A-21, A-23, A-24, new A-29, A-30; D-06 (chamber volume only), D-18, D-25.
- **Replaces:** D-25's housing material for Part 1; the questions document's recommendations 2–6 where the user chose otherwise.

## 2026-11-21: Single-detector sweep S-02

- **Decision (Claude, from the simulation; the user's rule adopts simulated values):** for A-29, build around 1-1/4 in schedule 40 pipe (ID 35.05 mm) with the board's top copper at +200 V from the HV board's transformer stage: 56 % of the gas volume to the active area (50–58 % between the die sections), $ID^2 f$ = 684 mm² against 145 for the old four-die array. Peak fields about 1.0 kV/mm or less. The NPT thread inside the flange carries no field; the PTFE washer should cover the seam at the pipe OD. A 0 V guard trace between the die and the copper.
- **Alternatives:** 1-1/2 in (7 % more index, 44 % share); 3/4 in (today's pipe, 83 % share, half the index); $V_{top}$ up to 600 V (up to 20 points more share, 2.6 kV/mm at the copper edge): left to the user (`docs/questions/2026-11-21-single-pd.md`). Schedule 10S: thin for a thread.
- **Reason:** S-02 (`sim/field/S-02-single-pd/`).
- **Affects:** A-29, R-39, R-47, R-75.
- **Replaces:** none.
