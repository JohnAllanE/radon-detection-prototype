# Candidates: ADC

**Need:** digitise four held peaks, one at a time, finer than the detector resolution (tens of keV) and fast enough for 100 events/s total (R-14, R-16).

**Pick:** both, firm (D-16, the user): TI ADS1220 (in stock) straight from the four holds, and TI ADS8689 behind a 4:1 mux. A jumper also routes the mux output to the ESP32-S3's own ADC.

**Relied on by:** A-17 (ADCs), A-16 (hold buffer drives the ADS8689 input), R-13 (per-channel conversion), R-14 (event rate), R-16 (ADC on merit).

## Candidates

Prices open (pass 2). The user has ADS1220 in stock (count not recorded in this project).

| Part | Maker | Price (CAD) | Stock or supplier | Package vs assembly | SPICE model | Lets the design | Costs the design |
|---|---|---|---|---|---|---|---|
| **ADS1220** | TI | open | In stock (user) | TSSOP-16 (`VERIFY`) | open | 24-bit, up to 2 kSPS, 4 single-ended inputs (AIN0–3), input mux, sub-eV per code | Slow: about 0.5 ms per conversion at 2 kSPS (latency `VERIFY`). Single-ended limits at gain 1 `VERIFY` |
| **ADS8689** | TI | open | open | open | open | 16-bit, 100 kSPS, 0–5.12 V: 0.52 keV per code at 150 mV/MeV, dead time tens of µs | Single channel: external mux. Resistive ≥ 1 MΩ input discharges a hold in ms, so each hold needs a buffer |
| ADS8685 | TI | open | open | Same family | open | 500 kSPS | Not needed at these rates |
| ADS8681 | TI | open | open | Same family | open | 1 MSPS | Not needed |
| ADS8688 | TI | open | open | open | open | 16-bit SAR with built-in 8-channel mux (as recalled, `VERIFY`) | Not pulled. Would remove the external mux |
| ESP32-S3 ADC | Espressif | in the MCU | — | — | — | High-rate, low-resolution test path | Performance not extracted (`VERIFY`) |

Prices: none checked.

- The user named "ADS8689" as the SAR alternative. It is single-channel, which is why the design adds a mux (D-16). The 8-channel ADS8688 may have been meant (`VERIFY` with the user).
- Why a fast path is mostly unnecessary: radon gives about 1 count/hour, and even a 2 ms conversion allows about 500/s. A fast path matters only for calibration with a strong source.

## What the pick sets

| Quantity | Value | From |
|---|---|---|
| ADS8689 LSB at 150 mV/MeV | 78 µV, 0.52 keV | [Signal levels](signal-levels.md) |
| Full scale used at 8.78 MeV | 26 % of ADS8689, inside ADS1220's 2.048 V | Same |
| Event dead time | tens of µs (ADS8689), about 0.5 ms (ADS1220) | ADS8689.json p1, ADS1220 data rate |
| Supply | ADS8689 AVDD from the +5 V analog rail | ADS8689.json p1 |

## Sources

- `datasheets/ADS1220.json`, `ADS8689.json` p1. Both already exist in `$ELECTRONICS_TOOLS/component-data/`.
