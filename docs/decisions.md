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
