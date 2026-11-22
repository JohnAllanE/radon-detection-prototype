"""S-02: one VTH2110 centred at the end of each tube. Sweep tube inner diameter (standard stainless
pipe, 1/4 to 1-1/2 in NPS, schedules 10S, 40S, 80S) against the bias V_top on the board's exposed
top copper around the die. Reuses S-01's axisymmetric solver (../S-01-chamber/field.py).

    .venv/bin/python sim/field/S-02-single-pd/run.py           # sweep at h = 0.1 mm, plots, summary
    .venv/bin/python sim/field/S-02-single-pd/run.py --quick   # two sizes only

Superposition: the problem is linear, so for each tube two fields are solved (tube 1 V with the
copper at 0 V, and the copper 1 V with the tube at 0 V) and combined for every V_top.
Sources and VERIFY marks: README.md.
"""
import json
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
from field import Grid, trace, bilinear  # noqa: E402

OUT = HERE / "results"
OUT.mkdir(exist_ok=True)
plt.rcParams.update({"svg.fonttype": "none", "font.size": 9, "font.family": "sans-serif"})

IN = 25.4
# Engineering ToolBox, "Stainless Steel Pipes - Dimensions and Weights" (ASME B36.19M): OD and wall, inches
PIPES = [  # (nominal, OD, {schedule: wall})
    ("1/4", 0.540, {"10S": 0.065, "40S": 0.088, "80S": 0.119}),
    ("3/8", 0.675, {"10S": 0.065, "40S": 0.091, "80S": 0.126}),
    ("1/2", 0.840, {"10S": 0.083, "40S": 0.109, "80S": 0.147}),
    ("3/4", 1.050, {"10S": 0.083, "40S": 0.113, "80S": 0.154}),
    ("1", 1.315, {"10S": 0.109, "40S": 0.133, "80S": 0.179}),
    ("1-1/4", 1.660, {"10S": 0.109, "40S": 0.140, "80S": 0.191}),
    ("1-1/2", 1.900, {"10S": 0.109, "40S": 0.145, "80S": 0.200}),
]
# NPT threads per inch (ASME B1.20.1); thread height 0.8 x pitch. VERIFY against the standard.
TPI = {"1/4": 18, "3/8": 18, "1/2": 14, "3/4": 14, "1": 11.5, "1-1/4": 11.5, "1-1/2": 11.5}

DIE = 5.67            # VTH2110.json p1: chip 5.67 x 5.67 x 0.30 mm, 5 x 5 mm active
DIE_T = 0.30
ACT = 2.5             # active half-width
R_DIE = DIE / np.sqrt(np.pi)   # equal-area disk: 3.20 mm. Side 2.835, diagonal 4.01 bound it
SECTIONS = {"equal area": R_DIE, "side": DIE / 2, "diagonal": DIE / np.sqrt(2)}
V_TUBE = 1000.0       # R-18, about +1 kV, VERIFY the final value
GAP = 1.0             # tube end above the board (PTFE washer, A-23), VERIFY
EDGE = 0.5            # inner edge radius of the tube end (S-01 machining note)
CLEAR = 0.3           # copper clearance to the die (detector-board note)
COPPER_IN = 0.9       # copper stops 0.9 mm inside the bore (S-01, point 5)
BOARD_T, EPS = 1.6, 4.4   # FR4, typical, VERIFY
ZMAX = 38.0           # boards 76 mm apart (A-23): mid-plane symmetry
FLANGE_W = 6.0        # flange modelled as HV metal from the pipe OD out to OD/2 + 6 mm (the domain edge)
# 20 V = PD bias (A-04); 100-200 V = the HV board's transformer stage (A-20); 600 V: copper-edge field
# passes about 1.7 kV/mm (h = 0.1 mm), beyond S-01's accepted margin
V_TOPS = [0.0, 20.0, 50.0, 100.0, 150.0, 200.0, 300.0, 400.0, 500.0, 600.0]
MU = 200.0            # mm^2/(V s), as S-01, VERIFY (transit times only)


def pipes():
    rows = []
    for nom, od, walls in PIPES:
        for sch, w in walls.items():
            rows.append(dict(nominal=nom, schedule=sch, od_mm=od * IN, wall_mm=w * IN,
                             id_mm=(od - 2 * w) * IN, thread_h_mm=0.8 * IN / TPI[nom]))
    return sorted(rows, key=lambda p: p["id_mm"])


def build(p, h, r_die=R_DIE):
    Rb, Ro = p["id_mm"] / 2, p["od_mm"] / 2
    g = Grid(Ro + FLANGE_W, -BOARD_T, ZMAX, h)
    R, Z = g.R, g.Z
    e = 1e-9
    g.eps[Z < -e] = EPS
    g.set_conductor(Z <= -BOARD_T + e, 0.0, 3)
    tube = (R >= Rb - e) & (Z >= GAP - e)          # pipe wall and flange, both at HV
    rho = min(EDGE, 0.45 * (Ro - Rb))
    cut = (R < Rb + rho) & (Z < GAP + rho) & (np.hypot(R - Rb - rho, Z - GAP - rho) > rho)
    tube &= ~cut
    g.set_conductor(tube, 1.0, 4)
    g.set_conductor((R <= r_die + e) & (Z >= -e) & (Z <= DIE_T + e), 0.0, 1)
    ri, ro = r_die + CLEAR, Rb - COPPER_IN
    if ro > ri:
        g.set_conductor((R >= ri - e) & (R <= ro + e) & (np.abs(Z) <= e), 0.0, 2)
    g.rdie, g.ri, g.ro, g.Rb, g.Ro, g.p = r_die, ri, ro, Rb, Ro, p
    return g


def solve_basis(p, h, r_die=R_DIE):
    """Two unit solutions: tube at 1 V, and copper at 1 V."""
    g = build(p, h, r_die)
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


def starts(g, n_r=40, n_z=76):
    z0 = GAP + 0.1
    rr = (np.arange(n_r) + 0.5) / n_r * (g.Rb - 0.15)
    zz = z0 + (np.arange(n_z) + 0.5) / n_z * (ZMAX - z0)
    R, Z = np.meshgrid(rr, zz, indexing="ij")
    R, Z = R.ravel(), Z.ravel()
    return R, Z, R


def active_share(rho, a=ACT, n=720):
    """Share of a circle of radius rho (azimuthal average) inside the 5 x 5 mm active square."""
    th = (np.arange(n) + 0.5) / n * 2 * np.pi
    x = np.abs(np.outer(rho, np.cos(th))); y = np.abs(np.outer(rho, np.sin(th)))
    return ((x < a) & (y < a)).mean(axis=1)


def classify(g, lab, rend):
    lab = lab.copy()
    lab[(lab == 6) & (rend <= g.rdie)] = 1
    lab[(lab == 6) & (rend >= g.ri) & (rend <= g.ro)] = 2
    return lab


def fields(g):
    """Peak |E| in the gas near the die's top corner, near the copper's two edges, and in the gap
    under the tube end at the pipe OD (where the thread meets the flange face)."""
    gas = (~g.fixed) & (g.Z >= -1e-9)
    near = lambda r, z, d=0.3: gas & (np.hypot(g.R - r, g.Z - z) <= d)
    out = dict(E_die_edge=float(g.Emag[near(g.rdie, DIE_T)].max()))
    if g.ro > g.ri:
        out["E_cu_inner"] = float(g.Emag[near(g.ri, 0.0)].max())
        out["E_cu_outer"] = float(g.Emag[near(g.ro, 0.0)].max())
    out["E_tube_edge"] = float(g.Emag[gas & (np.hypot(g.R - g.Rb, g.Z - GAP) <= 1.0) & (g.Z >= 0.5 * GAP)].max())
    j = np.argmin(np.abs(g.z - GAP / 2)); i = np.argmin(np.abs(g.r - g.Ro))
    out["E_thread_seam_gap"] = float(g.Emag[i, j])
    i1 = np.argmin(np.abs(g.r - (g.Ro - g.p["thread_h_mm"])))
    jj = np.argmin(np.abs(g.z - (GAP + 2.0)))
    out["V_drop_at_thread_root"] = float(V_TUBE - g.V[min(i1, g.shape[0] - 1), jj])   # inside metal: 0
    return out


def run_point(g, vt, r0, z0, w, ds):
    set_vtop(g, vt)
    lab, rend, L, T, _ = trace(g, r0, z0, ds=ds, max_len=200)
    lab = classify(g, lab, rend)
    W = w.sum()
    pd = lab == 1
    act = np.zeros_like(rend); act[pd] = active_share(rend[pd])
    res = dict(V_top=vt,
               to_die=float(w[pd].sum() / W),
               to_active=float((w * act).sum() / W),
               to_copper=float(w[lab == 2].sum() / W),
               to_fr4=float(w[lab == 6].sum() / W),
               not_ended=float(w[(lab == 7) | (lab == 8)].sum() / W),
               t_median_ms=float(1000 * np.median(T[pd] / MU)) if pd.any() else None,
               r_land_median=float(np.median(rend[pd])) if pd.any() else None)
    res.update(fields(g))
    return res


def sweep(h, quick=False):
    rows = []
    sel = pipes()
    if quick:
        sel = [p for p in sel if (p["nominal"], p["schedule"]) in (("3/4", "40S"), ("1-1/2", "40S"))]
    for p in sel:
        t0 = time.time()
        g = solve_basis(p, h)
        r0, z0, w = starts(g)
        feasible = DIE / np.sqrt(2) + CLEAR < p["id_mm"] / 2 - COPPER_IN
        for vt in V_TOPS:
            res = run_point(g, vt, r0, z0, w, ds=max(h, 0.05))
            res.update(p, h=h, die_corner_fits=bool(feasible),
                       index_per_mm=float(p["id_mm"] ** 2 * res["to_active"]),
                       index=float(np.pi * (p["id_mm"] / 2) ** 2 * ZMAX * res["to_active"]))   # per detector: half the tube
            rows.append(res)
        print(f"{p['nominal']:>6} {p['schedule']:>3} ID {p['id_mm']:5.2f}: active "
              + " ".join(f"{r['to_active']:.3f}" for r in rows[-len(V_TOPS):])
              + f"  ({time.time() - t0:.0f} s)", flush=True)
    return rows


def label(p):
    return f"{p['nominal']} {p['schedule']}, {p['id_mm']:.1f} mm"


REC = ("1-1/4", "40S", 200.0)   # the build point chosen in README.md


def heatmap(rows, key, fname, title, cbar, fmt, scale=1.0, cmap="Blues"):
    ps = []
    for r in rows:
        k = (r["nominal"], r["schedule"])
        if k not in [(q["nominal"], q["schedule"]) for q in ps]:
            ps.append(r)
    M = np.array([[next(r[key] for r in rows if (r["nominal"], r["schedule"]) == (p["nominal"], p["schedule"])
                        and r["V_top"] == v) * scale for v in V_TOPS] for p in ps])
    fig, ax = plt.subplots(figsize=(8.2, 7.4))
    m = ax.imshow(M, cmap=cmap, aspect="auto", origin="lower")
    vmax = M.max()
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            ax.text(j, i, fmt.format(M[i, j]), ha="center", va="center", fontsize=6.5,
                    color="white" if M[i, j] > 0.55 * vmax else "#1f1f1f")
    bi, bj = np.unravel_index(np.argmax(M), M.shape)
    ax.add_patch(plt.Rectangle((bj - 0.5, bi - 0.5), 1, 1, fill=False, ec="#d95926", lw=2, clip_on=False))
    ri = [(p["nominal"], p["schedule"]) for p in ps].index(REC[:2]); rj = V_TOPS.index(REC[2])
    ax.add_patch(plt.Rectangle((rj - 0.5, ri - 0.5), 1, 1, fill=False, ec="#d95926", lw=2, ls="--", clip_on=False))

    ax.set_xticks(range(len(V_TOPS)), [f"{v:.0f}" for v in V_TOPS])
    ax.set_yticks(range(len(ps)), [label(p) + ("" if p["die_corner_fits"] else "  (die too wide)")
                                   + ("  (thread?)" if p["schedule"] == "10S" else "") for p in ps],
                  fontsize=7.5)
    ax.set_xlabel("V_top, bias on the board's exposed top copper (V); tube +1 kV, die 0 V")
    ax.set_ylabel("Pipe: nominal size, schedule, inner diameter")
    ax.set_title(title + "\nOutlined: solid, highest in the sweep; dashed, recommended build point. "
                 "10S: NPT threading questionable", fontsize=9.5)
    fig.colorbar(m, ax=ax, shrink=0.85, label=cbar)
    fig.tight_layout(); fig.savefig(OUT / fname); plt.close(fig)


COL = {1: "#2a78d6", 2: "#8e44ad", 6: "#898781", 7: "#000000", 8: "#000000"}


def fieldline_plot(ax, g, vt, title):
    set_vtop(g, vt)
    zshow = min(ZMAX, max(14.0, 1.6 * g.Rb + 4))
    ax.contour(g.R, g.Z, np.where(g.Z < 0, np.nan, g.V), levels=np.arange(50, 1000, 50), colors="#b0b0b0",
               linewidths=0.4)
    n = 18
    r0 = np.concatenate([(g.Rb - 0.2) * np.sqrt((np.arange(n) + 0.5) / n), np.full(10, g.Rb - 0.25)])
    z0 = np.concatenate([np.full(n, zshow - 0.2), np.linspace(GAP + 0.5, zshow - 1, 10)])
    lab, rend, L, T, paths = trace(g, r0, z0, ds=g.h / 2, max_len=200)
    lab = classify(g, lab, rend)
    act = active_share(rend)
    for pth, k, a in zip(paths, lab, act):
        pth = np.array(pth)
        c = COL.get(int(k), "#000")
        if k == 1 and a < 0.5:
            c = "#7fb0e8"
        ax.plot(pth[:, 0], pth[:, 1], color=c, lw=0.9)
    ax.add_patch(plt.Rectangle((g.Rb, GAP), g.r[-1] - g.Rb, ZMAX - GAP, fc="#f2c94c", ec="k", lw=0.6))
    ax.add_patch(plt.Rectangle((0, -BOARD_T), g.r[-1], BOARD_T, fc="#cfe8cf", ec="k", lw=0.6))
    ax.add_patch(plt.Rectangle((0, 0), g.rdie, DIE_T, fc="#2a78d6", ec="k", lw=0.6))
    ax.axvline(ACT, ymin=0, ymax=0.03, color="k", lw=0.8)
    if g.ro > g.ri:
        ax.plot([g.ri, g.ro], [0, 0], color="#8e44ad", lw=3, solid_capstyle="butt")
    ax.plot([g.Ro, g.Ro], [GAP, zshow], color="k", lw=0.6, ls=":")
    ax.text(g.Ro + 0.2, GAP + 0.6, "pipe OD,\nthreads", fontsize=6.5)
    ax.set_xlim(0, g.r[-1]); ax.set_ylim(-BOARD_T, zshow); ax.set_aspect("equal")
    ax.set_xlabel("r (mm) from the tube axis"); ax.set_ylabel("z (mm) above the board")
    ax.set_title(title, fontsize=8.5)


if __name__ == "__main__":
    quick = "--quick" in sys.argv
    h = 0.1
    if "--plots" in sys.argv:          # redraw from the saved sweep
        rows = json.loads((OUT / "sweep.json").read_text())
        for r in rows:
            r["index"] = float(np.pi * (r["id_mm"] / 2) ** 2 * ZMAX * r["to_active"])
        (OUT / "sweep.json").write_text(json.dumps(rows, indent=1))
    else:
        rows = sweep(h, quick)
        (OUT / "sweep.json").write_text(json.dumps(rows, indent=1))
    heatmap(rows, "index_per_mm", "heatmap-index.svg",
            "S-02: interaction index per unit tube length, ID² × fraction on the active area (mm²)",
            "ID² × fraction to the 5 × 5 mm active area (mm²)", "{:.0f}")
    heatmap(rows, "to_active", "heatmap-fraction.svg",
            "S-02: fraction of the gas volume whose field line ends on the active area",
            "Fraction to the active area (%)", "{:.0f}", scale=100)
    lines = ["| Pipe | ID (mm) | Wall (mm) | NPT thread height (mm) | Die corner fits | V_top (V) | To die | To active area | To copper | To bare FR4 | Index ID²×f (mm²) | Index V×f per detector (cm³, 38 mm of tube) | E die edge | E copper inner | E copper outer | E tube edge | E at thread seam | Not ended (field-free) | Median transit (ms) |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| {r['nominal']} {r['schedule']} | {r['id_mm']:.2f} | {r['wall_mm']:.2f} | {r['thread_h_mm']:.2f} | "
                     f"{'yes' if r['die_corner_fits'] else 'no'} | {r['V_top']:.0f} | {100*r['to_die']:.1f} % | "
                     f"{100*r['to_active']:.1f} % | {100*r['to_copper']:.1f} % | {100*r['to_fr4']:.1f} % | "
                     f"{r['index_per_mm']:.0f} | {r['index']/1000:.1f} | {r['E_die_edge']:.0f} | "
                     f"{r.get('E_cu_inner', float('nan')):.0f} | {r.get('E_cu_outer', float('nan')):.0f} | "
                     f"{r['E_tube_edge']:.0f} | {r['E_thread_seam_gap']:.0f} | {100*r['not_ended']:.1f} % | {r['t_median_ms']:.1f} |")
    (OUT / "summary.md").write_text("Fields in V/mm at h = 0.1 mm (sharp corners grow with refinement: S-01 checks).\n\n"
                                    + "\n".join(lines) + "\n")
    print("done")
