# Radon detection prototype: part selection

| | |
|---|---|
| Project | Alpha detection with silicon photodiodes: radon progeny in air (Part 1) and weld samples in rough vacuum (Part 2), comparing a premium and a low-cost detector board |
| This document | The candidate part for each function on the detector, MCU and HV boards, with its status. No schematic exists yet |
| State | Draft |
| Open questions | 9 |

## Sourcing

| | |
|---|---|
| Suppliers | Not chosen (Q-15) |
| Stock and prices | `$ELECTRONICS_TOOLS/inventory/stock.csv` and supplier pages. Not checked yet: pass 2 work |
| Datasheet values | `datasheets/<MPN>.json` in this repo, with page numbers, until they move to `component-data/` |
| Original makers | VTH2110 from Excelitas only. The user's price remarks (LMP7721 $8.40 each, premium parts about $12, general op-amps about $4) are unchecked |

## Parts

Quantities assume 4 detector boards (2 low-cost, 2 premium) and count per MCU board where the MCU-board count is open (architecture question 9).

### Detector board

| Function | Part | Status | Qty | Stock | Why | Alternate |
|---|---|---|---|---|---|---|
| Photodiode | Excelitas VTH2110, bare chip, 5.67 mm, 5 mm active | firm | 16 | buy | A-02. The user's part. [Survey](../docs/notes/candidates-photodiode.md) | None (VTH2120 is a size variant). Lead time unknown |
| CSA op-amp, low-cost | TI OPA140, SOIC-8 | working | 8 | buy | A-06. 5.1 nV/√Hz, 0.5 pA, NC pins 1, 5, 8. [Survey](../docs/notes/candidates-csa-opamp.md) | OPA656, OPA657, TL071-class (not pulled) |
| CSA op-amp, premium | TI LMP7721, SOIC-8, own footprint | working | 8 | buy | A-07. 3 fA, guard on NC pins (LMP7721.json p3). Awaits the user (D-18) | ADA4817-1, ADA4530-1 or OPA656, only with a footprint change |
| Test port | Murata SWF switched coaxial receptacle | working | 16 | buy | A-09, R-60. Part number open | — |
| $C_f$, $R_f$, $C_{test}$ | 1 pF C0G, 100 MΩ, 1 pF C0G | open | 16 each | open | A-05, A-08. Not pulled | — |
| Connector | Molex PicoBlade-style, 14 pins proposed | working | 4 | open | A-12. Maximum circuit count to check | — |
| Noise reference (optional) | Cremat CR-110-R2.1 module | open | 1 | buy | Bench reference only. [JFET and module noise](../docs/notes/jfet-and-module-noise.md) | Amptek A250 family, BF862 JFET channel |

### MCU board

| Function | Part | Status | Qty | Stock | Why | Alternate |
|---|---|---|---|---|---|---|
| Shaper, peak-detect, hold buffer op-amps | TI TLV9062 dual, TLV9064 quad | working | open | open | A-13, A-16. 10 MHz, 0.5 pA. [TLV90xx](../docs/notes/tlv90xx-assessment.md) | TLV9002, TLV9004 for the shaper only |
| Comparator | TI TLV9061 with hysteresis | working | 4 | open | A-15. User preference | TLV3201 (40 ns), pinout `VERIFY` |
| Hold diode | BAS116 | open | 4 | open | A-16. Not pulled. Leakage ≪ 80 pA `VERIFY` | Other low-leakage diodes |
| Hold capacitor | 1 nF C0G or film | open | 4 | open | A-16. Droop and dielectric absorption `VERIFY` | 220 pF |
| Reset switch | TI TMUX1101 | working | 4 | open | A-16. 3 pA, −1.5 pC. [Survey](../docs/notes/candidates-mux-hold.md) | TMUX1102, TMUX1103 (polarity `VERIFY`) |
| Channel mux | TI TMUX1104, 4:1 | working | 1 | open | A-17. 3 pA, 1.5 pC, positive signals only | — |
| ADC, high resolution | TI ADS1220 | firm | 1 | on hand | A-17, D-16. [Survey](../docs/notes/candidates-adc.md) | — |
| ADC, fast | TI ADS8689 | firm | 1 | buy | A-17, D-16. 100 kSPS, needs buffered holds | ADS8685, ADS8681, ESP32-S3 ADC |
| MCU | Espressif ESP32-S3-WROOM-1, PCB antenna | firm | 1 | buy | A-18, D-08. Flash and PSRAM variant open. [Survey](../docs/notes/candidates-mcu.md) | WROOM-1U |
| ±4.5 V rails | TI LM27762 | working | 1 | open | A-19. Noise and PSRR `VERIFY` before use on a CSA rail | Discrete charge pump and LDOs |
| 3.3 V LDO | not chosen | open | 1 | open | A-19 | — |
| ESD and USB protection | not chosen | open | 1 | open | A-18 | — |
| 5 V wall adapter | Mean Well, model open | firm | 1 | open | R-25, D-08 | — |

### HV board

| Function | Part | Status | Qty | Stock | Why | Alternate |
|---|---|---|---|---|---|---|
| 48 V wall adapter | Mean Well, model open | firm | 1 | open | R-25, D-08 | — |
| Transformer, multiplier, PWM controller | not chosen | open | 1 | open | A-20. [Survey](../docs/notes/candidates-hv-generation.md) | Commercial HV module |

## Open

1. Prices, stock and suppliers for every part: pass 2 (Q-15).
2. VTH2110 lead time, and no alternate.
3. LMP7721 against ADA4817-1 for the premium board (D-18, architecture question 7).
4. ADS1220 single-ended limits at gain 1, and conversion latency.
5. BAS116 and $C_{hold}$ leakage against the 80 pA budget.
6. TMUX1101 family member for the reset polarity. TLV9061 and TLV3201 SOT-23-5 pinouts.
7. LM27762 output noise and PSRR.
8. PicoBlade maximum circuit count, and the SWF part number.
9. Datasheet JSONs to migrate to `$ELECTRONICS_TOOLS/component-data/` (run log).
