# TLV90xx on the MCU board: what the standard costs

**Conclusion:** The user's TLV90xx standard (D-23) costs nothing downstream of the CSA if the TLV906x family (10 MHz) is used for the peak detector and hold buffer. TLV9001 is fine for the shaper only. Neither belongs at the CSA, and both force a single +5 V analog rail.

**Relied on by:** A-13 (single +5 V analog chain), A-14 (shaper), A-15 (trigger), A-16 (peak hold), D-23.

## Working

### Supply rails

- TLV90xx parts are specified 1.8–5.5 V only (absolute maximum 7 V for TLV9001, 6 V for TLV9061; TLV9001.json p14, TLV9061.json p10). They can't run from the ±4.5 V (9 V total) CSA rails.
- So the MCU board's analog chain runs on a single +5 V rail with a baseline offset. In return the parts are rail-to-rail in and out, which removes the +1 V input limit OPA140 would have had.
- The negative rail (LM27762) is then needed only by the detector boards.

### The two families

| | TLV9001 (TLV900x) | TLV9061 (TLV906x) |
|---|---|---|
| GBW, slew | 1 MHz, 2 V/µs | 10 MHz, 6.5 V/µs |
| Noise | 27 nV/√Hz | 10 nV/√Hz |
| Input bias, typical | 5 pA | 0.5 pA (max `VERIFY` for both) |
| Open-loop output impedance | 1.2 kΩ | 100 Ω |
| Supply current per amplifier | — | 0.54 mA, 9× TLV9001: irrelevant on a wall adapter |

### Stage by stage

| Stage | TLV9001 | TLV9061 | Verdict |
|---|---|---|---|
| Shaper (4 µs, gain ≤ 5 per stage) | Adequate: adds about 0.7 keV FWHM, GBW supports gain 5 at 200 kHz | Better in every spec | Either |
| Peak detector driver | Marginal: 1.2 kΩ output into 1 nF, 1 MHz to track a crest | 100 Ω, 10 MHz | TLV9061, simulate |
| Hold buffer | 5 pA bias eats part of the 80 pA droop budget | 0.5 pA | TLV9061 |
| Comparator | Works, a few µs delay (0.85 µs overload recovery, TLV9001.json p17) | About 1 µs delay (0.2 µs overload recovery, TLV9061.json p13) | Either. TLV3201 only if pile-up counting at high rates matters |
| CSA | Not suitable: 27 nV/√Hz, 5 pF common-mode, 1 MHz | 10 nV/√Hz, worse than OPA140 (5.1) or ADA4817-1 (4) | No TLV90xx at the CSA |

### Trigger

- A TLV9061 as a comparator (user preference), with resistor hysteresis. Its delay is harmless because the hold keeps the value until reset and the radon rate is about 1 per hour.
- What it costs: a few-µs timestamp jitter, and no resolving closely spaced triggers for pile-up counting at high calibration rates.
- TLV3201 (40 ns, 1 mV offset, TLV3201.json p1) stays as a footprint-compatible alternate.
- Threshold from a filtered PWM or a small DAC, set in simulation.

### Footprints

- All three TLV parts share SOT-23-5 (and dual SOIC-8) footprints, so the choice can change at assembly. TLV9061 and TLV3201 SOT-23-5 pinouts `VERIFY`.
- Duals and quads: TLV9062, TLV9064 by default. TLV9002, TLV9004 the cheaper alternative for the shaper only.

## Sources

- `datasheets/TLV9001.json` p14, p17; `TLV9061.json` p10, p13; `TLV3201.json` p1.
