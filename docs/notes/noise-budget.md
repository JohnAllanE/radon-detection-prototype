# Noise budget for the charge-sensitive preamp

**Conclusion:** A plain op-amp CSA gives roughly 4–14 keV FWHM, depending on part and shaping time, against the 100 keV target (R-09). The detector's dead layer and straggling (tens of keV) will dominate the peak width, so the premium and low-cost boards are expected to look similar in the spectrum.

**Relied on by:** A-05 to A-07 (CSA and its op-amps), A-14 (shaping time), R-09 (energy resolution), R-53 (similar readings), the noise rows of the architecture's Expected performance.

## Working

### Why input noise matters

- An alpha arrives as a small charge (266 fC at 6 MeV). Noise at the preamp input is indistinguishable from it, and every later stage amplifies both, so the signal-to-noise ratio is fixed at the input. The CSA op-amp is chosen on noise, the later stages are not.
- Noise is quoted as equivalent noise charge (ENC, electrons rms): $\text{FWHM}\,[\text{keV}] = 2.355 \times \text{ENC} \times 3.62\ \text{eV}$. So 7 keV FWHM is about 1900 e FWHM, about 820 e rms.
- It sets the floor twice: the peak width, and the comparator threshold, about 5σ above baseline noise (σ of 3 keV puts the threshold near 15 keV, far below any 5–9 MeV alpha).
- Leakage enters twice too: as shot noise ($2qI$) and as DC offset. That is why board leakage matters and why the electrometer exists.

### Inputs (`sim/analytic/enc_budget.py`)

- $C_{pd}$ 33 pF (spec < 30 pF at 20 V, curve about 32 pF, VTH2110.json p1, p3), 2 pF stray, $C_f$ 1 pF, $R_f$ 100 MΩ.
- CR-RC shaping, form factor 0.924 (`VERIFY`), 3.62 eV per pair (`VERIFY`), dark current 0.15 nA typical to 2 nA maximum.
- Op-amp input capacitance: OPA140 17 pF, OPA656 3 pF (datasheets). OPA657 and LMP7721 not extracted, 5 pF assumed.

### Results (FWHM in keV, typical to maximum leakage)

| Op-amp ($e_n$) | τ 1 µs | 2 µs | 4 µs | 10 µs | CSA rise (10–90 %) |
|---|---|---|---|---|---|
| OPA140 (5.1 nV/√Hz) | 13.6 keV | 9.6 | 6.9–7.4 | 4.9–6.3 | about 1.7 µs |
| OPA656 (6.0) | 11.7 | 8.3 | 6.0–6.5 | 4.4–5.9 | about 60 ns |
| OPA657 (4.8, $C_{in}$ assumed) | 9.8 | 7.0 | 5.1–5.7 | 3.9–5.5 | about 9 ns |
| LMP7721 (6.5, $C_{in}$ assumed) | 13.3 | 9.5 | 6.8–7.3 | 4.8–6.2 | about 0.8 µs |
| ADA4817-1 (4.0, GBW ≥ 410 MHz) | 7.5 | 5.4 | 4.0 | 3.3 | about 31 ns |
| ADA4530-1 (14, 2 MHz) | 30.8 | 21.8 | 15.5 | 10.0 | about 7.5 µs |
| Cremat CR-110 (benchmark) | about 2.8 keV (200 e + 3.8 e/pF × 33 pF, at 1 µs) | | | | 3 ns |

- The two ADI rows are typical-leakage values from the same script.
- Downstream: a TLV900x first stage at gain 1 (27 nV/√Hz, TLV9001.json p17) adds about 0.7 keV FWHM at 4 µs (0.44 keV at 10 µs), small in quadrature against 7 keV, and smaller with first-stage gain. The TLV9061's 10 nV/√Hz adds about a quarter of that.
- Series noise dominates. Leakage shot noise and $R_f$ noise are a minor part.
- For OPA140 the CSA rise (1.7 µs) is shorter than a 4 µs shaping time, so ballistic deficit is a constant gain loss, not a resolution loss. Use τ ≥ 4 µs with OPA140.

### Limits of the model

- Ignores 1/f noise, assumes CR-RC rather than CR-RC^n, ignores layout parasitics and the non-ideal op-amp.
- Expect real numbers a few keV worse. `VERIFY` with an ngspice `.noise` simulation.

### What the detector adds

- A 150 nm dead layer costs about 25 keV at normal incidence, more at oblique angles ([physics reference](physics-reference.md)).
- A 7 keV op-amp amplifier and a 3 keV JFET amplifier, added in quadrature to a 25–50 keV physical width, give 26 against 25 keV: not visibly different. Details: [JFET and module noise](jfet-and-module-noise.md).

## Sources

- `sim/analytic/enc_budget.py` and `enc_budget.out.txt`.
- `datasheets/*.json`: VTH2110 p1, p3; OPA140 p7; OPA656 p5; ADA4817-1 p1, p4; TLV9001 p17; CR-110-R2.1 p1.
