"""S-03, third stage: the user's two thin-plate constructions (2026-11-22). A flat lip (theta 90) cut from
1.5 mm aluminium (waterjet; edge radius 0.5 mm after deburring) or from a laser-cut stainless stencil
(0.13 mm, VERIFY the stencil thickness ordered; edge radius 0.05 mm, nearly sharp). r_n 5.0 and 6.0 mm,
V_top 0. The sharp stencil edge needs a finer grid: h = 0.05 and 0.025 mm.

    .venv/bin/python sim/field/S-03-reduced-end/plates.py
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import run as S  # noqa: E402

CASES = [  # (name, thickness L_t, edge radius, grids)
    ("aluminium 1.5 mm", 1.5, 0.5, (0.1, 0.05)),
    ("stainless stencil 0.13 mm", 0.13, 0.05, (0.05, 0.025)),
]

if __name__ == "__main__":
    out = []
    for name, lt, edge, grids in CASES:
        for c in (1.0, 2.0):
            rn = S.CORNER + c
            for h in grids:
                S.EDGE = edge                      # build() reads the module-level edge radius
                g = S.solve_basis(rn, 90, lt, h)
                r0, z0, w = S.starts(g)
                res = S.run_point(g, 0.0, r0, z0, w, ds=min(0.05, h))
                res.update(case=name, rn=rn, lt=lt, edge=edge, h=h)
                out.append(res)
                print(f"{name:26s} r_n {rn:.1f} h {h}: active {100*res['to_active']:.1f} % index {res['index_cm3']:.1f} "
                      f"t50 {res['t_median_ms']:.0f} t90 {res['t90_ms']:.0f} ms | E lip edge {res['E_throat_edge']:.0f} "
                      f"E die {res['E_die_edge']:.0f} E cu outer {res['E_cu_outer']:.0f} V/mm", flush=True)
    (S.OUT / "plates.json").write_text(json.dumps(out, indent=1))
