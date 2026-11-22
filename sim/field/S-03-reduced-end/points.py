"""S-03, second stage: chosen geometries at h = 0.05 mm, with the die's side and diagonal sections as
bounds on the equal-area disk, and field-line plots.

    .venv/bin/python sim/field/S-03-reduced-end/points.py
"""
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import run as S  # noqa: E402
SECTIONS = S.SECTIONS   # S-02's: equal area, side, diagonal

# (r_n clearance to the die corner, theta, L_t, V_top, why)
POINTS = [
    (1.0, 45, 1.0, 0.0, "as sketched"),
    (1.0, 90, 0.5, 0.0, "best index: flat step, short throat"),
    (2.0, 90, 1.0, 0.0, "wider mouth, faster"),
    (None, 90, 1.0, 0.0, "no reduction (reference)"),
]

if __name__ == "__main__":
    out = []
    fig, axs = plt.subplots(1, len(POINTS), figsize=(15, 7.2))
    for ax, (c, th, lt, vt, why) in zip(axs, POINTS):
        rn = S.RB if c is None else S.CORNER + c
        for sec, rd in SECTIONS.items():
            for h in ((0.1, 0.05) if sec == "equal area" else (0.05,)):
                g = S.solve_basis(rn, th, lt, h, rd)
                r0, z0, w = S.starts(g)
                res = S.run_point(g, vt, r0, z0, w, ds=0.05)
                res.update(rn=rn, theta=th, lt=lt, section=sec, h=h, why=why)
                out.append(res)
                print(f"r_n {rn:5.2f} θ {th} L_t {lt} {vt:.0f} V {sec:10s} h={h}: active {res['to_active']:.3f} "
                      f"index {res['index_cm3']:.1f} t50 {res['t_median_ms']:.0f} t90 {res['t90_ms']:.0f} | "
                      f"E die {res['E_die_edge']:.0f} cu_in {res['E_cu_inner']:.0f} cu_out {res['E_cu_outer']:.0f} "
                      f"throat {res['E_throat_edge']:.0f} join {res['E_join']:.0f}", flush=True)
                if sec == "equal area" and h == 0.05:
                    S.fieldline_plot(ax, g, vt, f"{why}\nr_n {rn:.1f}, θ {th}°, L_t {lt:g}, V_top {vt:.0f} V\n"
                                     f"{100 * res['to_active']:.0f} % to active, median {res['t_median_ms']:.0f} ms")
    leg = [Line2D([], [], color=c, lw=1.4, label=l) for c, l in
           (("#2a78d6", "ends on the active area"), ("#7fb0e8", "ends on the die's edge region"),
            ("#d95926", "ends on the V_top copper"), ("#898781", "ends on bare FR4"),
            ("#000000", "does not end"))]
    fig.legend(handles=leg, loc="lower center", ncol=5, fontsize=8, frameon=False)
    fig.suptitle("S-03: field lines (positive-ion paths). Equipotentials: 100–800 V every 100 V (light), "
                 "900, 950, 980, 990, 995, 999 V (darker); tube +1 kV, die 0 V", fontsize=10)
    fig.tight_layout(rect=(0, 0.05, 1, 0.95)); fig.savefig(S.OUT / "fieldlines-points.svg"); plt.close(fig)
    (S.OUT / "points.json").write_text(json.dumps(out, indent=1))
