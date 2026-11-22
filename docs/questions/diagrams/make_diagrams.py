"""Diagrams for docs/questions/2026-11-21-detector.md. House style: $ELECTRONICS_TOOLS/diagrams/svgdiagram.py.

    ELECTRONICS_TOOLS=... python3 docs/questions/diagrams/make_diagrams.py
"""
import os, sys
from pathlib import Path
if "ELECTRONICS_TOOLS" not in os.environ:
    sys.exit("ELECTRONICS_TOOLS is not set: point it at the electronics-tools repo (environment/README.md)")
sys.path.insert(0, str(Path(os.environ["ELECTRONICS_TOOLS"]) / "diagrams"))
from svgdiagram import Svg, legend, wire, junction, res_h, gnd, cap_v

HERE = Path(__file__).resolve().parent
EXTRA = """
  .die { fill:var(--group); stroke:var(--edge); stroke-width:1.2; }
  .act { fill:var(--sig); fill-opacity:.18; stroke:var(--sig); stroke-width:1; }
  .dead { fill:var(--ctl); fill-opacity:.28; stroke:none; }
  .ring50 { fill:none; stroke:var(--ctl); stroke-width:1.8; stroke-dasharray:5 3; }
  .tube { fill:var(--pwr); fill-opacity:.18; stroke:var(--pwr); stroke-width:1.4; }
  .bar { fill:var(--sig); fill-opacity:.75; }
  .barx { fill:var(--sig); fill-opacity:.3; }
  .hl { fill:none; stroke:var(--ctl); stroke-width:2.2; }
"""


def array_landing():
    """Top view of the 2x2 array in the 21 mm bore, with the dead cross and S-01's landing circles."""
    s = 12.0                       # px per mm
    cx, cy = 200, 190
    d = Svg(680, 380, "Where ions land on the photodiode array", EXTRA)
    d.add(f'<circle class="tube" cx="{cx}" cy="{cy}" r="{13.335 * s}"/>')
    d.add(f'<circle cx="{cx}" cy="{cy}" r="{10.5 * s}" style="fill:var(--bg);stroke:var(--pwr);stroke-width:1.4"/>')
    die, gap, act = 5.67, 0.5, 5.0
    for sx in (-1, 1):
        for sy in (-1, 1):
            x0 = cx + (gap / 2 * s if sx > 0 else -(gap / 2 + die) * s)
            y0 = cy + (gap / 2 * s if sy > 0 else -(gap / 2 + die) * s)
            d.add(f'<rect class="die" x="{x0}" y="{y0}" width="{die * s}" height="{die * s}"/>')
            b = (die - act) / 2 * s
            d.add(f'<rect class="act" x="{x0 + b}" y="{y0 + b}" width="{act * s}" height="{act * s}"/>')
    a = 0.585 * s
    half = (die + gap / 2) * s
    d.add(f'<rect class="dead" x="{cx - a}" y="{cy - half}" width="{2 * a}" height="{2 * half}"/>')
    d.add(f'<rect class="dead" x="{cx - half}" y="{cy - a}" width="{2 * half}" height="{2 * a}"/>')
    d.add(f'<circle class="ring50" cx="{cx}" cy="{cy}" r="{1.0 * s}"/>')
    d.add(f'<circle class="ring50" cx="{cx}" cy="{cy}" r="{3.5 * s}"/>')
    x = 395
    d.text(x, 60, "Top view, 21 mm bore", "t")
    d.add(f'<rect class="act" x="{x}" y="88" width="18" height="14"/>'); d.text(x + 26, 100, "active area, 5 × 5 mm per die")
    d.add(f'<rect class="die" x="{x}" y="114" width="18" height="14"/>'); d.text(x + 26, 126, "inactive die border, 0.335 mm")
    d.add(f'<rect class="dead" x="{x}" y="140" width="18" height="14"/>'); d.text(x + 26, 152, "dead cross: gaps plus borders")
    d.add(f'<line class="ring50" x1="{x}" y1="173" x2="{x + 18}" y2="173"/>'); d.text(x + 26, 177, "S-01 landing radius:")
    d.text(x + 26, 195, "half the ions inside 1 mm,")
    d.text(x + 26, 213, "80 % inside 3.5 mm")
    d.text(x, 250, "About two-thirds of the ions that reach", "s")
    d.text(x, 268, "the array land in the dead cross", "s")
    d.text(x, 286, "(axisymmetric estimate).", "s")
    d.write(HERE / "array-landing.svg")


def premium_noise():
    """Electronic FWHM at 4 us per op-amp against R-09's 100 keV."""
    d = Svg(640, 300, "Electronic peak width per CSA op-amp against the resolution target", EXTRA)
    x0, y0, s = 150, 50, 4.2           # px per keV
    rows = [("OPA140 (low-cost)", 6.9, 7.4), ("LMP7721 (premium)", 6.8, 7.3), ("OPA656", 6.0, 6.5),
            ("ADA4817-1", 4.0, 4.7), ("OPA657", 5.1, 5.7)]
    for i, (name, lo, hi) in enumerate(rows):
        y = y0 + 34 * i
        d.text(x0 - 10, y + 13, name, "s", "end")
        d.add(f'<rect class="bar" x="{x0}" y="{y}" width="{lo * s}" height="18"/>')
        d.add(f'<rect class="barx" x="{x0 + lo * s}" y="{y}" width="{(hi - lo) * s}" height="18"/>')
        d.text(x0 + hi * s + 8, y + 13, f"{lo}–{hi} keV")
    yb = y0 + 34 * len(rows) + 4
    d.line([(x0, yb), (x0 + 100 * s, yb)], "flow", arrow=False)
    for k in (0, 25, 50, 75, 100):
        d.line([(x0 + k * s, yb), (x0 + k * s, yb + 5)], "flow", arrow=False)
        d.text(x0 + k * s, yb + 18, f"{k}", "s", "middle")
    d.text(x0 + 50 * s, yb + 36, "keV FWHM at 4 µs (sim/analytic/enc_budget.out.txt)", "s", "middle")
    d.line([(x0 + 100 * s, y0 - 14), (x0 + 100 * s, yb)], "ctl", arrow=False)
    d.text(x0 + 100 * s - 6, y0 - 20, "R-09: 100 keV total", "lctl", "end")
    d.write(HERE / "premium-noise.svg")


def hv_series():
    """HV board output, feedback divider, series resistor, tube; the flashover path."""
    d = Svg(700, 270, "HV output with the series resistor and the readback divider", EXTRA)
    d.box(20, 70, 130, 70, "HV board", ["48 V in, about +1 kV", "PWM, multiplier"])
    wire(d, [(150, 105), (230, 105)])
    junction(d, 230, 105)
    # divider down from the junction
    d.add('<rect class="box" x="222" y="125" width="16" height="44" rx="2"/>')
    d.text(246, 152, "100 MΩ")
    wire(d, [(230, 105), (230, 125)]); wire(d, [(230, 169), (230, 185)])
    junction(d, 230, 185)
    d.add('<rect class="box" x="222" y="195" width="16" height="30" rx="2"/>')
    d.text(246, 214, "100 kΩ")
    wire(d, [(230, 185), (230, 195)]); wire(d, [(230, 225), (230, 236)]); gnd(d, 230, 236)
    d.line([(230, 185), (150, 185), (150, 150)], "sig")
    d.text(30, 202, "1 V per kV: feedback,", "lsig"); d.text(30, 218, "MCU ADC, test point", "lsig")
    res_h(d, 300, 105, "R_{S} ≥ 10 MΩ (A-21)", 70)
    wire(d, [(230, 105), (300, 105)]); wire(d, [(370, 105), (450, 105)])
    d.add('<rect class="tube" x="450" y="70" width="150" height="70" rx="6"/>')
    d.text(525, 100, "Chamber tube", "t", "middle"); d.text(525, 118, "pA ion current", "s", "middle")
    cap_v(d, 490, 140, 200, "C_{tube} (VERIFY)", side="end"); gnd(d, 490, 200)
    d.line([(580, 140), (620, 200)], "ctl")
    d.text(560, 222, "flashover to a diode", "lctl"); d.text(560, 238, "or probe: ≤ 100 µA", "lctl")
    d.write(HERE / "hv-series.svg")


def run_record():
    """Q-02: what each run records, and where it comes from."""
    d = Svg(660, 250, "What each run records", EXTRA)
    d.box(250, 90, 160, 70, "Run record", ["one line per run", "in the host log"])
    items_l = [("MCU board", "time, HV readback, PD bias"), ("Operator", "air or N₂, flow or static, valves")]
    items_r = [("Room sensors", "T, RH, pressure (start, end)"), ("Boards", "serials, channels fitted")]
    for i, (t, s) in enumerate(items_l):
        y = 40 + 110 * i
        d.box(20, y, 190, 56, t, s)
        d.line([(210, y + 28), (250, 125)], "flow")
    for i, (t, s) in enumerate(items_r):
        y = 40 + 110 * i
        d.box(450, y, 190, 56, t, s)
        d.line([(450, y + 28), (410, 125)], "flow")
    d.write(HERE / "run-record.svg")


def gas_sources():
    """Q-17: the gas train with the parts to source marked."""
    d = Svg(700, 170, "Gas train parts to source", EXTRA)
    names = [("Sample", None), ("Filter", "PTFE 0.2 µm"), ("Desiccant", "Drierite"), ("Filter", "PTFE 0.2 µm"),
             ("Chamber", "2 ball valves"), ("Filter", "PTFE 0.2 µm"), ("Pump", None)]
    x = 14
    for i, (t, s) in enumerate(names):
        w = 86
        d.box(x, 50, w, 56, t, s)
        if t in ("Filter", "Desiccant"):
            d.add(f'<rect class="hl" x="{x - 4}" y="46" width="{w + 8}" height="64" rx="8"/>')
        if i < len(names) - 1:
            d.line([(x + w, 78), (x + w + 14, 78)], "flow")
        x += w + 14
    d.text(14, 140, "Outlined: the parts Q-17 asks about (D-02, D-13, D-25). One filter type at every port.", "s")
    d.write(HERE / "gas-sources.svg")


def oring_land():
    """Q-20: section through the tube end on the board, zoomed on the edge, with S-01's dimensions."""
    s = 36.0                            # px per mm, to scale
    r0 = 6.0                            # left edge of the view, mm from the axis
    d = Svg(680, 330, "Tube end on the detector board", EXTRA)
    X = lambda r: 30 + (r - r0) * s
    Y = lambda z: 230 - z * s
    d.add(f'<rect class="die" x="{X(r0)}" y="{Y(0)}" width="{X(14.5) - X(r0)}" height="{1.6 * s}"/>')
    d.text(X(6.2), Y(-0.9), "FR4 board, 1.6 mm, back copper 0 V")
    d.add(f'<rect class="act" x="{X(r0)}" y="{Y(0.3)}" width="{(8.37 - r0) * s}" height="{0.3 * s}"/>')
    d.add(f'<rect x="{X(8.67)}" y="{Y(0) - 4}" width="{0.93 * s}" height="6" style="fill:var(--pwr)"/>')
    d.add(f'<path class="tube" d="M{X(10.5)},{Y(5.2)} L{X(10.5)},{Y(1.5)} Q{X(10.5)},{Y(1.0)} {X(11.0)},{Y(1.0)} '
          f'L{X(12.835)},{Y(1.0)} Q{X(13.335)},{Y(1.0)} {X(13.335)},{Y(1.5)} L{X(13.335)},{Y(5.2)} Z"/>')
    d.add(f'<circle cx="{X(11.9)}" cy="{Y(0.5)}" r="{0.5 * s}" style="fill:var(--ink2)"/>')
    # labels with leaders
    d.text(X(6.2), Y(4.6), "dies to 8.37 mm (diagonal)", "lsig")
    d.line([(X(6.4), Y(4.35)), (X(6.4), Y(0.35))], "sig")
    d.text(X(6.6), Y(3.6), "ring on +20 V, 8.67–9.6 mm", "lpwr")
    d.line([(X(8.6), Y(3.4)), (X(9.1), Y(0.15))], "pwr")
    d.text(X(10.6), Y(5.5), "tube, +1 kV", "s")
    d.text(X(13.6), Y(4.2), "edges broken", "lctl"); d.text(X(13.6), Y(3.75), "to 0.5 mm radius", "lctl")
    d.line([(X(13.55), Y(3.6)), (X(13.25), Y(1.25))], "ctl")
    d.text(X(13.6), Y(2.2), "O-ring on bare", "s"); d.text(X(13.6), Y(1.75), "laminate, 1–2 mm", "s")
    d.text(X(13.6), Y(1.3), "compressed (VERIFY)", "s")
    d.text(X(6.2), Y(-1.55) + 34, "To scale, 36 px per mm. The 2.1 mm die-to-wall gap and 0.9 mm ring-to-wall gap are S-01's.", "s")
    d.write(HERE / "oring-land.svg")


if __name__ == "__main__":
    array_landing(); premium_noise(); hv_series(); run_record(); gas_sources(); oring_land()
    print("wrote", sorted(p.name for p in HERE.glob("*.svg")))
