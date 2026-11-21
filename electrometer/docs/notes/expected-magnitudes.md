# Expected magnitudes at the input node

**Conclusion:** Parasitic currents span fA to nA depending on cleaning and humidity, so they are measured, not computed. With PD bias on, dark-current drift (about 13 pA per kelvin at 150 pA) masks fA parasitics, so fA runs use PD bias at 0 V. The ion current from radon is about 0.2 fA: negligible.

**Relied on by:** R-01 (10 fA target), R-04 (resistance), R-06 (charge steps), R-14 (triboelectric pickup), R-16 (darkness), R-17 (temperature logging), U-5.

## Working

All inputs marked `VERIFY` are textbook or recalled values.

### Reference levels

- Photodiode dark current: 0.15 nA typical, 2 nA max at 20 V. 5 nA max at 40 V (VTH2110.json p1, p3).
- CSA op-amp bias: OPA140 0.5 pA typical, LMP7721 3 fA, ADA4530-1 20 fA max (ADA4530-1.json p1).
- Charge scale: a 6 MeV alpha gives about 270 fC, so **1 fC ≈ 22 keV**. Radon R-09 (energy resolution) is 100 keV FWHM.

### Parasitic paths

| Effect | Estimate | Consequence |
|---|---|---|
| Dark-current drift with PD bias on | Roughly doubles every ~8 °C (`VERIFY`), about 9 %/K: at 150 pA, **13 pA per kelvin**. Resolving 10 fA on top needs about 1 mK stability | fA runs at PD bias 0 V (the diode is then a capacitance and a shunt resistance), then ring bias and HV one at a time. With bias on, read differences (HV on vs off) at pA level, temperature logged |
| Surface leakage, 20 V across 0.25 mm × 20 mm | R = ρs × 0.25/20. ρs = 10¹⁵ down to 10¹² Ω/□ (`VERIFY`, clean vs humid FR-4): R = 1.25×10¹³ to 1.25×10¹⁰ Ω, **1.6 pA to 1.6 nA** | Depends on cleaning and RH: measured |
| Surface leakage, 1 kV across 2 mm × 70 mm (O-ring land, 22 mm bore) | 0.029 □: **35 pA (10¹⁵ Ω/□) to 35 nA (10¹² Ω/□)** | Most should land on a guard or ground. The residual into the input matters (U-1, U-5) |
| HV ripple through C(tube → input) | Q = C × ΔV. 50 fF × 0.1 V = 5 fC ≈ **110 keV**, above the resolution target | The ripple limit (radon R-19) needs this capacitance. Populated boards: bench gear. Bare boards: R-03 |
| Ring-bias noise through C(ring → input) | For 10 keV, C × V_noise ≤ 0.45 fC, e.g. ≤ 1 mV in the shaper band if C = 0.45 pF | Measure C(ring → input) |
| Ionisation of the chamber gas | 100 Bq/m³ in 26 cm³: 2.6 mBq × up to 3 alphas × 1.6×10⁵ pairs (5.5 MeV / 34 eV per pair, `VERIFY`) × 1.6×10⁻¹⁹ C = **0.2 fA**. Mine air (×100): 20 fA. Gamma and cosmic, ~10 pairs/cm³/s (`VERIFY`): 0.04 fA | Negligible. Exception: a 37 kBq Am-241 check source in the gas (half the alphas into the gas) gives about 0.5 nA of ion current |
| Stray light on a bare diode | 0.74 A/W peak (VTH2110.json p3): **1 fW gives 0.7 fA**, 1 nW gives 0.7 nA | Light-tight tin, no LEDs inside. FR-4 passes some light |
| Dielectric absorption after a step | Soak currents over seconds to hours, possibly orders above steady leakage (`VERIFY` for FR-4) | Time-stamped I(t), alternating polarity |
| Cable motion (triboelectric) | pA for ordinary coax, tens of fA for low-noise cable (`VERIFY`) | Probe cable fixed in the tin. Pump-on is itself a measurement |
| Micro-discharges at 1 kV | Charge bursts from fC up, look like events to the CSA | Optional step detection (R-06) |

- The ion current as a radon measurement is far below alpha counting, so it is out of scope.

## Sources

- `datasheets/VTH2110.json` p1, p3, `ADA4530-1.json` p1 (parent repo).
