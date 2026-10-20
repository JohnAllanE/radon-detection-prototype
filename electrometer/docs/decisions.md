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
