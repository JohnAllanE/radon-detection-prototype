"""Axisymmetric (r, z) electrostatics for the Part 1 chamber end: finite-volume Laplace solver with
per-node permittivity, field-line tracing for positive ions, and transit times.

Units: mm, V, V/mm. Grid: uniform spacing h in r and z. Nodes on fixed (conductor) masks hold their
potential; every other node satisfies div(eps grad V) = 0. Outer boundaries without a conductor are
zero-normal-field (Neumann): the top of the domain is the tube's mid-plane (symmetry between the two
detector boards), the outer radius is a far boundary.
"""
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

LABELS = {0: "gas", 1: "photodiode", 2: "ring", 3: "back plane", 4: "tube", 5: "sloped electrode",
          6: "bare FR4", 7: "out of domain", 8: "not ended"}


class Grid:
    def __init__(self, rmax, zmin, zmax, h):
        self.h = h
        self.r = np.arange(0.0, rmax + h / 2, h)
        self.z = np.arange(zmin, zmax + h / 2, h)
        self.R, self.Z = np.meshgrid(self.r, self.z, indexing="ij")
        self.shape = self.R.shape
        self.eps = np.ones(self.shape)
        self.fixed = np.zeros(self.shape, bool)
        self.V0 = np.zeros(self.shape)
        self.label = np.zeros(self.shape, np.int8)

    def set_conductor(self, mask, volts, label):
        self.fixed |= mask
        self.V0[mask] = volts
        self.label[mask] = label

    def solve(self):
        nr, nz = self.shape
        h, r, eps = self.h, self.r, self.eps
        idx = np.arange(nr * nz).reshape(nr, nz)
        rows, cols, vals = [], [], []
        diag = np.zeros((nr, nz))
        rhs = np.zeros((nr, nz))

        def harm(a, b):
            return 2 * a * b / (a + b)

        ri = r[:, None] * np.ones((1, nz))
        # coefficient of each face (flux per volt, per 2*pi), see module docstring of README
        # east/west faces at r +- h/2; axis node (i = 0) uses the disk control volume.
        cE = np.zeros((nr, nz)); cW = np.zeros((nr, nz)); cN = np.zeros((nr, nz)); cS = np.zeros((nr, nz))
        eE = harm(eps[:-1, :], eps[1:, :])                     # face between i and i+1
        eN = harm(eps[:, :-1], eps[:, 1:])                     # face between j and j+1
        cE[:-1, :] = (ri[:-1, :] + h / 2) * eE
        cW[1:, :] = (ri[1:, :] - h / 2) * eE
        cE[0, :] = (h / 2) * eE[0, :]
        cN[:, :-1] = ri[:, :-1] * eN
        cS[:, 1:] = ri[:, 1:] * eN
        cN[0, :-1] = (h / 8) * eN[0, :]
        cS[0, 1:] = (h / 8) * eN[0, :]
        free = ~self.fixed
        for c, di, dj in ((cE, 1, 0), (cW, -1, 0), (cN, 0, 1), (cS, 0, -1)):
            m = free & (c > 0)
            ii, jj = np.nonzero(m)
            ni, nj = ii + di, jj + dj
            cc = c[ii, jj]
            diag[ii, jj] += cc
            nb_fixed = self.fixed[ni, nj]
            rhs[ii[nb_fixed], jj[nb_fixed]] += cc[nb_fixed] * self.V0[ni[nb_fixed], nj[nb_fixed]]
            k = ~nb_fixed
            rows.append(idx[ii[k], jj[k]]); cols.append(idx[ni[k], nj[k]]); vals.append(-cc[k])
        fi, fj = np.nonzero(free)
        rows.append(idx[fi, fj]); cols.append(idx[fi, fj]); vals.append(diag[fi, fj])
        A = sp.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))),
                          shape=(nr * nz, nr * nz))
        sel = idx[free]
        V = self.V0.copy().ravel()
        V[sel] = spla.spsolve(A[sel][:, sel].tocsc(), rhs.ravel()[sel])
        self.V = V.reshape(nr, nz)
        Er, Ez = np.gradient(-self.V, h, h)
        self.Er, self.Ez = Er, Ez
        self.Emag = np.hypot(Er, Ez)
        return self.V


def bilinear(g, F, p):
    """F on the grid at points p (n x 2: r, z); zero outside."""
    h = g.h
    x = p[:, 0] / h
    y = (p[:, 1] - g.z[0]) / h
    nr, nz = g.shape
    inside = (x >= 0) & (x <= nr - 1) & (y >= 0) & (y <= nz - 1)
    x = np.clip(x, 0, nr - 1.000001); y = np.clip(y, 0, nz - 1.000001)
    i = x.astype(int); j = y.astype(int)
    fx = x - i; fy = y - j
    v = (F[i, j] * (1 - fx) * (1 - fy) + F[i + 1, j] * fx * (1 - fy)
         + F[i, j + 1] * (1 - fx) * fy + F[i + 1, j + 1] * fx * fy)
    return np.where(inside, v, 0.0)


def trace(g, r0, z0, ds=None, max_len=400.0, zfloor=0.0):
    """Follow +E (positive ions) from each start point until a conductor or the board surface.
    Returns end label, end r, path length (mm), and the integral of ds/|E| (mm^2/V): transit time is
    that integral divided by the mobility."""
    h = g.h
    ds = ds or h / 2
    fr = lambda p: bilinear(g, g.Er, p)
    fz = lambda p: bilinear(g, g.Ez, p)
    r = np.array(r0, float); z = np.array(z0, float)
    n = r.size
    alive = np.ones(n, bool)
    lab = np.full(n, 8, np.int8)
    L = np.zeros(n); T = np.zeros(n)
    rend = r.copy()
    nr, nz = g.shape
    paths = [[(r[k], z[k])] for k in range(n)] if n <= 400 else None
    for step in range(int(max_len / ds)):
        a = np.nonzero(alive)[0]
        if a.size == 0:
            break
        p = np.column_stack([r[a], z[a]])
        er, ez = fr(p), fz(p)
        e = np.hypot(er, ez) + 1e-30
        # midpoint (RK2) step along the unit field direction
        pm = p + 0.5 * ds * np.column_stack([er / e, ez / e])
        er2, ez2 = fr(pm), fz(pm)
        e2 = np.hypot(er2, ez2) + 1e-30
        r[a] = np.abs(p[:, 0] + ds * er2 / e2)          # reflect at the axis
        z[a] = p[:, 1] + ds * ez2 / e2
        L[a] += ds; T[a] += ds / e2
        if paths is not None:
            for k in a:
                paths[k].append((r[k], z[k]))
        i = np.clip(np.rint(r[a] / h).astype(int), 0, nr - 1)
        j = np.clip(np.rint((z[a] - g.z[0]) / h).astype(int), 0, nz - 1)
        hit = g.label[i, j]
        out = (r[a] > g.r[-1]) | (z[a] > g.z[-1]) | (z[a] < g.z[0])
        below = (z[a] < zfloor) & (hit == 0)
        done = (hit > 0) | out | below
        newlab = np.where(hit > 0, hit, np.where(out, 7, 6))
        lab[a[done]] = newlab[done]
        rend[a[done]] = r[a[done]]
        alive[a[done]] = False
    return lab, rend, L, T, paths
