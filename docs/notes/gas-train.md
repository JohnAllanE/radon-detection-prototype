# Part 1 gas train: drying, filters and humidity

**Conclusion:** At 1 L/min of 50 % RH air the desiccant takes up about 12.5 g of water a day, about 125 g of desiccant a day at 10 % uptake, so continuous air runs need a large column or frequent changes. Neither this nor flow is a design driver (D-13): both are characterised after the build.

**Relied on by:** R-29 (gas train order), R-30 (materials), R-32 and R-33 (characterised after build), R-34 (humidity at the outlet), R-37 (filters), Q-17 (desiccant and filter sourcing).

## Working

### Water load on the desiccant

- Saturated vapour density of air at 20 °C is about 17.3 g/m³, so 50 % RH holds about 8.65 g/m³.
- At 1 L/min (0.06 m³/h) that is 0.52 g/h, about 12.5 g per day.
- If the desiccant takes up about 10 % of its weight (`VERIFY` for the chosen product), that is about 125 g of desiccant per day of continuous running. The N₂ control is already dry.

### Why dry the sample

- Commercial radon monitors dry the sample and ask for low humidity at the detector, because water vapour reduces the fraction of Po-218 that stays charged.
- The Durridge RAD7 uses calcium sulfate desiccant (Drierite) at roughly 1 L/min (`VERIFY` from its manual).
- Preferred desiccant here: Drierite, indicating calcium sulfate (D-13). Sourcing is open (Q-15, Q-17).

### Filters (D-25, working)

- One filter type at every gas port: Part 1 inlet, Part 1 final filter after the desiccant, Part 1 chamber outlet, and the Part 2 chamber-to-pump line.
- Type: hydrophobic PTFE membrane, about 0.2 µm, vacuum-rated housing, membrane supported in both directions, SS or PFA/PTFE body, same end fittings everywhere. Details in D-25.

### Leaks and the pump

- The pump sits downstream (D-01), so the chamber runs slightly below ambient and any leak draws in unfiltered, undried room air (R-32).
- The outlet filter catches diaphragm-pump wear particles. It doesn't stop pump outgassing vapour, which the downstream position handles.

### No humidity sensor in the chamber (D-06)

- The chamber is a small volume (about 15 cm³ in the first estimate, 26–29 cm³ at the chosen bore), so a sensor body, its adsorbed water and any outgassing are large relative to it.
- It would sit next to a 1 kV wall, and its I²C lines would be a noise path into the preamps.
- Humidity is read at the outlet during the N₂ purge with a manual sensor (R-34), as the user suggested.

## Sources

- Decisions D-01, D-02, D-06, D-13, D-25.
- Durridge RAD7 manual, not yet consulted (`VERIFY`).
