# Proposed targets (working)

**Conclusion:** Claude's proposed numbers for each requirement, carried from requirements draft 3. They are working: the user confirmed the requirements' intent, and decides which numbers become firm and whether each is a limit or an objective. The architecture's derived specs design to them.

**Relied on by:** the R-xx named in each row, and the architecture's Derived specs.

## Working

| ID | Proposed target |
|---|---|
| R-01 | Noise ≤ 10 fA p-p over 60 s at 1 s per reading on the lowest range. Accuracy ±2 % of reading above 1 pA after zeroing |
| R-02 | 1 fC resolution over a 1 s window. A charge above about 100 pC at once is an overload, timestamped |
| R-03 | 1 fF to 100 pF at a 1 V step (charge ≤ 100 pC, larger C needs a proportionally smaller step), resolution 1 fF, accuracy ±(1 % + 2 fF). Steps of about ±1 V: 33 pF × 1 V = 33 pC fits the 10 pF integrator |
| R-04 | Up to 10¹⁵ Ω at 50 V (50 fA), ±10 % |
| R-06 | Steps ≥ 50 fC (≈ 1.1 MeV equivalent), 1 ms timing |
| R-08 | 10 mV steps, current limit ≤ 100 µA, noise ≤ 10 µV rms in 0.1–10 Hz (100 pF × 10 µV at 1 Hz moves only 6 fA), controlled slew so a step doesn't overload the input |
| R-10 | Zero and noise floor re-checked after a deliberate test. `VERIFY` the energy available from the HV board's output capacitance |
| R-13 | Settled when the 60 s slope is below the R-01 noise floor. Longer settling is a DUT soak effect, logged, not hidden |
| R-15 | Tube to tin clearance ≥ 10 mm (`VERIFY` against the rule chosen for radon Q-12). Tube on insulating standoffs. Board back reachable with the probe while assembled |
| R-16 | Stray light ≤ 1 fW on a diode (≤ 1 fA). Check: diode at 20 V, tin closed, room lights on vs off |
| R-17 | ±0.5 °C accuracy, 0.01 °C resolution, ±3 % RH |
| R-20 | Command names follow the Keithley 6514/6517B where they overlap, as the load-cell reader follows the SDM3055 |
| R-22 | 1–10 readings/s with integration over whole mains cycles; up to 1 kS/s in charge-step mode (R-06) |
| R-23 | Transmissions scheduled between integration windows if needed |
| R-24 | ≥ 24 h of logging (R-05). Two 18650 cells in parallel give about 25 h with the source on (D-08) |
| R-26 | Ramp example: 1 V/s into 10 pF gives 10 pA. The reference capacitor's tolerance is the accuracy limit (`VERIFY`). Procedure in the test plan |
| R-27 | ≤ 60 V DC (`VERIFY` the limit against IEC 61010-1) |
| R-29 | 2 or 4 layers. ADA4530-1 as the premium op-amp candidate |
| R-33 | S coax ≤ 30 cm (`VERIFY` against the capacitance budget). Script prompt and confirmation logged with each run |

## Sources

- Requirements draft 3 section 4, in git history before the contract rewrite.
