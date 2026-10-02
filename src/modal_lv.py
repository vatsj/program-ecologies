"""Modal arm with more proof levels (predictions/2026-10-02-drift-closure.md).

modal.py allows boxes at level 0 (PA) and level 1 (PA + Con(PA)).  Second-order prudence ("cooperate iff you
provably cooperate with me and provably defect on ALLC") needs level 2: P_C = and(BOX(THEM(ME)), BOXD_L(THEM(^C)))
must prove that P_C itself defects on ALLC, and P_C's defection on ALLC holds only from world 2 on (every box is
vacuously true at worlds 0 and 1 for level 1), so with L = 1 P_C defects on itself.  This module is modal.py with
levels 0..Lmax: BOX_L(s) holds at world n iff s holds at every world m with L <= m < n, i.e. provability in
PA + Con^L(PA) on the linear GL chain.  Names print the level as a suffix (BOX2, BOXD2).  A labelled grammar choice.
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from abm import njit
import modal as M


class ModalLanguageLv(M.ModalLanguage):
    def _src_box(self, kind, level, form, arg):
        inner = {M.TM: 'THEM(ME)', M.TT: 'THEM(THEM)'}.get(form) or 'THEM(^%s)' % self.rep[arg]
        return '%s%s(%s)' % ('BOX' if kind == M.KC else 'BOXD', str(level) if level else '', inner)


@njit(cache=True)
def _evaluate_lv(nat, ak, al, af, aa, tt, nlev, max_worlds):
    K = nat.shape[0]
    hc = np.ones((nlev, K, K), np.bool_)
    hd = np.ones((nlev, K, K), np.bool_)
    val = np.zeros((K, K), np.int8)
    for n in range(max_worlds):
        for x in range(K):
            for y in range(K):
                idx = 0
                for j in range(nat[x]):
                    f = af[x, j]
                    if f == 0:
                        p, q = y, x
                    elif f == 1:
                        p, q = y, y
                    else:
                        p, q = y, aa[x, j]
                    L = al[x, j]
                    b = hc[L, p, q] if ak[x, j] == 0 else hd[L, p, q]
                    if b: idx |= 1 << j
                val[x, y] = (tt[x] >> idx) & 1
        changed = False
        for L in range(nlev):
            if n < L:
                continue
            for x in range(K):
                for y in range(K):
                    c = val[x, y] == 1
                    if hc[L, x, y] and not c:
                        hc[L, x, y] = False; changed = True
                    if hd[L, x, y] and c:
                        hd[L, x, y] = False; changed = True
        if not changed and n >= nlev:
            return val, n
    return val, -1


def build_lv(n, lmax=2, pay=M.PD):
    kinds = tuple((k, l) for l in range(lmax + 1) for k in (M.KC, M.KD))
    L = ModalLanguageLv(n, kinds)
    val, worlds = _evaluate_lv(*L.arrays(), lmax + 1, 300)
    if worlds < 0:
        raise RuntimeError('modal evaluation did not stabilize')
    U, PCC = M.pd_payoffs(val, pay)
    prov = M.ModalProvider(U, PCC, L.mu_canon, L.rep, L.bits_canon)
    prov.sizes = np.array([L.count_canon[m].sum() for m in prov.members])
    return L, val, worlds, prov
