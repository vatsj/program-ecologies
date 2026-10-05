"""A semantic legibility gate on the modal arm (specs/2026-10-04-bounded-provers.md;
predictions/2026-10-04-bounded-provers.md).

This is NOT a bounded-Loeb implementation.  The cost of x reading y is semantic stabilization,
    v(x, y) = k(y) * (1 + settle(y, x)),
with k(y) the number of y's essential box atoms and settle(y, x) the last world at which y's atom-value
vector against x changes (modal._evaluate_priced's `last`), read off the *bounded* trace.  Constants cost 0.
x's boxes reading y are open iff v(x, y) <= b(x); a closed gate makes every box atom of x false at every
world (BOX_b, BOXD_b, BOX1_b, BOXD1_b alike).  Costs and plays are mutually dependent, so the bounded game is
a joint fixed point: free play -> costs -> gate -> re-evaluate -> costs ... until the gate repeats.

Arms (`build_arm`):
  ('global', b)      every reader has budget b (b = inf is the free arm)
  ('random', b)      control: as many (k(x) > 0, k(y) > 0) pairs masked as the global-b gate, at random, fixed seed
  ('atom', b)        control: mask iff k(y) > b
  ('fixed', None)    per-program budgets b in {1..4}, no node cost: mu(f)/4 per budget
  ('penal', None)    per-program budgets, annotation costs b nodes, length prior recomputed
  ('clique', None)   free arm plus one clique spelling at FairBot's mass (modal.build_priced(n, 0, m_cliques=1))
"""
import os, sys, json, time, hashlib
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from abm import njit
import modal as M

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INF = float('inf')
FB = 'BOX(THEM(ME))'
PB = 'and(BOX(THEM(ME)),BOXD1(THEM(^D)))'
PSTAR = 'and(BOX1(THEM(ME)),not(BOX(THEM(ME))))'
BUDGETS = (1, 2, 3, 4, 6, 8, INF)
PP_BUDGETS = (1, 2, 3, 4)


@njit(cache=True)
def _evaluate_gated(nat, ak, al, af, aa, tt, gate, nlev, max_worlds):
    """modal._evaluate_priced with a fixed gate: gate[x, y] = 0 makes every box atom of x false at every
    world when x reads y.  Returns val, stable world (-1 if none), last (world of the last change of x's
    atom vector against y), hc, hd."""
    K = nat.shape[0]
    hc = np.ones((nlev, K, K), np.bool_)
    hd = np.ones((nlev, K, K), np.bool_)
    val = np.zeros((K, K), np.int8)
    prev = -np.ones((K, K), np.int64)
    last = np.zeros((K, K), np.int64)
    for n in range(max_worlds):
        for x in range(K):
            for y in range(K):
                idx = 0
                if gate[x, y]:
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
            return val, n, last, hc, hd
    return val, -1, last, hc, hd


@njit(cache=True)
def _evaluate_online(nat, ak, al, af, aa, tt, bvec, nlev, max_worlds):
    """World-indexed (online) gate, the adopted semantics after the joint iteration cycled: at world n, x's boxes
    reading y are open iff k(y) * (1 + last_{<n}(y, x)) <= b(x), with last_{<n} the last world < n at which y's
    atom vector against x changed.  Cost is non-decreasing in n, so a gate closes at most once and box truth
    (hc and gate) is monotone non-increasing: the trace settles, with no fixed point to select.
    Returns val, stable world, last, hc, hd, final gate, close_world (world the gate closed, -1 if open)."""
    K = nat.shape[0]
    hc = np.ones((nlev, K, K), np.bool_)
    hd = np.ones((nlev, K, K), np.bool_)
    val = np.zeros((K, K), np.int8)
    prev = -np.ones((K, K), np.int64)
    last = np.zeros((K, K), np.int64)
    gate = np.ones((K, K), np.bool_)
    closew = -np.ones((K, K), np.int64)
    for n in range(max_worlds):
        changed = False
        # gate at world n from the trace before n
        for x in range(K):
            for y in range(K):
                if gate[x, y] and nat[y] * (1 + last[y, x]) > bvec[x]:
                    gate[x, y] = False; closew[x, y] = n; changed = True
        for x in range(K):
            for y in range(K):
                idx = 0
                if gate[x, y]:
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
                    last[x, y] = n; changed = True
                prev[x, y] = idx
                val[x, y] = (tt[x] >> idx) & 1
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
            return val, n, last, hc, hd, gate, closew
    return val, -1, last, hc, hd, gate, closew


@njit(cache=True)
def _soundness(nat, ak, al, af, aa, gate, val, hc, hd):
    """Every open atom that is true at the stable world names a proposition that holds in the stable bounded
    play.  Returns (number of true open atoms checked, violations) by kind/level: arrays [kind, level]."""
    K = nat.shape[0]
    nlev = hc.shape[0]
    checked = np.zeros((2, nlev), np.int64); bad = np.zeros((2, nlev), np.int64)
    for x in range(K):
        for y in range(K):
            if not gate[x, y]:
                continue
            for j in range(nat[x]):
                f = af[x, j]
                if f == 0:
                    p, q = y, x
                elif f == 1:
                    p, q = y, y
                else:
                    p, q = y, aa[x, j]
                L = al[x, j]; kd = ak[x, j]
                tru = hc[L, p, q] if kd == 0 else hd[L, p, q]
                if tru:
                    checked[kd, L] += 1
                    want = 1 if kd == 0 else 0
                    if val[p, q] != want:
                        bad[kd, L] += 1
    return checked, bad


def online(arr, bvec, nlev=2, max_worlds=300):
    """Adopted semantics (world-indexed gate), with the soundness check and a Gamma-consistency diagnostic:
    re-evaluating with the final gate held fixed from world 0, how many plays differ."""
    nat, ak, al, af, aa, tt = arr
    bv = np.asarray(bvec, float)
    val, w, last, hc, hd, gate, closew = _evaluate_online(nat, ak, al, af, aa, tt, bv, nlev, max_worlds)
    assert w >= 0, 'online evaluation did not settle'
    checked, bad = _soundness(nat, ak, al, af, aa, gate, val, hc, hd)
    gam = cost_matrix(nat, last) <= bv[:, None]
    v2, w2, l2, _, _ = _evaluate_gated(nat, ak, al, af, aa, tt, gate, nlev, max_worlds)
    return dict(val=val, last=last, gate=gate, worlds=w, closew=closew, sound_checked=checked, sound_bad=bad,
                gate_consistent=bool(np.array_equal(gam, gate)), fixed_gate_play_diff=int((v2 != val).sum()),
                hc=hc, hd=hd)


def cost_matrix(nat, last):
    """v[x, y] = k(y) * (1 + last[y, x])."""
    return nat[None, :].astype(float) * (1.0 + last.T.astype(float))


def joint_fixed_point(arr, bvec, nlev=2, max_rounds=60, max_worlds=300):
    """Iterate free play -> costs -> gate -> bounded play until the gate repeats.  bvec[x] = reader x's budget."""
    nat, ak, al, af, aa, tt = arr
    K = len(nat)
    gate = np.ones((K, K), np.bool_)
    val, w, last, hc, hd = _evaluate_gated(nat, ak, al, af, aa, tt, gate, nlev, max_worlds)
    assert w >= 0
    free_val, free_last = val.copy(), last.copy()
    bcol = np.asarray(bvec, float)[:, None]
    gate_free = cost_matrix(nat, free_last) <= bcol
    seen = {hashlib.sha1(gate.tobytes()).hexdigest(): 0}
    rounds = 0; cycle = None; history = []
    while True:
        new = cost_matrix(nat, last) <= bcol
        if np.array_equal(new, gate):
            break
        h = hashlib.sha1(new.tobytes()).hexdigest()
        if h in seen:
            cycle = (seen[h], rounds + 1)
        seen[h] = rounds + 1
        history.append(int((new != gate).sum()))
        gate = new; rounds += 1
        val, w, last, hc, hd = _evaluate_gated(nat, ak, al, af, aa, tt, gate, nlev, max_worlds)
        assert w >= 0
        if cycle is not None or rounds >= max_rounds:
            break
    checked, bad = _soundness(nat, ak, al, af, aa, gate, val, hc, hd)
    return dict(val=val, last=last, gate=gate, worlds=w, rounds=rounds, cycle=cycle, converged=cycle is None and rounds < max_rounds,
                changes=history, free_val=free_val, free_last=free_last, gate_free=gate_free,
                sound_checked=checked, sound_bad=bad, hc=hc, hd=hd)


# ------------------------------------------------------------------ languages and arms
_LANG = {}


def lang(n):
    if n not in _LANG:
        _LANG[n] = M.ModalLanguage(n)
    return _LANG[n]


def genotypes(L, budgets=PP_BUDGETS):
    """Per-program budgets: constants unannotated; each non-constant canonical f gets (f, b).  A quoted argument
    ^A inside (f, b) is evaluated as (A, b).  Returns arrays, bvec, base (canon id per genotype), gb (budget)."""
    nat0, ak0, al0, af0, aa0, tt0 = L.arrays()
    K0 = len(nat0)
    const = [c for c in range(K0) if nat0[c] == 0]
    nonc = [c for c in range(K0) if nat0[c] > 0]
    gid = {}
    base = []; gb = []
    for c in const:
        gid[(c, None)] = len(base); base.append(c); gb.append(INF)
    for b in budgets:
        for c in nonc:
            gid[(c, b)] = len(base); base.append(c); gb.append(b)
    G = len(base); base = np.array(base); gb = np.array(gb, float)
    nat, ak, al, af, tt = nat0[base], ak0[base], al0[base], af0[base], tt0[base]
    aa = np.zeros_like(aa0[base])
    for g in range(G):
        c = base[g]
        for j in range(nat[g]):
            if af[g, j] == M.TL:
                A = aa0[c, j]
                aa[g, j] = gid[(A, None)] if nat0[A] == 0 else gid[(A, gb[g])]
    return (nat, ak, al, af, aa, tt), gb, base, gid


def penal_prior(L, base, gb):
    """Length prior over the extended language where the budget annotation costs b nodes."""
    n = L.n; cnt = L.cnt_by_size
    nat0 = L.arrays()[0]
    a = np.zeros(n + 1)
    for s in range(1, n + 1):
        for c, m in cnt[s].items():
            if nat0[c] == 0:
                a[s] += m
            else:
                for b in PP_BUDGETS:
                    if s + b <= n: a[s + b] += m
    mu = np.zeros(len(base))
    for g in range(len(base)):
        c = base[g]; b = gb[g]
        for s in range(1, n + 1):
            m = cnt[s].get(c, 0)
            if not m: continue
            t = s if not np.isfinite(b) else s + int(b)
            if t <= n:
                mu[g] += m / (a[t] * 2.0 * t * t)
    return mu


def random_gate(gate, nat, seed=12345):
    """Matched-frequency random mask over pairs with k(x) > 0 and k(y) > 0."""
    K = len(nat)
    elig = (nat[:, None] > 0) & (nat[None, :] > 0)
    nmask = int((elig & ~gate).sum())
    idx = np.flatnonzero(elig.ravel())
    rng = np.random.default_rng(seed)
    pick = rng.choice(idx, nmask, replace=False)
    g = np.ones(K * K, np.bool_); g[pick] = False
    return g.reshape(K, K)


def _joint_summary(j, fp):
    """The spec's synchronous joint iteration, kept as a reported diagnostic."""
    return dict(rounds=j['rounds'], cycle=j['cycle'], converged=j['converged'], changes=j['changes'],
                play_diff_vs_online=int((j['val'] != fp['val']).sum()), gate_diff_vs_online=int((j['gate'] != fp['gate']).sum()),
                free_gate_diff_vs_online=int((j['gate_free'] != fp['gate']).sum()))


_ARMS = {}


def build_arm(n, kind, b=None):
    """Returns dict(prov, names, U, PCC, val, gate, fp (fixed-point info or None), mu, base, gb, members)."""
    key = (n, kind, b)
    if key in _ARMS:
        return _ARMS[key]
    L = lang(n)
    if kind == 'clique':
        Lc, val, worlds, prov = M.build_priced(n, 0.0, m_cliques=1)
        out = dict(prov=prov, names=prov.names, fp=None, val=val, gate=None, kind=kind, b=b, n=n)
        _ARMS[key] = out
        return out
    if kind in ('global', 'random', 'atom'):
        arr = L.arrays(); nat = arr[0]; K = len(nat)
        base = np.arange(K); gb = np.full(K, b if b is not None else INF, float)
        mu = L.mu_canon.copy(); names = list(L.rep); bits = L.bits_canon.copy()
        if kind == 'global':
            fp = online(arr, gb)
            fp['joint'] = _joint_summary(joint_fixed_point(arr, gb), fp)
            val, gate = fp['val'], fp['gate']
        else:
            fp = None
            if kind == 'random':
                g0 = build_arm(n, 'global', b)['gate']
                gate = random_gate(g0, nat)
            else:
                gate = np.ones((K, K), np.bool_) & (nat[None, :] <= b)
            val, w, last, hc, hd = _evaluate_gated(*arr, gate, 2, 300)
            assert w >= 0
            chk, bad = _soundness(*arr[:5], gate, val, hc, hd)
            fp = dict(val=val, last=last, gate=gate, rounds=0, cycle=None, converged=True, sound_checked=chk, sound_bad=bad, worlds=w)
    elif kind in ('fixed', 'penal'):
        arr, gb, base, gid = genotypes(L)
        fp = online(arr, gb)
        fp['joint'] = _joint_summary(joint_fixed_point(arr, gb), fp)
        val, gate = fp['val'], fp['gate']
        if kind == 'fixed':
            mu = np.array([L.mu_canon[c] / (1.0 if not np.isfinite(gb[g]) else len(PP_BUDGETS)) for g, c in enumerate(base)])
        else:
            mu = penal_prior(L, base, gb)
        names = [L.rep[c] if not np.isfinite(gb[g]) else '%s@%d' % (L.rep[c], gb[g]) for g, c in enumerate(base)]
        bits = np.array([L.bits_canon[c] + (gb[g] if np.isfinite(gb[g]) else 0) for g, c in enumerate(base)])
    else:
        raise ValueError(kind)
    U, PCC = M.pd_payoffs(val, M.PD)
    keep = np.nonzero(mu > 0)[0]
    Uk = U[np.ix_(keep, keep)].astype(float); Pk = PCC[np.ix_(keep, keep)]
    prov = M.ModalProvider(Uk, Pk, mu[keep], [names[i] for i in keep], bits[keep])
    cnt = L.count_canon[base[keep]]
    prov.sizes = np.array([cnt[mm].sum() for mm in prov.members])
    prov.members_geno = [[int(keep[i]) for i in mm] for mm in prov.members]
    out = dict(prov=prov, names=prov.names, fp=fp, val=val, gate=gate, mu=mu, base=base, gb=gb, keep=keep, kind=kind, b=b, n=n,
               U=U, PCC=PCC)
    _ARMS[key] = out
    return out


def class_of_geno(arm):
    """genotype index -> class index in arm['prov'] (only genotypes with mu > 0)."""
    m = {}
    for k, mem in enumerate(arm['prov'].members_geno):
        for g in mem: m[g] = k
    return m
