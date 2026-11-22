# Candidates: ambient and purge-line environment sensors

**Need:** the user's answer to Q-02 (2026-11-21): ambient temperature and RH on the board, in room air, plus whatever else helps track the measurement; and, if one exists with a tube interface, an RH/T sensor the inlet or outlet air passes through during purges (R-27, R-34). Nothing inside the chamber (D-06 stands for the chamber volume).

**Pick:** working. On the MCU board: a Sensirion SHT45 (T, RH) and a Bosch BME280 or similar barometer (pressure, for room radon and for R-43). On the purge line: an SHT45-AD1F (filter-membrane variant) in a small machined PTFE or stainless flow cell on the outlet, at the pump side of the outlet valve. Prices, stock and the flow cell's design are open (pass 2).

**Relied on by:** R-17, R-27, R-34, R-76, A-30.

## Candidates

| Part | Measures | Accuracy (headline) | Interface | Tube interface | Lets the design | Costs the design | Source |
|---|---|---|---|---|---|---|---|
| **Sensirion SHT45** | T, RH | ±1.0 %RH, ±0.1 °C | I²C, 1.08–3.6 V, DFN | None: on-board | The best RH and T in a small part; on the MCU board in room air | Keep it away from the board's warm parts | [SHT45 product page](https://sensirion.com/products/catalog/SHT45), [datasheet](https://cdn.sparkfun.com/assets/9/7/7/a/d/SHT45-AD1B-R2_datasheet.pdf) |
| **Sensirion SHT45-AD1F** | T, RH | as SHT45 | I²C, DFN with a PTFE filter membrane | Needs a flow cell (machined) | The same sensor on the purge line; the membrane keeps dust off | A small machined cell, and a 4-wire lead | [SHT45-AD1F](https://sensirion.com/products/catalog/SHT45-AD1F) |
| Bosch BME280 | T, RH, pressure | ±3 %RH (20–80 %RH, 25 °C), ±1.0 hPa absolute | I²C/SPI, LGA | None | Pressure, which room radon follows; the chamber's ambient-pressure check (R-43) | RH three times worse than the SHT45: use it for pressure only | [BME280 datasheet](https://cdn.sparkfun.com/assets/5/3/0/f/7/BME280_Datasheet.pdf) |
| Atlas Scientific Gas Flow Cap | housing only | n/a | 3/16 in tubing ports | Yes, for Atlas's own gas and humidity sensor boards | Off-the-shelf flow-through housing, USD 19.99 | "Not designed to work under pressure"; materials not stated (R-30); sensor fit `VERIFY` | [Atlas Scientific](https://atlas-scientific.com/connectors/gas-flow-cap/) |
| Panametrics HygroTrace, Vaisala DRYCAP | dew point | process grade | Analyzer | Flow-through cell with VCR or compression fittings | Trace moisture | Far above this budget | [Instrumart](https://instrumart.com/products/22884/panametrics-hygrotrace) |

## Notes

- **Where the flow cell goes:** on the outlet, between the outlet valve and the pump (the pump is downstream, D-01), so the cell sees chamber air at about ambient pressure and adds nothing upstream of the chamber (R-30). Body PTFE or stainless, the sensor's seal not rubber or silicone (R-30 applies upstream only, but the outlet cell is cheap to make clean).
- **Use:** during the N₂ purge it shows when the chamber is dry (R-34), replacing the manual sensor; in flow-through runs it logs the sample's RH after the desiccant.
- **Why on-board T matters:** diode dark current rises with temperature (roughly doubling every 8–10 °C for silicon, `VERIFY` for the VTH2110), and the VTH2110 is rated to 60 % RH (VTH2110.json p2).
- **What this changes:** R-17 (the MCU board reads no chamber sensors) stays for the chamber volume; ambient and purge-line sensors are now in scope (R-76). D-06's "no compensation" stands: the readings are logged, not applied.
