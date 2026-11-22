# Decay-chain lines, the resolution that separates them, and the Am-241 check source

**Conclusion:** The radon-chain lines that land on the photodiode are Po-210 5304 keV, Po-218 6003 keV and Po-214 7687 keV, with Rn-222 itself at 5489 keV from the gas. The closest pair is Po-210 and Rn-222, 185 keV apart: R-09's 100 keV FWHM separates them (1.85 FWHM), and 92 keV or better separates them by 2 FWHM. The electronics' 4–14 keV adds almost nothing in quadrature, so the detector (dead layer, entry angle, source foil) sets the peak width. A smoke-alarm Am-241 source (about 1 µCi, 37 kBq or less) emits 5486 keV, only 4 keV from Rn-222, and its 43 keV doublet is a direct test of resolution.

**Relied on by:** R-09 (resolution target), R-08 (range), R-51 (check source), Q-04, Q-14, A-14 (shaping time after first runs).

## Working

### Lines (NuDat 3 from ENSDF, retrieved 2026-11-21)

| Nuclide | Alpha energy | Intensity | Half-life | Where it decays | Source |
|---|---|---|---|---|---|
| Rn-222 | 5489.48 keV | 99.92 % | 3.82 d | In the gas: reaches the diode only from within an alpha range, after losing energy in the gas, so a tail below 5.49 MeV rather than a line | Singh et al., Nucl. Data Sheets 160, 405 (2019) |
| Po-218 | 6002.55 keV | 99.98 % | 3.097 min | On the diode, after ion collection (R-47) | Zhu and McCutchan, NDS 175, 1 (2021) |
| Po-214 | 7686.82 keV | 99.99 % | 163.6 µs | On the diode, after Pb-214 and Bi-214 (tens of minutes, `VERIFY` with NuDat) | Basunia, NDS 121, 561 (2014) |
| Po-210 | 5304.33 keV | 100 % | 138.38 d | On the diode, from Pb-210 built up by earlier runs: background that grows over months | Kondev, NDS 201, 346 (2025) |
| Am-241 | 5485.56 keV, 5442.80 keV, 5388 keV | 84.8 %, 13.1 %, 1.66 % | 432.6 y | Check source (R-51) | Basunia, NDS 107, 3323 (2006) |

The thoron-chain lines in [physics reference](physics-reference.md) are older figures, still `VERIFY`: Bi-212 at about 6.05 MeV sits about 50 keV from Po-218, which only a resolution near 25–50 keV separates.

### What "discriminate the chain" asks of the resolution

- Two equal Gaussian peaks of width $w$ (FWHM) show a dip between them once their separation $\Delta E$ exceeds $2\sigma = 0.85\,w$. For counting each peak with little spill-over, this project takes $\Delta E \ge 2w$ as the working criterion (Claude's choice: spill-over below a few per cent for Gaussians; real alpha peaks have a low-energy tail, so it is optimistic on the low side).

| Pair | $\Delta E$ | Needed FWHM ($\Delta E/2$) | At R-09's 100 keV |
|---|---|---|---|
| Po-210 and Rn-222 | 185.15 keV | 93 keV | Separated, 1.85 FWHM |
| Rn-222 and Po-218 | 513.07 keV | 257 keV | Easily |
| Po-210 and Po-218 | 698.22 keV | 349 keV | Easily |
| Po-218 and Po-214 | 1684.27 keV | 842 keV | Easily |
| Am-241 5485.56 and 5442.80 | 42.76 keV | 21 keV | Not separated: the doublet shows only as a shoulder |

- So R-09 at 100 keV meets the user's target, with Po-210 and Rn-222 the pair to watch. A low-energy tail on Po-218 (oblique entry, dead layer) spills into that region before any Gaussian width does.
- Widths add in quadrature: $w = \sqrt{w_{det}^2 + w_{el}^2}$. With the electronics at 4–14 keV ([noise budget](noise-budget.md)) and a 100 keV total, the detector may take $\sqrt{100^2 - 14^2} = 99$ keV. The electronics are not the limit; shaping time can be chosen after the first runs (Q-04).

### The smoke-alarm Am-241 source (Q-14)

- Activity: most current smoke detectors hold about 1 µCi (37 kBq) of Am-241 or less; some older units held up to 80 µCi (US NRC smoke detector fact sheet). A Kidde unit's manual states 0.9 µCi (33 kBq). Read the label of the unit used.
- Its line coincides with Rn-222 (3.92 keV apart): run it in N₂ or in Part 2 vacuum, so the gas holds no radon.
- Smoke-alarm sources are foils with a thin protective metal cover (`VERIFY`: thickness unknown here), which lowers and widens the peak. The 43 keV doublet will not show, and the peak position is not 5486 keV. That is why the user's plan transfers the source's peak and rate from a RAD7 measurement before using it as a reference.
- In air an alpha of 5.5 MeV loses roughly 1 MeV per cm ([physics reference](physics-reference.md), `VERIFY`), so in Part 1 at atmosphere the source has to sit within millimetres of the diode, or the check runs in Part 2 vacuum.
- Count rate: a bare 37 kBq source 10 mm from a 25 mm² diode (5 mm square active area, `VERIFY` with VTH2110.json) sees a solid-angle fraction of about $A / (4\pi d^2) = 25 / (4\pi \cdot 100) = 2$ %, so roughly 700 alphas/s, above R-14's 100 events/s. Use distance, a pinhole cap or a single channel. At 30 mm it is about 80/s.

## Sources

- NNDC NuDat 3 decay radiation search (ENSDF), nuclides 222Rn, 218Po, 214Po, 210Po, 241Am, retrieved 2026-11-21; references in the table.
- US NRC, "Smoke Detectors" backgrounder, nrc.gov/reading-rm/doc-collections/fact-sheets/smoke-detectors.html; Kidde 0976CA manual (manualslib), retrieved 2026-11-21.
- `sim/analytic/enc_budget.out.txt` for the electronics' width.
