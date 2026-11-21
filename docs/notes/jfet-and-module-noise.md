# Why the Cremat module beats the op-amps, and whether it matters

**Conclusion:** The Cremat CR-110's lower noise comes from a large discrete JFET input sized to the detector, not from trimming. A JFET front end would reach about 2–3 keV FWHM, but the detector's own width (tens of keV) hides it, so a JFET is worth building only as a bench noise reference.

**Relied on by:** A-06 and A-07 (CSA op-amps), R-53 (similar readings), architecture question on a noise reference channel.

## Working

### Where the difference comes from

- No matching or calibration trick shows in the public documents: CR-110-R2.1.json p1 gives a measured, typical specification. Nothing on per-unit trimming, and the input transistor isn't disclosed.
- Series noise is set by the input transistor's transconductance. Cremat's ENC slope of 3.8 e/pF implies about 0.6–1.2 nV/√Hz, depending on what its "Gaussian shaping time constant" means (undefined in the datasheet, and the "µ" is missing from the extracted text).
- The op-amps are at 4.0 nV/√Hz (ADA4817-1), 5.1 (OPA140) and 6.5 (LMP7721): a 4–8× gap.
- A module uses a large, high-gm discrete JFET (or several in parallel) biased at a few mA. Its gate capacitance is tens of pF, which a general-purpose op-amp avoids (1.3 pF for ADA4817-1, 17 pF for OPA140). Power is spent freely: CR-110 runs on ±6 V at about 85 mW (`VERIFY`).
- For a JFET, series noise is lowest when its input capacitance is of the order of the detector's (a classic rule, quoted in a BYU thesis found by search). With a 33 pF diode, a JFET of 10–30 pF is the right size. That is the "component matching".

### Check with the budget script

- A hypothetical BF862-class JFET (about 0.8 nV/√Hz and about 10 pF from a search snippet, datasheet not pulled, `VERIFY`) in front of a fast op-amp gives about 233 e (2.0 keV FWHM) at 1 µs, close to the module's roughly 325 e (2.8 keV).
- With a JFET front end, series noise falls to 70–110 e at 4–10 µs. The diode's shot noise (80–480 e for 0.15–2 nA) and the 100 MΩ feedback resistor (150–240 e) take over. Practical floor: about 2–3 keV FWHM at typical leakage, about 5 keV at 2 nA.

### Options if premium noise is wanted

1. Buy one Cremat CR-110-R2.1 as a reference channel on a bench fixture.
2. A discrete-JFET plus op-amp CSA on one channel of a test board (BF862 or similar; 2SK152 and similar as alternates; datasheets and availability to check).
3. ADA4817-1 as the off-the-shelf premium, about 4 keV at 4 µs.

Amptek's A250 family is another module benchmark (not pulled: its app note was HTML only).

## Sources

- `datasheets/CR-110-R2.1.json` p1, `sim/analytic/enc_budget.out.txt`.
- BF862 figures from a web search snippet, not a datasheet (`VERIFY`).
