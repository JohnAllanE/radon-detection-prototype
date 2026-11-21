# Candidates: MCU

**Need:** native USB to the host, an ESP-NOW option, two SPI chip selects, four comparator interrupts, mux-select and reset lines, pulse counters and a timer (R-13, R-15).

**Pick:** Espressif ESP32-S3-WROOM-1 with its PCB antenna, firm (D-08). Flash and PSRAM variant open, chosen from the ordering table.

**Relied on by:** A-18 (MCU), A-26 (event firmware), R-15 (reports to the host), R-14 (event rate).

## Candidates

Only two: the user chose the ESP32-S3. Prices and stock open (pass 2).

| Part | Maker | Price (CAD) | Stock or supplier | Package vs assembly | SPICE model | Lets the design | Costs the design |
|---|---|---|---|---|---|---|---|
| **ESP32-S3-WROOM-1** | Espressif | open | open | Castellated module | — | PCB antenna, USB native, ESP-NOW | Needs a board edge clear of copper, analog kept away from it |
| ESP32-S3-WROOM-1U | Espressif | open | open (the electrometer's stocked -1U-N16R8 is earmarked) | Module with antenna connector | — | External antenna | A cable and a panel hole |

## What the pick sets

| Quantity | Value | From |
|---|---|---|
| Supply | 3.0–3.6 V, from a 3.3 V LDO (not chosen) | ESP32-S3-WROOM-1.json p2 |
| Strapping pins to avoid for interrupts | 4 | p1 |
| Peripherals used | 2 SPI chip selects (ADS1220, ADS8689), 4 interrupts, 2 mux selects, 4 resets, pulse counters, a timer | Architecture A-18 |
| Internal ADC | Optional fast path, performance `VERIFY` | Not extracted |

- ESP-NOW transmit bursts are a likely noise source on the supply, so firmware may hold off a conversion during a burst.
- Layout: the analog section away from the antenna and the digital area, one solid ground pour per layer, no digital traces under the shaper.

## Sources

- `datasheets/ESP32-S3-WROOM-1.json` p1, p2. component-data has `ESP32-S3-WROOM-1U-N16R8` but not the -1 module.
