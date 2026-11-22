"""Generate the detector project's architecture diagrams as SVG (light and dark mode via prefers-color-scheme).

Edit the layouts below and rerun:  python3 docs/diagrams/make_diagrams.py
Standard library only (no Svg.math()). The style and helpers come from $ELECTRONICS_TOOLS/diagrams/svgdiagram.py.
Outputs sit next to this file and are embedded in ../02-architecture.md. The electrometer has its own
script in electrometer/docs/diagrams/.
"""

import os
import sys
from pathlib import Path

if "ELECTRONICS_TOOLS" not in os.environ:
    sys.exit("ELECTRONICS_TOOLS is not set: point it at the electronics-tools repo (environment/README.md)")
sys.path.insert(0, str(Path(os.environ["ELECTRONICS_TOOLS"]) / "diagrams"))
from svgdiagram import Svg, legend  # noqa: E402

HERE = Path(__file__).resolve().parent


def system_block():
    d = Svg(1000, 470, "System block diagram: in each chamber, two detector boards (premium and low-cost) each carry "
                       "four photodiodes and four charge-sensitive preamps and connect to the MCU board, which shapes, "
                       "holds, digitises and reports to the host. The HV board makes about +1 kV for the Part 1 "
                       "chamber walls and the regulated photodiode bias.")
    d.add('<rect class="encl" x="20" y="20" width="330" height="300" rx="12"/>')
    d.text(36, 42, "CHAMBER (DETECTOR BOARD IS THE SEAL)", "g")
    d.box(40, 60, 290, 60, "4 × silicon photodiode", "chamber side, 2 × 2 array")
    d.box(40, 150, 290, 70, "4 × charge-sensitive preamp", ["atmosphere side", "detector board: premium or low-cost"])
    d.line([(185, 120), (185, 148)])
    d.box(40, 245, 290, 55, "Second detector board", "the other variant, same field")

    d.box(430, 120, 280, 150, "MCU board",
          ["pulse shaping, peak hold", "comparator trigger, channel mux", "ADCs, ESP32-S3 microcontroller",
           "outside the chamber"])
    d.line([(330, 185), (428, 185)])
    d.line([(330, 272), (380, 272), (380, 200), (428, 200)])
    d.text(379, 176, "board-to-board", "lsig", "middle")
    d.text(379, 290, "wire connector", "lsig", "middle")

    d.box(790, 145, 180, 60, "Host", "PC")
    d.line([(710, 175), (788, 175)], "ctl")
    d.text(750, 166, "USB", "lctl", "middle")
    d.text(750, 194, "ESP-NOW option", "lctl", "middle")

    d.box(430, 345, 280, 95, "HV board",
          ["48 V in, PCB transformer to 100–200 V", "Walton multiplier, fixed output", "regulated PD bias"])
    d.line([(430, 395), (205, 395), (205, 322)], "pwr")
    d.text(318, 386, "about +1 kV to the Part 1 walls", "lpwr", "middle")
    d.line([(430, 420), (12, 420), (12, 90), (38, 90)], "pwr")
    d.text(120, 412, "regulated PD bias", "lpwr", "middle")

    d.box(790, 345, 180, 40, "48 V wall adapter")
    d.line([(790, 365), (712, 365)], "pwr")
    d.box(790, 250, 180, 40, "5 V wall adapter")
    d.line([(790, 270), (712, 270)], "pwr")
    d.line([(430, 160), (332, 160)], "pwr")
    d.text(379, 152, "±4.5 V", "lpwr", "middle")
    legend(d, 458, ["sig", "ctl", "pwr"])
    d.write(HERE / "system-block.svg")


def signal_chain():
    d = Svg(1100, 520, "Per-channel signal chain, repeated four times per detector board: photodiode into a "
                       "charge-sensitive preamp with a test-charge input and a filtered bias, over the connector to "
                       "the MCU board, where a pole-zero and gain stage feeds a CR-RC^n shaper, a comparator that "
                       "interrupts the ESP32-S3, and a peak detector with a reset switch and a hold buffer. The "
                       "buffered hold goes straight to the ADS1220 and through a 4:1 mux to the ADS8689 or, as an "
                       "option, the ESP32-S3's own ADC.")
    d.add('<rect class="group" x="20" y="20" width="300" height="300" rx="10"/>')
    d.text(36, 42, "DETECTOR BOARD (ATMOSPHERE SIDE EXCEPT PD)", "g")
    d.box(40, 140, 90, 45, "VTH2110", "photodiode")
    d.box(170, 135, 130, 55, "CSA", "C_{f}, R_{f}, op-amp")
    d.line([(130, 162), (168, 162)])
    d.box(170, 230, 130, 45, "Output", "series R")
    d.line([(235, 190), (235, 228)])
    d.box(40, 60, 120, 50, "PD bias filter", "from the HV board")
    d.line([(100, 110), (100, 138)], "pwr")
    d.box(180, 60, 120, 50, "Test charge", "C_{test}")
    d.line([(240, 110), (240, 133)])

    d.add('<rect class="group" x="360" y="20" width="720" height="460" rx="10"/>')
    d.text(376, 42, "MCU BOARD (SINGLE +5 V, TLV90XX)", "g")
    d.line([(300, 252), (380, 252)])
    d.text(330, 244, "PicoBlade", "lsig", "middle")
    d.box(382, 225, 120, 55, "Pole-zero", "and gain stage")
    d.box(540, 225, 120, 55, "Shaper", ["CR-RC^{n}", "τ 2 to 10 µs"])
    d.line([(502, 252), (538, 252)])
    d.box(700, 90, 140, 50, "Comparator", "TLV9061 or TLV3201")
    d.line([(660, 240), (680, 240), (680, 115), (698, 115)])
    d.box(700, 225, 140, 55, "Peak detector", ["op-amp, diode, C_{hold}"])
    d.line([(660, 252), (698, 252)])
    d.box(700, 330, 140, 45, "Reset switch", "TMUX1101", ctl=True)
    d.line([(770, 330), (770, 282)], "ctl")
    d.box(870, 225, 90, 55, "Hold", "buffer")
    d.line([(840, 252), (868, 252)])
    d.box(980, 120, 85, 55, "ADS1220", "AIN0–3, SE")
    d.line([(960, 240), (970, 240), (970, 147), (978, 147)])
    d.box(870, 330, 90, 45, "TMUX1104", "4:1 mux", ctl=True)
    d.line([(915, 280), (915, 328)])
    d.box(980, 300, 85, 45, "ADS8689")
    d.line([(960, 345), (970, 345), (970, 322), (978, 322)])
    d.box(980, 400, 85, 50, "ESP32-S3", "ADC, option")
    d.line([(960, 360), (972, 360), (972, 425), (978, 425)])
    d.box(382, 60, 120, 55, "ESP32-S3", "MCU")
    d.line([(770, 90), (770, 75), (504, 75)], "ctl")
    d.text(637, 68, "interrupt, channel ID", "lctl", "middle")
    d.line([(382, 100), (372, 100), (372, 465), (915, 465), (915, 377)], "ctl")
    d.line([(770, 465), (770, 377)], "ctl")
    d.text(640, 457, "mux select, reset", "lctl", "middle")
    legend(d, 505, ["sig", "ctl", "pwr", "dot"])
    d.write(HERE / "signal-chain.svg")


def gas_train():
    d = Svg(1140, 250, "Part 1 gas train, in order: sample gas (air, or bottled N2 as the control), inlet filter, "
                       "desiccant column, final filter, chamber inlet ball valve, the chamber (304 SS tube, walls at "
                       "about +1 kV, two detector boards), outlet ball valve, outlet filter, diaphragm pump, exhaust.")
    steps = [("Sample gas", "air or N_{2}"), ("Inlet filter", None), ("Desiccant", "column"),
             ("Final filter", None), ("Ball valve", "SS + PTFE"), ("Chamber", "304 SS, +1 kV"),
             ("Ball valve", "SS + PTFE"), ("Outlet filter", "D-25, working"), ("Diaphragm", "pump"),
             ("Exhaust", None)]
    x, w, gap = 15, 100, 12
    for i, (t, s) in enumerate(steps):
        d.box(x, 70, w, 60, t, s)
        if i < len(steps) - 1:
            d.line([(x + w, 100), (x + w + gap - 2, 100)], "flow")
        x += w + gap
    d.text(20, 40, "PTFE TUBING THROUGHOUT. PUMP DOWNSTREAM, SO THE CHAMBER RUNS SLIGHTLY BELOW AMBIENT", "g")
    d.text(20, 170, "Insulating PTFE sections between the +1 kV chamber and the valves (R-38). One filter type at "
                    "every port is a working proposal (D-25).", "s")
    d.text(20, 190, "Humidity is read at the outlet during the N_{2} purge with a manual sensor (R-34).", "s")
    legend(d, 225, ["flow"], flow="Gas flow")
    d.write(HERE / "gas-train.svg")


def decay_chain():
    d = Svg(1180, 495, "The radon-222 decay chain as this detector sees it: Rn-222 decays in the gas; Po-218, "
                       "Po-214 and, over months, Po-210 decay on the die and their alphas are counted.")
    W, H = 150, 66
    xs = [20, 280, 505, 730, 955]
    y1, y2 = 110, 310
    groups = [(10, 180, y1 - 40, y1 + H + 22, "IN THE GAS"),
              (265, 1115, y1 - 40, y1 + H + 22, "ON THE DIE: COUNTED IN EVERY RUN"),
              (265, 890, y2 - 22, y2 + H + 36, "LONG-LIVED: BUILDS UP ON THE DIE OVER MONTHS")]
    for x0, x1, ya, yb, t in groups:
        d.add(f'<rect class="group" x="{x0}" y="{ya}" width="{x1 - x0}" height="{yb - ya}" rx="8"/>')
        d.text(x0 + 12, ya + 18 if ya < 200 else yb - 10, t, "g")
    row1 = [("Rn-222", ["3.82 d", "moves with the gas"]),
            ("Po-218", ["3.10 min", "ion: drifts to the die"]),
            ("Pb-214", ["27.1 min", "beta: small pulse"]),
            ("Bi-214", ["19.7 min", "beta: small pulse"]),
            ("Po-214", ["164 µs", "follows Bi-214 at once"])]
    row2 = [("Pb-210", ["22.2 y", "beta: small pulse"]),
            ("Bi-210", ["5.0 d", "beta: small pulse"]),
            ("Po-210", ["138 d", "growing background"]),
            ("Pb-206", ["stable", None])]
    for x, (t, sub) in zip(xs, row1):
        d.box(x, y1, W, H, t, sub)
    for x, (t, sub) in zip(xs[1:], row2):
        d.box(x, y2, W, H, t, [s for s in sub if s], cls="off" if t == "Pb-206" else "box")
    ym1, ym2 = y1 + H / 2, y2 + H / 2
    arrows1 = [("sig", "α 5.49 MeV"), ("sig", "α 6.00 MeV"), ("flow", "β"), ("flow", "β")]
    for i, (k, lab) in enumerate(arrows1):
        xa, xb = xs[i] + W, xs[i + 1]
        d.line([(xa, ym1), (xb - 2, ym1)], k)
        d.text((xa + xb) / 2, ym1 - 8, lab, "lsig" if k == "sig" else "s", "middle")
    # Po-214 down to Pb-210
    xc = xs[4] + W / 2
    d.line([(xc, y1 + H), (xc, 250), (xs[1] + W / 2, 250), (xs[1] + W / 2, y2 - 2)], "sig")
    d.text((xc + xs[1] + W / 2) / 2, 244, "α 7.69 MeV", "lsig", "middle")
    arrows2 = [("flow", "β"), ("flow", "β"), ("sig", "α 5.30 MeV")]
    for i, (k, lab) in enumerate(arrows2):
        xa, xb = xs[i + 1] + W, xs[i + 2]
        d.line([(xa, ym2), (xb - 2, ym2)], k)
        d.text((xa + xb) / 2, ym2 - 8, lab, "lsig" if k == "sig" else "s", "middle")
    d.text(20, 440, "Rn-222's own alpha reaches the die only from a few cm of gas, with energy lost on the way: "
                    "a tail below 5.49 MeV, not a line. Half-lives: IAEA LiveChart.", "s")
    legend(d, 470, ["sig", "flow"], sig="Alpha: counted when it goes into the die (about half do)",
           flow="Beta: tens of keV, can trigger, outside the alpha window")
    d.write(HERE / "decay-chain.svg")


if __name__ == "__main__":
    system_block()
    signal_chain()
    gas_train()
    decay_chain()
