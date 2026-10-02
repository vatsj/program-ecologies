"""Background-fringe and prior-boost variants of the free modal arm (predictions/2026-10-02-drift-closure.md).

Fringe: every program also meets a fixed background population nu with weight delta, so the payoff matrix becomes
    U'[x, y] = U[x, y] + delta * f(x),   f(x) = sum_q nu(q) U[x, q].
The fringe is held fixed: it is not the resident population and it does not evolve.  Kinds:
    'D'   nu = DefectBot only: f(x) = u(x, D).  Charges cooperation with D (suckerability by D), nothing else.
    'CD'  nu = 1/2 ALLC + 1/2 DefectBot: also rewards exploiting ALLC.
    'mu'  nu = the mutation prior over classes (diagnostic).
delta = 0 is the free modal arm (modal.build).  Members of a behavioural class have identical rows, so f is
constant on classes and the class merge stays exact.

Prior boost (a labelled prior choice, not a mechanism): give one class the prior mass of another (e.g. PrudentBot
at FairBot's mass, as if PrudentBot were a 3-node primitive), then renormalize.
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import modal as M

FB = 'BOX(THEM(ME))'
FB1 = 'BOX1(THEM(ME))'
PB = 'and(BOX(THEM(ME)),BOXD1(THEM(^D)))'
PSTAR = 'and(BOX1(THEM(ME)),not(BOX(THEM(ME))))'
BTT = 'BOX(THEM(THEM))'

_CACHE = {}


def base(n):
    if n not in _CACHE:
        _CACHE[n] = M.build(n)
    return _CACHE[n]


def fringe_vector(prov, kind):
    names = prov.names; U = prov.Ufull
    mu = np.array([c[2] for c in prov.classes])
    iC, iD = names.index('C'), names.index('D')
    if kind == 'D':
        return U[:, iD].copy()
    if kind == 'CD':
        return 0.5 * (U[:, iC] + U[:, iD])
    if kind == 'mu':
        return U @ (mu / mu.sum())
    raise ValueError(kind)


class _Prov(M.ModalProvider):
    """A ModalProvider with a replaced payoff matrix and prior (same classes)."""
    def __init__(self, src, U, mu):
        self.__dict__.update(src.__dict__)
        self.Ufull = U
        mu = np.asarray(mu, float); mu = mu / mu.sum()
        self.classes = [(i, [i], float(mu[i])) for i in range(len(mu))]


P12B = 'and(and(BOX1(THEM(ME)),not(BOX(THEM(^C)))),BOXD2(THEM(^D)))'


def base_extra(n, extra):
    """L_n plus extra programs (possibly longer than n, possibly using PA + Con^2 boxes), each with the prior mass
    of FairBot: a labelled grammar choice ('as if it were a 3-node primitive').  extra: tuple of names from EXTRAS."""
    key = (n, extra)
    if key not in _CACHE:
        import modal_lv as LV
        L = LV.ModalLanguageLv(n)
        o = L.op; b = lambda k, l, f, a=None: o((k, l, f), a)
        ids = [EXTRAS[e](o, b) for e in extra]
        val, worlds = LV._evaluate_lv(*L.arrays(), 3, 300)
        if worlds < 0:
            raise RuntimeError('did not stabilize')
        U, PCC = M.pd_payoffs(val, M.PD)
        K0 = len(L.mu_canon); K = len(L.funcs)
        iFB = L.op((0, 0, M.TM))
        mu = np.zeros(K); mu[:K0] = L.mu_canon
        bits = np.full(K, 1e9); bits[:K0] = L.bits_canon
        names = list(L.rep) + [None] * (K - K0)
        for e, c in zip(extra, ids):
            if c < K0 or names[c] is not None:      # already in L_n, or a duplicate of another extra: skip
                continue
            mu[c] = L.mu_canon[iFB]; bits[c] = L.bits_canon[iFB]; names[c] = e
        keep = [c for c in range(K) if mu[c] > 0]          # drop helper sub-formulas created by op
        U = U[np.ix_(keep, keep)]; PCC = PCC[np.ix_(keep, keep)]
        prov = M.ModalProvider(U, PCC, mu[keep], [names[c] for c in keep], bits[keep])
        _CACHE[key] = (L, val, worlds, prov)
    return _CACHE[key]


EXTRAS = {
    P12B: lambda o, b: o('and', o('and', b(0, 1, M.TM), o('not', b(0, 0, M.TL, o('C')))), b(1, 2, M.TL, o('D'))),
}
# [after review, fable/astra] P12b's same-size siblings: the first atom over {THEM(ME), THEM(THEM)}, the negated box
# over {^C, THEM(ME), THEM(THEM)}; each at FairBot's mass, so the language covers P12b's neighbourhood evenly.
P12B_SIBS = []
for _f1 in (M.TM, M.TT):
    for _f2, _lab2 in (((M.TL, 'C'), 'THEM(^C)'), ((M.TM, None), 'THEM(ME)'), ((M.TT, None), 'THEM(THEM)')):
        _nm = 'and(and(BOX1(%s),not(BOX(%s))),BOXD2(THEM(^D)))' % ('THEM(ME)' if _f1 == M.TM else 'THEM(THEM)', _lab2)
        if _nm == P12B:
            continue
        EXTRAS[_nm] = (lambda f1, f2: lambda o, b: o('and', o('and', b(0, 1, f1), o('not', b(0, 0, f2[0], o(f2[1]) if f2[1] else None))),
                                                     b(1, 2, M.TL, o('D'))))(_f1, _f2)
        P12B_SIBS.append(_nm)


def build_variant(n, delta=0.0, kind='D', boost=None, extra=()):
    """boost: None or (target_name, source_name): set mu(target) = mu(source) before renormalizing.
    extra: names from EXTRAS added at FairBot's prior mass (base_extra)."""
    L, val, worlds, prov = base_extra(n, tuple(extra)) if extra else base(n)
    U = prov.Ufull.astype(float).copy()
    if delta:
        U = U + delta * fringe_vector(prov, kind)[:, None]
    mu = np.array([c[2] for c in prov.classes])
    if boost is not None:
        t, s = boost
        mu = mu.copy(); mu[prov.names.index(t)] = mu[prov.names.index(s)]
    p = _Prov(prov, U, mu)
    return L, p
