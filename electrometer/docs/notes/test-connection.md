# Test connection, grounding and shielding

**Conclusion:** The measured node sits at virtual ground, so the electrometer common is the guard potential and the coax shield is the guard up to the board's switch connector. The electrometer floats on its battery and bonds to the rest of the system only at the detector board's 0 V, through the probe shield.

**Relied on by:** R-11 (one probe cable), R-14 (cable tie-down), R-19 (switch connectors on the detector board), R-24 (battery), R-31 (grounding), Q-12, Q-13.

## Working

### Grounding (R-31)

| Point | Connects to |
|---|---|
| Probe and coax centre | The CSA input node through the switch connector, held at virtual ground |
| Coax shield, electrometer end | Analog common (0 V): the op-amp's + input, the head's shield box, the source's reference |
| Coax shield, board end | The switch connector's shell, soldered to the 0 V guard ring around the input node (same net as GND and the CSA's + input) |
| The tin | Electrometer common, bonded once |
| Single bond point | Common meets the rest of the system only at the detector board's 0 V, through the coax shield |
| HV return | The HV board's own wiring, never a coax shield |

- The detector board's GND also reaches mains earth through the MCU board, USB and the PC. So the electrometer must float (battery, ESP-NOW), or a ground loop puts its millivolts between guard and input.
- No separate driven guard is needed: burden ≤ 1 mV keeps the node at the common's potential.

### The switch connector (R-19, feeds radon R-60)

- A Murata SWF-type switched coaxial connector per CSA input, on the back side, in series between the diode node and the CSA input. Unmated it connects diode to CSA. With the probe in, it routes the diode node to the probe and disconnects the CSA. Its shell is soldered to the 0 V guard ring.
- $C_{test}$ sits on the diode side, so the electrometer can measure it. No soldering on an input node after the board is cleaned. The bare-board test board uses the same footprints.
- SWF: 2.5 × 2.5 × 1.4 mm, rated 100 mating cycles with a Murata probe, 30 Vrms ([Murata SWF](https://www.murata.com/en-global/products/connector/switchconnector/overview/lineup/swf)). Service boards see 1–2 cycles per connector.
- Leakage and the probe's own cycle life are not published, only the receptacle's 100 cycles with a probe (Q-12): ask Murata for the approval sheet, and measure on the test board (U-6) before relying on it at 10 fA.
- The open contact sits between the diode node (virtual ground) and the CSA input (idling at 0 V), so it has about 0 V across it. The body likewise has about 0 V from centre to shell. Its leakage should be small whatever the plastic. U-6 measures it.
- With its diode disconnected, the measured channel's CSA becomes a follower of its 0 V input through $R_f$, so other channels keep running, provided the CSA op-amp is stable at a noise gain of 1. OPA140 and OPA656 are unity-gain stable. A decompensated part such as OPA657 relies on the diode capacitance and may oscillate (`VERIFY` for the chosen parts, otherwise turn the rails off while measuring).

### The probe (R-11, R-14)

- A Murata SWF-series probe with an SMA end, for example MXHS83QE3000 (300 mm) or MXHS83QE1000 (100 mm).
- Murata warns that cable stress on a mated probe can unmate it, damage the connector or peel its electrodes off the board. So the cable is tied down and strain-relieved in the tin.

### Space (Q-13)

Four 2.5 × 2.5 mm connectors with guard rings, plus the CSAs, on the back of the detector board (quoted as ≤ 20 mm), and room for the probe with the chamber assembled in the tin.

### Alternatives considered (D-02)

A guarded reed-relay matrix, soldered PTFE pigtails to an SMA bulkhead, plain U.FL plus a 0 Ω link, and a stand-alone fixture without the chamber. Reasons in D-02.

## Sources

- Murata SWF lineup page. Electrometer decisions D-02.
