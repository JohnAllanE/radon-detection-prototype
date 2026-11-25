# Four probes on four channels: the comparison plan

**Conclusion:** One instrument with four channels: two probes on the radon tube (one at each end, on its axis) and two on the vacuum chamber, swapped at intervals. Four probe types differ only in the CSA. The radon lines give each probe an absolute energy scale over about a day, and the test pulse covers minutes to hours.

**Relied on by:** R-05 (two probes per chamber, rotated), R-06 (one diode per probe, four channels), R-52 (drift), R-53 (similar readings), A-07, A-27, A-29, A-31 (JFET probe), A-32 (test pulse), [test pulse and monitor outputs](test-pulse-and-monitor.md).

## Working

### Terms

- A **probe** is one detector board: one VTH2110 on the tube axis, one CSA, its test-pulse parts and connector.
- A **channel** is one MCU-board chain: pole-zero, shaper, trigger, peak hold, ADC input, monitor output.

### The four probe types

Same board outline, connector and pinout (R-07). Only the CSA differs. Resolution is the electronics alone at τ = 4 µs, typical to maximum diode leakage (`sim/analytic/enc_budget.out.txt`).

| Probe | CSA | FWHM | What it tests |
|---|---|---|---|
| P-A | ADA4817-1 | 4.0–4.7 keV | Lowest-noise single op-amp |
| P-L | LMP7721 on local ±2.5 V | 6.8–7.3 keV | Leakage control: fA bias, guard pins |
| P-T | OPA140 on the standard SOIC-8 footprint (R-10) | 6.9–7.4 keV | The low-cost baseline |
| P-J | JFE2140 matched JFET pair ahead of an OPA140 (A-31) | 2.2–3.5 keV | Whether a cheap JFET stage beats the premium parts |

- The LTC6268 was read as an alternative for P-L and not taken: same leakage idea, no lower noise at 4 µs ([survey](candidates-csa-opamp.md)).
- P-J is expected to be the quietest probe, not a midpoint: about 2–3 keV against 4 keV for the ADA4817-1. Details: [JFET and module noise](jfet-and-module-noise.md).
- The alpha peaks are tens of keV wide from the die's dead layer ([noise budget](noise-budget.md)), so all four spectra should look alike (R-53). The probes' electronic noise is read from the test-pulse peak width instead, where it is the only contribution.

### Arrangement and swapping

- Radon side: both probes see the same gas in the same tube, so their count ratio compares collection and efficiency directly.
- Vacuum side: two probes face the sample. The sample's emission is not symmetric, so only swapping separates the probe from its position.
- Each swap is logged with the probe serial, the channel and the position (R-27). Moving a probe to another channel also separates the probe from the MCU-board chain.
- Four periods put every probe in every position once. The schedule: `DECIDE AT TEST`.

### The radon lines as a calibration

- Po-218 (6003 keV) and Po-214 (7687 keV) decay on the die surface. Their energies are fixed by nuclear physics, so two peaks give each probe its gain and its offset, diode included.
- How fast drift can be seen is set by counting. A peak of width σ located from $N$ counts has a centroid error of $\sigma/\sqrt{N}$.
- Rate, working: S-03's index is 33.1 cm³ per detector. At 100 Bq/m³ that volume holds 3.3 mBq, 11.9 radon decays per hour. With 88 % charged and half the alphas entering the die, about 5 Po-218 counts per hour, and at most as many Po-214.
- So 100 counts per line take about 20 hours indoors. With a 50 keV FWHM peak (σ = 21 keV), the centroid is then known to 2.1 keV, 0.035 % of 6 MeV.
- The lines track drift over a day or more at indoor levels, faster in proportion to the radon level. Anything quicker needs the test pulse.
- The two references see different things. The lines see the whole probe, the pulse only the electronics. A line that moves while the pulse stays still points at the diode: dead layer, bias, charge collection.

### What a swap carries across

- Short-lived progeny on the die (Pb-214, Bi-214, Po-214) clear in about 3 hours. Wait that long after moving a probe to the vacuum side, or subtract them.
- Pb-210 (22.2 years) stays and feeds Po-210 (5304 keV). At most 10.5 atoms arrive per hour at 100 Bq/m³ (11.9 × 0.88), so 30 days leave at most 7,500 atoms.
- Their activity is $7500 \times \ln 2 / (22.2 \times 8766\ \text{h}) = 0.027$ decays per hour, half into the die: at most about 0.3 counts per day, per month of exposure, growing in over about a year (Po-210, 138 days).
- It is a sharp surface line at a known energy, so it can be told from a sample's alphas, which arrive degraded. A blank run in vacuum with no sample after each swap measures it for that probe.

## Sources

- `sim/analytic/enc_budget.out.txt`; `sim/field/S-03-reduced-end/README.md` (index, thin plates).
- [Decay chain for the detector](radon-chain-for-the-detector.md) (88 % charged, recoil loss, 3 hours to clear), [decay-chain lines](decay-chain-lines.md) (energies, half-lives).
