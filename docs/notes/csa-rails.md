# CSA supply rails: is a programmable low-noise rail needed?

**Conclusion:**

- No programmable rail: a CSA's resolution does not depend on its rail voltage. Each op-amp candidate gets a fixed rail inside its range, set by resistors when the board is built.
- Rail noise reaches the input only through the op-amp's power-supply rejection. Even the LM27762's 22 µV<sub>rms</sub> stays far below the OPA140's own 5.1 nV/√Hz if the PSRR in the shaping band is above about 30 dB (`VERIFY` per part from its curve).
- The rails that need care touch the input through a capacitance: the photodiode bias and, in A-29, the top-copper bias $V_{top}$.
- Best practice: charge pump, fixed low-noise LDO, local RC or LC filter and decoupling at each op-amp. TI's ANY-OUT parts (TPS7A47, TPS7A33) fit, pins strapped, not switched. An op-amp buffer as the rail is worse: its own noise, and stability into the decoupling.

**Relied on by:** A-05, A-07, A-19, A-29, R-09, R-19, the user's answer 2 of 2026-11-21.

## Working

### How rail noise reaches the charge

- An op-amp's supply noise appears at its input divided by the PSRR: $e_{ps} = e_{rail} / \mathrm{PSRR}(f)$. It then adds to the op-amp's own voltage noise $e_n$ in quadrature, and both act on the total input capacitance like any series voltage noise.
- The shaper (A-14, τ = 4 µs) passes a band around $1/(2\pi\tau) \approx 40$ kHz. Only rail noise in that band counts; the LM27762's 2 MHz switching (LM27762.pdf p1) is shaped away and only needs local decoupling.
- LM27762: 22 µV<sub>rms</sub>, 10 Hz–100 kHz, on each output (LM27762.pdf p5). Spread evenly, that is $22\ \mu\mathrm{V}/\sqrt{10^5\ \mathrm{Hz}} \approx 70$ nV/√Hz.
- For the rail to add under 10 % to $e_n$ in quadrature, $e_{ps} < 0.46\, e_n$. For the OPA140 ($e_n$ = 5.1 nV/√Hz, OPA140.pdf p1): $e_{ps} < 2.3$ nV/√Hz, so PSRR > 70/2.3 ≈ 30 (30 dB) at 40 kHz. The OPA140's DC PSRR is 0.1 µV/V (140 dB, OPA140.pdf p7); its value at 40 kHz is read from Fig. 6-7 (`VERIFY`), and JFET-input precision parts usually keep well above 30 dB there.
- A TPS7A47 (4 µV<sub>rms</sub>, 10 Hz–100 kHz; PSRR 82 dB at 100 Hz, 60 dB at 100 kHz, [TI product page](https://www.ti.com/product/TPS7A47)) and a TPS7A33 (16 µV<sub>rms</sub>, 72 dB, [TI datasheet](https://www.ti.com/lit/pdf/SBVS169)) lower that further, at a cost and board area the noise budget doesn't ask for.

### Why programmability doesn't help

- The CSA's noise is set by $e_n$, the input capacitance, the feedback parts and leakage (`noise-budget.md`), none of which move with the rail. The rail only has to cover the output swing: 389 mV for an 8.78 MeV pulse plus up to 200 mV of dark-current offset (questions 2026-11-21, question 2).
- With four tubes carrying four different op-amps (A-29), each tube's board is built for its part: ±2.5 V for the LMP7721 (1.8–5.5 V total, LMP7721.json p5), ±4.5 V for the OPA140 and ADA4817-1 (ADA4817-1: 5–10 V total, ADA4817-1.json p7). A strapped ANY-OUT LDO, or a fixed LDO with two resistors, does it. A shift register on the set pins adds switch leakage and parts for no gain.
- An op-amp buffer as the rail: its own noise is often higher than a good LDO's, and driving the bypass capacitors invites oscillation. Not used.

### The rails that do matter

- **Photodiode bias (A-04):** its noise $v_b$ injects $C_{pd} v_b$ directly, with no PSRR in between. Same 10 % rule: $v_b$ below about 2 nV/√Hz at 40 kHz. The planned 1 MΩ and 100 nF filter attenuates by $2\pi f R C \approx 2.5 \times 10^4$ at 40 kHz, so the source may carry up to about 60 µV/√Hz there.
- **Top-copper bias $V_{top}$ (A-29, S-02):** couples through the small capacitance between the copper and the die and its trace (`VERIFY`, below 1 pF expected): the same RC filter type at each board, the larger $V_{top}$ (up to +200 V) using a resistor and capacitor rated for it.

### Recommendation

Keep A-19: LM27762, then a fixed LDO and an RC filter per board (TPS7A47/TPS7A33 strapped if a premium board wants the margin), a local pair for the LMP7721 board. Measure the rail noise once on the first board (risk 6).
