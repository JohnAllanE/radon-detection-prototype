# Data link, power input and sealing for a floating femtoamp instrument

**Conclusion:**

- **Data link:** wired USB-C, as the bench gear now is, through a USB isolator (ADuM3160 class) inside the electrometer. With the battery pack as its only supply, the electrometer then floats: no galvanic path from the host's mains earth to the head's common, and no change to the gateway HAT. An optical-fibre UART (TOSLINK class) is the alternative, but needs a port added to the gateway HAT. The radio (ESP-NOW, antenna on a bulkhead) stays an option for battery-only use.
- **Power:** a separate battery pack (the bench "power tool" strategy, `bench-test-gear/battery-pack/`), charged outside this project, arriving on the GX12-4 power input (`bench-test-gear/CONNECTORS.md`). The same socket takes a bench PSU, so battery and PSU noise can be compared; a PSU run floats only if that PSU's output is isolated from earth (`VERIFY` per PSU).
- **Sealing:** the user's idea of sealing the head with desiccant is right. At femtoamps the insulation's moisture film, not the amplifier, sets the floor. Seal the head's shield box (A-16) with desiccant and a humidity indicator card visible through a window or checked at the lid, plus the SHT4x (A-14) inside.

**Relied on by:** R-17, R-20, R-24, R-29, R-31, A-10, A-12, A-13, A-14, A-16, the user's answers 2–4 of 2026-11-21.

## Working

### Why isolate the data link

- A femtoamp input measures against its own common (R-31). Any second galvanic path from that common to earth, here the USB cable's shield and ground to the PC, forms a loop: mains-frequency currents and ground offsets drive current through the input's surroundings ([questions](../questions/2026-11-21-electrometer.md), question 4).
- **ADuM3160:** Analog Devices' full- and low-speed USB isolator, 12 and 1.5 Mbps, 2.5 kV rms, transparent to USB traffic so the peripheral needs no change; 4.5–5.5 V VBUS on the host side ([ADuM3160 product page and datasheet](https://www.analog.com/en/products/adum3160.html)). The ESP32-S3's USB is 2.0 full speed (ESP32-S3-WROOM-1.json), inside the isolator's rate.
- The host side of the isolator takes its power from the host's VBUS; the electrometer side from the electrometer's own 3.3 V or 5 V (`VERIFY` the side supplies in the datasheet). No host power crosses.
- What remains: the barrier's few-pF coupling capacitance (`VERIFY`) passes some AC. Unplug for the lowest-floor runs, as A-13 already schedules the radio between integration windows.
- **Optical fibre UART:** no capacitance across the link at all, a plastic fibre and two transceivers. Cost: a fibre port on the gateway HAT and a UART protocol in place of USB. Keep it in reserve if the isolated USB shows in the floor.

### Power input

- GX12-4 is the universal power socket: pin 1 +V, pin 2 0 V, pin 3 −V for a split supply, pin 4 free (`CONNECTORS.md`, power in). A battery pack and a PSU use the same cable.
- The pack is the floating source. A bench PSU shares its common with the PSU's chassis if its outputs are referenced to earth: check before a femtoamp comparison run.
- This replaces A-10's internal cells and charger. R-24 (battery life) becomes the pack's, measured with it.

### Sealing and humidity

- ADA4530-1 datasheet, Humidity Effects (ADA4530-1.pdf p35–36): below about 70 °C the insulation resistance of the construction causes larger leakage than the amplifier; relative humidity is the most important error source. Adsorbed water films conduct and act in parallel with the insulation (guarding helps); absorbed water raises bulk conductivity (guarding does not). Its example: 100 TΩ to +5 V and 250 TΩ to −5 V give −30 fA.
- Keithley's Low Level Measurements Handbook gives the same advice: clean, dry insulators, low humidity ([7th edition](https://xdevs.com/doc/Keithley/LowLevelHandbook_7Ed.pdf), `VERIFY` the section).
- So: the head box closed with a gasket, a desiccant sachet inside, a humidity indicator card, and the SHT4x logging the inside RH (R-17). Change the desiccant when the card turns.
- A sealed box needs a sealed connector: an IP-rated USB-C receptacle if the USB-C port is on the sealed box (the user's answer 4). The probe and range-panel SMAs need sealing too (`VERIFY`).
