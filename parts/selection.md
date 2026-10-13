# Part selection (candidates, DRAFT)

Created 2026-10-12 as a preview of phase 3, before the architecture gate. Nothing is committed to a schematic.

**Not done:** price and stock checks (none recorded, so none claimed); `parts/inventory.csv` does not exist (the user says the ADS1220 is in stock; path and format of the inventory are open, Q-15); suppliers not chosen. The user's own estimates: dedicated premium CSP chips about $12, general op-amps about $4 (unverified).

Datasheet column: **JSON** = PDF and `datasheets/<MPN>.json` exist; **no** = not pulled yet.

| Block | Candidate (default first) | Alternates | Datasheet | Why / notes |
|---|---|---|---|---|
| Photodiode | **VTH2110** (Excelitas, 5.67 mm chip, 5 mm active) | VTH2120 (10 mm, more capacitance) | JSON | Fixed by the user. Chip only: needs die attach and bond pad connection |
| CSA op-amp, low-cost | **OPA140** SOIC-8 | OPA656, OPA657 (SOIC-8, same footprint); TL071-class (not pulled) | JSON | 5.1 nV/√Hz, 11 MHz, 0.5 pA bias, standard pin 1/5/8 NC. Use shaping ≥ 4 µs |
| CSA op-amp, premium | **LMP7721** SOIC-8 (non-standard pinout, guard-friendly) | **ADA4817-1** (4 nV/√Hz, FB pin, 19 mA each, expensive per the user); **ADA4530-1** (20 fA, guard pins, 14 nV/√Hz, keep for the electrometer) | JSON for all three | LMP7721: $8.40 each per the user; 3 fA bias, 6.5 nV/√Hz, 17 MHz. Noise not better than OPA140, so its advantage is leakage and guarding, not peak width |
| CSA, noise reference (hypothetical) | BF862-class JFET + fast op-amp on a single test channel | 2SK152 and similar | no | A search snippet gives about 0.8 nV/√Hz and 10 pF: would reach roughly 2–3 keV; datasheet not pulled, `VERIFY` |
| CSA benchmark | CR-110-R2.1 (Cremat module) | Amptek A250 family (not pulled; app note page was HTML only) | JSON | ENC 200 e + 3.8 e/pF; bench reference only, not part of the boards |
| Shaper, peak-detect, hold-buffer op-amps | **TLV9062 / TLV9064** (TLV906x, 10 MHz) | TLV9002 / TLV9004 (1 MHz; shaper only) | JSON (TLV9061.json, TLV9001.json) | User's TLV900x standard. Single +5 V rail. 10 nV/√Hz, 0.5 pA bias, 100 Ω output impedance; TLV9001 is marginal for peak detect and hold (architecture §2.5) |
| Hold diode | **BAS116** | other low-leakage diodes | no | Leakage must be ≪ 80 pA at the hold node (budget in architecture §2.2): `VERIFY` |
| Hold capacitor | 1 nF C0G / film | | no | Droop and dielectric absorption: `VERIFY` |
| Reset switch | **TMUX1101** (SPST) | TMUX1102/1103 (other logic polarity) | JSON | 3 pA leakage, −1.5 pC charge injection, listed for sample-and-hold. Which family member suits the reset polarity: `VERIFY` |
| Channel mux | **TMUX1104** (4:1) | | JSON | 3 pA, 1.5 pC, signal range GND to VDD (positive peaks only) |
| Comparator | **TLV9061** used as a comparator (user preference) | TLV3201 (40 ns, faster, pinout to verify) | JSON | ~1 µs delay is harmless because the peak is held |
| ADC, high resolution | **ADS1220** (user stock) | | JSON | 4 SE channels, 2 kSPS, 24-bit; single-ended input limits at gain 1 to be checked |
| ADC, fast | **ADS8689** | ADS8685 (500 kSPS), ADS8681 (1 MSPS) same family | JSON | Single channel, 16-bit, 100 kSPS, ≥ 1 MΩ input, 0–5.12 V range |
| ADC, optional | ESP32-S3 internal ADC | | JSON (module datasheet, ADC specs not extracted) | Low-resolution path only |
| MCU | **ESP32-S3-WROOM-1** (PCB antenna) | WROOM-1U (external antenna) | JSON | USB native, ESP-NOW for the pivot; flash/PSRAM variant open |
| Analog rails | **LM27762** (±4.5 V from 5 V) | discrete charge pump + LDOs | JSON | Output noise and PSRR not extracted, `VERIFY` before use on a CSA rail |
| 3.3 V LDO | not chosen | | no | |
| Connectors | Molex PicoBlade (detector to MCU) | | no | Max circuit count to check; 14 pins proposed |
| ESD / USB protection | not chosen | | no | |

## Alternates required for critical or long-lead parts (workflow §5)
- VTH2110: no alternate chosen (VTH2120 is a size variant, not a drop-in). Lead time unknown.
- ADS8689 and ADS1220: other ADS868x variants or an ESP32 ADC cover the function.
- LMP7721: ADA4530-1 or OPA656 as a substitute for the premium footprint only if the footprint is changed.
