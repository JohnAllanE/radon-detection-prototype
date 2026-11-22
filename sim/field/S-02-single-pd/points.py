"""S-02, second stage: three representative points from the sweep. Field-line plots, the fields at the
die edge, copper edges, tube edge and thread seam at h = 0.05 mm, and the side and diagonal sections
of the square die as bounds on the equal-area disk the sweep uses.

    .venv/bin/python sim/field/S-02-single-pd/points.py
"""
import json
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import run as S  # noqa: E402

# (nominal, schedule, V_top, why)
POINTS = [
    ("3/4", "40S", 20.0, "today's tube, PD bias"),
    ("1-1/4", "40S", 200.0, "recommended"),
    ("1-1/2", "40S", 600.0, "sweep corner"),
]

if __name__ == "__main__":
    pipes = {(p["nominal"], p["schedule"]): p for p in S.pipes()}
    out = []
    fig, axs = plt.subplots(1, 3, figsize=(13, 6.2))
    for ax, (nom, sch, vt, why) in zip(axs, POINTS):
        p = pipes[(nom, sch)]
        for sec, rd in S.SECTIONS.items():
            for h in ((0.1, 0.05) if sec == "equal area" else (0.05,)):
                g = S.solve_basis(p, h, rd)
                r0, z0, w = S.starts(g)
                res = S.run_point(g, vt, r0, z0, w, ds=0.05)
                res.update(nominal=nom, schedule=sch, id_mm=p["id_mm"], section=sec, h=h, why=why)
                out.append(res)
                print(f"{nom} {sch} {vt:.0f} V {sec:10s} h={h}: die {res['to_die']:.3f} active {res['to_active']:.3f} "
                      f"cu {res['to_copper']:.3f} ne {res['not_ended']:.3f} | E die {res['E_die_edge']:.0f} "
                      f"cu_in {res.get('E_cu_inner', 0):.0f} cu_out {res.get('E_cu_outer', 0):.0f} "
                      f"tube {res['E_tube_edge']:.0f} seam {res['E_thread_seam_gap']:.0f} "
                      f"Vdrop(thread root) {res['V_drop_at_thread_root']:.2g}", flush=True)
                if sec == "equal area" and h == 0.05:
                    S.fieldline_plot(ax, g, vt, f"{nom} in {sch}, ID {p['id_mm']:.1f} mm, V_top {vt:.0f} V\n"
                                     f"{why}: {100 * res['to_active']:.0f} % to the active area")
    leg = [Line2D([], [], color=c, lw=1.4, label=l) for c, l in
           (("#2a78d6", "ends on the active area"), ("#7fb0e8", "ends on the die's edge region"),
            ("#8e44ad", "ends on the V_top copper"), ("#898781", "ends on bare FR4"),
            ("#000000", "does not end (field-free middle)"))]
    fig.legend(handles=leg, loc="lower center", ncol=5, fontsize=8, frameon=False)
    fig.suptitle("S-02: field lines (positive-ion paths), equipotentials every 50 V; tube and flange +1 kV, die 0 V",
                 fontsize=10)
    fig.tight_layout(rect=(0, 0.05, 1, 0.95)); fig.savefig(S.OUT / "fieldlines-points.svg"); plt.close(fig)
    (S.OUT / "points.json").write_text(json.dumps(out, indent=1))
