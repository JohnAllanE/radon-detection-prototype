# The radon decay chain, read for this detector

<!-- doclint-allow: words — a reading reference the user asked for (2026-11-22), one topic: the chain against this detector's timescales -->

**Conclusion:** The detector never counts radon itself. It counts the alphas of three polonium isotopes sitting on the die. Po-218 (half-life 3.10 min) is born as a positive ion in the gas and drifts to the die in milliseconds, which is what the field simulations S-01 to S-03 model. Po-214 follows on the same die about an hour later, after two beta decays. Po-210 builds up over months and stays as background. None of the radon chain decays in the milliseconds of the drift. The millisecond concern in S-03 is the ion **losing its charge** (neutralisation) before it arrives, after which the field no longer steers it.

**Relied on by:** R-01 (progeny collected on the die), R-09 (lines to separate), R-31 (static runs), R-47 (ion steering), R-53 (comparing boards), S-03 (transit against neutralisation). Line energies and their separation: [decay-chain lines](decay-chain-lines.md).

## Working

![The radon-222 chain in two rows. In the gas: Rn-222, 3.82 days, alpha 5.49 MeV. On the die, counted every run: Po-218, 3.10 minutes, alpha 6.00 MeV, then Pb-214 about 27 minutes and Bi-214 19.9 minutes, both beta and not counted, then Po-214, 164 microseconds, alpha 7.69 MeV. Long-lived, building up over months: Pb-210 22.2 years and Bi-210 5.0 days, both beta, then Po-210, 138 days, alpha 5.30 MeV, ending at stable Pb-206.](../diagrams/decay-chain.svg)

### One radon atom through the chamber

1. **Rn-222 decays in the gas.** At 3.82 days it hardly changes during a run. Its 5.49 MeV alpha reaches the die only from within a few cm of gas (about 4 cm range in air, `VERIFY`), losing energy on the way, so it shows as a tail below 5.49 MeV rather than a line.
2. **Po-218 is born and recoils.** The alpha kicks the new atom back with about $5.49 \times 4/218 \approx 0.10$ MeV, and it stops within roughly 0.1 mm of gas (`VERIFY`). Most of these atoms are positive ions at that point (often quoted near 90 %, `VERIFY`). That is why a +1 kV tube with the die at 0 V collects them at all.
3. **It drifts to the die, racing three losses.**
   - Neutralisation: the ion picks up an electron from a trace gas or water molecule, or meets a negative ion made by the alpha tracks. A neutral atom no longer follows the field: it diffuses and sticks to the nearest wall, usually the tube. Water vapour speeds this up, which is why radon monitors dry the gas ([gas train](gas-train.md)). The time scale for our dried gas is not known here (`VERIFY`). It decides how much S-03's slower transit costs.
   - Gas flow: in flow-through runs, ions in weak-field regions are carried downstream (S-01, point 8). Static runs (R-31) avoid it.
   - Decay in flight: negligible, minutes against milliseconds.
4. **Po-218 on the die.** It decays with a 3.10 min half-life. Its 6.00 MeV alpha goes into the die about half the time and is counted. The other half leave upwards and are lost. The Po-218 count rate settles about 15 min (5 half-lives) after radon is introduced.
5. **Recoil off the die.** When the alpha goes into the die, the Pb-214 daughter recoils the other way, out of the surface into the gas. When the alpha goes up, the daughter is driven into the die and stays. So roughly half of the Pb-214 can leave the die (`VERIFY`: some is recaptured, and charged recoils drift back in the field). Po-214 counts can therefore fall below Po-218 counts. Their ratio is a useful diagnostic, not a fault.
6. **Pb-214 and Bi-214 decay by beta (about 27 and 19.9 min).** A beta leaves only tens of keV in the die, below the alpha threshold, so it isn't counted (`VERIFY` against the threshold). Bi-214 then gives Po-214, which decays 164 µs later, at once by the detector's standards: 7.69 MeV. Po-214 counts take about 3 hours to settle and take as long to die away after the radon is removed.
7. **Pb-210 stays (22.2 years).** Each Po-214 decay that keeps its recoil on the die leaves a Pb-210 atom. Through Bi-210 (5.0 days) it feeds Po-210 (138 days, 5.30 MeV). That line grows slowly with each board's exposure history and doesn't go away.

### Timescales against what the detector does

| Process | Time | What it means here |
|---|---|---|
| Ion drift to the die | 13 ms to 1 s (S-02, S-03) | Must beat neutralisation and, in flow runs, the flow |
| Neutralisation | Unknown here; depends strongly on humidity and trace gases (`VERIFY`) | The open number behind the S-03 mouth size. A measurement can settle it: count rate against $V_{tube}$ or against geometry |
| Po-218 on the die | 3.10 min; about 15 min to settle | Fast response: a short run reads Po-218 alone |
| Po-214 on the die | About 3 h to settle and to clear | Memory: after a radon run, wait hours before an N₂ control run, or subtract the decaying Po-214 |
| Rn-222 in a sealed chamber | 3.82 d | Static runs lose about 17 % of their radon per day: correct for it |
| Pb-210 → Po-210 | Months to years | Background grows with each board's history. For R-53, give both boards in a chamber the same history |

At equilibrium, each radon decay in the collected volume gives one Po-218 and one Po-214 decay on the die, each with about a 50 % chance of entering it. Hence "up to two alphas per radon decay" in [chamber sensitivity](chamber-sensitivity.md).

### Thoron (Rn-220), briefly

- Rn-220 has a 55.6 s half-life, so most of it decays in a long gas line before reaching the chamber. Weld samples (Part 2) may carry thorium and so produce it directly.
- Its first daughter, Po-216 (0.145 s, 6.78 MeV), is the one daughter whose decay competes with the drift: at S-03's 50–500 ms transits, a good share decays before arriving.
- Pb-212 (10.6 h) then feeds Bi-212 (60.6 min): 36 % alpha at 6.05 MeV, close to Po-218, and 64 % beta to Po-212 (0.30 µs, 8.78 MeV). Its signature is the 6.78 and 8.78 MeV lines ([physics reference](physics-reference.md)).

## Sources

- NNDC NuDat 3 (ENSDF), retrieved 2026-11-21 for Rn-222, Po-218, Po-214 and Po-210, as cited in [decay-chain lines](decay-chain-lines.md).
- Half-lives of Pb-214, Bi-214, Pb-210, Bi-210 and the thoron chain: standard values from Claude's background knowledge, `VERIFY` against NuDat.
- Charged fraction, recoil range, recoil loss from the die and neutralisation: general radon-progeny literature, not checked against a source here, `VERIFY`.
