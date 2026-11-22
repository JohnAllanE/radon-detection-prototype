"""S-01: 2D axisymmetric electrostatic field of the Part 1 chamber end, with the ion paths.

    .venv/bin/python sim/field/S-01-chamber/run.py            # all cases, plots, summary
    .venv/bin/python sim/field/S-01-chamber/run.py --quick    # coarse grid only

Geometry (mm), all parameters in GEOM; sources and VERIFY marks are in README.md. One detector board
end of the tube is modelled; the tube's mid-plane (38 mm up) is a symmetry plane, so the other board
sees the same. The square 2x2 photodiode array is not axisymmetric: two sections bound it, the
diagonal (die corners at 8.37 mm, the smallest gap to the wall) and the side (die edge at 5.92 mm).
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
sys.path.insert(0, str(HERE))
from field import Grid, trace, bilinear, LABELS

OUT = HERE / "results"
OUT.mkdir(exist_ok=True)
plt.rcParams.update({"svg.fonttype": "none", "font.size": 9, "font.family": "sans-serif"})

DIE = 5.67            # VTH2110.json p1: chip 5.67 x 5.67 x 0.30 mm
DIE_T = 0.30
DIE_GAP = 0.5         # A-02: 0.5 mm gaps in the 2x2 array
HALF = DIE + DIE_GAP / 2                     # array half-width, 5.92 mm
SECTIONS = {"diagonal": HALF * np.sqrt(2), "side": HALF}

GEOM = dict(
    bore=21.0,            # R-39: 21-22 mm
    tube_od=26.67,        # 3/4 in NPS pipe OD, 1.050 in (ASME B36.10M)
    oring_gap=1.0,        # tube end face height above the board: compressed O-ring, VERIFY (Q-20)
    ring_out=9.6,         # exposed ring copper outer radius, Claude's layout assumption
    ring_clear=0.3,       # copper clearance between die and ring (detector-board note)
    board_t=1.6,          # FR4 thickness, back copper at 0 V
    eps_fr4=4.4,          # FR4 relative permittivity, typical, VERIFY
    rmax=16.0, zmax=38.0, # 76 mm between boards (A-23): mid-plane at 38 mm
    V_tube=1000.0,        # R-18, about +1 kV, VERIFY the final value
    V_pd=0.0,             # diode front: CSA input (virtual 0 V) or bias; 20 V changes little
    V_ring=0.0,
    cone=None,            # sloped electrode: dict(V=, r1=, z1=, r2=, z2=, t=)
    edge_round=0.0,       # radius of the tube end's inner edge; 0 = sharp (the model's worst case)
    section="diagonal",
)
CONE = dict(r1=8.6, z1=2.0, r2=9.8, z2=7.0, t=0.3)   # inner lip low over the die corners, outer edge up
MU = 200.0            # ion mobility, mm^2/(V s) = 2 cm^2/(V s), order of small air ions, VERIFY
FLOW_V = 16667 / (np.pi * 10.5 ** 2)  # mm/s: 1 L/min (gas-train note) through a 21 mm bore
PO218_HALF = 186.0    # s, 3.097 min (NuDat, Zhu and McCutchan 2021)
DEST = {1: "photodiode", 2: "ring", 5: "sloped electrode", 6: "bare FR4", 3: "back plane"}
COL = {1: "#2a78d6", 2: "#8e44ad", 5: "#d95926", 6: "#898781", 3: "#52514e", 7: "#000000", 8: "#000000"}


def build(geom, h):
    G = dict(GEOM, **geom)
    rpd = SECTIONS[G["section"]]
    Rb, Ro, ho = G["bore"] / 2, G["tube_od"] / 2, G["oring_gap"]
    g = Grid(G["rmax"], -G["board_t"], G["zmax"], h)
    R, Z = g.R, g.Z
    e = 1e-9
    g.eps[Z < -e] = G["eps_fr4"]
    g.set_conductor(Z <= -G["board_t"] + e, 0.0, 3)
    tube = (R >= Rb - e) & (R <= Ro + e) & (Z >= ho - e)
    rho = G["edge_round"]
    if rho > 0:
        cut_in = (R < Rb + rho) & (Z < ho + rho) & (np.hypot(R - Rb - rho, Z - ho - rho) > rho)
        cut_out = (R > Ro - rho) & (Z < ho + rho) & (np.hypot(R - Ro + rho, Z - ho - rho) > rho)
        tube &= ~(cut_in | cut_out)
    g.set_conductor(tube, G["V_tube"], 4)
    g.set_conductor((R <= rpd + e) & (Z >= -e) & (Z <= DIE_T + e), G["V_pd"], 1)
    ri = rpd + G["ring_clear"]
    if ri < G["ring_out"]:
        g.set_conductor((R >= ri - e) & (R <= G["ring_out"] + e) & (np.abs(Z) <= e), G["V_ring"], 2)
    c = G["cone"]
    if c:
        # a sloped sheet of thickness t between (r1, z1) and (r2, z2)
        p1, p2 = np.array([c["r1"], c["z1"]]), np.array([c["r2"], c["z2"]])
        d = p2 - p1; L = np.hypot(*d); u = d / L
        q = np.stack([R - p1[0], Z - p1[1]], -1)
        s = q @ u
        n = np.abs(q @ np.array([-u[1], u[0]]))
        g.set_conductor((s >= 0) & (s <= L) & (n <= c["t"] / 2 + h / 2), c["V"], 5)
    g.G, g.rpd = G, rpd
    return g


def starts(g, n_r=40, n_z=76):
    """Volume-weighted start points in the gas inside the bore."""
    G = g.G
    Rb = G["bore"] / 2
    z0 = max(G["oring_gap"], DIE_T) + 0.1
    rr = (np.arange(n_r) + 0.5) / n_r * (Rb - 0.15)
    zz = z0 + (np.arange(n_z) + 0.5) / n_z * (G["zmax"] - z0)
    R, Z = np.meshgrid(rr, zz, indexing="ij")
    R, Z = R.ravel(), Z.ravel()
    i = np.rint(R / g.h).astype(int); j = np.rint((Z - g.z[0]) / g.h).astype(int)
    keep = ~g.fixed[i, j]
    return R[keep], Z[keep], R[keep]          # weight = r


def classify(g, lab, rend):
    lab = lab.copy()
    G = g.G
    ri = g.rpd + G["ring_clear"]
    on_ring = (lab == 6) & (rend >= ri) & (rend <= G["ring_out"])
    lab[on_ring] = 2
    lab[(lab == 6) & (rend <= g.rpd)] = 1
    return lab


DEAD = DIE_GAP / 2 + (DIE - 5.0) / 2   # 0.585 mm: half the 0.5 mm gap plus the 0.335 mm inactive die border


def dead_cross(rho, a=DEAD, n=720):
    """Fraction of a circle of radius rho (azimuthal average: the model is axisymmetric) inside the
    central cross |x| < a or |y| < a, where the four dies meet: gaps and inactive borders."""
    th = (np.arange(n) + 0.5) / n * 2 * np.pi
    x = np.abs(np.outer(rho, np.cos(th))); y = np.abs(np.outer(rho, np.sin(th)))
    return ((x < a) | (y < a)).mean(axis=1)


def peak_fields(g):
    """Peak fields in the gas: overall (the tube's inner corner), near the die's top corner, and along
    the board surface between the ring and the tube's outside (the O-ring land: creepage)."""
    G = g.G
    gas = (~g.fixed) & (g.Z >= -1e-9)
    E = np.where(gas, g.Emag, 0)
    k = np.unravel_index(np.argmax(E), E.shape)
    Rb, Ro, ho = G["bore"] / 2, G["tube_od"] / 2, G["oring_gap"]
    corner = np.hypot(Rb - g.rpd, ho - DIE_T)
    near_die = gas & (np.hypot(g.R - g.rpd, g.Z - DIE_T) <= 0.3)
    j0 = np.argmin(np.abs(g.z))
    j1 = j0 + 1                                   # first gas row above the board surface
    land = (g.r >= G["ring_out"] + g.h) & (g.r <= Ro)
    return dict(E_max=float(E[k]), at_r=float(g.r[k[0]]), at_z=float(g.z[k[1]]),
                E_die_corner=float(E[near_die].max()),
                E_board_surface=float(np.max(g.Emag[land, j1])),
                Et_board_surface=float(np.max(np.abs(g.Er[land, j1]))),
                gap_die_tube=float(corner), E_avg_gap=float((G["V_tube"] - G["V_pd"]) / corner),
                E_mid_axis=float(g.Emag[0, -1]))


def run_case(name, geom, h, ds=None, keep=False):
    t0 = time.time()
    g = build(geom, h)
    g.solve()
    r0, z0, w = starts(g)
    lab, rend, L, T, _ = trace(g, r0, z0, ds=ds or max(h, 0.05), max_len=150)
    lab = classify(g, lab, rend)
    t = T / MU
    res = dict(name=name, h=h, geom={k: v for k, v in geom.items()}, **peak_fields(g))
    W = w.sum()
    res["fractions"] = {DEST.get(k, LABELS[k]): float(w[lab == k].sum() / W) for k in np.unique(lab)}
    pd = lab == 1
    res["pd_within_10s"] = float(w[pd & (t < 10)].sum() / W)
    res["pd_within_po218_half"] = float(w[pd & (t < PO218_HALF)].sum() / W)
    res["t_median_s"] = float(np.median(t[pd])) if pd.any() else None
    res["t_max_s"] = float(t.max())
    Es = np.hypot(bilinear(g, g.Er, np.column_stack([r0, z0])), bilinear(g, g.Ez, np.column_stack([r0, z0])))
    res["vol_drift_below_flow"] = float(w[MU * Es < FLOW_V].sum() / W)
    res["pd_in_dead_cross"] = float((w[pd] * dead_cross(rend[pd])).sum() / w[pd].sum()) if pd.any() else None
    res["pd_landing_r_median"] = float(np.median(np.repeat(rend[pd], 1))) if pd.any() else None
    res["seconds"] = round(time.time() - t0, 1)
    print(f"{name:34s} h={h}: PD {res['fractions'].get('photodiode', 0):.3f}  "
          f"Emax {res['E_max']:.0f} V/mm at ({res['at_r']:.2f},{res['at_z']:.2f})  "
          f"avg gap {res['E_avg_gap']:.0f} V/mm  t_med {res['t_median_s']}  ({res['seconds']} s)", flush=True)
    if keep:
        return res, g, (r0, z0, w, lab, t)
    return res


CASES = [
    ("base, diagonal", {}),
    ("base, side", {"section": "side"}),
    ("22 mm bore, diagonal", {"bore": 22.0}),
    ("22 mm bore, side", {"bore": 22.0, "section": "side"}),
    ("ring +20 V (PD bias), side", {"section": "side", "V_ring": 20.0}),
    ("ring +50 V, side", {"section": "side", "V_ring": 50.0}),
    ("ring +100 V, side", {"section": "side", "V_ring": 100.0}),
    ("ring +100 V, diagonal", {"V_ring": 100.0}),
    ("O-ring gap 2 mm, diagonal", {"oring_gap": 2.0}),
    ("tube edge rounded 0.5 mm, diagonal", {"edge_round": 0.5}),
    ("sloped +300 V, diagonal", {"cone": dict(CONE, V=300.0)}),
    ("sloped +300 V, side", {"section": "side", "cone": dict(CONE, V=300.0)}),
    ("sloped +500 V, diagonal", {"cone": dict(CONE, V=500.0)}),
    ("sloped +500 V, side", {"section": "side", "cone": dict(CONE, V=500.0)}),
    ("sloped +700 V, side", {"section": "side", "cone": dict(CONE, V=700.0)}),
    ("FR4 charged (no flux), side", {"section": "side", "eps_fr4": 1e-6}),
]

LEGEND = [Line2D([], [], color=COL[k], lw=1.4, label=v) for k, v in
          ((1, "ends on a photodiode"), (2, "ends on the ring"), (5, "ends on the sloped electrode"),
           (6, "ends on bare FR4"), (7, "does not end (mid-plane)"))]


def draw_geometry(ax, g):
    G = g.G
    Rb, Ro, ho = G["bore"] / 2, G["tube_od"] / 2, G["oring_gap"]
    ax.add_patch(plt.Rectangle((Rb, ho), Ro - Rb, G["zmax"] - ho, fc="#f2c94c", ec="k", lw=0.6))
    ax.add_patch(plt.Rectangle((0, -G["board_t"]), G["rmax"], G["board_t"], fc="#cfe8cf", ec="k", lw=0.6))
    ax.add_patch(plt.Rectangle((0, 0), g.rpd, DIE_T, fc="#2a78d6", ec="k", lw=0.6))
    ri = g.rpd + G["ring_clear"]
    if ri < G["ring_out"]:
        ax.plot([ri, G["ring_out"]], [0, 0], color="#8e44ad", lw=3, solid_capstyle="butt")
    ax.add_patch(plt.Rectangle((Rb + 0.3, 0), Ro - Rb - 0.6, ho, fc="#555", ec="none", alpha=0.6))
    c = G["cone"]
    if c:
        ax.plot([c["r1"], c["r2"]], [c["z1"], c["z2"]], color="#d95926", lw=2.5)


def field_plot(ax, g, title, zmax=20.0):
    G = g.G
    Rb = G["bore"] / 2
    levels = np.arange(50, 1000, 50)
    ax.contour(g.R, g.Z, np.where(g.Z < 0, np.nan, g.V), levels=levels, colors="#9a9a9a",
               linewidths=0.4)
    # lines from evenly spaced points (equal volume) at z = zmax, and along the wall
    r_top = Rb * np.sqrt((np.arange(16) + 0.5) / 16)
    z_wall = np.linspace(1.6, zmax, 14)
    r0 = np.concatenate([r_top, np.full(z_wall.size, Rb - 0.25)])
    z0 = np.concatenate([np.full(r_top.size, zmax), z_wall])
    lab, rend, L, T, paths = trace(g, r0, z0, ds=g.h / 2, max_len=150)
    lab = classify(g, lab, rend)
    for p, k in zip(paths, lab):
        p = np.array(p)
        ax.plot(p[:, 0], p[:, 1], color=COL[int(k)], lw=0.9)
    draw_geometry(ax, g)
    ax.set_xlim(0, G["rmax"]); ax.set_ylim(-G["board_t"], zmax)
    ax.set_aspect("equal")
    ax.set_xlabel("r (mm) from the tube axis"); ax.set_ylabel("z (mm) above the board")
    ax.set_title(title, fontsize=9)


def emag_plot(ax, g, title, fig):
    G = g.G
    Em = np.where(g.fixed | (g.Z < 0), np.nan, g.Emag)
    m = ax.pcolormesh(g.R, g.Z, Em, shading="auto", cmap="viridis", vmin=0, vmax=1200, rasterized=True)
    ax.contour(g.R, g.Z, np.where(g.Z < 0, np.nan, g.V), levels=np.arange(100, 1000, 100),
               colors="w", linewidths=0.4)
    draw_geometry(ax, g)
    ax.set_xlim(5, 14.5); ax.set_ylim(-G["board_t"], 4.5); ax.set_aspect("equal")
    ax.set_xlabel("r (mm)"); ax.set_ylabel("z (mm)"); ax.set_title(title, fontsize=9)
    fig.colorbar(m, ax=ax, shrink=0.8, label="|E| (V/mm)")


if __name__ == "__main__":
    quick = "--quick" in sys.argv
    h = 0.1 if quick else 0.05
    results = []
    # grid study on the base case
    for hh in ((0.1, 0.05) if quick else (0.1, 0.05, 0.025)):
        results.append(run_case("grid study, base, diagonal", {}, hh))
    for name, geom in CASES:
        results.append(run_case(name, geom, h))
    (OUT / "results.json").write_text(json.dumps(results, indent=1))

    # field-line plots
    pairs = [("fieldlines-base", [("Base, diagonal section (die corners)", {}),
                                  ("Base, side section (die edges)", {"section": "side"})]),
             ("fieldlines-ring", [("Ring +100 V, side section", {"section": "side", "V_ring": 100.0}),
                                  ("Ring +100 V, diagonal section", {"V_ring": 100.0})]),
             ("fieldlines-sloped", [("Sloped electrode +500 V, diagonal", {"cone": dict(CONE, V=500.0)}),
                                    ("Sloped electrode +500 V, side", {"section": "side", "cone": dict(CONE, V=500.0)})])]
    for fname, items in pairs:
        fig, axs = plt.subplots(1, 2, figsize=(9.5, 6.4))
        for ax, (title, geom) in zip(axs, items):
            g = build(geom, h); g.solve()
            field_plot(ax, g, title)
        fig.legend(handles=LEGEND, loc="lower center", ncol=5, fontsize=7.5, frameon=False)
        fig.suptitle("S-01: field lines (positive-ion paths) and equipotentials every 50 V; tube +1 kV, board 0 V",
                     fontsize=9.5)
        fig.tight_layout(rect=(0, 0.04, 1, 0.96)); fig.savefig(OUT / f"{fname}.svg"); plt.close(fig)

    fig, axs = plt.subplots(1, 2, figsize=(10, 4.2))
    for ax, (title, geom) in zip(axs, [("|E| at the die corner and tube end, base diagonal", {}),
                                       ("|E| with the sloped electrode at +500 V", {"cone": dict(CONE, V=500.0)})]):
        g = build(geom, h); g.solve()
        emag_plot(ax, g, title, fig)
    fig.tight_layout(); fig.savefig(OUT / "field-strength.svg"); plt.close(fig)

    # where on the array the ions land
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    for name, geom, col in (("base, diagonal", {}, "#2a78d6"), ("base, side", {"section": "side"}, "#8e44ad"),
                            ("sloped +500 V, side", {"section": "side", "cone": dict(CONE, V=500.0)}, "#d95926")):
        res, g, (r0, z0, w, lab, t) = run_case(name + " (landing)", geom, h, keep=True)
        _, rend, *_ = trace(g, r0, z0, ds=max(h, 0.05), max_len=150)
        pd = lab == 1
        o = np.argsort(rend[pd])
        ax.plot(rend[pd][o], np.cumsum(w[pd][o]) / w.sum(), color=col, label=name)
    ax.axvspan(0, DEAD, color="#cccccc", alpha=0.6, lw=0)
    ax.text(DEAD + 0.1, 0.05, "inside 0.585 mm of the axis: the dies' meeting point, gaps and inactive borders", fontsize=7.5)
    ax.axvline(HALF, color="#52514e", lw=0.8, ls="--"); ax.text(HALF + 0.1, 0.5, "die edge, side", fontsize=7.5)
    ax.axvline(HALF * np.sqrt(2), color="#52514e", lw=0.8, ls=":"); ax.text(HALF * np.sqrt(2) + 0.1, 0.35, "die corner", fontsize=7.5)
    ax.set_xlim(0, 10.5); ax.set_ylim(0, 1)
    ax.set_xlabel("Landing radius on the array (mm)"); ax.set_ylabel("Cumulative fraction of the gas volume")
    ax.set_title("S-01: ions land mostly near the centre of the array", fontsize=10)
    ax.legend(loc="lower right", fontsize=8); ax.grid(alpha=0.3)
    fig.tight_layout(); fig.savefig(OUT / "landing-radius.svg"); plt.close(fig)

    # summary bar chart
    rows = [r for r in results if not r["name"].startswith("grid")]
    fig, ax = plt.subplots(figsize=(8, 5.6))
    names = [r["name"] for r in rows]
    left = np.zeros(len(rows))
    for key, col in (("photodiode", COL[1]), ("ring", COL[2]), ("sloped electrode", COL[5]),
                     ("bare FR4", COL[6]), ("not ended", "#cccccc")):
        v = np.array([r["fractions"].get(key, 0.0) for r in rows])
        ax.barh(names, v, left=left, color=col, label=key)
        left += v
    for i, r in enumerate(rows):
        ax.text(0.01, i, f"{100 * r['fractions'].get('photodiode', 0):.0f} %", va="center", color="w", fontsize=8)
    ax.invert_yaxis(); ax.set_xlim(0, 1)
    ax.set_xlabel("Fraction of the gas volume whose field line ends on each surface (volume-weighted)")
    ax.legend(loc="upper center", bbox_to_anchor=(0.4, -0.12), ncol=5, fontsize=8, frameon=False)
    ax.set_title("S-01: where ions from the gas volume land", fontsize=10)
    fig.tight_layout(); fig.savefig(OUT / "destinations.svg"); plt.close(fig)

    lines = ["| Case | h (mm) | To photodiodes | Ring | Sloped | Bare FR4 | Peak E (V/mm), where | E near die corner | E on board at O-ring land (tangential) | Median transit | Volume where 1 L/min flow beats drift | Landing in the central dead cross |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in results:
        f = r["fractions"]
        lines.append(f"| {r['name']} | {r['h']} | {100*f.get('photodiode',0):.1f} % | {100*f.get('ring',0):.1f} % | "
                     f"{100*f.get('sloped electrode',0):.1f} % | {100*f.get('bare FR4',0):.1f} % | "
                     f"{r['E_max']:.0f} at ({r['at_r']:.2f}, {r['at_z']:.2f}) | {r['E_die_corner']:.0f} | "
                     f"{r['E_board_surface']:.0f} ({r['Et_board_surface']:.0f}) | "
                     f"{1000*r['t_median_s']:.1f} ms | {100*r['vol_drift_below_flow']:.1f} % | {100*r['pd_in_dead_cross']:.0f} % |")
    (OUT / "summary.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
