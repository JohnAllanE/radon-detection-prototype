"""S-01 solver checks against analytic answers (run before trusting run.py).

1. Coaxial: inner rod r <= a at V0, outer cylinder r >= b at 0, long (Neumann ends):
   V(r) = V0 ln(b/r) / ln(b/a). Checks the radial (1/r) terms.
2. Parallel plates with a dielectric layer: plate at z = d1 + d2 at V0, plate at z = 0 at 0 V,
   slab eps_r over 0..d1 (Neumann sides). Gas field E_gas = V0 / (d2 + d1/eps_r). Checks the
   permittivity faces and the axis node.
    .venv/bin/python sim/field/S-01-chamber/verify.py
"""
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent))
from field import Grid

out = []
for h in (0.1, 0.05):
    a, b, V0 = 1.0, 10.0, 1000.0
    g = Grid(b, 0.0, 2.0, h)
    g.set_conductor(g.R <= a + 1e-9, V0, 4)
    g.set_conductor(g.R >= b - 1e-9, 0.0, 3)
    g.solve()
    rr = g.r[(g.r > a) & (g.r < b)]
    exact = V0 * np.log(b / rr) / np.log(b / a)
    num = g.V[(g.r > a) & (g.r < b), g.shape[1] // 2]
    err = np.max(np.abs(num - exact))
    out.append(f"coax h = {h} mm: max |V - exact| = {err:.3f} V of {V0:.0f} V ({100 * err / V0:.3f} %)")

    d1, d2, er = 1.6, 3.0, 4.4
    g = Grid(5.0, 0.0, d1 + d2, h)
    g.eps[g.Z < d1 - 1e-9] = er
    g.set_conductor(np.isclose(g.Z, 0.0), 0.0, 3)
    g.set_conductor(np.isclose(g.Z, d1 + d2), V0, 4)
    g.solve()
    Egas = V0 / (d2 + d1 / er)
    zz = g.z
    jm = np.argmin(np.abs(zz - (d1 + d2 / 2)))
    num = -(g.V[:, jm + 1] - g.V[:, jm - 1]) / (2 * h)
    out.append(f"slab h = {h} mm: E_gas = {abs(num).mean():.2f} V/mm (axis {abs(num[0]):.2f}), exact {Egas:.2f} V/mm")
txt = "\n".join(out)
print(txt)
(Path(__file__).resolve().parent / "results" / "verify.out.txt").write_text(txt + "\n")
