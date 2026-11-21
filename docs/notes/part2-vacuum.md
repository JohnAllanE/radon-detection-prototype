# Part 2: vacuum chamber, pump and oil

**Conclusion:** The Edwards E2M8 reaches far lower pressure than Part 2 needs, so the risks are oil backstreaming onto the samples and pump vibration, not pressure. Pump only to a few ×10⁻² to 10⁻¹ mbar, trap the foreline, and count with the chamber sealed and the pump off.

**Relied on by:** R-03 (rough vacuum), R-46 (Part 2 chamber), R-57 (no pump oil on samples), R-58 (sealed counting), R-59 (vacuum gauge), Q-21 (gasket), Q-22 (samples).

## Working

### Chamber and samples (D-10, D-19)

- Custom aluminium chamber with gaskets, a cylinder of 50 mm ID.
- Weld coupons about 15 mm wide × 30 mm tall, 5–10 mm from the detectors.
- N₂ purge first to remove free radon, then pump down. No HV in Part 2.
- The detector board is O-ring sealed with its back at atmosphere, as in Part 1.

### Pump (D-24)

- Two-stage oil-sealed rotary vane, NW25 inlet. Ultimate 1×10⁻³ mbar without gas ballast. Full figures in D-24.
- About 1–10 mbar is enough for the 5–10 mm gap ([physics reference](physics-reference.md)), so the margin is wide.
- Use gas ballast only on the first pump-down from humid air or the N₂ purge.

### Keeping oil off the samples (R-57)

- Pump only to a few ×10⁻² to 10⁻¹ mbar, not to ultimate: oil vapour backstreams in molecular flow.
- A foreline trap (activated alumina or molecular sieve) between chamber and pump. Trap type and part open.
- Close the chamber valve before the pump is stopped.
- Vent with dry N₂ through the chamber inlet, never back through the pump line.
- The PTFE membrane filter (D-25) stops oil mist and particles but not oil vapour. It also lowers conductance in molecular flow, which costs pump-down time but not usable pressure.

### Sealed counting (R-58)

- Counting with the chamber sealed and the pump off removes pump vibration, motor EMI (R-41) and backstreaming.
- The allowed run length is set by the leak-up rate measured on the built chamber, up to about 1–10 mbar (R-03). The gauge (R-59, Pirani or similar on an NW25 tee) measures it.

### Gasket (Q-21, answered: Viton)

- Viton (FKM) is fine for a prototype.
- For low-background work the concerns are radon emanation and permeation, and U/Th in fillers. Indium wire, PTFE or FEP-encapsulated O-rings are the usual lower-background choices, and screening a lot is the proper check (`VERIFY`). The user asked for lower-background materials to be considered in later revisions.

## Sources

- Edwards E2M2–E2M12 instruction manual, Table 3 (decisions D-24).
- Decisions D-10, D-19, D-24, D-25.
