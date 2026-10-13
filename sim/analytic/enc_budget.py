"""Equivalent noise charge (ENC) and rise-time budget for the 4 candidate CSP op-amps.

Phase 2 back-of-envelope, NOT a simulation. Models: series (voltage) noise, shot noise of
detector leakage, thermal noise of the feedback resistor, for a CR-RC shaper.
Assumptions to VERIFY (all printed with the results):
  - CR-RC noise form factors F_v = F_i = 0.924 for peaking time = shaping time constant
  - 3.62 eV per electron-hole pair in silicon
  - 1/f voltage noise ignored (op-amp e_n taken from the datasheet density quoted for the
    flat region); parallel noise from the bias-network resistor ignored (set to be large)
Inputs come from datasheets/*.json (source pages are listed there).

Run:  python3 -I sim/analytic/enc_budget.py
"""
import math

q = 1.602176634e-19      # C
kT = 1.380649e-23 * 300  # J at 300 K
w_si = 3.62              # eV per pair  (VERIFY)
F = 0.924                # CR-RC form factor (VERIFY)

# --- fixed inputs -----------------------------------------------------------
C_pd = 33e-12            # VTH2110 at 20 V: spec < 30 pF, curve ~32 pF (VTH2110.json p1, p3)
C_stray = 2e-12          # board + feedback stray, estimate
Cf = 1e-12               # feedback capacitor (design choice, to be simulated)
Rf = 100e6               # feedback resistor (design choice)
I_leak = {"typ 0.15 nA": 0.15e-9, "max 2 nA": 2e-9}   # VTH2110.json p1, p3

# name: (e_n nV/rtHz, Cin pF, GBW MHz, note)
amps = {
    "OPA140":   (5.1, 17.0, 11.0,   "Cin = 10 diff + 7 cm (OPA140.json p7)"),
    "OPA656":   (6.0, 3.0,  230.0,  "Cin = 2.6 diff + 0.4 cm (OPA656.json p5)"),
    "OPA657":   (4.8, 5.0,  1600.0, "Cin NOT extracted, 5 pF assumed (VERIFY)"),
    "LMP7721":  (6.5, 5.0,  17.0,   "Cin NOT extracted, 5 pF assumed (VERIFY)"),
    # ADI datasheets added by the user 2026-10-12 (ADA4817-1_4817-2.pdf, ADA4530-1.pdf)
    "ADA4817-1": (4.0, 1.4, 410.0,  "Cin = 1.3 cm + 0.1 diff (ADA4817-1.json p1); GBW >= 410 MHz (p4)"),
    "ADA4530-1": (14.0, 8.0, 2.0,   "e_n at 10 kHz; Cin 8 pF; GBW 2 MHz (ADA4530-1 datasheet)"),
    # HYPOTHETICAL discrete-JFET front end (not a pulled datasheet): NXP BF862 as quoted by a web search
    # result (e_n about 0.8 nV/rtHz at 100 kHz, Ciss about 10 pF). Loop GBW is a placeholder. VERIFY everything.
    "BF862 + op-amp (hypothetical)": (0.8, 10.0, 100.0, "BF862 figures from a search snippet, datasheet NOT pulled; GBW assumed"),
}
shaping_us = [1, 2, 4, 10]


def enc_series(en, ctot, tau):
    return en * ctot * math.sqrt(F / tau) / q


def enc_shot(i, tau):
    return math.sqrt(2 * q * i * F * tau) / q


def enc_rf(rf, tau):
    return math.sqrt(4 * kT / rf * F * tau) / q


def kev_fwhm(enc_e):
    return enc_e * w_si * 2.355 / 1000.0


print(f"C_pd = {C_pd*1e12:.0f} pF, C_stray = {C_stray*1e12:.0f} pF, Cf = {Cf*1e12:.1f} pF, Rf = {Rf/1e6:.0f} Mohm")
print(f"Gain Q/Cf: {1e6 / w_si * q / Cf * 1e3:.1f} mV per MeV  (Cf = {Cf*1e12:.1f} pF)")
print(f"Rf*Cf decay time constant = {Rf*Cf*1e6:.0f} us ;  dark current x Rf offset = "
      + ", ".join(f"{k}: {v*Rf*1e3:.0f} mV" for k, v in I_leak.items()))
print()
for name, (en, cin, gbw, note) in amps.items():
    ctot = C_pd + C_stray + cin * 1e-12
    gain_noise = ctot / Cf
    tau_amp = gain_noise / (2 * math.pi * gbw * 1e6)
    print(f"{name}: e_n = {en} nV/rtHz, Ctot = {ctot*1e12:.0f} pF, noise gain Ctot/Cf = {gain_noise:.0f}, "
          f"GBW = {gbw:.0f} MHz -> amp time const {tau_amp*1e9:.0f} ns, 10-90% rise ~ {2.2*tau_amp*1e9:.0f} ns  [{note}]")
    for t in shaping_us:
        tau = t * 1e-6
        s = enc_series(en * 1e-9, ctot, tau)
        for lk, i in I_leak.items():
            sh = enc_shot(i, tau)
            rf = enc_rf(Rf, tau)
            tot = math.sqrt(s ** 2 + sh ** 2 + rf ** 2)
            print(f"   tau = {t:>2} us, leak {lk:>11}: series {s:6.0f} e, shot {sh:4.0f} e, Rf {rf:4.0f} e "
                  f"-> ENC {tot:6.0f} e rms = {kev_fwhm(tot):5.1f} keV FWHM")
    print()

print("Benchmark: Cremat CR-110-R2.1 (CR-110-R2.1.json p1): 200 e + 3.8 e/pF at 1 us (premium module)")
for c in (C_pd * 1e12,):
    enc = 200 + 3.8 * c
    print(f"   at {c:.0f} pF: about {enc:.0f} e rms = {kev_fwhm(enc):.1f} keV FWHM (simple sum, VERIFY)")

print()
# Downstream stage noise (TLV900x, 27 nV/rtHz at 10 kHz, TLV9001.json p17), referred to the CSA output:
# a voltage noise e_n at the CSA output is equivalent to charge noise e_n*Cf (signal = Q/Cf), same CR-RC form.
for t in shaping_us:
    tau = t * 1e-6
    e_ds = enc_series(27e-9, Cf, tau)
    print(f"Downstream TLV900x first stage (gain 1), tau = {t:>2} us: {e_ds:4.0f} e rms = {kev_fwhm(e_ds):.2f} keV FWHM (smaller if the first stage has gain)")
print()
print("Signal: 1 MeV in Si -> %.2f fC; 6.0 MeV -> %.0f fC; 7.69 MeV -> %.0f fC; 8.78 MeV -> %.0f fC"
      % tuple([m * 1e6 / w_si * q * 1e15 for m in (1.0, 6.0, 7.69, 8.78)]))
