# References: papers and manuals

Open documents kept for the radon detector's physics notes. This repo is public, so only files whose licence allows redistribution are committed. The others are git-ignored: download them again from the URL, and check against the SHA-256 (first 16 hex digits shown).

| File | What it is | Used for | Licence | In git | SHA-256 (start) |
|---|---|---|---|---|---|
| `hosokawa-2015-ptep-80L-radon-detector.pdf` | K. Hosokawa et al., "Development of a high-sensitivity 80 L radon detector for purified gases", PTEP 2015, 033H01. [Kobe repository copy](https://da.lib.kobe-u.ac.jp/da/kernel/90002758/90002758.pdf) | Electrostatic collection on a PIN photodiode; HV and humidity dependence; "more than 90 %" of Po-218 charged | CC BY 4.0 | Yes | 9fc66dbd06893326 |
| `okamoto-2021-arxiv-2112.06614-large-pin.pdf` | K. Okamoto et al., "Improvement of radon detector performance by using a large-sized PIN-photodiode", [arXiv:2112.06614](https://arxiv.org/abs/2112.06614) | Larger diode: 3.8 % more efficiency below 1 g/m³, 10–20 % above | CC BY 4.0 | Yes | 2c757e44fe7cf90f |
| `nakano-2017-arxiv-1704.06886-sk-buffer-gas.pdf` | Y. Nakano et al., "Measurement of radon concentration in Super-Kamiokande's buffer gas", [arXiv:1704.06886](https://arxiv.org/abs/1704.06886) | Humidity fit $CF = 2.25 - 0.29\sqrt{AH}$; Pb-210 build-up on the diode | arXiv non-exclusive | No | 4252b9839907ddb4 |
| `takeuchi-1999-arxiv-hep-ex-9903006-sk-radon.pdf` | Y. Takeuchi et al., "Development of high sensitivity radon detectors", [arXiv:hep-ex/9903006](https://arxiv.org/abs/hep-ex/9903006) | The original SK design | arXiv (assumed) | No | 2b540bdb70e780a4 |
| `dayabay-2016-arxiv-1601.04885-radon-monitor.pdf` | "The radon monitoring system in Daya Bay reactor neutrino experiment", [arXiv:1601.04885](https://arxiv.org/abs/1601.04885) | $r_+$ = 88 % (citing Hopke, Health Phys. 57 (1989) 39); about 70 % collection; drying to 1 g/m³ | arXiv non-exclusive | No | b37809284a87b418 |
| `porstendoerfer-2004-bmu-schriftenreihe-644-radonzerfallsprodukte.pdf` | J. Porstendörfer et al., BMU Schriftenreihe Reaktorsicherheit und Strahlenschutz 2004-644 (German). [BMUV](https://bmuv.de/fileadmin/Daten_BMU/Download_PDF/Strahlenschutz/schriftenreihe_2004_644_radonzerfallsprodukte.pdf) | 88 % charged (Wellisch 1913); the three neutralisation mechanisms (Chu and Hopke 1988); measured neutralisation rates against RH (table 2); cluster mobility 0.7–2 cm²/(V·s) | Rights reserved | No | 0d99ac3106979fcd |
| `rad7-manual-durridge.pdf` | Durridge RAD7 user manual. [Durridge](https://durridge.com/documentation/RAD7%20Manual.pdf) | Why humidity lowers sensitivity (water clusters slow the ions); below 10 % RH no correction; Sniff mode counts Po-218 only | © Durridge, rights reserved | No | e87b0f52778bb47e |

Data services used without a saved file (retrieved 2026-11-22):
- Half-lives and branchings: IAEA LiveChart API, `https://nds.iaea.org/relnsd/v1/data?fields=ground_states&nuclides=<n>`.
- Alpha CSDA ranges in dry air: NIST ASTAR, material 104 (`https://physics.nist.gov/PhysRefData/Star/Text/ASTAR.html`).
