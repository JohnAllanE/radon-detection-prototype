"""General-arrangement sketch for S-03 (aluminium tube with a machined reduced end). House style:
$ELECTRONICS_TOOLS/diagrams/svgdiagram.py.

    ELECTRONICS_TOOLS=... python3 sim/field/S-03-reduced-end/sketch.py
"""
import math
import os
import sys
from pathlib import Path

if "ELECTRONICS_TOOLS" not in os.environ:
    sys.exit("ELECTRONICS_TOOLS is not set: point it at the electronics-tools repo (environment/README.md)")
sys.path.insert(0, str(Path(os.environ["ELECTRONICS_TOOLS"]) / "diagrams"))
from svgdiagram import Svg

HERE = Path(__file__).resolve().parent
EXTRA = """
  .die { fill:var(--sig); fill-opacity:.45; stroke:var(--sig); stroke-width:1; }
  .cu { fill:var(--ctl); stroke:none; }
  .fr4 { fill:var(--group); stroke:var(--edge); stroke-width:1; }
  .al { fill:var(--pwr); fill-opacity:.22; stroke:var(--pwr); stroke-width:1.4; }
  .ptfe { fill:var(--bg); stroke:var(--edge); stroke-width:1; stroke-dasharray:3 2; }
  .scr { fill:var(--edge); fill-opacity:.35; stroke:var(--edge); stroke-width:1; }
  .dim { fill:none; stroke:var(--ink2); stroke-width:1; }
  .axis { fill:none; stroke:var(--ink2); stroke-width:1; stroke-dasharray:10 3 2 3; }
  .sym { fill:none; stroke:var(--ink2); stroke-width:1; stroke-dasharray:5 4; }
  .bore { fill:none; stroke:var(--ink2); stroke-width:1.2; stroke-dasharray:4 3; }
  .sq { fill:var(--pwr); fill-opacity:.12; stroke:var(--pwr); stroke-width:1.4; }
"""

# Nominal geometry (mm). Swept parameters marked "sweep" are drawn at a mid value.
RB = 35.05 / 2      # main bore radius: 1-1/4 in sch 40 ID, as S-02
RO = 50.8 / 2       # tube and bar OD 2 in (VERIFY: stock size)
RN = 5.0            # reduced bore radius (sweep): die corner 4.01 + 1 mm
G = 1.0             # PTFE washer: end-piece face above the board
LT = 1.0            # straight throat length (sweep)
TH = 45.0           # taper half-angle from the axis (sweep)
LC = (RB - RN) / math.tan(math.radians(TH))   # taper length
ZJ = G + LT + LC    # height of the join between end piece and tube
ZS = 38.0           # symmetry plane: middle of a 76 mm tube (A-23), as S-02
DIE, DT = 5.67 / 2, 0.30
RBC = 22.0          # bolt circle radius (schematic)

S = 9.0             # px per mm, both axes: to scale
XC, YB = 400, 470   # axis x, board top y (main section)
XL = 700            # labels column
DX0, DY0, DK = 1075, 255, 26.0   # detail view: axis x, board top y, px per mm


def X(r):
    return XC + r * S


def Y(z):
    return YB - z * S


def dX(r):
    return DX0 + r * DK


def dY(z):
    return DY0 - z * DK


def poly(d, pts, cls, fx=X, fy=Y):
    d.add(f'<polygon class="{cls}" points="{" ".join(f"{fx(r):.1f},{fy(z):.1f}" for r, z in pts)}"/>')


def rect(d, r0, z0, r1, z1, cls, fx=X, fy=Y):
    x0, x1 = sorted((fx(r0), fx(r1)))
    y0, y1 = sorted((fy(z0), fy(z1)))
    d.add(f'<rect class="{cls}" x="{x0:.1f}" y="{y0:.1f}" width="{x1 - x0:.1f}" height="{y1 - y0:.1f}"/>')


def taper_r(z):
    """Bore radius of the end piece at height z."""
    if z <= G + LT:
        return RN
    return min(RB, RN + (z - G - LT) * math.tan(math.radians(TH)))


def section(d):
    ztop = ZS + 4
    for sg in (1, -1):
        rect(d, 0, -1.6, sg * (RO + 2), 0, "fr4")
        rect(d, sg * (DIE + 0.3), 0, sg * (RN - 0.3), 0.12, "cu")
        rect(d, sg * (RN + 0.2), 0, sg * RO, G, "ptfe")
        poly(d, [(sg * RN, G), (sg * RO, G), (sg * RO, ZJ), (sg * RB, ZJ), (sg * RN, G + LT)], "al")
        poly(d, [(sg * RB, ZJ), (sg * RO, ZJ), (sg * RO, ztop), (sg * RB, ztop)], "al")
        rect(d, sg * (RBC - 2.6), G, sg * (RBC + 2.6), G + 3.0, "scr")
        rect(d, sg * (RBC - 1.5), G + 3.0, sg * (RBC + 1.5), ZJ + 8, "scr")
        r0, r1 = sg * RB, sg * RO
        d.add(f'<path class="dim" d="M{X(r0)},{Y(ztop)} L{X((r0 + r1) / 2) - 4},{Y(ztop) - 5} '
              f'L{X((r0 + r1) / 2) + 4},{Y(ztop) + 5} L{X(r1)},{Y(ztop)}"/>')
    rect(d, -DIE, 0, DIE, DT, "die")
    d.add(f'<line class="axis" x1="{X(0)}" y1="{Y(ztop + 2)}" x2="{X(0)}" y2="{Y(-4)}"/>')
    d.text(X(0) + 4, Y(ztop + 2) + 2, "axis", "s")
    d.add(f'<line class="sym" x1="{X(-RO - 3)}" y1="{Y(ZS)}" x2="{X(RO + 3)}" y2="{Y(ZS)}"/>')
    # box marking the detail view
    rect(d, -1, -2.2, 9.5, 5, "encl")
    d.text(X(9.5) + 4, Y(-2.2) + 14, "detail", "s")
    # dimensions, left half
    d.line([(X(0), Y(ZS - 6)), (X(-RB), Y(ZS - 6))], "flow", arrow=True, start_arrow=True)
    d.text(X(-RB / 2), Y(ZS - 6) - 6, "R_{b} 17.5, fixed", "s", "middle")
    xv = X(-RO - 2.5)

    def vdim(z0, z1, a, b):
        d.line([(xv, Y(z0)), (xv, Y(z1))], "flow", arrow=True, start_arrow=True)
        ym = (Y(z0) + Y(z1)) / 2
        d.text(xv - 6, ym - 3, a, "s", "end")
        d.text(xv - 6, ym + 12, b, "s", "end")

    vdim(G + LT, ZJ, "taper", "12.5 at θ 45°")
    vdim(ZJ, ZS, "board to", "symmetry plane 38")


def labels(d):
    def lead(r, z, ytxt, lines):
        d.line([(X(r), Y(z)), (XL - 6, ytxt - 4)], "flow", arrow=False)
        for i, (t, c) in enumerate(lines):
            d.text(XL, ytxt + 15 * i, t, c)

    lead(0.5, ZS, 78, [("Symmetry plane: middle of a 76 mm tube", "s"),
                       ("between two boards, as S-02", "s")])
    lead(RB + 2.5, ZS - 4, 140, [("Main tube, +1 kV", "lpwr"),
                                 ("Thick-wall aluminium, ID 35.05 (1-1/4 in", "s"),
                                 ("sch 40, as S-02), OD 2 in (VERIFY stock)", "s")])
    lead(RBC + 1.5, ZJ + 6, 222, [("Axial screws into tapped holes in the tube", "s"),
                                  ("wall, heads in counterbores in the end-piece", "s"),
                                  ("face (positions schematic)", "s")])
    lead(RO, ZJ, 290, [("Join: face to face, both pieces at +1 kV", "s"),
                       ("(seals not drawn)", "s")])
    lead(RN + 8, G + 5, 362, [("End piece from solid bar, +1 kV", "lpwr"),
                              ("Reduced bore r_{n} with a straight throat L_{t},", "s"),
                              ("then a taper at θ up to the main bore", "s")])
    lead(RO - 1, -0.8, 440, [("Detector board on a 1 mm PTFE washer", "s"),
                             ("(VERIFY, as S-02): details at right", "s")])


def detail(d):
    rmax, zmax = 9.0, 4.6
    d.text(dX(4), dY(zmax) - 30, "Detail at the die (26 px/mm)", "g", "middle")
    rect(d, -1, -1.6, rmax, 0, "fr4", dX, dY)
    rect(d, DIE + 0.3, 0, RN - 0.3, 0.06, "cu", dX, dY)
    rect(d, -1, 0, DIE, DT, "die", dX, dY)
    rect(d, RN + 0.2, 0, rmax, G, "ptfe", dX, dY)
    poly(d, [(RN, G), (rmax, G), (rmax, zmax), (taper_r(zmax), zmax), (RN, G + LT)], "al", dX, dY)
    d.add(f'<line class="axis" x1="{dX(0)}" y1="{dY(zmax + 0.6)}" x2="{dX(0)}" y2="{dY(-2.2)}"/>')
    # r_n
    zr = zmax - 0.5
    d.line([(dX(0), dY(zr)), (dX(RN), dY(zr))], "flow", arrow=True, start_arrow=True)
    d.text(dX(RN / 2), dY(zr) - 6, "r_{n} (sweep)", "s", "middle")
    # throat length and washer gap, right of the bore wall
    def vd(z0, z1, xr, label):
        d.line([(dX(xr), dY(z0)), (dX(xr), dY(z1))], "flow", arrow=False)
        for z in (z0, z1):
            d.add(f'<line class="dim" x1="{dX(xr) - 4}" y1="{dY(z)}" x2="{dX(xr) + 4}" y2="{dY(z)}"/>')
        d.text(dX(xr) - 6, (dY(z0) + dY(z1)) / 2 + 4, label, "s", "end")
    vd(G, G + LT, RN - 0.45, "L_{t} (sweep)")
    vd(0, G, RN - 0.15, "g 1.0")
    # theta arc at the throat top
    rc, zc, rr = RN, G + LT, 2.0
    a = math.radians(TH)
    d.add(f'<line class="dim" x1="{dX(rc)}" y1="{dY(zc)}" x2="{dX(rc)}" y2="{dY(zc + rr + 0.3)}"/>')
    p1 = (dX(rc), dY(zc + rr))
    p2 = (dX(rc + rr * math.sin(a)), dY(zc + rr * math.cos(a)))
    d.add(f'<path class="dim" d="M{p1[0]:.1f},{p1[1]:.1f} A{rr * DK},{rr * DK} 0 0 1 {p2[0]:.1f},{p2[1]:.1f}"/>')
    d.text(dX(rc + 0.55), dY(zc + 2.7), "θ", "s", "middle")
    d.text(dX(7.4), dY(1.5), "end piece", "lpwr", "middle")
    d.text(dX(7.2), dY(0.5) + 4, "PTFE", "s", "middle")
    # labels under the detail
    yl = dY(-1.6) + 22
    d.text(dX(-1), yl, "Blue: VTH2110 at 0 V (CSA input), side section", "lsig")
    d.text(dX(-1), yl + 16, "Orange: exposed board copper at V_{top}, 0 V", "lctl")
    d.text(dX(-1), yl + 32, "or modest (sweep 0, 20, 100, 200 V)", "lctl")


def topview(d):
    k = 9.0
    cx, cy = dX(0.2), 505
    sq = DIE + 1.0
    d.text(dX(4), cy - 72, "Throat from above (9 px/mm)", "g", "middle")
    d.add(f'<circle class="bore" cx="{cx}" cy="{cy}" r="{RN * k}"/>')
    d.add(f'<rect class="sq" x="{cx - sq * k}" y="{cy - sq * k}" width="{2 * sq * k}" height="{2 * sq * k}" '
          f'rx="{1.5 * k}"/>')
    d.add(f'<rect class="die" x="{cx - DIE * k}" y="{cy - DIE * k}" width="{2 * DIE * k}" height="{2 * DIE * k}"/>')
    x2 = cx + RN * k + 14
    for i, t in enumerate(["Dashed: round bore r_{n} (modelled)", "Purple: rounded square with",
                           "1 mm clearance, the optional", "CNC loft. Not modelled: the die's",
                           "side and diagonal sections", "bracket it, as in S-02"]):
        d.text(x2, cy - 38 + 15 * i, t, "s")


def main():
    d = Svg(1340, 600, "S-03 general arrangement: tube with a reduced, tapered end over one photodiode", EXTRA)
    section(d)
    labels(d)
    detail(d)
    topview(d)
    d.text(40, 582, "Full section through the axis, to scale on both axes (9 px/mm); the model is axisymmetric "
                    "(one half). Drawn at r_{n} 5.0, L_{t} 1.0, θ 45°. Dimensions in mm.", "s")
    d.write(HERE / "arrangement.svg")


if __name__ == "__main__":
    main()
