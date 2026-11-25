# On-probe test pulse and scope monitor outputs

**Conclusion:** Each probe makes its own test-charge step with a local switch and $C_{test}$, on a logic trigger from the MCU, from a DC level sent by the MCU board. One pulse locates the electronics' gain to about 0.05 %, and the pulse peak's width is the probe's electronic noise. Each channel's CSA output is buffered to a rear-panel SMA for a scope.

**Relied on by:** R-49 (gain by charge injection), R-52 (drift), R-77 (periodic test pulse), R-78 (monitor outputs), A-08, A-32, A-33, [four-probe plan](four-probe-plan.md).

## Working

### How the pulse is made (A-32)

- A voltage step $\Delta V$ on the far side of $C_{test}$ pushes a charge $Q = C_{test}\,\Delta V$ into the CSA input, as an alpha does. With 1 pF, 266 mV is 266 fC, the charge of a 6 MeV alpha.
- On the probe: an SPDT analog switch moves the driven end of $C_{test}$ between 0 V and a DC level $V_{cal}$, held on a local capacitor. An RC after the switch sets the edge to about 100 ns, far below the shaping time.
- The switch sits on the low-impedance side of $C_{test}$, so its charge injection and leakage never reach the input node.
- The cable carries a logic trigger and a DC level. Neither is a fast analog edge, which was the reason to generate the step on the probe.

### Where $V_{cal}$ comes from

| Option | Gives | Costs |
|---|---|---|
| (a) One reference and DAC on the MCU board, sent as DC, RC-filtered on each probe | One reference for all four probes, so probe ratios don't depend on it. Amplitude programmable: linearity, threshold checks, the pulse placed clear of the alpha lines | One more connector pin. DC ground offset between the boards (µV, negligible) |
| (b) A reference and divider on each probe | No analog pin | Four references drifting separately. Fixed amplitude |

Chosen: (a), agreed by the user.

### What to watch in the layout

- The logic trigger must not couple to the input node. A 3.3 V edge through 1 fF of stray injects 3.3 fC, which reads as 75 keV, and it moves with the 3.3 V rail.
- Keep the trigger trace outside the 0 V guard, far from the input, and slow its edge with an RC at the connector.
- The return edge injects the opposite charge. The positive-only trigger ignores it. Wait several $R_f C_f$ (100 µs) before the next pulse.

### What the pulse measures

- Single-pulse precision: the electronics' noise, about 7 keV FWHM (σ = 3 keV) for the OPA140 probe, 0.05 % of 6 MeV.
- One pulse a minute per channel is 1,440 a day. The MCU fires them, so they are tagged and kept out of the alpha spectrum. Dead time is negligible.
- The peak's width is the electronic noise of that probe and channel, measured directly. This is how the four probe types are compared, since the alpha peaks hide the difference.
- The pulse height follows $\Delta V \, C_{test} / C_f$. It sees the CSA, cable, shaper, hold and ADC. It does not see the diode.
- $C_{test}$ and $C_f$ are both C0G (±30 ppm/°C, `VERIFY` the parts): 5 °C moves either by 150 ppm, about 1 keV at 6 MeV. Board stray across $C_f$ (0.1–0.3 pF through FR-4, [signal levels](signal-levels.md)) is less stable, and is the more likely source of a real gain change.

### Monitor outputs (A-33)

- The MCU sees only the held peak. A scope on the CSA output shows the rise, the decay and any ringing or pickup.
- Tap: the CSA output where it arrives on the MCU board, before the pole-zero stage. The shaped signal is on a test point, not an SMA.
- Level: 44.3 mV/MeV, 266 mV at 6 MeV, on a 15–200 mV offset from dark current, so the buffer runs on the ±4.5 V rails.
- Buffer: high-impedance input so the chain is not loaded, 50 Ω series output. Full amplitude into a 1 MΩ scope input, half into 50 Ω.
- Bandwidth: the fastest probe's CSA rise is about 31 ns (ADA4817-1), so 50 MHz or more. The part is open.
- What the rise time means: with the OPA140 probe (about 1.7 µs) and the LMP7721 probe (about 0.8 µs) it is the amplifier's own speed. Charge collection in the diode is far faster and shows, if at all, only on the fast probes.
- Risk: a scope ties the board's ground to mains earth through the SMA shells. Compare the test-pulse width with the scope connected and disconnected before trusting spectra taken with it attached.

## Sources

- `sim/analytic/enc_budget.out.txt` (rise times, noise, charge per MeV).
- [Detector board](detector-board.md) (test charge, guard), [signal levels](signal-levels.md).
