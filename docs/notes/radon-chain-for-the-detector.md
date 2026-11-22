# The radon decay chain, read for this detector

<!-- doclint-allow: words — a reading reference the user asked for (2026-11-22), one topic: the chain against this detector's timescales -->

**Conclusion:**

- The detector never counts radon itself. It counts the alphas of three polonium isotopes on the die: Po-218 (3.10 min), Po-214 about an hour later after two beta decays, and Po-210, which builds up over months as background.
- Po-218 is born, about 88 % of the time, as a positive ion that drifts to the die. None of the chain decays during the drift.
- The risk in flight is the ion **losing its charge** (neutralisation). Measured rates in air give a charged lifetime of 11–70 s. Against S-03's transits (0.03–0.7 s), that costs about 1 % in dried gas and at most about 6 % at 50 % RH for the best geometry.
- New finding: Bi-214's beta can trigger the channel, and Po-214's alpha follows 164 µs later. A dead time longer than that loses Po-214 counts, unless the threshold for radon runs sits above the betas.

**Relied on by:** R-01 (progeny collected on the die), R-09 (lines to separate), R-13 and A-15/A-26 (trigger threshold and dead time), R-31 (static runs), R-47 (ion steering), R-53 (comparing boards), S-03 (transit against neutralisation). Line energies: [decay-chain lines](decay-chain-lines.md). Papers and manuals: [references](../references/README.md).

## Working

![The radon-222 chain in two rows. In the gas: Rn-222, 3.82 days, alpha 5.49 MeV. On the die, counted every run: Po-218, 3.10 minutes, alpha 6.00 MeV, then Pb-214 27.1 minutes and Bi-214 19.7 minutes, both beta giving small pulses, then Po-214, 164 microseconds, alpha 7.69 MeV. Long-lived, building up over months: Pb-210 22.2 years and Bi-210 5.0 days, both beta, then Po-210, 138 days, alpha 5.30 MeV, ending at stable Pb-206.](../diagrams/decay-chain.svg)

### One radon atom through the chamber

1. **Rn-222 decays in the gas** (3.82 d). Its 5.49 MeV alpha has a range of 4.15 cm in air (NIST ASTAR, projected range). It reaches the die only from within that distance, losing energy on the way, so it shows as a tail below 5.49 MeV rather than a line.
2. **Po-218 is born and recoils** with about $5.49 \times 4/218 \approx 0.10$ MeV. Its stopping distance in gas is quoted near 0.1 mm (`VERIFY`: no source found yet). The alpha strips electrons as it leaves. Within milliseconds some are recaptured, leaving **88 % positively charged** (Wellisch 1913, via Porstendörfer 2004; Hopke 1989 via Daya Bay). Hosokawa (2015) says "more than 90 %". In air the atom at once forms PoO₂ and gathers water and trace gases into a cluster about 1 nm across.
3. **It drifts to the die, racing three losses.**
   - Neutralisation. Chu and Hopke (1988) found three paths: direct electron transfer to the charged PoO₂ (dominant in air), recombination with small negative ions made by the alpha tracks, and electron scavenging by OH radicals from radiolysed water (dominant without oxygen, as in the N₂ control gas). Measured total rates in air: $1.5 \times 10^{-2}$ s⁻¹ at 0.1 % RH, $4.9 \times 10^{-2}$ at 11 %, $7.8 \times 10^{-2}$ at 50 %, $8.9 \times 10^{-2}$ at 70 % (Porstendörfer 2004, table 2). That is a mean charged life of 11 to 70 s. Those rates were measured at a high ionisation rate. Two of the paths scale with its square root, so in our chamber the rates should be lower.
   - Slower ions in wet gas. Water clusters lower the ion's mobility, so it has more time to be neutralised (RAD7 manual, 3.12.2). Cluster mobility is 0.7–2 cm²/(V·s) (Porstendörfer 2004, p. 63). S-01 to S-03 assume 2, the fast end, so their transit times may be up to 2.9 times too short.
   - Gas flow in flow-through runs (S-01, point 8). Decay in flight is negligible.
4. **Po-218 on the die** decays with a 3.10 min half-life. Its alpha goes into the die about half the time and is counted. The Po-218 rate settles about 15 min after radon is introduced. The RAD7's Sniff mode counts Po-218 alone for this reason.
5. **Recoil off the die.** When the alpha goes into the die, the Pb-214 recoils out of the surface. On a flat surface that is at most half of the decays. Measured recoil loss from aerosol particles is 0.5 ± 0.15 (Porstendörfer 2004). A charged recoil may drift back in the field, so for our die the figure is `VERIFY`. Po-214 counts can fall below Po-218 counts. Their ratio is a diagnostic, not a fault.
6. **Pb-214 (27.1 min) and Bi-214 (19.7 min) decay by beta.** A beta crossing the VTH2110's depletion layer (at least 90 µm at 20 V, VTH2110.json) leaves roughly 25–35 keV, and a slow one leaves all its energy. That is above the 15 keV trigger threshold (architecture), so **betas trigger**. They sit far below the alpha window, so they never enter the radon spectrum. But Bi-214's beta comes 164 µs before Po-214's alpha. If the beta triggers, the conversion dead time hides the alpha: 12 % of the time for 30 µs (ADS8689 path), 88 % for 0.5 ms (ADS1220). About half of the betas go into the die, so this loses 6–44 % of Po-214 counts. A threshold of a few hundred keV in radon runs removes the problem, and A-15's threshold is programmable.
7. **Pb-210 stays (22.2 years)** and feeds Po-210 (138 d, 5.30 MeV) through Bi-210 (5.0 d). The Super-K detector saw this line grow with its diode's history (Nakano 2017).

### Timescales against what the detector does

| Process | Time | What it means here |
|---|---|---|
| Ion drift to the die | 13 ms to 0.7 s at 2 cm²/(V·s) (S-02, S-03); up to 2.9 times longer at 0.7 | Fast against neutralisation |
| Neutralisation in air | Mean life 11 s (dry) to 70 s; 11 s at 70 % RH | About 1 % loss in dried gas for S-03's best geometry. Keep the desiccant (RAD7: below 10 % RH needs no correction) |
| Po-218 on the die | 3.10 min; about 15 min to settle | A short run reads Po-218 alone |
| Bi-214 → Po-214 | 164 µs | Longer than the dead time: set the radon-run threshold above the betas |
| Po-214 on the die | About 3 h to settle and to clear | After a radon run, wait hours before an N₂ control run, or subtract it |
| Rn-222 in a sealed chamber | 3.82 d | Static runs lose 16.6 % of their radon per day: correct for it |
| Pb-210 → Po-210 | Months to years | For R-53, give both boards in a chamber the same history |

Field results with the same design give a scale. Super-K's 80 L detector at −2 kV loses 26 % of its sensitivity between 0.002 and 4.1 g/m³ of water ($CF = 2.25 - 0.29\sqrt{AH}$, Nakano 2017). Its drift paths are tens of cm, so its transits are seconds. Our 38 mm tube collects ten to a hundred times faster.

### Thoron (Rn-220), briefly

- Rn-220 (55.6 s) mostly decays in a long gas line. Weld samples (Part 2) may carry thorium and produce it directly.
- Po-216 (0.144 s, 6.78 MeV) is the one daughter whose decay competes with the drift: at S-03's transits, from a few per cent to about half decay before arriving.
- Pb-212 (10.6 h) feeds Bi-212 (60.6 min): 36 % alpha at 6.05 MeV, near Po-218. The other 64 % beta-decay to Po-212 (0.29 µs, 8.78 MeV, range 8.8 cm in air).

### Alpha ranges in air (NIST ASTAR, projected range, dry air at sea level)

| Line | 5.30 MeV (Po-210) | 5.49 MeV (Rn-222) | 6.00 MeV (Po-218) | 6.78 MeV (Po-216) | 7.69 MeV (Po-214) | 8.78 MeV (Po-212) |
|---|---|---|---|---|---|---|
| Range | 3.93 cm | 4.15 cm | 4.76 cm | 5.77 cm | 7.05 cm | 8.76 cm |

## Sources

- Half-lives and branchings: IAEA LiveChart API (ENSDF), retrieved 2026-11-22. Line energies: NuDat 3, as in [decay-chain lines](decay-chain-lines.md).
- Ranges: NIST ASTAR, material 104, retrieved 2026-11-22.
- Papers and manuals: [references](../references/README.md). Charged fraction, neutralisation rates and paths, mobility, recoil loss: Porstendörfer et al. 2004 (BMU 2004-644). Humidity in practice: RAD7 manual, Hosokawa 2015, Nakano 2017, Daya Bay 2016.
- Beta energy in the die: Claude's estimate from silicon's stopping power for fast electrons (about 0.39 keV/µm, textbook value) and the depletion depth.
