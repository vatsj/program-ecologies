"""Arms of the pair-worth easy case along N (spec specs/2026-11-03-pair-worth-n.md; notes/pair-worth-n.md).

New on top of the stored machinery (src/pair_worth.py, unedited):
  F(sigma_i; c)   flexible grand bid: grand line over every feasible pair (a, b) of the others' grand demands (one decision-list
                  line per pair), then the two level-1 exclusion handshakes, then c.
  F4              F with sigma_i <= 4 only.   FM (F-minus): F's grand lines, then c (no handshakes).
  B*_k            C founders plus exactly k copies per slot of B*(sigma; c) on one split per island (fixed-count inoculation).
Importable without side effects.
"""
import os, sys
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pair_worth as PW

GNAME = 'pw13'
SPL28 = PW.splits(6)
SH28 = np.array([s[0] for s in SPL28], np.int64)        # first coordinate of the m-th split (ascending: 7, 6, ..., 1 splits)
F_KINDS = ('F', 'F4', 'FM')
CODES = {'B': 1, 'G': 4, 'F': 3, 'F4': 3, 'FM': 3}


def F_program(G, s, share, c, fallback=True):
    """(lines, default) of F(share; c) in slot s (G1/3, sixths).  Grand lines at level 0, handshakes at level 1."""
    j, k = PW.others(s)
    Gd = G.Gd
    lines = []
    for a in range(Gd + 1):
        for b in range(Gd + 1 - a):
            if a + b <= Gd - share:
                lines.append(([(j, G.act(j, PW.ALL, a), 0, 1), (k, G.act(k, PW.ALL, b), 0, 1)], G.act(s, PW.ALL, share)))
    if fallback:
        lines += PW._pair_lines(G, s, (share, share, share), 1)
    return (lines, c)


class FamilyN(PW.Family):
    def __init__(self, kind, sigmas, dose):
        self.kind, self.sigmas, self.dose = kind, sigmas, dose
        self.code = CODES[kind]


class MenuN(PW.Menu):
    """Menu with the flexible-bid families.  F member ids are (share, c) pairs: id = off + share * nact + c."""

    def prog(self, s, m):
        fi, si, c = self.decode(m)
        if fi >= 0 and self.fams[fi].kind in F_KINDS:
            f = self.fams[fi]
            return F_program(self.G, s, f.sigmas[si][0], c, fallback=(f.kind != 'FM'))
        return super().prog(s, m)

    def draw(self, u1, u2, u3, u4=None):
        n = self.G.nact
        m = np.minimum((u1 * n).astype(np.int64), n - 1)
        lo = 0.0
        for fi, f in enumerate(self.fams):
            hi = self.cum[fi]
            sel = (u2 >= lo) & (u2 < hi)
            if f.kind in F_KINDS:
                M = 25 if f.kind == 'F4' else 28
                tot = M * n
                memb = np.minimum((u3 * tot).astype(np.int64), tot - 1)          # same decomposition as B*: member = n * m + c
                mi = memb // n; cc = memb % n
                mem = SH28[mi] * n + cc
            else:
                mem = np.minimum((u3 * self.size[fi]).astype(np.int64), self.size[fi] - 1)
            m = np.where(sel, self.off[fi] + mem, m)
            lo = hi
        return m


def arm_menu_n(arm, delta=0.05):
    G = PW.get_game(GNAME)
    if arm in ('C', 'CB', 'CBs', 'CG', 'CA'):
        return PW.arm_menu(GNAME, arm, delta)
    if arm == 'CF':
        return MenuN(G, [FamilyN('F', [(s,) for s in range(7)], delta)])
    if arm == 'CF4':
        return MenuN(G, [FamilyN('F4', [(s,) for s in range(5)], delta)])
    if arm == 'CFm':
        return MenuN(G, [FamilyN('FM', [(s,) for s in range(7)], delta)])
    if arm in ('CBk1', 'CBk4'):                    # C law (dose 0); the named copies are placed explicitly
        return PW.Menu(G, [PW.Family('B', PW.bid_sigmas(GNAME, 'all'), 0.0)])
    raise ValueError(arm)


def founders_bk(menu, N, r, I, k):
    """C founders (dose 0 reproduces C's draws exactly) with k copies per slot of B*(sigma; c) on one split per island."""
    base = '%s|N%d|I%d' % (GNAME, N, I)
    f = PW.draw_founders(menu, base, r, I, N).copy()
    assert (f < menu.G.nact).all()
    rng = np.random.default_rng(PW.seed_int('Bk', k, N, r))
    for i in range(I):
        sig = SPL28[int(rng.integers(len(SPL28)))]
        for s in range(3):
            pos = rng.choice(N, size=k, replace=False)
            for p in pos:
                f[i, s, p] = menu.member_id('B', sig, int(f[i, s, p]))
    return f
