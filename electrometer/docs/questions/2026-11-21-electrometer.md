# Questions with their context: the electrometer after pass 1, 2026-11-21

Five decisions from the pass 1 review (`docs/reviews/pass-1.md`), each with the piece of the design it concerns, what was found, the options and their costs, and a recommendation. Review question 2 (≥ 10 MΩ at the radon HV board, A-18) is the detector's question 3 in `../../../docs/questions/2026-11-21-detector.md`: one decision covers both. Several of the review's question 7 items are settled by your detector answers and S-01 (end of the document). Diagrams: `diagrams/make_diagrams.py`.

## Question 1: self-test by an injection capacitor (A-06)

![The head: the probe input joins the guarded summing node of the ADA4530-1, whose feedback is a resistor range or the integrating capacitor. A 1 pF injection capacitor connects the summing node to an RC-filtered MCP4821 DAC. A dashed cal plug, a known resistor to a known voltage, fits the probe input in place of a board to check the resistor ranges.](diagrams/cinj.svg)

**What R-25 asked for.** A check of each range before a session: input zero and a known reference. Your requirement assumed a switched reference resistor or capacitor at the summing node.

**The finding.** Any switch at the summing node leaks more than the 10 fA being measured, and a resistor left there adds noise: 1 GΩ adds 2.87 fA rms in 1 s ([self-test note](../notes/self-test.md)). A permanent 1 pF capacitor driven by a DAC does the job without a switch: held still it passes no current, a ramp gives $I = C\,dV/dt$ (1 V/s gives 1 pA, 0.01 V/s 10 fA), a step a known charge. It doesn't check the resistor values, so a cal plug (a known resistor to a known voltage, plugged into the probe input) does that before a session.

| Option | Cost | Gives |
|---|---|---|
| (a) $C_{inj}$ plus an external cal plug | MCP4821 (in stock), one 1 pF C0G, a plug | Zero and current checks in place, resistors checked off-line |
| (b) Switched references at the node (R-25 as written) | A reed relay at the node, its leakage and charge | Everything in place, at the cost of the floor |

**Recommendation:** (a), and amend R-25's wording to match.

## Question 2: the antenna (Q-14)

![The grounded tin holds the head and the control board with an ESP32-S3-WROOM-1U. A u.FL coax runs from the module to an SMA bulkhead in the tin wall, with the antenna outside. The alternative puts the control board outside and passes the head's signals through filtered feedthroughs.](diagrams/antenna.svg)

**The finding.** The tin blocks 2.4 GHz (R-32), so the antenna must be outside. The in-stock module is the -1U, with a u.FL connector for an external antenna.

| Option | Cost | Risk |
|---|---|---|
| (a) Control board inside, coax to an SMA bulkhead | One bulkhead, one short coax, an antenna | Radio bursts inside the tin: A-13 already transmits between integration windows |
| (b) Control board outside | Filtered feedthroughs for the ADC and control lines | Every feedthrough is a noise path into the head's enclosure |

**Recommendation:** (a).

## Question 3: power input (battery alone, or the bench standard's GX12)

![A 1S2P Li-ion pack of two 18650 cells feeds the main switch, fuse and protection, then the 3.3 V, plus and minus 5 V and plus and minus 60 V rails. A GX12 2-pin connector feeds a charger, which connects only when the main switch is off.](diagrams/power.svg)

**The conflict.** `PROJECTS.md` lists the electrometer among boxes following the bench power standard (GX12 2-pin input). But R-24 and R-31 need it floating on its battery while it measures: any supply cable ties its common to another box's ground and makes a loop through the femtoamp input.

**Options.** (a) Battery only, charged off the box: no connector, but cells come out to charge. (b) **GX12 2-pin as the charge input only, live only with the main switch off:** keeps the bench standard's connector and charger, never connected while measuring. (c) GX12 as a running supply: breaks R-31.

**Recommendation:** (b), and note in `PROJECTS.md` that the electrometer takes the standard's connector for charging only (a shared-repo change for the reviewer).

## Question 4: a USB console during bring-up

![The electrometer floats on its battery; its ESP32-S3 has native USB. With a USB cable to a PC, the PC's mains earth reaches the head's common through the cable: a ground loop.](diagrams/usb.svg)

**Why it comes up.** Control goes through lab-gateway over ESP-NOW (R-20), whose phase 3 is on hold and whose HAT is still being designed. Until then nothing can command the electrometer.

**The finding.** The ESP32-S3 is flashed over USB anyway, so the connector is on the board regardless. Plugged in, it ties the PC's ground to the head's common: fine for bring-up and for the µA to nA ranges, not for femtoamp runs.

**Recommendation:** yes: a USB-serial console with the same SCPI-style commands (A-13) for bring-up, unplugged for femtoamp runs. No extra parts.

## Question 5: the budget (Q-09)

![Three purchases and what each unlocks: the ADA4530-1, not in stock, is the head itself; the Murata SWF probe, one cable, enables in-situ measurement; SWF receptacles, 16 on four detector boards plus a test board, are the R-60 test ports.](diagrams/budget.svg)

**The context.** Your detector answer applies the same rule here: low cost first, this being preliminary work for a funded effort. Prices are not checked (`VERIFY`, pass 2). The ADA4530-1 has no stand-in: the LMP7721 (3 fA typical, 20 fA maximum bias, LMP7721.json p5) runs only from 1.8 to 5.5 V in total, which would halve the head's ±4 V swing and its ranges.

| Purchase | Minimum | Why |
|---|---|---|
| ADA4530-1 | 2 (one fitted, one spare) | Hand-soldered guard layout; a spare covers a damaged part |
| Murata SWF probe | 1 | One channel measured at a time |
| SWF receptacles | 16 for four detector boards, plus about 4 for the bare test board | R-60 needs them on every detector board anyway |

**Recommendation:** these minimum quantities, priced in pass 2 before ordering.

## Settled without you

- **Q-04 (1 kV from the project HV board only?):** yes. Your detector answer defers an HV probe to a funded effort; the ±50 V source covers low-voltage leakage curves.
- **Q-10 (lab RH, tin purge):** the lab is not monitored; R-17's sensor logs T and RH in the tin with every reading. A purge is `DECIDE AT TEST`, if RH turns out to limit the floor.
- **Q-15 (O-ring land copper or bare, a 0 V ring inside it):** bare laminate under the O-ring (S-01). The detector's exposed ring, on +20 V from 8.67 to 9.6 mm, is the nearest copper to the tube and catches surface leakage before it reaches a CSA input, which is on the back side. No extra ring.
- **Q-12 (SWF leakage), Q-13 (space on the detector board's back):** `DECIDE AT TEST` on the bare test board, and at detector layout. The board is at least 26.67 mm across (the tube's outside), not "≤ 20 mm".

## Your decisions

| # | Decision | Recommendation | Your answer (2026-11-21) |
|---|---|---|---|
| 1 | Self-test (A-06) | $C_{inj}$ plus an external cal plug; amend R-25 | Yes: R-25 reworded |
| 2 | Antenna (Q-14) | SMA bulkhead, control board inside | Wired USB-C now (bench strategy); (a) if the radio is used on battery; optical UART possible, would need the gateway HAT. Claude: an isolated USB link ([note](../notes/data-link-and-power.md)) |
| 3 | Power input | GX12 2-pin for charging only, main switch off | A separate battery pack, charged elsewhere, on GX12-4, so PSU and battery can be compared; the board sealed with desiccant |
| 4 | USB console for bring-up | Yes, unplugged for femtoamp runs | USB-C for firmware as on the other devices; second-wave project; IP-rated USB-C if sealed |
| 5 | Budget (Q-09) | 2 ADA4530-1, 1 probe, about 20 receptacles, priced in pass 2 | Tentatively yes |
| — | ≥ 10 MΩ at the HV board (A-18) | Decided with the detector's question 3 | Agreed (radon A-21) |
