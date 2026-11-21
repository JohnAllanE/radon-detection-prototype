# Self-test without a switch at the summing node

**Conclusion:** A permanent 1 pF injection capacitor ($C_{inj}$) from a quiet DAC line replaces R-25's switchable reference capacitor and resistor. Held at 0 V it leaks nothing, a ramp injects a known current and a step a known charge. The resistor ranges are checked with an external cal plug on the probe. Awaiting the user (architecture draft question 3).

**Relied on by:** A-06 ($C_{inj}$), A-17 (power-up range check), R-25 (built-in checks), R-26 (calibration), R-33 (range readback).

## Working

### Currents from $C_{inj}$

$I = C_{inj} \, dV/dt$, with $C_{inj}$ = 1 pF:

| Ramp | Current |
|---|---|
| 0.01 V/s | 10 fA |
| 0.1 V/s | 100 fA |
| 1 V/s | 1 pA |
| 4 V/s | 4 pA |

- A static DAC offset gives no current, and an ideal capacitor has no thermal noise.
- Its DAC is an MCP4821 (in stock), RC-filtered, which also smooths the 1 mV staircase into a ramp.

### Why not a resistor fixed to the summing node

| Resistor left on the node | Thermal noise | From a source 10 mV off at "0 V" |
|---|---|---|
| 1 GΩ | 4 fA/√Hz, 2.87 fA rms in 1 s | 10 pA |
| 100 GΩ | 0.4 fA/√Hz, 287 aA rms in 1 s | 100 fA |

Both are large against 10 fA, and disconnecting the resistor needs a switch at the summing node, which this design avoids.

### Power-up range check (D-03, optional)

A $C_{inj}$ step and the decay identify the connected range: integrate, no decay. R2 (1 GΩ), about 10 ms. R1 (3.9 MΩ), about 40 µs. An input shorted by a mis-set Sa/Sc gives almost no step.

## Sources

- `sim/analytic/budget.out.txt`, sections "Calibration currents" and "cal plug". Decisions D-03, D-07.
