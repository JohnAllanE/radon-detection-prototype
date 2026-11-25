# Why the Cremat module beats the op-amps, and whether it matters

**Conclusion:** The Cremat CR-110's lower noise comes from a large discrete JFET input sized to the detector, not from trimming. A JFE2140 matched pair ahead of an OPA140 would reach about 2–3.5 keV FWHM, below the ADA4817-1. The detector's own width (tens of keV) hides it in the alpha peaks, so it shows in the test-pulse width. It is built as the fourth probe type (A-31).

**Relied on by:** A-06 and A-07 (CSA op-amps), A-31 (JFET probe), R-53 (similar readings).

## Working

### Where the difference comes from

- No per-unit trimming shows in the public documents (CR-110-R2.1.json p1), and the input transistor isn't disclosed.
- Series noise is set by the input transistor's transconductance. Cremat's ENC slope of 3.8 e/pF implies about 0.6–1.2 nV/√Hz, depending on what its "Gaussian shaping time constant" means (undefined in the datasheet, and the "µ" is missing from the extracted text).
- The op-amps are at 4.0 nV/√Hz (ADA4817-1), 5.1 (OPA140) and 6.5 (LMP7721): a 4–8× gap.
- A module uses a large, high-gm discrete JFET biased at a few mA, with tens of pF of gate capacitance. CR-110 runs on ±6 V at about 85 mW (`VERIFY`).
- A JFET's series noise is lowest when its input capacitance is near the detector's (a classic rule): 10–30 pF for a 33 pF diode.

### Check with the budget script

- A hypothetical BF862-class JFET (about 0.8 nV/√Hz and about 10 pF from a search snippet, datasheet not pulled, `VERIFY`) in front of a fast op-amp gives about 233 e (2.0 keV FWHM) at 1 µs, close to the module's roughly 325 e (2.8 keV).
- With a JFET front end, series noise falls to 70–110 e at 4–10 µs. The diode's shot noise (80–480 e for 0.15–2 nA) and the 100 MΩ feedback resistor (150–240 e) take over. Practical floor: about 2–3 keV FWHM at typical leakage, about 5 keV at 2 nA.

### The JFET probe (A-31)

**What a JFET input stage is.** An op-amp's noise is set by its input transistors, which are small so its input capacitance stays low. A discrete JFET is large and run at a few mA, so its transconductance $g_m$ is high and its noise voltage, roughly $\sqrt{4kT \cdot \tfrac{2}{3} / g_m}$, is low. Placed ahead of the op-amp with voltage gain, it sets the noise and the op-amp's own noise is divided by that gain.

**Why a matched pair.** Two JFETs as a differential pair, sources joined to a current sink, drains on resistors to the positive rail and into the op-amp's inputs. One gate is the CSA input, the other sits at 0 V.

- The input node rests at 0 V, like the op-amp probes: the 0 V guard (A-11), the test port (A-09) and the diode bias are unchanged. A single JFET would hold its gate about 1 V negative.
- Offset and drift cancel between the matched halves.
- The price is $\sqrt{2}$ in noise, since two devices contribute: 1.27 nV/√Hz at 5 mA each, against 5.1 for the OPA140 alone.

**The part.** TI JFE2140 (TI product page, datasheet tables not extracted, `VERIFY`): 0.9 nV/√Hz at 5 mA and 1.1 at 2 mA (1 kHz), 13 pF input capacitance at $V_{DS}$ = 5 V, 30 mS, 10 pA maximum gate current, SOIC-8 or 2 mm WSON, active. The BF862 named earlier is no longer manufactured (NXP product page).

**Result** (`enc_budget.out.txt`, typical to maximum leakage): 2.2–3.3 keV FWHM at 4 µs with 5 mA per device, 2.4–3.5 keV with 2 mA. The diode's shot noise and $R_f$ now dominate, so more JFET current buys little: 2 mA each, about 36 mW on ±4.5 V.

**The cascode.** A cascode is a second transistor stacked on each drain that holds the JFET's drain voltage fixed. It stops the gate-drain capacitance being multiplied by the stage's gain (the Miller effect) and keeps gate leakage low. Here the op-amp already holds the two drains within microvolts of each other, and the ±4.5 V rails keep the drain-gate voltage to a few volts. So the cascode is expected to buy little. Working: build the pair without it, and add it only if the pass-2 simulation shows a gain.

**To simulate first (pass 2).** The pair adds gain inside the loop, so the composite must be checked for stability with the diode connected and with the test port open (R-60), as the OPA657 failed to be.

### If a noise reference is wanted

One Cremat CR-110-R2.1 on a bench fixture. The other probes: [four-probe plan](four-probe-plan.md).

## Sources

- `datasheets/CR-110-R2.1.json` p1, `sim/analytic/enc_budget.out.txt`.
- BF862 figures from a web search snippet, not a datasheet (`VERIFY`). Status: nxp.com/products/BF862, "No Longer Manufactured".
- JFE2140: ti.com/product/JFE2140 (features list), datasheet Rev. B. Application notes SBOA563 and SBOA589, not read.
