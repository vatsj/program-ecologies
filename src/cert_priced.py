"""Certificate pricing for the priced modal arm (predictions/2026-10-01-cert-pricing.md).

Lazy pricing (src/modal.py: build_priced(pricing='lazy')) makes a check free against constant opponents and
exact copies, and charges the atoms price c * k(x) * (1 + settle world of x's atoms against y) against
everything else.  It rewards sameness.  Certificate pricing keeps lazy's price function and changes only
the free set:

    x's check of y is free iff y's action toward x is decided in PA + l * Con   (cert level l)

i.e. PA (l = 0) or PA + Con(PA) (l = 1) proves "y plays C against x" or proves "y plays D against x".
On the linear GL chain this is: y's value toward x is constant on worlds >= l, read off the evaluator's
hc[l, y, x] / hd[l, y, x] at stabilization.  Constants are always certified, so a check of C or D is free
under every variant.

Variants (the `pricing` argument):
  'cert0'  free iff y's action toward x is PA-decided (primary)
  'cert1'  free iff decided in PA + Con(PA) (looser)
  'certC'  free iff y is a constant or PA proves y cooperates with x (cooperation-only reading)
  'lazy', 'atoms' (c = 0 is the free arm): the existing references, rebuilt here from the same evaluator.
Controls added after review [after review]:
  'mono'       syntactic: free iff y is constant, or y is monotone in its box atoms and (y cooperates with x, or
               y's world-0 action is D).  Fable: cert0 should coincide with this on almost all mass.
  'cert0flat'  cert0's free set, flat price c per non-free check (no atom or settle-world multiplier).
  'lazycert0'  union of lazy's and cert0's free sets: copies always free, plus certified cross-reads.
  'cert0diag'  constants free; copies free only if the self-play is PA-decided; no cross-program exemption.
  'cert0v'     cert0, plus a verification charge of c/10 on every free check by a program with boxes.
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from abm import njit
import modal as M


@njit(cache=True)
def _evaluate_cert(nat, ak, al, af, aa, tt, max_worlds):
    """As modal._evaluate_priced without cliques, also returning hc, hd at stabilization:
    hc[l, x, y] = x plays C against y at every world >= l (likewise hd for D)."""
    K = nat.shape[0]
    hc = np.ones((2, K, K), np.bool_)
    hd = np.ones((2, K, K), np.bool_)
    val = np.zeros((K, K), np.int8)
    prev = -np.ones((K, K), np.int64)
    last = np.zeros((K, K), np.int64)
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
                if prev[x, y] >= 0 and idx != prev[x, y]:
                    last[x, y] = n
                prev[x, y] = idx
                val[x, y] = (tt[x] >> idx) & 1
        changed = False
        for L in range(2):
            if n < L:
                continue
            for x in range(K):
                for y in range(K):
                    c = val[x, y] == 1
                    if hc[L, x, y] and not c:
                        hc[L, x, y] = False; changed = True
                    if hd[L, x, y] and c:
                        hd[L, x, y] = False; changed = True
        if not changed and n >= 2:
            return val, n, last, hc, hd
    return val, -1, last, hc, hd


_CACHE = {}


def evaluate_lang(n, kinds=((0, 0), (1, 0), (0, 1), (1, 1))):
    key = (n, tuple(kinds))
    if key not in _CACHE:
        L = M.ModalLanguage(n, kinds)
        arrs = L.arrays()
        val, worlds, last, hc, hd = _evaluate_cert(*arrs, 200)
        if worlds < 0:
            raise RuntimeError('evaluation did not stabilize')
        _CACHE[key] = (L, arrs, val, worlds, last, hc, hd)
    return _CACHE[key]


def free_mask(pricing, nat, hc, hd):
    """free[x, y] = True iff x's check of y costs nothing."""
    K = len(nat)
    const = nat == 0
    if pricing == 'lazy':
        F = np.zeros((K, K), bool); F[:, const] = True; np.fill_diagonal(F, True); return F
    if pricing == 'atoms':
        F = np.zeros((K, K), bool); return F
    if pricing == 'cert0':
        return (hc[0] | hd[0]).T.copy()          # [x, y] <- y's action toward x decided in PA
    if pricing == 'cert1':
        return (hc[1] | hd[1]).T.copy()
    if pricing == 'certC':
        F = hc[0].T.copy(); F[:, const] = True; return F
    if pricing in ('cert0flat', 'cert0v'):
        return free_mask('cert0', nat, hc, hd)
    if pricing == 'lazycert0':
        return free_mask('lazy', nat, hc, hd) | free_mask('cert0', nat, hc, hd)
    if pricing == 'cert0diag':
        F = np.zeros((K, K), bool); F[:, const] = True
        d = free_mask('cert0', nat, hc, hd).diagonal().copy()
        F[np.arange(K), np.arange(K)] |= d
        return F
    raise ValueError(pricing)


def monotone(tt, k):
    """Is the truth table tt over k atoms monotone non-decreasing in every atom?"""
    for j in range(k):
        for i in range(1 << k):
            if not (i >> j) & 1 and ((tt >> i) & 1) > ((tt >> (i | (1 << j))) & 1):
                return False
    return True


def free_mask_mono(nat, tt, val):
    """Syntactic control: free iff y constant, or y monotone and (y plays C toward x, or y's default is D)."""
    K = len(nat)
    mono = np.array([monotone(int(tt[y]), int(nat[y])) for y in range(K)])
    default_c = np.array([(int(tt[y]) >> ((1 << int(nat[y])) - 1)) & 1 for y in range(K)])  # all atoms true
    F = np.zeros((K, K), bool)
    for y in range(K):
        if nat[y] == 0:
            F[:, y] = True
        elif mono[y]:
            F[:, y] = (val[y, :] == 1) | (default_c[y] == 0)
    return F, mono


def build_cert(n, c=0.0, pricing='cert0', pay=M.PD, kinds=((0, 0), (1, 0), (0, 1), (1, 1))):
    """Returns L, val, worlds, prov, extra (dict with cost, free, hc, hd at canonical level)."""
    L, arrs, val, worlds, last, hc, hd = evaluate_lang(n, kinds)
    nat = arrs[0]
    U, PCC = M.pd_payoffs(val, pay)
    U = U.astype(float)
    if pricing == 'cert0flat':
        cost = c * (nat[:, None] > 0).astype(float) * np.ones_like(last, dtype=float)
    else:
        cost = c * nat[:, None].astype(float) * (1.0 + last)      # the atoms price, as in build_priced
    if pricing == 'mono':
        F, _ = free_mask_mono(nat, arrs[5], val)
    else:
        F = free_mask(pricing, nat, hc, hd)
    cost[F] = 0.0
    if pricing == 'cert0v':
        cost[F & (nat[:, None] > 0)] = c / 10.0
    U = U - cost
    prov = M.ModalProvider(U, PCC, L.mu_canon, list(L.rep), L.bits_canon)
    prov.sizes = np.array([L.count_canon[m].sum() for m in prov.members])
    extra = dict(cost=cost, free=F, hc=hc, hd=hd, last=last, nat=nat)
    return L, val, worlds, prov, extra
