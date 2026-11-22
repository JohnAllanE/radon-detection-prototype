"""S-03: one VTH2110 under an aluminium tube (ID 35.05 mm, as S-02's 1-1/4 in sch 40) whose end piece
reduces the bore to r_n over the die, with a straight throat L_t and a taper at half-angle theta up to
the main bore. Both pieces at +1 kV. Sweep theta and V_top (the exposed board copper inside r_n), at a
few small r_n. Geometry: sketch.py / arrangement.svg. Solver: ../S-01-chamber/field.py, unchanged.

    .venv/bin/python sim/field/S-03-reduced-end/run.py           # sweep at h = 0.1 mm, plots, summary
    .venv/bin/python sim/field/S-03-reduced-end/run.py --quick   # one geometry
    .venv/bin/python sim/field/S-03-reduced-end/run.py --plots   # redraw from sweep.json

Superposition as S-02: per geometry, one solve with the tube at 1 V and one with the copper at 1 V.
"""
import json
import math
import sys
import time
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "S-01-chamber"))
from field import Grid, trace  # noqa: E402
import importlib.util  # noqa: E402
_spec = importlib.util.spec_from_file_location("s02_run", HERE.parent / "S-02-single-pd" / "run.py")
S02 = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(S02)   # S-02's run.py, by its own name
active_share, SECTIONS = S02.active_share, S02.SECTIONS
DIE, DIE_T, R_DIE, V_TUBE, GAP, EDGE = S02.DIE, S02.DIE_T, S02.R_DIE, S02.V_TUBE, S02.GAP, S02.EDGE
CLEAR, BOARD_T, EPS, ZMAX, MU = S02.CLEAR, S02.BOARD_T, S02.EPS, S02.ZMAX, S02.MU

OUT = HERE / "results"
OUT.mkdir(exist_ok=True)
plt.rcParams.update({"svg.fonttype": "none", "font.size": 9, "font.family": "sans-serif"})

RB = 35.05 / 2            # main bore: 1-1/4 in sch 40 ID, as S-02
RO = 50.8 / 2             # 2 in OD bar and tube, VERIFY stock
LTS = [0.5, 1.0, 2.0, 4.0, 8.0]           # straight throat length L_t (0.5 = the edge radius alone)
CU_IN = 0.3               # exposed copper stops 0.3 mm inside the reduced bore
CORNER = DIE / math.sqrt(2)               # 4.01 mm: a round bore must clear the die's corner
RNS = [CORNER + c for c in (0.5, 1.0, 2.0, 4.0)]   # 4.5, 5.0, 6.0, 8.0 mm
THETAS = [20, 30, 45, 60, 75, 90]          # taper half-angle from the axis; 90 = flat plate with a hole
V_TOPS = [0.0, 20.0, 50.0, 100.0, 200.0]
S02_REF = dict(to_active=0.555, index_cm3=20.4, V_top=200.0)   # S-02 build point, README


def bore(z, rn, th, lt):
    """Bore radius of the metal at height z (above the washer)."""
    if th >= 90:
        return np.where(z < GAP + lt, rn, RB)
    return np.clip(rn + (z - GAP - lt) * math.tan(math.radians(th)), rn, RB)


def build(rn, th, lt, h, r_die=R_DIE):
    g = Grid(RO + 1.0, -BOARD_T, ZMAX, h)
    R, Z = g.R, g.Z
    e = 1e-9
    g.eps[Z < -e] = EPS
    g.set_conductor(Z <= -BOARD_T + e, 0.0, 3)
    metal = (Z >= GAP - e) & (R >= bore(Z, rn, th, lt) - e)
    rho = EDGE                                        # 0.5 mm radius on the throat's lower inner edge
    cut = (R < rn + rho) & (Z < GAP + rho) & (np.hypot(R - rn - rho, Z - GAP - rho) > rho)
    metal &= ~cut
    g.set_conductor(metal, 1.0, 4)
    g.set_conductor((R <= r_die + e) & (Z >= -e) & (Z <= DIE_T + e), 0.0, 1)
    ri, ro = r_die + CLEAR, rn - CU_IN
    g.set_conductor((R >= ri - e) & (R <= ro + e) & (np.abs(Z) <= e), 0.0, 2)
    g.rdie, g.ri, g.ro, g.rn, g.th, g.lt = r_die, ri, ro, rn, th, lt
    return g


def solve_basis(rn, th, lt, h, r_die=R_DIE):
    g = build(rn, th, lt, h, r_die)
    g.solve(); V1 = g.V.copy()
    tube = g.label == 4; cu = g.label == 2
    g.V0[tube] = 0.0; g.V0[cu] = 1.0
    g.solve(); V2 = g.V.copy()
    g.V0[tube] = 1.0; g.V0[cu] = 0.0
    g.V1, g.V2 = V1, V2
    return g


def set_vtop(g, vt):
    g.V = V_TUBE * g.V1 + vt * g.V2
    Er, Ez = np.gradient(-g.V, g.h, g.h)
    g.Er, g.Ez, g.Emag = Er, Ez, np.hypot(Er, Ez)


def starts(g, n_r=60, n_z=120):
    """Volume-weighted start points in the gas inside the bore, from just above the die to the
    symmetry plane. The washer's gap (r > r_n, z < GAP) is PTFE in reality and is left out."""
    rr = (np.arange(n_r) + 0.5) / n_r * RB
    zz = DIE_T + 0.1 + (np.arange(n_z) + 0.5) / n_z * (ZMAX - DIE_T - 0.1)
    R, Z = np.meshgrid(rr, zz, indexing="ij")
    R, Z = R.ravel(), Z.ravel()
    ok = R < np.where(Z < GAP, g.rn, bore(Z, g.rn, g.th, g.lt)) - 0.15
    i = np.clip(np.rint(R / g.h).astype(int), 0, g.shape[0] - 1)
    j = np.clip(np.rint((Z - g.z[0]) / g.h).astype(int), 0, g.shape[1] - 1)
    ok &= g.label[i, j] == 0
    dA = (rr[1] - rr[0]) * (zz[1] - zz[0])
    R, Z = R[ok], Z[ok]
    return R, Z, 2 * np.pi * R * dA                   # weights: volume in mm^3


def classify(g, lab, rend):
    lab = lab.copy()
    lab[(lab == 6) & (rend <= g.rdie)] = 1
    lab[(lab == 6) & (rend >= g.ri) & (rend <= g.ro)] = 2
    return lab


def fields(g):
    gas = (~g.fixed) & (g.Z >= -1e-9)
    near = lambda r, z, d=0.3: gas & (np.hypot(g.R - r, g.Z - z) <= d)
    return dict(E_die_edge=float(g.Emag[near(g.rdie, DIE_T)].max()),
                E_cu_inner=float(g.Emag[near(g.ri, 0.0)].max()),
                E_cu_outer=float(g.Emag[near(g.ro, 0.0)].max()),
                E_throat_edge=float(g.Emag[gas & (np.hypot(g.R - g.rn, g.Z - GAP) <= 1.0)].max()),
                E_join=_max(g.Emag[near(RB, GAP + g.lt + (RB - g.rn) / math.tan(math.radians(min(g.th, 89.99))), 1.0)]))


def _max(a):
    """None where the probe is empty: the taper reaches the main bore only beyond the symmetry plane."""
    return float(a.max()) if a.size else None


def run_point(g, vt, r0, z0, w, ds):
    set_vtop(g, vt)
    lab, rend, L, T, _ = trace(g, r0, z0, ds=ds, max_len=200)
    lab = classify(g, lab, rend)
    W = w.sum()
    pd = lab == 1
    act = np.zeros_like(rend); act[pd] = active_share(rend[pd])
    t = T[pd] / MU * 1000
    wt = w[pd]
    def wq(q):
        if not pd.any():
            return None
        o = np.argsort(t); c = np.cumsum(wt[o]) / wt.sum()
        return float(t[o][np.searchsorted(c, q)])
    res = dict(V_top=vt, gas_cm3=float(W / 1000),
               to_die=float(w[pd].sum() / W), to_active=float((w * act).sum() / W),
               to_copper=float(w[lab == 2].sum() / W), to_metal=float(w[lab == 4].sum() / W),
               to_fr4=float(w[lab == 6].sum() / W), not_ended=float(w[(lab == 7) | (lab == 8)].sum() / W),
               index_cm3=float((w * act).sum() / 1000), t_median_ms=wq(0.5), t90_ms=wq(0.9))
    res.update(fields(g))
    return res


def geometries(quick):
    if quick:
        return [(CORNER + 1.0, 45, 1.0)]
    return [(rn, th, lt) for rn in RNS for th in THETAS for lt in LTS] + [(RB, 90, 1.0)]   # last: no reduction, the reference


def sweep(h, quick):
    rows = []
    for rn, th, lt in geometries(quick):
        t0 = time.time()
        g = solve_basis(rn, th, lt, h)
        r0, z0, w = starts(g)
        for vt in V_TOPS:
            res = run_point(g, vt, r0, z0, w, ds=max(h, 0.05))
            res.update(rn=rn, clearance=rn - CORNER, theta=th, lt=lt, h=h)
            rows.append(res)
        print(f"r_n {rn:5.2f} θ {th:2d} L_t {lt:3.1f}: active " + " ".join(f"{r['to_active']:.3f}" for r in rows[-len(V_TOPS):])
              + "  index " + " ".join(f"{r['index_cm3']:.1f}" for r in rows[-len(V_TOPS):])
              + f"  t50 {rows[-len(V_TOPS)]['t_median_ms']:.0f} ms ({time.time() - t0:.0f} s)", flush=True)
    return rows


def heatmaps(rows, key, fname, title, cbar, fmt, scale=1.0, vt=0.0, cmap="Blues"):
    """Panels per r_n: theta (rows) against L_t (columns), at one V_top."""
    sel = [r for r in rows if r["rn"] < RB and r["V_top"] == vt]
    vals = [r[key] * scale for r in sel if r[key] is not None]
    vmin, vmax = min(vals), max(vals)
    fig, axs = plt.subplots(1, len(RNS), figsize=(14, 4.8), sharey=True)
    for ax, rn in zip(axs, RNS):
        M = np.array([[next(r[key] for r in sel if r["rn"] == rn and r["theta"] == th and r["lt"] == lt) * scale
                       for lt in LTS] for th in THETAS])
        m = ax.imshow(M, cmap=cmap, aspect="auto", origin="lower", vmin=vmin, vmax=vmax)
        for i in range(M.shape[0]):
            for j in range(M.shape[1]):
                dark = (M[i, j] - vmin) > 0.55 * (vmax - vmin)
                ax.text(j, i, fmt.format(M[i, j]), ha="center", va="center", fontsize=7.5,
                        color="white" if dark else "#1f1f1f")
        ax.set_xticks(range(len(LTS)), [f"{v:g}" for v in LTS])
        ax.set_yticks(range(len(THETAS)), [f"{t}°" for t in THETAS])
        ax.set_title(f"r_n {rn:.1f} mm (die corner + {rn - CORNER:.1f})", fontsize=9)
        ax.set_xlabel("Straight throat L_t (mm)")
    axs[0].set_ylabel("Taper half-angle θ (90° = flat step)")
    ref = next(r for r in rows if r["rn"] == RB and r["V_top"] == vt)
    fig.suptitle(title + f", V_top {vt:.0f} V\nNo reduction (bore 35.05 mm to the board), same model: "
                 + fmt.format(ref[key] * scale), fontsize=9.5)
    fig.colorbar(m, ax=axs, shrink=0.85, label=cbar)
    fig.savefig(OUT / fname, bbox_inches="tight"); plt.close(fig)


def tradeoff(rows, vt=0.0):
    """Index against median transit, every geometry at one V_top."""
    fig, ax = plt.subplots(figsize=(7.5, 5))
    cols = ["#2a78d6", "#3aa37a", "#d95926", "#8e44ad"]
    for rn, c in zip(RNS, cols):
        sel = [r for r in rows if r["rn"] == rn and r["V_top"] == vt]
        ax.scatter([r["t_median_ms"] for r in sel], [r["index_cm3"] for r in sel], s=[8 + 6 * r["lt"] for r in sel],
                   color=c, alpha=0.8, label=f"r_n {rn:.1f} mm")
    ref = [r for r in rows if r["rn"] == RB]
    ax.scatter([r["t_median_ms"] for r in ref], [r["index_cm3"] for r in ref], marker="x", color="k",
               label="no reduction, V_top 0–200 V")
    ax.set_xscale("log")
    ax.set_xlabel("Median transit to the die (ms), mobility 2 cm²/(V·s)")
    ax.set_ylabel("Index: gas volume to the active area (cm³)")
    ax.set_title(f"S-03: index against transit, all θ and L_t at V_top {vt:.0f} V (marker size: L_t)", fontsize=9.5)
    ax.grid(alpha=0.3); ax.legend(fontsize=8)
    fig.tight_layout(); fig.savefig(OUT / "tradeoff.svg"); plt.close(fig)


COL = {1: "#2a78d6", 2: "#d95926", 4: "#8e44ad", 6: "#898781", 7: "#000000", 8: "#000000"}


def fieldline_plot(ax, g, vt, title):
    set_vtop(g, vt)
    V = np.where(g.label == 4, np.nan, g.V)
    V = np.where(g.Z < 0, np.nan, V)
    ax.contour(g.R, g.Z, V, levels=[900, 950, 980, 990, 995, 999], colors="#b0b0b0", linewidths=0.4)
    ax.contour(g.R, g.Z, V, levels=np.arange(100, 900, 100), colors="#d0d0d0", linewidths=0.4)
    n = 22
    r0 = np.concatenate([(RB - 0.3) * np.sqrt((np.arange(n) + 0.5) / n), np.full(8, 1.0), np.full(8, 0.5 * RB)])
    z0 = np.concatenate([np.full(n, ZMAX - 0.3), np.linspace(4, ZMAX - 3, 8), np.linspace(22, ZMAX - 3, 8)])
    keep = r0 < bore(z0, g.rn, g.th, g.lt) - 0.2
    r0, z0 = r0[keep], z0[keep]
    lab, rend, L, T, paths = trace(g, r0, z0, ds=g.h / 2, max_len=200)
    lab = classify(g, lab, rend)
    act = active_share(rend)
    for pth, k, a in zip(paths, lab, act):
        pth = np.array(pth)
        c = COL.get(int(k), "#000")
        if k == 1 and a < 0.5:
            c = "#7fb0e8"
        ax.plot(pth[:, 0], pth[:, 1], color=c, lw=0.9)
    zz = np.linspace(GAP, ZMAX, 400)
    ax.fill_betweenx(zz, bore(zz, g.rn, g.th, g.lt), RO, color="#d9c7e6", ec="k", lw=0.6)
    ax.add_patch(plt.Rectangle((0, -BOARD_T), RO, BOARD_T, fc="#cfe8cf", ec="k", lw=0.6))
    ax.add_patch(plt.Rectangle((0, 0), g.rdie, DIE_T, fc="#2a78d6", ec="k", lw=0.6))
    ax.plot([g.ri, g.ro], [0, 0], color="#d95926", lw=3, solid_capstyle="butt")
    ax.set_xlim(0, RO); ax.set_ylim(-BOARD_T, ZMAX); ax.set_aspect("equal")
    ax.set_xlabel("r (mm)"); ax.set_ylabel("z (mm) above the board")
    ax.set_title(title, fontsize=8.5)


def summary(rows):
    lines = ["| r_n (mm) | Clearance to die corner (mm) | θ | L_t (mm) | V_top (V) | Gas (cm³) | To die | To active area | To copper | To metal | Not ended | Index (cm³) | Median transit (ms) | 90 % transit (ms) | E die edge | E copper inner | E copper outer | E throat edge | E join |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    f = lambda x: "–" if x is None else f"{x:.0f}"
    for r in rows:
        lines.append(f"| {r['rn']:.2f} | {r['clearance']:.1f} | {r['theta']}° | {r['lt']:.1f} | {r['V_top']:.0f} | {r['gas_cm3']:.1f} | "
                     f"{100*r['to_die']:.1f} % | {100*r['to_active']:.1f} % | {100*r['to_copper']:.1f} % | "
                     f"{100*r['to_metal']:.1f} % | {100*r['not_ended']:.1f} % | {r['index_cm3']:.1f} | "
                     f"{f(r['t_median_ms'])} | {f(r['t90_ms'])} | {r['E_die_edge']:.0f} | {r['E_cu_inner']:.0f} | "
                     f"{r['E_cu_outer']:.0f} | {r['E_throat_edge']:.0f} | {f(r['E_join'])} |")
    (OUT / "summary.md").write_text("Index: gas volume (cm³, one detector's 38 mm of tube) whose field line ends on the "
                                    "active area. Fields in V/mm at h = 0.1 mm (sharp corners grow with refinement).\n\n"
                                    + "\n".join(lines) + "\n")


if __name__ == "__main__":
    quick = "--quick" in sys.argv
    if "--plots" in sys.argv:
        rows = json.loads((OUT / "sweep.json").read_text())
    else:
        rows = sweep(0.1, quick)
        (OUT / "sweep.json").write_text(json.dumps(rows, indent=1))
    if not quick:
        heatmaps(rows, "index_cm3", "heatmap-index.svg",
                 "S-03: index per detector, gas volume whose field line ends on the active area (cm³)",
                 "Index (cm³)", "{:.1f}")
        heatmaps(rows, "to_active", "heatmap-fraction.svg",
                 "S-03: share of the gas volume whose field line ends on the active area (%)",
                 "Share to the active area (%)", "{:.0f}", scale=100)
        heatmaps(rows, "t_median_ms", "heatmap-transit.svg",
                 "S-03: median transit to the die (ms) at a mobility of 2 cm²/(V·s)", "Median transit (ms)", "{:.0f}",
                 cmap="Oranges")
        tradeoff(rows)
    summary(rows)
    print("done")
