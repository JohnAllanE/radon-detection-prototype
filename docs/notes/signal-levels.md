# Signal levels, gain and the hold-node budget

**Conclusion:** With $C_f$ = 1 pF and a shaper gain of about 3.4, the chain gives a nominal 150 mV/MeV: 8.78 MeV is about 1.3 V above a 0.2–0.3 V baseline on a single +5 V rail. ADC bits are not the limit, the hold node's leakage is: about 80 pA total for 0.03 % droop.

**Relied on by:** A-05 (CSA), A-13 and A-14 (MCU board chain and shaper), A-16 (peak hold), A-17 (ADCs), R-09 (energy resolution), R-13 (per-channel hold), R-14 (event rate).

## Working

### Gain

- Charge: 44.3 fC per MeV ([physics reference](physics-reference.md)).
- CSA with $C_f$ = 1 pF: 44.3 mV per MeV, 389 mV at 8.78 MeV.
- Board stray across a 1 pF part is about 0.1–0.3 pF (`VERIFY` by measurement), so the real gain differs from nominal by tens of percent. Calibration with the test-charge input (R-49) is mandatory.
- System gain 150 mV/MeV nominal (shaper gain about 3.4, trimmed in simulation since a CR-RC^n shaper peaks below its gain). 8.78 MeV gives about 1.3 V. That fits the ADS1220's 2.048 V range at gain 1 and uses 26 % of the ADS8689's 0–5.12 V range.
- A 1 MHz GBW part limits each stage to a gain of about 5 or less at 100–200 kHz.

### Baseline and offsets

- The shaper output rests at about 0.2–0.3 V so noise and undershoot don't clip at the rail (TLV9001 swings within 10–20 mV of the rail at 10 kΩ, TLV9001.json p17).
- The hold captures baseline plus signal. Firmware subtracts a stored per-channel baseline.
- TLV9001 offset ±0.4 mV typical, ±1.6 mV maximum (p17): 2.7–11 keV at 150 mV/MeV, so offsets are calibrated. The architecture's risk list quotes ±0.3 to ±1.6 mV (2–11 keV) for the TLV90xx family.
- CSA output offset from dark current: $I_{dark} R_f$ = 0.15–2 nA × 100 MΩ = 15–200 mV (VTH2110.json p1, p3). The pole-zero stage AC-couples it away. With $R_f$ = 1 GΩ it would be up to 2 V.
- $R_f C_f$ decay 100 µs. Against a 4 µs shaper, an uncancelled decay undershoots by about 4 %, so the pole-zero network cancels it.

### ADC resolution

- ADS8689 on 0–5.12 V: LSB = 5.12 V / 65536 = 78 µV = 0.52 keV per code at 150 mV/MeV.
- ADS1220 at gain 1, 2.048 V reference, single-ended (half the code range, still about 23 bits): sub-eV per code (`VERIFY` single-ended input limits).
- In general: 16 bits over 0–9 MeV is about 0.14 keV per code, and even 12 bits is about 2 keV. The detector and preamp resolution will be tens of keV, so noise, droop and charge injection in the hold set the limit, not ADC bits.
- Single-ended inputs are adequate: the held peaks are ground-referenced unipolar pulses. Common-mode noise is handled first by layout and shielding.

### Peak-hold droop budget

$$I_{leak} \le \frac{0.4\ \text{mV} \times 1\ \text{nF}}{5\ \text{ms}} = 80\ \text{pA}$$

- 0.03 % of about 1.3 V full scale is 0.4 mV, over a 5 ms worst-case hold, with $C_{hold}$ = 1 nF.
- Contributors: TMUX1101 leakage 3 pA (TMUX1101.json p1), TLV9001 bias ±5 pA typical (max not extracted, TLV9001.json p17), the diode `VERIFY`.
- A 220 pF $C_{hold}$ would tighten the budget to about 15 pA.
- Reset charge injection about −1.5 pC into 1 nF is about 1.5 mV after reset: constant, absorbed in the baseline calibration.

### Event sequence and dead time (R-13, R-14)

1. Comparator fires. The ESP32 notes the channel and time.
2. Wait about the peaking time. The hold keeps the value, so timing jitter doesn't matter.
3. Select that channel on the mux, convert, read the code.
4. Pulse that channel's reset only. Other channels keep their holds.

- A second trigger on the same channel before reset is counted (pulse counter) and flags pile-up.
- ADS8689 keeps dead time to tens of µs. ADS1220 is slower, about one conversion period (0.5 ms at 2 kSPS, latency `VERIFY`): the high-resolution, low-rate path.

## Sources

- `datasheets/*.json` (TLV9001 p17, TMUX1101 p1, VTH2110 p1 and p3, ADS8689 p1), to migrate to component-data.
- `sim/analytic/enc_budget.out.txt` for the gain and decay figures.
