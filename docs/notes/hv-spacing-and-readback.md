# HV spacing, touch safety and reading back 1 kV

**Conclusion:** Creepage is the distance along an insulating surface between two conductors; clearance is the shortest distance through the gas between them. The working rule for +1 kV on bare board surfaces is IPC-2221 Table 6-1 column B2, about 5.0 mm, `VERIFY` against the standard. The 1 kV readback is the HV board's own feedback divider, about 1000:1, tapped to an MCU ADC and a test point, placed before the ≥ 10 MΩ series resistor (A-21). Touch safety is the user's insulated enclosure with an interlock; the darkness check shows a board or seal missing, not an open enclosure.

**Relied on by:** R-22, R-23, R-38, R-51, A-20, A-21, A-22, Q-10, Q-12, Q-14, the field simulation S-01.

## Working

### Creepage and clearance (Q-12)

- **Clearance:** the shortest path through the gas between two conductors. Too small: a spark.
- **Creepage:** the shortest path along an insulator's surface. Too small: moisture and dirt conduct, and the surface tracks (carbonises).
- IPC-2221 Table 6-1: above 500 V, each volt adds a per-volt amount to the 301–500 V value. Column B2 (external conductors, uncoated, below 3050 m): 2.5 mm at 500 V plus 0.005 mm/V, so $2.5 + 0.005 \times (1000 - 500) = 5.0$ mm at 1000 V. Column B4 (external, permanent polymer coating): $0.8 + 0.00305 \times 500 = 2.3$ mm. From secondary summaries that disagree on B4: `VERIFY` against IPC-2221B.
- Column B3 (uncoated, above 3050 m) is for reduced pressure: the Part 1 chamber runs below ambient (R-32), so B3 is the honest column on the chamber side. Its 1 kV value is unchecked (`VERIFY`).
- IPC-2221 spacing is functional insulation, not safety isolation, which is IEC 60664-1's subject (not consulted, `VERIFY`). Touch safety here comes from the enclosure, so the IPC rule is enough on the boards.
- Working rule (R-38): **5.0 mm creepage and clearance from any +1 kV conductor to any other conductor on a bare board surface, outside the chamber; on the chamber side, the field simulation S-01 sets the clearance from the peak field.**

Where it applies:

| Place | Path | Present value | Against 5.0 mm |
|---|---|---|---|
| Tube end on the board's O-ring land | Board surface from the tube's contact to the nearest copper at 0 V or bias, and around the board edge to the back side | Not designed (Q-20) | Sets the O-ring land and the copper keep-out. S-01 |
| Die corner to tube wall | Gas, inside the chamber | 2.1–2.6 mm | Below; S-01 checks the field there |
| HV board, HV wire, enclosure feedthrough | Board surface, air | Not designed | Sets the layout |

### Touch safety (R-22)

- The user's approach: an insulated outer enclosure with an interlock (D-20): a lid switch removes the HV board's PWM enable, and a normally-closed contact discharges the output.
- Darkness check (the user's idea): the photodiodes sit inside a steel tube closed by the detector boards, so opening the enclosure lets no light in. Light reaches them only if a board is missing or off its seal, or through unplated FR4. The check proves the chamber is closed, not that the enclosure is shut. The CSA's DC output (dark current × $R_f$, 15–200 mV) rises with light, but the MCU board AC-couples it: the check needs one DC tap per board, or the PD bias current. Working: optional, after the interlock.

### Reading back 1 kV without an HV probe (Q-10, Q-14)

- A resistive divider of about 1000:1: a 100 MΩ top and a 100 kΩ bottom give 1.0 V at 1 kV, 10 µA, 10 mW.
- A DMM's 10 MΩ input across the 100 kΩ bottom reads 1 % low: include it in the ratio.
- The top holds 1 kV. Chip resistors are rated about 200 V working (typical 1206 thick film, `VERIFY` per part): ten 10 MΩ in series (100 V each), or one resistor rated ≥ 1.5 kV, laid out to keep 5.0 mm creepage end to end.
- If the bottom resistor opens, the tap rises toward 1 kV through 100 MΩ (10 µA at most): clamp it to the ADC rail.
- **Position against A-21:** a divider at the tube end would draw its 10 µA through the ≥ 10 MΩ series resistor and read 100 V (10 %) low. The tube draws only ion and leakage current, far below a µA, so put the divider on the HV board's side.
- The HV board's feedback divider (D-20) is that divider: tap it to an MCU ADC and a test point. A later HV probe checks the ratio.
- HV board load (Q-10): its divider (about 10 µA) plus leakage.

## Sources

- IPC-2221 Table 6-1 values via pcbsync.com "IPC-2221" guide and resources.altium.com "Using an IPC-2221 PCB clearance calculator for high voltage design", retrieved 2026-11-21 (secondary, `VERIFY` against IPC-2221B).
- D-20 (HV divider feeds the PWM controller), A-21 (series resistance), R-32 (chamber below ambient).
- `docs/02-architecture.md` derived specs (dark current offset 15–200 mV).
