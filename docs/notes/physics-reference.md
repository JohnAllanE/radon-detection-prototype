# Physics reference: alpha energies, charge and energy loss

**Conclusion:** A 6 MeV alpha releases about 1.7 × 10⁶ pairs in silicon (about 270 fC, 44.3 fC per MeV), and rough vacuum of about 1–10 mbar or below makes the energy loss over a 5–10 mm gap negligible. All values here are standard or recalled figures, `VERIFY` before they drive a design decision.

**Relied on by:** R-03 (Part 2 in rough vacuum), R-08 (energy range), R-09 (energy resolution), R-39 and R-43 (die-corner gap and no HV below ambient), the architecture's gain and noise budgets.

## Working

### Charge per alpha

- Si pair-creation energy: about 3.6 eV per pair (3.62 eV in the budgets), `VERIFY`.
- A 6 MeV alpha: about 1.7 × 10⁶ pairs, about 270 fC.
- Charge per MeV: $Q = \dfrac{1\ \text{MeV}}{3.62\ \text{eV}} \times 1.602 \times 10^{-19}\ \text{C} = 44.3$ fC. 6.0 MeV gives 266 fC, 7.69 MeV gives 340 fC, 8.78 MeV gives 389 fC.

### Alpha energies (MeV, `VERIFY` against ENSDF)

| Nuclide | Energy | Note |
|---|---|---|
| Po-218 | 6.00 | Radon progeny |
| Po-214 | 7.69 | Radon progeny |
| Po-210 | 5.30 | From Pb-210 (half-life about 22 y): accumulates on surfaces, shows as background |
| Po-216 | 6.78 | Thoron chain |
| Po-212 | 8.78 | Thoron chain |
| Bi-212 | 6.05 | Thoron chain, 36 % branch |
| Rn-220 | 6.29 | Thoron |

- Self-contamination: Pb-210 and Po-210 deposited by previous air runs stay on the photodiode and chamber, which is why the N₂ control run exists (D-05).
- Weld contamination may need roughly 4–9 MeV (Th and U chains, Q-05).
- Telling Bi-212 6.05, Rn-220 6.29 and Po-216 6.78 MeV apart for thoron or weld work needs about 100 keV FWHM or better (R-09). Po-210, Po-218 and Po-214 separate easily at that resolution.

### Energy loss in rough vacuum (Part 2)

- A 5.5 MeV alpha loses roughly 1 MeV per cm of air at atmospheric pressure, so about 10 keV per cm at 10 mbar (`VERIFY`).
- Over the 5–10 mm sample gap (D-19): about 100 keV at 100 mbar, 10 keV at 10 mbar, 1 keV at 1 mbar, about 10 eV at 10⁻² mbar.
- So anything at or below about 1–10 mbar is enough for R-09. The Edwards E2M8 reaches 1×10⁻³ mbar (D-24), about four orders of magnitude of margin.

### Alpha ranges and dead layer in silicon

- Ranges: about 30 µm at 5.5 MeV and 65 µm at 8.8 MeV (`VERIFY` with NIST ASTAR). The VTH2110 depletes more than 90 µm at 20 V (VTH2110.json p1), so 20 V stops alphas inside the depletion layer.
- A 150 nm dead layer (VTH2110.json p1) costs about 25 keV at normal incidence (about 160 keV/µm in Si, `VERIFY`), more at the oblique angles usual for ions plated on the surface.

### Breakdown at reduced pressure (Paschen, `VERIFY`)

- Die corner to the 1 kV wall: about 2.1 mm (21 mm bore) to 2.6 mm (22 mm bore). At 1 atm the average field is small, about 5 kV/cm.
- Uniform-field estimate for 2.1 mm at 100 mbar: about 1.46 kV. Corners are worse, so R-43 (no HV below ambient) stays.
- An earlier rough estimate: a gap of about 1 mm can approach 1 kV near 100 mbar, and the ~8 mm gaps are safe down to about 15 mbar.

## Sources

- `datasheets/VTH2110.json` p1, p3 (to migrate to component-data).
- ENSDF and NIST ASTAR, not yet consulted (`VERIFY`).
- Edwards E2M8 instruction manual, Table 3 (decisions D-24).
