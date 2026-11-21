# Answered questions

**Conclusion:** The user's answers to the electrometer's requirements questions (Q-01 to Q-11) and to the architecture draft's questions. Open ones stay in the requirements and architecture.

**Relied on by:** D-01 to D-08, R-01, R-02, R-08, R-11, R-24, A-01 to A-10.

## Working

### Requirements questions

| Q | Answer |
|---|---|
| Q-01 | U-5 in the tin is the primary validation; the bench test diagnoses (D-02) |
| Q-02 | Target 10 fA. Consequence: PTFE or in-air input node, guarded range switching, careful cleaning (D-01) |
| Q-03 | One ±50 V source channel. The HV board's regulated PD bias and the real ring supply are selected at the breakout (D-06) |
| Q-05 | Murata SWF switch connectors per input, one probe cable (D-02) |
| Q-06 | No matrix. Four inputs per board via the probe, other nets through the PicoBlade (D-02) |
| Q-07 | Battery (D-02) |
| Q-08 | Mains frequency (50 or 60 Hz) not needed: integration over multiples of 100 ms rejects both (D-06) |
| Q-11 | No 1 nF charge range. Charge and capacitance stay optional firmware modes on the 10 pF integrator (D-04) |

### Architecture draft questions

| # | Question | Answer |
|---|---|---|
| 1 | Topology and ranges | Approved: ±5 V rails, R1 3.9 MΩ, R2 1 GΩ, 10 pF integrator, T reset with a reed relay and an analog switch |
| 2 | R-01 burden | Approved: ≤ 1 mV up to 4 nA, ≤ 10 mV on the 1 µA range (D-05) |
| 3 | R-25 self-test with C_inj | Still open, clarification given ([self-test](self-test.md)) |
| 4 | Q-03 | One source channel (D-06) |
| 5 | Q-08 | Closed (D-06) |
| 6 | HV board series resistance | Still open ([input protection](input-protection.md)) |
| 7 | Source DAC | MCP4922 as coarse + fine (D-07). C_inj moves to an MCP4821 |
| 8 | Battery | Two 18650 cells in parallel (D-08) |

## Sources

- Requirements draft 3 section 7 and architecture draft 2 section 8, in git history before the contract rewrite.
