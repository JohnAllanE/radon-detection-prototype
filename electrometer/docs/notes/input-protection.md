# Input protection, burden and the HV fault current

**Conclusion:** A 10 kΩ series resistor and low-leakage clamps protect the input with 40 µV burden at 4 nA and 10 mV at 1 µA (D-05). Surviving a tube flashover also needs the radon HV board to limit its fault current: ≥ 10 MΩ output series resistance gives about 100 µA, easy to clamp. That request is open.

**Relied on by:** A-05 (input protection), A-18 (HV series resistance, radon A-21), R-01 (burden), R-10 (survives faults), R-27 (source limit).

## Working

### Series resistor against burden

| Series R | Burden at 1 µA | Burden at 4 nA | Thermal noise (adds to $e_n$) |
|---|---|---|---|
| 10 kΩ | 10 mV | 40 µV | 12.8 nV/√Hz |
| 100 kΩ | 100 mV | 400 µV | 40.6 nV/√Hz |

- ≤ 1 mV everywhere would force the series resistor down to 1 kΩ and the clamps to take ten times the fault current. 10 mV is negligible against the node biases (20 V PD, the ring), so D-05 splits the burden by range.
- The clamps run from the summing node to common with about 0 V across them, so their leakage scales with $V_{os}$. Low-leakage diodes or diode-connected JFETs (`VERIFY` leakage at mV).

### HV fault current (open request on the radon HV board)

- A flashover from the tube to a diode node while the probe is on it is survivable only if the HV board's output has series resistance.
- At ≥ 10 MΩ the fault current is 100 µA at 1 kV (`VERIFY` against the HV board's design). It also protects the CSAs in service, and changes nothing on the detector board.
- The alternative, 10 MΩ at the electrometer input, gives 10 V burden at 1 µA and 40 mV at 4 nA.

## Sources

- `sim/analytic/budget.out.txt`, "Input protection vs burden". Decision D-05.
