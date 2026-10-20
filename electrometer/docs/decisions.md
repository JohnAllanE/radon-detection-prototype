# Decisions: electrometer

Short dated entries: decision, alternatives considered, reason. Don't re-open an entry without saying why. IDs are local to the electrometer; radon-project decisions are written "radon D-xx".

## 2026-10-20

**D-01 Scope: a DC current meter that complements the bench DMM.**
The primary function is DC current from a small overlap with the SDM3055's lowest range (200 µA range, 1 nA resolution) down to a 10 fA target. Capacitance is mainly left to the bench gear: the SDM3055 for two-terminal values from about 100 pF up, and the siggen, scope and CSA test-charge method for fF coupling on populated boards (requirements §2). Charge and capacitance modes (R-02, R-03) are optional, kept only if the current topology makes them almost free.
Alternative considered: a combined current, charge and fF-capacitance instrument (draft 1, Claude's proposal).
Reason (user): the gap in the bench gear is small currents; standard gear handles most capacitances.

**D-02 Test arrangement: the built chamber in a grounded tin, one probe cable, switched connectors on the detector board.**
The primary test (U-5) is a built Part 1 chamber at +1 kV with its detector board(s), plus the electrometer, inside a grounded metal enclosure ("cookie tin") that is also the shield and dark box. The HV board stays outside and feeds the tube through an HV feedthrough with a lid interlock. Each CSA input has a Murata SWF-type switched coaxial connector on the board's back side, between the diode node and the CSA input; one probe cable is moved between them by hand with the tin open and HV off. Range switching in the head is manual (T-switch per branch) with the position read back by the MCU; the integrator reset and the source stay under MCU control. The electrometer runs on battery and floats; its common, the coax shields and the tin bond to the detector board's 0 V at one point. The radio antenna sits outside the tin.
Alternatives considered: a guarded reed-relay matrix (draft 1; the matrix's open contacts limit the floor, and it is the largest hardware item); soldered PTFE coax pigtails to an SMA bulkhead with shorting caps (works on a sacrificial board, but soldering on a populated, cleaned input node leaves flux on the most sensitive node); plain U.FL plus a 0 Ω link (needs soldering to disconnect the CSA); a stand-alone bench fixture without the chamber (cannot include the 1 kV wall meaningfully).
Reason (user): the 1 kV chamber bias can only be included meaningfully in situ; populated detector boards are low-volume and expensive and go into service after one or two test cycles; the user has used the Murata switch connectors before. Murata rates the SWF at 100 mating cycles with its probe. Leakage at fA is unpublished and is measured first (Q-12).

**D-03 Range switching and its readback (phase-2 arrangement, recorded early).**
Three feedback paths: 10 MΩ (1 µA full scale) and 1 GΩ (10 nA full scale), each switched by a T-switch, and a 10 pF integrator that is always connected (it also sets the resistor ranges' bandwidth) with the MCU's reset switch across it. Values are examples for phase 2. One rotary switch selects the mutually exclusive modes (1 µA, 10 nA, integrate, plus charge if Q-11 keeps it); each resistor branch uses two poles: Sa (summing node to midpoint) and a changeover with its common on the midpoint (resistor when on = Sb, 0 V when off = Sc). All Sa poles share one wafer, whose contacts are all near 0 V; the Sb/Sc poles, which carry Vout, are on another. The position is read without contacts: a diametrically magnetised disc magnet on the shaft and two DRV5055 Hall sensors in quadrature (90° apart, off-axis, facing the magnet), atan2 to an angle, nearest stored detent with a margin; between detents is "invalid". The sensors and their 3.3 V wiring stay outside the head's shield; the head box is non-ferrous where the field has to pass.
Alternatives considered: separate toggles (allow ambiguous combinations); an extra one-hot wafer on the shaft read by GPIOs (simplest, but puts 3.3 V digital lines into the switch body next to the summing node); an optical encoder.
Reason (user): DRV5055s are in stock (10 each of A1–A4), cheap, and keep the readback electrically separate from the switch.
Update 2026-10-20 (user): **range switches on an off-board panel**, so a cheap panel can be built now and a rotary panel later on the same head board. The feedback resistors and the 10 pF integrator (with its reset switch) stay on the head board. The panel connects through short stiff PTFE coax: S (summing node, shared), E1 and E2 (each resistor's free end; the other end is on Vout), shields at 0 V; the T's midpoint lives on the panel. Cheap panel: per branch an SPST (Sa: S to midpoint) and an SPDT (Sb/Sc: midpoint to E, or to 0 V) in separate bodies at any spacing, a magnet on each SPDT lever read by a DRV5055. Premium panel: the rotary arrangement above, same interface. No panel = integrate-only mode. Ranges are changed with the power off, then the MCU checks the readback and the range's response at power-up. A single DPDT per branch is rejected: inside one body the off branch's resistor terminal (at Vout, up to 10 V) sits millimetres from the summing-node terminal, and 10 V across 1-100 GΩ of switch plastic is 10 nA to 100 pA.
Update 2026-10-20 (user): **no position sensing.** The script tells the operator how to set the switches, the operator confirms, and the reading is logged with that range. The DRV5055 readback is dropped: its mounting could fail, it adds parts to a box whose priority is low cost, and a commercial picoammeter may replace this instrument later. Kept as an optional firmware check, no extra parts: at power-up the R-25 reference capacitor injects a small charge step, and the decay identifies the connected range (integrate: none; 1 GΩ: about 10 ms; R1 (3.9 MΩ in the architecture): about 40 µs; input shorted by a mis-set Sa/Sc: almost no step).

**D-04 No 1 nF charge range in this build.**
The 1 nF integrator capacitor (with its own T-switch and panel position) would only add measurement of charges larger than about 100 pC arriving faster than the 10 pF integrator can reset: a large voltage step into the diode node, or a nC discharge burst. Everything else is covered without it: currents by the resistor ranges and the 10 pF integrator, slow charge by reset counting, diode C-V by steps of about ±1 V. Large fast charges are logged as timestamped overloads. The panel stays at two branches (lines S, E1, E2), and Q-11 is resolved.
Alternatives considered: keep the 1 nF for a ±10 nC charge range (draft 2, R-02).
Reason (user): stay focused on the immediate need; a later revision is likely anyway once building turns up real issues, and the range can be added then.


**D-05 Burden split by range (R-01).**
Burden ≤ 1 mV up to 4 nA and ≤ 10 mV on the 1 µA range.
Alternative considered: ≤ 1 mV everywhere (requirements draft 3), which forces the input protection's series resistor down to 1 kΩ and the clamps to take ten times the fault current.
Reason: 10 mV is negligible against the node biases (20 V PD, ring); the 10 kΩ series resistor stays (architecture §1.5). Approved by the user.

**D-06 One source channel; mains frequency not needed (Q-03, Q-08).**
One ±50 V channel. In the chamber the real PD bias and ring supplies are selected by hand at the PicoBlade breakout, with a 0 V position; the built-in source serves bench tests, bare boards and alternating-polarity resistance. Q-08 is closed: integration over multiples of 100 ms and the ADC's simultaneous 50/60 Hz mode reject both.
Alternative considered: two channels, for PD bias and ring at the same time.
Reason: the real supplies are the right ones in situ (architecture §1.7). Approved by the user.

**D-07 Source DAC: the dual 12-bit MCP4922 as coarse + fine.**
The fine channel is attenuated so its full scale spans 4 coarse LSBs and is summed with the coarse channel at unity gain (MCP4922 datasheet §6.7), as on the user's microbalance. The overlap covers the coarse channel's DNL. The firmware sets the coarse code and trims the fine code against the source readback (R-21), so steps are monotonic and the setpoint accurate; about 24 µV per step at the output, against 10 mV required. C_inj gets its own DAC (MCP4821, in stock).
Alternatives considered: a 16-bit DAC (to buy); the 12-bit MCP4922 alone (about 25 mV steps, misses R-08).
Reason (user): uses stock, and the method is proven on the microbalance.

**D-08 Two 18650 cells in parallel (1S2P).**
About 38 h with the source off and 25 h with it on (budget; draws `VERIFY`).
Alternatives considered: three cells in parallel (about 38 h with the source on; capacity only, since parallel cells add no voltage); cells in series (2S or 3S: needs a balancing charger and protection, and buys nothing because every rail comes from a converter anyway).
Reason (user): the two-cell figures are acceptable. If the measured draws miss R-24, a third parallel cell is the fix.
