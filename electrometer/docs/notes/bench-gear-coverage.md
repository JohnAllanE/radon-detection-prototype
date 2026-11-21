# What the bench gear already measures

**Conclusion:** Nothing on the bench resolves below about 1 nA directly, but a powered CSA board read by the DMM shows in-situ leakage down to roughly 1 pA, and the siggen, scope and CSA measure fF coupling on populated boards. The electrometer is needed below 1 pA, for bare boards, and for an absolute $C_{test}$: the only reasons R-02 and R-03 exist.

**Relied on by:** D-01 (scope), R-02 and R-03 (optional modes), R-07 (overlap with the DMM), R-26 (calibration), U-2, U-3.

## Working

### Current

- SDM3055 lowest current range: 200 µA with about 1 nA resolution (`instruments.json`). The DP2031 PSU reads back to 1 µA.
- Below 100 nA the SDM3055 has fewer than 100 counts on that range, so the useful overlap is 100 nA to 1 µA (R-07, low-range accuracy `VERIFY`).
- On a populated, powered board the CSA is itself a transimpedance amplifier for DC, with $R_f$ = 100 MΩ (radon architecture A-05). A leakage I shifts the output by I × 100 MΩ: 1 pA gives 100 µV, which the SDM3055 resolves on its 200 mV range.
- Reading with HV on and off cancels the op-amp offset, so in-situ leakage down to roughly 1 pA is measurable today (`VERIFY`: CSA offset drift and $R_f$ tolerance limit it).

### Capacitance

- **From about 100 pF up** (diode junction, decoupling, cables): the SDM3055 capacitance function. Lowest range 2 nF, about 1 pF resolution (`VERIFY`: `instruments.json` lists only "capacitance"). It can't guard, so it reads lead capacitance and each node's path to ground in series.
- **fF coupling on a populated, powered board:** step the suspect node (ring, PD bias, tube) with the SDG2122X and read the CSA output step on the scope: $C_x = C_f \, \Delta V_{out} / \Delta V_{step}$.
- Through the test-charge input the same gives $C_x / C_{test}$, so $C_f$ cancels, but the absolute value is only as good as $C_{test}$: ±25 % for a 1 pF ±0.25 pF part, adequate for a ripple limit. This is the measurement behind radon R-19.
- **Not covered:** fF coupling on a bare board (U-2) and an absolute $C_{test}$ (U-3).

## Sources

- `$ELECTRONICS_TOOLS/bench-test-gear/instruments.json` (SDM3055, DP2031, SDG2122X).
