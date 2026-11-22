"""Diagrams for electrometer/docs/questions/2026-11-21-electrometer.md. House style: $ELECTRONICS_TOOLS/diagrams/svgdiagram.py.

    ELECTRONICS_TOOLS=... python3 electrometer/docs/questions/diagrams/make_diagrams.py
"""
import os, sys
from pathlib import Path
if "ELECTRONICS_TOOLS" not in os.environ:
    sys.exit("ELECTRONICS_TOOLS is not set: point it at the electronics-tools repo (environment/README.md)")
sys.path.insert(0, str(Path(os.environ["ELECTRONICS_TOOLS"]) / "diagrams"))
from svgdiagram import Svg, wire, junction, res_h, gnd, cap_v

HERE = Path(__file__).resolve().parent


def opamp(d, x, y, label):
    """Op-amp triangle, inputs at (x, y - 20) minus and (x, y + 20) plus, output at (x + 80, y)."""
    d.add(f'<polygon class="box" points="{x},{y - 40} {x},{y + 40} {x + 80},{y}"/>')
    d.text(x + 6, y - 16, "−", "t"); d.text(x + 6, y + 26, "+", "t"); d.text(x + 10, y + 58, label, "s")


def cinj():
    d = Svg(680, 300, "Self-test by an injection capacitor, and the cal plug", "")
    d.box(20, 40, 120, 56, "Probe input", ["SWF probe"])
    d.box(20, 190, 120, 56, "Cal plug", ["known R to a", "known voltage"], cls="off")
    d.line([(80, 190), (80, 100)], "ctl")
    d.text(88, 150, "fitted instead of a board, to", "lctl"); d.text(88, 166, "check the resistor ranges", "lctl")
    wire(d, [(140, 68), (300, 68), (300, 130), (360, 130)])
    junction(d, 300, 130)
    d.text(306, 60, "summing node (guarded)", "s")
    opamp(d, 360, 150, "ADA4530-1")
    wire(d, [(360, 170), (340, 170), (340, 190)]); gnd(d, 340, 190)
    wire(d, [(440, 150), (520, 150)])
    d.text(526, 155, "to ADC", "s")
    wire(d, [(300, 68), (300, 30), (480, 30), (480, 150)])
    d.box(392, 18, 68, 24, "R or C_{f}")
    # injection
    d.box(160, 200, 120, 56, "MCP4821 DAC", ["RC filtered"], ctl=True)
    wire(d, [(280, 228), (300, 228)])
    cap_v(d, 300, 228, 130, "C_{inj} 1 pF", side="end")
    d.text(160, 282, "Held at 0 V while measuring: no current. A ramp gives I = C dV/dt, a step a known charge.", "s")
    d.write(HERE / "cinj.svg")


def antenna():
    d = Svg(680, 280, "Where the radio sits relative to the tin", "")
    d.add('<rect class="encl" x="20" y="30" width="400" height="220" rx="8"/>')
    d.text(32, 50, "Grounded tin: blocks 2.4 GHz (R-32)", "g")
    d.box(40, 120, 110, 60, "Head", ["fA input"])
    d.box(210, 120, 130, 60, "Control board", ["ESP32-S3-1U"], ctl=True)
    d.line([(150, 150), (210, 150)], "sig")
    d.line([(340, 150), (420, 150)], "ctl", arrow=False)
    d.add('<rect class="box" x="414" y="140" width="14" height="20"/>')
    d.text(210, 205, "u.FL coax to an SMA bulkhead", "lctl")
    d.line([(428, 150), (470, 150), (470, 80)], "ctl", arrow=False)
    d.add('<line x1="470" y1="80" x2="470" y2="60" style="stroke:var(--ctl);stroke-width:5"/>')
    d.text(480, 74, "antenna outside", "s")
    d.text(490, 110, "(a) as drawn: one coax", "s")
    d.text(490, 128, "through the wall", "s")
    d.text(440, 200, "(b) the alternative: control", "s")
    d.text(440, 218, "board outside, head signals", "s")
    d.text(440, 236, "through filtered feedthroughs", "s")
    d.write(HERE / "antenna.svg")


def power():
    d = Svg(680, 230, "Battery-only power with a charge-only input", "")
    d.box(20, 80, 130, 64, "1S2P Li-ion", ["two 18650 cells"])
    d.line([(150, 112), (220, 112)], "pwr")
    d.box(220, 84, 110, 56, "Main switch", ["fuse, protection"])
    d.line([(330, 112), (400, 112)], "pwr")
    d.box(400, 80, 150, 64, "Rails", ["3.3 V, ±5 V, ±60 V"])
    d.box(20, 170, 130, 44, "GX12 2-pin", None, cls="off")
    d.box(220, 170, 110, 44, "Charger", None)
    d.line([(150, 192), (220, 192)], "pwr")
    d.line([(275, 170), (275, 144)], "pwr")
    d.text(340, 192, "only with the main switch off: it floats while measuring", "lctl")
    d.text(20, 40, "No earth pin. The bench standard's GX12 2-pin is the charge input only (R-24, R-31).", "s")
    d.write(HERE / "power.svg")


def usb():
    d = Svg(680, 250, "A USB console during bring-up, and the loop it makes", "")
    d.add('<rect class="encl" x="20" y="40" width="300" height="170" rx="8"/>')
    d.text(32, 60, "Electrometer, floating on its battery", "g")
    d.box(40, 100, 110, 56, "Head", ["fA input"])
    d.box(180, 100, 120, 56, "ESP32-S3", ["native USB"], ctl=True)
    d.line([(150, 128), (180, 128)], "sig")
    d.line([(300, 128), (440, 128)], "ctl")
    d.text(318, 148, "USB: flash, console", "lctl")
    d.box(440, 100, 120, 56, "PC", ["mains earth"])
    d.line([(500, 156), (500, 220), (95, 220), (95, 156)], "flow", arrow=False)
    d.text(200, 238, "with USB in: the PC's ground reaches the head's common: a loop", "s")
    d.write(HERE / "usb.svg")


def budget():
    d = Svg(680, 200, "What each purchase unlocks", "")
    items = [("ADA4530-1", "the head itself", "not in stock"), ("Murata SWF probe", "in-situ measurement", "one cable"),
             ("SWF receptacles", "R-60 test ports", "16 on 4 boards, plus a test board")]
    for i, (t, s, n) in enumerate(items):
        x = 20 + 220 * i
        d.box(x, 40, 200, 56, t, [n])
        d.line([(x + 100, 96), (x + 100, 130)], "flow")
        d.box(x, 130, 200, 44, s, None, cls="group")
    d.write(HERE / "budget.svg")


if __name__ == "__main__":
    cinj(); antenna(); power(); usb(); budget()
    print("wrote", sorted(p.name for p in HERE.glob("*.svg")))
