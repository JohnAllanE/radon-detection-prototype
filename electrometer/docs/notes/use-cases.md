# Use cases and the measurement procedure

**Conclusion:** The primary use is U-5: a built Part 1 chamber at +1 kV with its detector boards and the electrometer, all in a grounded tin, one probe cable moved by hand between the boards' switch connectors (D-02). The bench version with a sacrificial board finds causes.

**Relied on by:** R-01 (DC current), R-11 (one probe cable), R-12 (no floating node), R-13 (settling), R-15 (the tin), R-19 (switch connectors on the detector board), R-21 (records).

## Working

### What feeds current into a CSA input node

| Source | Level | Path into the input node |
|---|---|---|
| Photodiode reverse bias | 20 V default, 40 V option (VTH2110.json p1) | Dark current (the wanted baseline), and surface leakage from the bias net |
| Ring bias on the exposed ENIG (radon R-47, the ion-steering ring) | Slightly positive, value from the field simulation | Surface leakage across the top face, capacitive coupling of ring noise |
| Chamber wall | About +1 kV, ~2.1–2.6 mm from the die corners (radon R-39) | Surface and bulk leakage from the O-ring land, coupled HV ripple (radon R-19), micro-discharges |
| Radon-progeny ions steered onto the diodes | Function of the field | Ionisation current in the gas: tiny ([expected magnitudes](expected-magnitudes.md)) |

"Working" means: for each path, the electrometer says how much DC current reaches the input node, finely enough to show it is small against the dark current, or that it isn't. Capacitive coupling of noise is measured mostly with the bench gear ([bench gear](bench-gear-coverage.md)).

### Use cases

| ID | Use case | DUT state | Main measurements |
|---|---|---|---|
| U-5 | **Primary validation, in the tin.** Board on a built Part 1 chamber, walls at +1 kV from the real HV board, ring bias on, air vs N₂, pump on vs off (radon R-41). PD bias 0 V for fA runs, on for the in-service picture | Populated, mounted, probe on one channel's switch connector | DC current vs condition, charge steps from micro-discharges |
| U-1 | **Bare-board leakage map** on a test board with the same footprints. Input node against guard, ring, PD bias, TEST, ground at 10–50 V. O-ring land at 1 kV, on the chamber or with a metal ring pressed on it | Bare, cleaned, sacrificial (wires may be soldered) | I(t) after a step, R by alternating polarity |
| U-2 | *Optional (D-01).* **Bare-board capacitance matrix**: input node against every other node, especially $C_f$ stray, ring → input, O-ring land → input | Bare test board | Guarded cross-capacitance, fF |
| U-3 | **Populated board before service.** Input leakage per channel with CSA, $C_f$, $R_f$, $C_{test}$ fitted. *Optional:* each $C_{test}$ measured, so charge-injection calibration (radon R-49) doesn't rely on a 1 pF ±0.25 pF tolerance. One or two mating cycles per connector | Populated, cleaned, in the tin | Leakage, optionally capacitance |
| U-4 | **Photodiode dark current** vs bias (0–40 V) and temperature, in the dark | Diodes fitted | I–V, I–T |
| U-6 | **Self-baseline.** Probe unmated and parked, tin closed, cables flexed, radio on vs off. Probe on an unpopulated footprint of the test board | No DUT | Noise floor, triboelectric pickup, offsets, connector leakage |

### Procedure, in outline

1. HV off and discharged (interlock), open the tin.
2. Move the probe to the next switch connector.
3. Close the tin, re-purge if the run needs dry gas.
4. The script waits for settling (R-13), then HV and biases on, then measure.
5. The script asks the operator which channel the probe is on and logs it (R-21).

## Sources

- Electrometer decisions D-01, D-02. `datasheets/VTH2110.json` in the parent repo.
