"""Prudent openness against identity (notes/prudent-openness.md §1): families, tilt and scan seed laws, seed payoffs,
compatibility paths, stage statistics, the 50% crossing with its paired bootstrap.

Reuses the identity-and-tags catalogue, class table and kernel conventions (src/identity_tags*.py, unchanged).
"""
import os
import sys
from collections import Counter

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import identity_tags as IT

CBP_X = ('if', ('and', IT.A_(IT.S_C), IT.A_(('chk', 'them', 'C', 'D'))), ('C',), ('D',))   # the spec's CBP
XB_X = ('if', IT.A_(('chk', 'me', 'CB', 'C')), ('D',), ('if', IT.A_(IT.S_C), ('C',), ('D',)))  # the CBP|XC bridge
ALLC_EXC_X = ('if', IT.A_(('chk', 'me', 'them', 'C')), ('if', IT.A_(('chk', 'me', 'C', 'C')), ('C',), ('C',)), ('D',))

CKPTS = (500, 1000, 2000, 5000, 10000)
FAMS = ('FP', 'core', 'nice', 'CBset', 'open', 'identity', 'EQten', 'FX')   # bit order of the family mask
SCAN_M = (0.0, 2e-4, 5e-4, 1e-3, 2e-3, 5e-3, None, 2e-2)                    # None = L's own identity mass m_L


class PO:
    """Families and seed laws on top of identity_tags_run.Static (the cached class table)."""

    def __init__(self, st=None):
        if st is None:
            import identity_tags_run as R
            st = R.Static()
        self.st = st
        A = st.A
        self.A = A
        self.U = st.U
        self.nc = st.nc
        self.mut = (A == 1) & (A.T == 1)
        self.lab = st.label()
        self.muL = st.class_prior('L')
        nm = st.named
        self.cbp = st.class_of(CBP_X, 0)
        self.cb, self.cc, self.xc, self.eq = nm['CB'], nm['Cc'], nm['XC'], nm['EQ']
        self.xb = st.class_of(XB_X, 0)
        self.M = st.family_mass()
        cl = st.families()['cliques']
        self.cliques = cl
        self.FP = self._heaviest(cl, self.cbp)
        self.FX = self._heaviest(cl, self.xc)
        self.core = np.array([x for x in self.FP if A[x, self.cc] == 0], np.int64)
        self.nice = np.array([x for x in self.FP if A[x, self.cc] == 1], np.int64)
        cat = st.cat
        dcb = cat.sx_dt[cat.sx_index[IT.CB_X]]
        self.CBset = np.unique(st.cos[np.nonzero(cat.sp_dt == dcb)[0]])
        self.ten_cb = st.heaviest_spellings_of_dt(IT.CB_X, 10)
        self.ten_eq = st.heaviest_spellings_of_dt(IT.EQ_X, 10)
        self.EQten = np.unique(st.cos[self.ten_eq])
        self.ident = np.nonzero(self.lab == 'identity')[0]
        self.allc = np.nonzero(st.allc)[0]
        self.NCB = st.open_neighbourhood()                       # establishers mutual with CB, and CB
        self.open = self.NCB
        rowc = (A == 1).all(1) | (A == 0).all(1)
        self.readers = ~rowc
        self.w0 = cat.spelling_weights() / cat.spelling_weights().sum()
        self.groups = dict(FP=self.FP, core=self.core, nice=self.nice, CBset=self.CBset, open=self.open,
                           identity=self.ident, EQten=self.EQten, FX=self.FX)
        self.famask = np.zeros(self.nc, np.int64)
        for b, f in enumerate(FAMS):
            self.famask[self.groups[f]] |= (1 << b)
        self.m_L = float(self.muL[self.ident].sum())

    def _heaviest(self, cl, c0):
        best, bm = None, -1.0
        for c in cl:
            if c0 in c:
                m = float(self.muL[c].sum())
                if m > bm:
                    best, bm = c, m
        return np.array(best, np.int64)

    # ---------------------------------------------------------------- seed laws
    def mask(self, cls):
        m = np.zeros(self.nc, bool)
        m[np.asarray(cls, np.int64)] = True
        return m

    def sp_of(self, cls):
        return np.nonzero(self.mask(cls)[self.st.cos])[0]

    def tilt(self, blocks, removed=()):
        """notes §1.6, the one fixed rule.  blocks: [(spellings, total mass | list of per-spelling masses)];
        removed: class sets whose spellings outside the blocks are set to 0; the rest is rescaled to 1 - block mass."""
        w = self.w0.copy()
        inblk = np.zeros(len(w), bool)
        for sp, _ in blocks:
            inblk[np.asarray(sp, np.int64)] = True
        rm = np.zeros(len(w), bool)
        for r in removed:
            rm |= self.mask(r)[self.st.cos]
        w[rm & ~inblk] = 0.0
        tot = sum(float(m) if np.isscalar(m) else float(sum(m)) for _, m in blocks)
        rest = ~inblk
        w[rest] = w[rest] / w[rest].sum() * (1.0 - tot)
        for sp, m in blocks:
            sp = np.asarray(sp, np.int64)
            if np.isscalar(m):
                w[sp] = self.w0[sp] / self.w0[sp].sum() * m
            else:
                w[sp] = np.asarray(m, float)
        return w

    def scan_weights(self, m, with_fp):
        """notes §1.7: identity group rescaled to m, F_P to M (second curve), the rest to the remainder."""
        I = self.mask(self.ident)[self.st.cos]
        F = self.mask(self.FP)[self.st.cos] if with_fp else np.zeros(len(self.w0), bool)
        assert not (I & F).any()
        w = self.w0.copy()
        R = ~(I | F)
        fm = self.M if with_fp else 0.0
        w[I] = self.w0[I] / self.w0[I].sum() * m
        if with_fp:
            w[F] = self.w0[F] / self.w0[F].sum() * fm
        w[R] = self.w0[R] / self.w0[R].sum() * (1.0 - m - fm)
        return w

    def cell_weights(self, cell):
        M = self.M
        ten_cb = (np.array(self.ten_cb), [M / 10] * 10)
        ten_eq = (np.array(self.ten_eq), [M / 20] * 10)
        FP, core, nice = self.sp_of(self.FP), self.sp_of(self.core), self.sp_of(self.nice)
        T = {
            'P1': ([(FP, M)], []),
            'P2': ([ten_cb], [self.NCB]),
            'P3': ([(FP, M)], [self.ident]),
            'P4': ([(FP, M)], [self.allc]),
            "P4'": ([ten_cb], [self.NCB, self.allc]),
            'P5': ([(FP, M / 2), ten_eq], []),
            'P1p': ([(core, M)], [self.nice]),
            'P2n': ([(nice, M)], [self.core]),
            'P3p': ([(core, M)], [self.nice, self.ident]),
            'P4p': ([(core, M)], [self.nice, self.allc]),
            'P4n': ([(nice, M)], [self.core, self.allc]),
            'P5p': ([(core, M / 2), ten_eq], [self.nice]),
        }
        if cell == 'L':
            return self.tilt([])
        if cell in T:
            return self.tilt(*T[cell])
        if cell.startswith('scan'):
            # scanA_<i> / scanB_<i> (B = with F_P at M)
            cur, i = cell[4], int(cell.split('_')[1])
            m = SCAN_M[i] if SCAN_M[i] is not None else self.m_L
            return self.scan_weights(m, cur == 'B')
        raise ValueError(cell)

    def class_prior(self, cell):
        """Class prior.  Cells whose law equals an identity-run prior use that prior's exact vector (same floats, so the
        paired seeds reproduce the identity run's runs): L, P2 (= T1c), scanA_0 (= no-clique), scanA_6 (= L).
        (scanB_6 is not P1: the scan holds the identity mass at m_L, P1 renormalizes it to 0.00883; notes §1.14.)"""
        st = self.st
        alias = {'L': 'L', 'P2': 'T1c', 'scanA_0': 'noclique', 'scanA_6': 'L'}
        if cell in alias:
            return st.class_prior(alias[cell])
        return st.mass(self.cell_weights(cell))

    # ---------------------------------------------------------------- statics
    def seed_payoff(self, mu):
        return self.U @ mu

    def block_masses(self, mu):
        g = {k: float(mu[v].sum()) for k, v in self.groups.items()}
        g['allc'] = float(mu[self.allc].sum()); g['D'] = float(mu[self.st.iD])
        return g

    def paths(self):
        """notes §1.5 (iii): compatibility paths of length <= 3 between F_P and F_X in the establisher graph."""
        est = np.nonzero(self.st.est)[0]
        mut = self.mut
        FPs, FXs = set(self.FP.tolist()), set(self.FX.tolist())
        d1 = [(int(a), int(b)) for a in self.FP for b in self.FX if mut[a, b]]
        mid = [int(x) for x in est if x not in FPs | FXs and mut[x, self.FP].any() and mut[x, self.FX].any()]
        A1 = [int(x) for x in est if x not in FPs and mut[x, self.FP].any()]
        B1 = set(int(x) for x in est if x not in FXs and mut[x, self.FX].any())
        n3 = 0
        for a in A1:
            nb = np.nonzero(mut[a, est])[0]
            n3 += sum(1 for b in est[nb] if int(b) in B1 and int(b) != a)
        bridges = [int(x) for x in np.nonzero(self.st.selfc)[0] if mut[x, self.cbp] and mut[x, self.xc] and x not in (self.cbp, self.xc)]
        return dict(direct=d1, n_direct=len(d1), direct_FX_members=sorted({b for _, b in d1}),
                    mid=mid, n_mid=len(mid), mass_mid=float(self.muL[mid].sum()), n_len3_pairs=int(n3),
                    cbp_xc_bridges=bridges, mass_bridges=float(self.muL[bridges].sum()))

    def ninv(self, c):
        U = self.U
        return int((U[:, c] > U[c, c] + 1e-9).sum())


# -------------------------------------------------------------------- stages (notes §1.10)
def stage_stats(c0, zg, fh, held_ck, ckpts=CKPTS):
    """Per-family stage statistics for one run.
    c0[i]: initial count on island i; zg[i]: generation of the first zero (-1 never); fh[i]: first hold check (-1 never);
    held_ck[t, i]: held by the family at checkpoint t.  Returns a dict of counts at each checkpoint."""
    c0 = np.asarray(c0); zg = np.asarray(zg); fh = np.asarray(fh); held_ck = np.asarray(held_ck, bool)
    occ = c0 > 0
    seeded = occ & (fh >= 0) & ((zg < 0) | (zg >= fh))
    out = dict(n0=int(c0.sum()), occupied=int(occ.sum()), est_times=[int(x) for x in fh[seeded]])
    for t, T in enumerate(ckpts):
        se = seeded & (fh <= T)
        ext = occ & (zg >= 0) & (zg < T) & ((fh < 0) | (zg < fh))
        held = held_ck[t]
        out[T] = dict(seeded_est=int(se.sum()), extinct=int(ext.sum()), held=int(held.sum()),
                      persist=int((se & held).sum()), spread=int((held & ~seeded).sum()))
    return out


# -------------------------------------------------------------------- the 50% crossing (notes §1.11)
def crossing(ms, f, level=0.5):
    """First m at which f falls through `level`, interpolated linearly in log m (linearly in m on the first interval
    when it starts at 0).  Returns (m*, flag) with flag 'ok', 'below' (f < level already at the first point) or
    'above' (f >= level at every point; m* = the last m)."""
    ms = np.asarray(ms, float); f = np.asarray(f, float)
    if f[0] < level:
        return float(ms[0]), 'below'
    for j in range(1, len(ms)):
        if f[j] < level:
            a, b = ms[j - 1], ms[j]
            fa, fb = f[j - 1], f[j]
            t = (fa - level) / (fa - fb)
            if a <= 0:
                return float(a + t * (b - a)), 'ok'
            return float(np.exp(np.log(a) + t * (np.log(b) - np.log(a)))), 'ok'
    return float(ms[-1]), 'above'


def bootstrap_crossing(ms, X, B=2000, seed=0, level=0.5):
    """X[j, r] = 1 if run r of scan point j is universal (replicates paired across points).  Paired bootstrap over
    replicate indices.  Returns (m*, flag, lo, hi, samples)."""
    X = np.asarray(X, float)
    m0, fl = crossing(ms, X.mean(1), level)
    rng = np.random.default_rng(seed)
    R = X.shape[1]
    s = []
    for _ in range(B):
        idx = rng.integers(0, R, R)
        s.append(crossing(ms, X[:, idx].mean(1), level)[0])
    s = np.array(s)
    return m0, fl, float(np.quantile(s, 0.025)), float(np.quantile(s, 0.975)), s


def fit_exp(ms, f, prefactor=False):
    """Least squares f ~ f0 exp(-6400 m q) (f0 = 1 unless prefactor) on the given points (grid search + refine)."""
    ms = np.asarray(ms, float); f = np.asarray(f, float)
    best = None
    for q in np.concatenate([np.linspace(0, 0.5, 5001)]):
        e = np.exp(-6400.0 * ms * q)
        f0 = 1.0
        if prefactor:
            f0 = float((e @ f) / max(e @ e, 1e-300))
        r = f - f0 * e
        sse = float(r @ r)
        if best is None or sse < best[0]:
            best = (sse, q, f0)
    return dict(q=best[1], f0=best[2], sse=best[0])


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))
