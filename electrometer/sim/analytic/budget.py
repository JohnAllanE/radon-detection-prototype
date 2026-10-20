#!/usr/bin/env python3
"""Electrometer phase-2 budgets: ranges, noise floor, stability, reset timing, leakage, battery.

Standard library only. Run:  python3 electrometer/sim/analytic/budget.py > electrometer/sim/analytic/budget.out.txt
Every input is listed in INPUTS with its source; `VERIFY` marks assumptions not yet checked.
Requirement IDs refer to electrometer/docs/01-requirements.md.
"""

import math

K_B, T = 1.380649e-23, 298.0
Q_E = 1.602176634e-19

INPUTS = {
    # ADA4530-1 (datasheets/ADA4530-1.pdf, SOIC, 25 C)
    "vos_max": (40e-6, "V", "input offset voltage max (p3, p5)"),
    "vos_drift_max": (0.5e-6, "V/K", "offset drift max, 0..125 C (p3, p5)"),
    "en_pp_0p1_10": (4e-6, "Vpp", "voltage noise 0.1-10 Hz (p4, p5)"),
    "en_1k": (16e-9, "V/rtHz", "voltage noise density at 1 kHz (p4)"),
    "in_0p1": (0.07e-15, "A/rtHz", "current noise density at 0.1 Hz (p4)"),
    "ib_max": (20e-15, "A", "input bias max, -40..85 C (p1)"),
    "cin_amp": (8e-12, "F", "input capacitance typ (p3)"),
    "gbw": (2e6, "Hz", "GBW typ, G = 100 (p3)"),
    "isy_amp": (1.3e-3, "A", "supply current max (p3)"),
    "out_swing": (4.0, "V", "usable output swing on +/-5 V rails: VOH/VOL within 40 mV of rails at 10 V supply (p5); 4 V keeps margin for the ADC front end"),
    # Feedback network (PROPOSED, architecture §3.1)
    "cf": (10e-12, "F", "integrator capacitor, always in (D-03)"),
    "r1": (3.9e6, "ohm", "range 1 resistor (1 uA full scale at 3.9 V)"),
    "r2": (1e9, "ohm", "range 2 resistor (3.9 nA full scale at 3.9 V)"),
    "t_reset_min": (10e-3, "s", "shortest integration ramp allowed between resets (settling after reset charge injection), PROPOSED"),
    # Input-node capacitance contributions
    "c_diode_20v": (33e-12, "F", "VTH2110 at 20 V (VTH2110.json p1, p3)"),
    "c_diode_0v": (150e-12, "F", "VTH2110 at 0 V bias: VERIFY (curve stops at 20 V; larger at low bias)"),
    "c_probe_cable": (30e-12, "F", "Murata probe, 300 mm cable, ~100 pF/m: VERIFY"),
    "c_s_coax": (30e-12, "F", "range-panel S coax, 300 mm, ~100 pF/m: VERIFY"),
    "c_inj": (1e-12, "F", "permanent injection capacitor for self-test and calibration (PROPOSED, architecture §3.1)"),
    # Power (all VERIFY until parts are chosen in phase 3)
    "i_mcu": (100e-3, "A", "ESP32-S3 module with radio receiving for ESP-NOW, average at 3.3 V: VERIFY"),
    "i_analog": (15e-3, "A", "head + ADC + DACs + T/RH + references at 5 V rails: VERIFY"),
    "p_source": (0.25, "W", "+/-50 V source: boost to about +/-60 V plus a low-power HV amplifier, when enabled: VERIFY"),
    "eff": (0.85, "", "converter efficiency from the cell: VERIFY"),
    "v_cell": (3.6, "V", "Li-ion 1S nominal under load"),
    "cell_ah": (3.0, "Ah", "one 18650 cell, usable: VERIFY per cell"),
    # Source DAC (architecture §3.4): MCP4922 coarse + fine, per the MCP4922 datasheet §6.7 (dual DAC as double precision)
    "src_span": (100.0, "V", "source output span, -50..+50 V (R-08)"),
    "dac_bits": (12, "bit", "MCP4922, each channel"),
    "fine_overlap_bits": (2, "bit", "fine channel's full scale spans 2^n coarse LSBs, so it covers the coarse DNL"),
    "src_zero_err": (10e-3, "V", "source output at a commanded 0 V, uncalibrated (DAC offset x gain ~20): VERIFY"),
}


def v(name):
    return INPUTS[name][0]


def eng(x, unit=""):
    if x == 0:
        return f"0 {unit}"
    prefixes = [(1e12, "T"), (1e9, "G"), (1e6, "M"), (1e3, "k"), (1, ""), (1e-3, "m"), (1e-6, "u"), (1e-9, "n"),
                (1e-12, "p"), (1e-15, "f"), (1e-18, "a")]
    for scale, p in prefixes:
        if abs(x) >= scale:
            return f"{x / scale:.3g} {p}{unit}"
    return f"{x:.3g} {unit}"


def section(title):
    print(f"\n== {title} ==")


def main():
    print("Electrometer phase-2 budgets (budget.py). Inputs:")
    for k, (val, unit, src) in INPUTS.items():
        print(f"  {k:16s} {val:<10.4g} {unit:7s} {src}")

    swing, cf, r1, r2 = v("out_swing"), v("cf"), v("r1"), v("r2")

    section("Ranges (R-01, R-07)")
    q_max = cf * swing
    i_int_max = q_max / v("t_reset_min")
    print(f"Integrator: charge per ramp = Cf x swing = {eng(q_max, 'C')}; "
          f"max current at {eng(v('t_reset_min'), 's')} per ramp = {eng(i_int_max, 'A')}")
    for name, r in (("R1", r1), ("R2", r2)):
        fs = swing / r
        off = v("vos_max") / r
        drift = v("vos_drift_max") / r
        print(f"{name} = {eng(r, 'ohm')}: full scale {eng(fs, 'A')}; offset before zeroing {eng(off, 'A')}; "
              f"offset drift {eng(drift, 'A')}/K; lowest reading at 1 % of reading after zeroing ~ {eng(100 * drift, 'A')} per K of drift")
    print("Coverage: integrator 10 fA..~4 nA, R2 ~4 pA..3.9 nA (continuous), R1 ~1 nA..1 uA. "
          "Overlap with the SDM3055 200 uA range: 100 nA..1 uA (R-07).")

    section("Input capacitance and noise gain")
    for label, cd in (("PD bias on (20 V)", v("c_diode_20v")), ("PD bias 0 V (fA runs)", v("c_diode_0v"))):
        cin = cd + v("c_probe_cable") + v("c_s_coax") + v("cin_amp") + v("c_inj")
        ng = 1 + cin / cf
        print(f"{label}: Cin = {eng(cin, 'F')}, noise gain (integrator) = 1 + Cin/Cf = {ng:.1f}")

    section("Integrator current resolution, op-amp limited (R-01 target 10 fA)")
    for label, cd in (("PD bias on", v("c_diode_20v")), ("PD bias 0 V", v("c_diode_0v"))):
        cin = cd + v("c_probe_cable") + v("c_s_coax") + v("cin_amp") + v("c_inj")
        ng = 1 + cin / cf
        for t_int in (1.0, 10.0):
            # Slope from a ramp of length t_int: the voltage-noise contribution is the 0.1-10 Hz p-p noise times the
            # noise gain, referred to current by Cf / t_int. Current noise adds directly.
            dv = v("en_pp_0p1_10") * ng
            i_v = cf * dv / t_int
            i_i = v("in_0p1") * math.sqrt(1 / (2 * t_int)) * 6.6  # p-p of white noise in ENBW 1/(2T)
            print(f"  {label}, T = {t_int:4.0f} s: from en {eng(i_v, 'A')}pp, from in {eng(i_i, 'A')}pp, "
                  f"total ~ {eng(math.hypot(i_v, i_i), 'A')}pp")
    print("Conclusion: the amplifier is not the limit for 10 fA; leakage, triboelectric charge, dielectric absorption "
          "and humidity are (risks R1-R4 in the architecture).")

    section("Resistor ranges: thermal noise of Rf (1 s reading, ENBW 0.5 Hz)")
    for name, r in (("R1", r1), ("R2", r2)):
        i_n = math.sqrt(4 * K_B * T / r)
        print(f"{name}: {eng(i_n, 'A')}/rtHz -> {eng(i_n * math.sqrt(0.5), 'A')} rms per 1 s reading")

    section("Loop stability, transimpedance ranges (worst case Cin)")
    cin = v("c_diode_0v") + v("c_probe_cable") + v("c_s_coax") + v("cin_amp") + v("c_inj")
    for name, r in (("R1", r1), ("R2", r2)):
        f_zero = 1 / (2 * math.pi * r * (cin + cf))
        f_pole = 1 / (2 * math.pi * r * cf)
        ng_hf = 1 + cin / cf
        f_cross = v("gbw") / ng_hf
        # Phase margin from the noise-gain pole/zero pair, single-pole amplifier
        pm = 90 + math.degrees(math.atan(f_cross / f_pole) - math.atan(f_cross / f_zero))
        print(f"{name}: noise-gain zero {eng(f_zero, 'Hz')}, pole {eng(f_pole, 'Hz')}, HF noise gain {ng_hf:.1f}, "
              f"crossover {eng(f_cross, 'Hz')}, phase margin ~{pm:.0f} deg; signal bandwidth {eng(f_pole, 'Hz')}")
    print("Both ranges have more than 60 deg margin; a SPICE check (S-01) confirms with the real model.")

    section("Mains rejection (Q-08)")
    print("A slope or average over a multiple of 100 ms spans whole cycles of both 50 Hz (5) and 60 Hz (6), and a "
          "delta-sigma ADC with simultaneous 50/60 Hz rejection does the same for the resistor ranges, so the design "
          "does not need to know the mains frequency.")

    section("Leakage at the summing node (everything has about Vos across it)")
    for r_ins in (1e12, 1e14):
        print(f"  {eng(v('vos_max'), 'V')} across {eng(r_ins, 'ohm')} -> {eng(v('vos_max') / r_ins, 'A')}")
    print(f"  Op-amp input bias max {eng(v('ib_max'), 'A')} (zeroed; the typical value at 25 C is far lower)")
    print("  Open Sa contacts, clamp diodes, the reset switch's summing-node side and C_inj's drive line all sit at "
          "~0 V, so their leakage scales with Vos, not with the 4 V output or the 50 V source.")

    section("Calibration currents from the injection capacitor (architecture §3.1)")
    for rate in (0.01, 0.1, 1.0, 4.0):
        print(f"  C_inj x ramp {rate:g} V/s = {eng(v('c_inj') * rate, 'A')}")

    section("Input protection vs burden (R-01, R-10)")
    for r_s in (10e3, 100e3):
        print(f"  Series R {eng(r_s, 'ohm')}: burden {eng(1e-6 * r_s, 'V')} at 1 uA, {eng(4e-9 * r_s, 'V')} at 4 nA; "
              f"thermal noise {eng(math.sqrt(4 * K_B * T * r_s), 'V')}/rtHz (adds to en)")
    print("  Fault current from a 1 kV flashover is set by the HV board's output resistance: at 10 Mohm it is 100 uA, "
          "which clamp diodes and a 10 kohm series R handle easily (requirement on the HV board).")

    section("Why the resistor check is an external cal plug, not a resistor fixed to the summing node (R-25)")
    for r_cal in (1e9, 1e11):
        i_n = math.sqrt(4 * K_B * T / r_cal)
        print(f"  {eng(r_cal, 'ohm')} left on the node: thermal noise {eng(i_n, 'A')}/rtHz "
              f"({eng(i_n * math.sqrt(0.5), 'A')} rms in a 1 s reading) and {eng(v('src_zero_err') / r_cal, 'A')} "
              f"from a source 'at 0 V' that is {eng(v('src_zero_err'), 'V')} off, against the 10 fA target")
    print("  C_inj injects only C*dV/dt: a static DAC offset gives no current, and an ideal capacitor has no thermal noise.")

    section("Source DAC, coarse + fine (R-08: 10 mV steps)")
    coarse = v("src_span") / 2 ** v("dac_bits")
    fine = coarse * 2 ** v("fine_overlap_bits") / 2 ** v("dac_bits")
    print(f"  12-bit alone: {eng(coarse, 'V')} per step")
    print(f"  coarse + fine (fine full scale = {2 ** v('fine_overlap_bits')} coarse LSB): {eng(fine, 'V')} per step, "
          f"about {math.log2(v('src_span') / fine):.0f} bits; monotonic and accurate only through the ADC readback (R-21)")

    section("Battery (R-24: >= 24 h)")
    p_base = v("i_mcu") * 3.3 + v("i_analog") * 10
    for label, p in (("source off", p_base), ("source on", p_base + v("p_source"))):
        i_cell = p / v("eff") / v("v_cell")
        for n in (2, 3):
            hours = n * v("cell_ah") / i_cell
            print(f"  {label}: {p:.2f} W -> {eng(i_cell, 'A')} from the cell; {n} x 18650: {hours:.0f} h")


if __name__ == "__main__":
    main()
