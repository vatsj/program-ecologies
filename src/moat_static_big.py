"""Static drift-closure map for large n (specs/2026-10-04-conjecture4.md, Task 2).

Same objects as src/moat_static.py (static_map and the frontier), computed without dense float payoff matrices so
that n = 12 and 13 fit in memory:
- the evaluator stores one uint8 trace per pair (bit m = plays C at world m) instead of the hc/hd history arrays;
  BOX_L(p, q) at world n reads bits [L, n) of the trace, exactly as modal._evaluate's hc/hd flags do;
- behavioural classes are merged as in modal.ModalProvider (identical payoff row and column against all of L_n,
  which with four distinct PD payoffs is identical val row and val column), using row/column hashes checked exactly;
- all class-level quantities are computed from the class-level 0/1 matrix V.
Adds, per n: program counts and prior mass by size and by syntactic box-nesting depth, and the shell decomposition
(by program size) of the direct leak of FairBot and of every unsuckerable class.

    python3 src/moat_static_big.py 6 8 9 10 11 12 13     (writes runs/conjecture4.json and runs/conjecture4_static.md)
"""
import json, os, sys, time
from collections import defaultdict
import numpy as np
from numba import njit, prange, set_num_threads
sys.path.insert(0, os.path.dirname(__file__))
import modal as M

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FB = 'BOX(THEM(ME))'


class CountedLanguage(M.ModalLanguage):
    """ModalLanguage that keeps the per-size counts cnt[s][canon] (the DP's own table)."""
    def _enumerate(self):
        super()._enumerate()

    def size_counts(self):
        # re-run the counting DP using the memoized ops (cheap: every op is cached)
        n = self.n
        cnt = [defaultdict(int) for _ in range(n + 1)]
        for name in ('C', 'D'):
            cnt[1][self.op(name)] += 1
        for s in range(2, n + 1):
            for c, m in list(cnt[s - 1].items()):
                cnt[s][self.op('not', c)] += m
            for i in range(1, s - 1):
                for ca, ma in cnt[i].items():
                    for cb, mb in cnt[s - 1 - i].items():
                        for nm in ('and', 'or'):
                            cnt[s][self.op(nm, ca, cb)] += ma * mb
            for kind, level in self.kinds:
                if s == 3:
                    for form in (M.TM, M.TT):
                        cnt[s][self.op((kind, level, form))] += 1
                if s >= 4:
                    for ca, ma in cnt[s - 3].items():
                        cnt[s][self.op((kind, level, M.TL), ca)] += ma
        return cnt


def depth_counts(n, nkinds=4):
    """Syntactic program counts by (size, box-nesting depth); depth 0 = no box, 1 = boxes with no box inside an
    argument, ...  Independent of canonicalization."""
    N = [defaultdict(int) for _ in range(n + 1)]
    N[1][0] = 2
    for s in range(2, n + 1):
        for d, m in N[s - 1].items():
            N[s][d] += m
        for i in range(1, s - 1):
            for da, ma in N[i].items():
                for db, mb in N[s - 1 - i].items():
                    N[s][max(da, db)] += 2 * ma * mb
        if s == 3:
            N[s][1] += 2 * nkinds
        if s >= 4:
            for d, m in N[s - 3].items():
                N[s][d + 1] += nkinds * m
    return N


@njit(parallel=True, cache=True)
def _traces(nat, ak, al, af, aa, tt, maxw, nlev):
    """modal._evaluate with its state packed into one byte per pair: bit L = hc[L] (C at every world m with
    L <= m < n), bit 3 + L = hd[L], bit 6 = val at the current world.  nlev <= 3.  Same update order and the same
    stopping rule (no flag changed at world n, and n >= nlev)."""
    K = nat.shape[0]
    T = np.full((K, K), np.uint8(63), np.uint8)
    for n in range(maxw):
        for xx in prange(K):
            x = np.int64(xx)
            for yy in range(K):
                y = np.int64(yy)
                idx = 0
                for j in range(nat[x]):
                    f = af[x, j]
                    q = np.int64(0)
                    if f == 0:
                        q = x
                    elif f == 1:
                        q = y
                    else:
                        q = np.int64(aa[x, j])
                    L = al[x, j]
                    bit = L if ak[x, j] == 0 else 3 + L
                    if (T[y, q] >> bit) & 1:
                        idx |= 1 << j
                v = (tt[x] >> idx) & 1
                T[x, y] = np.uint8((T[x, y] & 63) | (v << 6))
        changed = 0
        for xx in prange(K):
            c = 0
            for y in range(K):
                t = T[xx, y]
                cval = (t >> 6) & 1
                nt = t
                for L in range(nlev):
                    if n < L:
                        continue
                    if cval == 0:
                        nt = nt & ~np.uint8(1 << L)
                    else:
                        nt = nt & ~np.uint8(1 << (3 + L))
                if nt != t:
                    c += 1
                    T[xx, y] = np.uint8(nt)
            changed += c
        if changed == 0 and n >= nlev:
            return T, n
    return T, -1


@njit(parallel=True, cache=True)
def _to_stable(T, n):
    K = T.shape[0]
    for x in prange(K):
        for y in range(K):
            T[x, y] = (T[x, y] >> 6) & 1


@njit(parallel=True, cache=True)
def _hashes(V, w1, w2):
    K = V.shape[0]
    hr = np.zeros(K, np.uint64); hc = np.zeros(K, np.uint64)
    for x in prange(K):
        a = np.uint64(0); b = np.uint64(0)
        for y in range(K):
            if V[x, y]:
                a += w1[y]
            if V[y, x]:
                b += w2[y]
        hr[x] = a; hc[x] = b
    return hr, hc


@njit(cache=True)
def _same(V, a, b):
    K = V.shape[0]
    for y in range(K):
        if V[a, y] != V[b, y] or V[y, a] != V[y, b]:
            return False
    return True


@njit(parallel=True, cache=True)
def _sub(V, R):
    k = R.shape[0]
    out = np.zeros((k, k), np.uint8)
    for i in prange(k):
        for j in range(k):
            out[i, j] = V[R[i], R[j]]
    return out


@njit(parallel=True, cache=True)
def _suck(V):
    k = V.shape[0]
    out = np.zeros(k, np.bool_)
    for i in prange(k):
        for j in range(k):
            if V[i, j] == 1 and V[j, i] == 0:
                out[i] = True
                break
    return out


@njit(cache=True)
def _components(V, S):
    """Components of the mutual-cooperation graph on the self-cooperating classes S (indices into V)."""
    m = S.shape[0]
    comp = -np.ones(m, np.int64)
    queue = np.zeros(m, np.int64)
    nc = 0
    for s in range(m):
        if comp[s] >= 0:
            continue
        comp[s] = nc; h = 0; t = 0; queue[t] = s; t += 1
        while h < t:
            a = queue[h]; h += 1
            ia = S[a]
            for b in range(m):
                if comp[b] < 0:
                    ib = S[b]
                    if V[ia, ib] == 1 and V[ib, ia] == 1:
                        comp[b] = nc; queue[t] = b; t += 1
        nc += 1
    return comp, nc


@njit(cache=True)
def _drift(V, S, suckS):
    m = S.shape[0]
    d = np.full(m, -1, np.int64)
    queue = np.zeros(m, np.int64); h = 0; t = 0
    for i in range(m):
        if suckS[i]:
            d[i] = 0; queue[t] = i; t += 1
    while h < t:
        a = queue[h]; h += 1
        ia = S[a]
        for b in range(m):
            if d[b] < 0:
                ib = S[b]
                if V[ia, ib] == 1 and V[ib, ia] == 1:
                    d[b] = d[a] + 1; queue[t] = b; t += 1
    return d


def static_map_big(n, threads=3, maxw=200):
    set_num_threads(threads)
    t0 = time.time()
    L = CountedLanguage(n)
    nat, ak, al, af, aa, tt = L.arrays()
    nlev = int(al.max()) + 1
    assert nlev <= 3
    T, nf = _traces(nat, ak, al, af, aa, tt, maxw, nlev)
    if nf < 0:
        raise RuntimeError('did not stabilize within %d worlds' % maxw)
    _to_stable(T, nf); V = T                     # V[x, y] = 1 iff x plays C against y (stable)
    t_eval = time.time() - t0
    K = V.shape[0]
    # behavioural classes (as modal.ModalProvider): identical val row and column
    rng = np.random.default_rng(12345)
    w1 = rng.integers(1, 2**63, K, dtype=np.uint64); w2 = rng.integers(1, 2**63, K, dtype=np.uint64)
    hr, hc = _hashes(V, w1, w2)
    groups = defaultdict(list)
    for c in range(K):
        groups[(int(hr[c]), int(hc[c]))].append(c)
    mu_c = L.mu_canon; bits = L.bits_canon
    classes = []
    for mem in groups.values():
        rep = min(mem, key=lambda c: (bits[c], c))
        for c in mem:
            assert c == rep or _same(V, rep, c), 'hash collision'
        classes.append((rep, mem, float(mu_c[mem].sum())))
    classes.sort(key=lambda t: -t[2])
    Z = sum(t[2] for t in classes)
    R = np.array([t[0] for t in classes], np.int64)
    mu = np.array([t[2] for t in classes]) / Z
    names = [L.rep[r] for r in R]
    cls_of = np.zeros(K, np.int64)
    for i, t in enumerate(classes):
        cls_of[t[1]] = i
    W = _sub(V, R)
    del V, T
    k = len(R)
    selfc = np.array([W[i, i] == 1 for i in range(k)])
    S = np.nonzero(selfc)[0].astype(np.int64)
    suck = _suck(W)
    comp, nc = _components(W, S)
    dS = _drift(W, S, suck[S])
    iFB = names.index(FB); iC = names.index('C'); iD = names.index('D')
    pos = {int(s): j for j, s in enumerate(S)}
    cFB = comp[pos[iFB]]
    comps = defaultdict(list)
    for j, s in enumerate(S):
        comps[int(comp[j])].append(int(s))
    closed = [c for c, mem in comps.items() if not suck[mem].any()]
    KFB = [s for s in comps[cFB] if s != iC]
    muKFB = mu[KFB].sum()
    # per-size counts of each class, for shells
    cnt = L.size_counts()
    a = L.a
    shell_w = np.array([0.0] + [2.0 ** (-(np.log2(a[s]) + 2 * np.log2(s) + 1)) for s in range(1, n + 1)])   # per program
    cls_shell = np.zeros((k, n + 1))
    for s in range(1, n + 1):
        for c, m in cnt[s].items():
            cls_shell[cls_of[c], s] += m * shell_w[s]
    # frontier: unsuckerable self-cooperators
    front = []
    for j, s in enumerate(S):
        s = int(s)
        if suck[s]:
            continue
        mates = [int(y) for y in S if y != s and W[s, y] == 1 and W[y, s] == 1]
        lk = [y for y in mates if suck[y]]
        closure_lk = [y for y in comps[int(comp[j])] if suck[y]]
        front.append(dict(name=names[s], mu=float(mu[s]), leak=float(mu[lk].sum()), closure_leak=float(mu[closure_lk].sum()),
                          ratio=float(mu[lk].sum() / mu[s]),
                          universality=float(mu[[y for y in KFB if W[s, y] == 1 and W[y, s] == 1]].sum() / muKFB),
                          coop_FB=bool(W[s, iFB] == 1 and W[iFB, s] == 1), coop_ALLC=bool(W[s, iC] == 1),
                          n_mates=len(mates), n_leak=len(lk),
                          leak_shell=[float(x) for x in cls_shell[lk].sum(axis=0)] if lk else [0.0] * (n + 1),
                          mu_shell=[float(x) for x in cls_shell[s]],
                          top_leaks=[names[y] for y in sorted(lk, key=lambda y: -mu[y])[:3]]))
    front.sort(key=lambda r: r['ratio'])
    Nd = depth_counts(n)
    by_size = [dict(size=s, programs=int(a[s]), mass=float(1.0 / (2 * s * s)),
                    by_depth={int(d): int(m) for d, m in sorted(Nd[s].items())}) for s in range(1, n + 1)]
    out = dict(n=n, canon=K, worlds=int(nf), classes=k, self_coop=int(len(S)), mu_self_coop=float(mu[S].sum()),
               n_components=int(nc), n_closed=len(closed), mu_closed=float(sum(mu[comps[c]].sum() for c in closed)),
               max_drift=int(dS.max()), KFB_size=len(KFB) + 1, KFB_mu=float(muKFB),
               n_suckerable_selfcoop=int(suck[S].sum()), Z=float(Z), by_size=by_size,
               frontier=front, t_eval=t_eval, t_total=time.time() - t0)
    return out


def fmt(o):
    L = ['## n = %d' % o['n'], '',
         '- canonical functions %d, behavioural classes %d, stable at world %d; self-cooperating %d (μ %.4f), of which suckerable %d' % (
             o['canon'], o['classes'], o['worlds'], o['self_coop'], o['mu_self_coop'], o['n_suckerable_selfcoop']),
         '- components of G: %d; closed components: %d (μ %.3g); max drift distance %d; FairBot component %d classes, μ %.4f (without ALLC)' % (
             o['n_components'], o['n_closed'], o['mu_closed'], o['max_drift'], o['KFB_size'], o['KFB_mu']),
         '- time %.0f s (evaluation %.0f s)' % (o['t_total'], o['t_eval']), '',
         '| unsuckerable class | μ | direct leak | leak/μ | closure leak | universality | coop FB | coop ALLC | top leaks |',
         '|---|---|---|---|---|---|---|---|---|']
    for r in o['frontier']:
        L.append('| `%s` | %.3e | %.3e | %.4g | %.3g | %.3f | %s | %s | %s |' % (
            r['name'], r['mu'], r['leak'], r['ratio'], r['closure_leak'], r['universality'], r['coop_FB'], r['coop_ALLC'],
            ', '.join('`%s`' % t for t in r['top_leaks'][:2])))
    return '\n'.join(L) + '\n'


def main():
    ns = [int(a) for a in sys.argv[1:]] or [6, 8, 9, 10, 11]
    path = os.path.join(ROOT, 'runs', 'conjecture4.json')
    res = json.load(open(path)) if os.path.exists(path) else {}
    for n in ns:
        o = static_map_big(n)
        res[str(n)] = o
        fb = [r for r in o['frontier'] if r['name'] == FB][0]
        print('n=%d classes=%d selfc=%d comps=%d closed=%d FB leak/mu=%.4f min=%s %.4f t=%.0fs' % (
            n, o['classes'], o['self_coop'], o['n_components'], o['n_closed'], fb['ratio'], o['frontier'][0]['name'],
            o['frontier'][0]['ratio'], o['t_total']), flush=True)
        json.dump(res, open(path, 'w'), indent=1)


if __name__ == '__main__':
    main()
