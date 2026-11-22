"""Diagrams for docs/questions/2026-11-21-single-pd.md. House style: $ELECTRONICS_TOOLS/diagrams/svgdiagram.py.

    ELECTRONICS_TOOLS=... python3 docs/questions/diagrams/make_single_pd.py
"""
import os, sys
from pathlib import Path
if "ELECTRONICS_TOOLS" not in os.environ:
    sys.exit("ELECTRONICS_TOOLS is not set: point it at the electronics-tools repo (environment/README.md)")
sys.path.insert(0, str(Path(os.environ["ELECTRONICS_TOOLS"]) / "diagrams"))
from svgdiagram import Svg

HERE = Path(__file__).resolve().parent
EXTRA = """
  .die { fill:var(--sig); fill-opacity:.35; stroke:var(--edge); stroke-width:1.2; }
  .cu { fill:var(--ctl); stroke:none; }
  .gd { fill:var(--edge); stroke:none; }
  .fr4 { fill:var(--group); stroke:var(--edge); stroke-width:1; }
  .tube { fill:var(--pwr); fill-opacity:.25; stroke:var(--pwr); stroke-width:1.4; }
  .thr { fill:none; stroke:var(--pwr); stroke-width:1.2; }
  .ptfe { fill:var(--bg); stroke:var(--edge); stroke-width:1; stroke-dasharray:3 2; }
"""


def tube_end():
    """Half-section of the 1-1/4 in sch 40 tube end on the single-detector board, to scale in r."""
    s = 11.0                      # px per mm
    x0, yb = 40, 250              # axis x, board top y
    d = Svg(760, 400, "Single detector at the end of a 1-1/4 in tube: what V_top does", EXTRA)
    Rb, Ro, gap = 35.05 / 2, 42.16 / 2, 1.0
    rdie, cl, cu_out = 3.20, 0.3, Rb - 0.9
    X = lambda r: x0 + r * s
    d.add(f'<rect class="fr4" x="{X(0)}" y="{yb}" width="{X(Ro + 6) - X(0)}" height="{1.6 * s}"/>')
    d.add(f'<rect class="die" x="{X(0)}" y="{yb - 0.3 * s * 3}" width="{rdie * s}" height="{0.3 * s * 3}"/>')
    d.add(f'<rect class="gd" x="{X(rdie + 0.05)}" y="{yb - 3}" width="{0.2 * s}" height="3"/>')
    d.add(f'<rect class="cu" x="{X(rdie + cl)}" y="{yb - 4}" width="{(cu_out - rdie - cl) * s}" height="4"/>')
    top = 40
    d.add(f'<rect class="tube" x="{X(Rb)}" y="{top}" width="{X(Ro + 6) - X(Rb)}" height="{yb - gap * s * 3 - top}"/>')
    for k in range(9):
        y = top + 20 + k * 18
        d.add(f'<path class="thr" d="M{X(Ro) - 6},{y} l6,9 l-6,9"/>')
    d.add(f'<rect class="ptfe" x="{X(Rb + 0.2)}" y="{yb - gap * s * 3}" width="{X(Ro + 5) - X(Rb + 0.2)}" height="{gap * s * 3}"/>')
    d.line([(X(0), top - 10), (X(0), yb + 1.6 * s + 10)], "flow", arrow=False)
    d.text(X(0) + 4, top - 14, "axis", "s")
    xn = X(Ro + 6) + 30
    d.line([(X(Ro), top + 100), (xn - 6, top + 100)], "flow", arrow=False)
    d.text(xn, top + 104, "NPT thread, inside the flange: at +1 kV on both sides, no field", "s")
    d.line([(X(Rb + 3), top + 30), (xn - 6, top + 30)], "flow", arrow=False)
    d.text(xn, top + 34, "Pipe wall and flange, +1 kV", "s")
    d.line([(X(Ro + 3), yb - 1.5 * s), (xn - 6, yb - 1.5 * s)], "flow", arrow=False)
    d.text(xn, yb - 1.5 * s + 4, "PTFE washer, 1 mm (VERIFY): covers the thread seam", "s")
    d.text(xn, 60 + 120, "Top copper at V_top (orange), die at 0 V (blue):", "lctl")
    d.text(xn, 60 + 140, "200 V: 56 % of the gas volume to the active area", "s")
    d.text(xn, 60 + 158, "600 V: 76 %, but 1.7 kV/mm at the copper's inner edge", "s")
    d.text(X(0) + 4, yb + 1.6 * s + 22, "VTH2110 at 0 V (CSA input), proposed 0 V guard trace beside it", "s")
    d.text(X(0) + 4, top - 14, "axis", "s")
    d.text(X(0), 360, "Radius to scale (11 px/mm), heights exaggerated three times. Numbers: S-02, h = 0.1 mm.", "s")
    d.write(HERE / "single-pd-tube-end.svg")


if __name__ == "__main__":
    tube_end()
