# Detector board: mounting, bias, CSA input and cleanliness

**Conclusion:** Which VTH2110 electrode is on top is unknown and decides the bias polarity, pulse polarity, ion steering and which pad is the sensitive node: a DMM diode test on a spare chip settles it before layout. The input node needs a 0 V guard, RMA flux, an IPA clean and a bake.

**Relied on by:** A-01 to A-12 (detector board choices), R-06, R-47, R-48, R-52, R-54, R-60, Q-11, Q-24, Q-26.

## Working

### Photodiode mounting (Q-26)

- The datasheet shows a bond pad on the top face and a conductive-epoxy die attach (VTH2110.json p1, p2). It doesn't say which electrode is on top.
- Die attach with conductive epoxy to a pad (back contact), plus a connection to the 0.4 mm top bond pad.
- Options: wire bond (needs a bonding-compatible finish, plain ENIG may not suit ultrasonic bonding, `VERIFY`), or a fine wire attached with conductive epoxy by hand.
- Excelitas offers chips "assembled on a carrier" (p1): ask if hand bonding is impractical.

### Which node is sensitive

- If the top face is the anode: CSA input on the small top pad, bias on the large die-attach pad (low impedance).
- Otherwise bias and ion-steering polarity reverse, and the large pad becomes the CSA input node: more area, more capacitance, more noise. Measure first.

### Bias (Q-11)

- 20 V default. Dark current is specified at 20 V and 40 V, breakdown > 100 V (VTH2110.json p1).
- Depletion is more than 90 µm at 20 V, deeper than the alpha ranges, so 20 V is enough.
- Higher bias lowers C (about 32 pF at 20 V to about 21 pF at 50 V, Fig 3, approximate) and so noise, but raises dark current.
- Per-board filter: RC low-pass (R about 1 MΩ, C about 100 nF, to simulate) from the HV board. One bias for all four diodes, a resistor per diode so one leaky diode doesn't load the others.

### CSA and test charge

- Non-inverting input at 0 V, ±4.5 V rails. $C_f$ = 1 pF C0G (tolerance and stray to measure) in parallel with $R_f$ = 100 MΩ (decay 100 µs).
- Output series resistor for cable isolation, value from simulation. Pulse polarity follows the diode, and the MCU board's input stage handles either.
- Test charge (R-49): about 1 pF C0G per channel from a common TEST line, $Q = C_{test} \Delta V$. It adds about 1 pF at the input, acceptable at 33 pF.

### Test port (R-60, electrometer D-02)

- A Murata SWF switched coaxial connector per CSA input, on the back side, in series between diode node and CSA input, shell on the 0 V guard ring. $C_{test}$ sits on the diode side.
- SWF 2.5 × 2.5 mm, rated 100 cycles. Service boards see 1–2 mating cycles per connector. A bare-board test board uses the same footprints.
- With its diode disconnected, the CSA must be stable at a noise gain of 1 (electrometer requirements).
- Fit: four connectors with guard rings plus the CSAs on the back of the board, quoted as "≤ 20 mm" (electrometer Q-13). `VERIFY` against the board outline, which must also cover the 21–22 mm bore and O-ring land.

### Guarding and cleanliness (R-48)

- Keep the input trace short and straight, inside a guard trace at 0 V on the same layer. Remove solder mask over it if the fab permits (`VERIFY`). Keep the node off the board edge and away from digital lines.
- Coat the atmosphere side only in a way that doesn't add leakage.
- Flux residue is a real leakage path. ADA4530-1.json p38 recommends RMA paste, an ultrasonic IPA clean and a 125 °C bake (about 15 min clean plus 1.5 h bake for RMA, much longer for no-clean).
- Hand-assemble the input nodes with RMA flux, clean, bake, handle with gloves.

### Humidity

VTH2110 is rated to 60 % RH non-condensing (VTH2110.json p2). Keep spare chips in a dry box and assemble dry.

### Connector (R-24)

Molex PicoBlade-style, pin count ≤ 15 `VERIFY`. Proposed 14 pins: OUT1–4 each paired with a ground, +4.5 V, −4.5 V, GND, PD bias, ring bias, TEST.

### Rails

±4.5 V from the MCU board's LM27762, plus a local RC or ferrite filter and bulk capacitance per board. LM27762 noise and PSRR are not extracted: `VERIFY` before relying on it for a CSA rail.

## Sources

- `datasheets/VTH2110.json` p1, p2, Fig 3; `ADA4530-1.json` p38; `LM27762.json`.
- Murata SWF lineup page (electrometer requirements R-19).
