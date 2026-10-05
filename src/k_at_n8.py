"""K at n = 8, lemma sharing, and non-per-match budget prices (specs/2026-10-05-k-at-n8.md;
predictions/2026-10-05-k-at-n8.md).

    python3 src/k_at_n8.py ktables --budgets 3 4 6 8 12 16 24 32 54 [--workers 3]
    python3 src/k_at_n8.py ...

K is `src/bounded_k.py` unchanged in its rules.  At n = 8 the closure is made tractable by a *GL-erasure prune*: every
K rule is GL-sound once budgets are erased (BoxEq: []P -> []phi(P) and back are GL+Def theorems; Nec and JLoeb are
necessitation and Loeb), so K |- A implies GL+Def |- erase(A), and the free arm's box-fact tables hc/hd are exactly
GL+Def provability (RESULTS "Proof length", audit).  A content whose erasure is not a GL theorem is never searched,
and the JLoeb candidate sets S contain only GL theorems.  The prune removes only derivations that cannot exist; it is
validated by reproducing the published n = 6 K tables exactly.
"""
import argparse, json, os, sys, time
import numpy as np
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(__file__))
import bounded_k as BK
from gl_proofs import FP, FBOT, FTOP, FNOT, FAND, FOR, FIMP, FBOX
from conj4 import parse, src as psrc

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS = os.path.join(ROOT, 'runs')
KDIR = os.path.join(RUNS, 'k-at-n8')
os.makedirs(KDIR, exist_ok=True)

FB = 'BOX(THEM(ME))'
PB = 'and(BOX(THEM(ME)),BOXD1(THEM(^D)))'
PSTAR = 'and(BOX1(THEM(ME)),not(BOX(THEM(ME))))'
P2 = 'and(BOX1(THEM(ME)),not(BOX(THEM(^C))))'


# ------------------------------------------------------------------ the GL-erasure prune
_TABLES = {}


def tables(n):
    if n not in _TABLES:
        import gl_proofs as G
        L, val, hc, hd = G.box_tables(n)
        _TABLES[n] = (L, val, hc, hd)
    return _TABLES[n]


def make_prune(K, L, hc, hd):
    """prune(A) for KTheory: False iff erase(A) is known not GL+Def-provable (None when the formula is not of a
    recognized shape).  Shapes: P_xy (hc[0]), ~P_xy (hd[0]), ~[]^k F -> P_xy (hc[k]), ~[]^k F -> ~P_xy (hd[k]),
    a definition phi(P_xy) (hc[0] of P_xy), F (never), T (always)."""
    canon = {psrc(parse(s)): i for i, s in enumerate(L.rep)}
    tcanon = {}
    F = K.forms
    nlev = hc.shape[0]

    def cid(g):
        ti, b = K.genos[g]
        c = tcanon.get(ti)
        if c is None:
            c = tcanon[ti] = canon.get(psrc(K.trees[ti]), -1)
        return c

    def pair(f):
        t = F[f]
        if t[0] != FP: return None
        a, b = cid(t[1]), cid(t[2])
        if a < 0 or b < 0: return None
        return a, b

    def boxbot_k(f):
        k = 0
        while F[f][0] == FBOX:
            k += 1; f = F[f][1]
        return k if F[f][0] == FBOT else None

    def prune(A):
        t = F[A]; k = t[0]
        if k == FBOT: return False
        if k == FTOP: return True
        if k == FP:
            p = pair(A)
            return None if p is None else bool(hc[0, p[0], p[1]])
        if k == FNOT and F[t[1]][0] == FP:
            p = pair(t[1])
            return None if p is None else bool(hd[0, p[0], p[1]])
        if k == FIMP and F[t[1]][0] == FNOT:
            lev = boxbot_k(F[t[1]][1])
            if lev is not None and 1 <= lev < nlev:
                s = t[2]
                if F[s][0] == FP:
                    p = pair(s)
                    return None if p is None else bool(hc[lev, p[0], p[1]])
                if F[s][0] == FNOT and F[F[s][1]][0] == FP:
                    p = pair(F[s][1])
                    return None if p is None else bool(hd[lev, p[0], p[1]])
        Ps = K.inv.get(A)
        if Ps:
            p = pair(Ps[0])
            if p is not None: return bool(hc[0, p[0], p[1]])
        return None
    return prune


# ------------------------------------------------------------------ K play table at a global budget
def ktable(n, b, prune=True, filter_first=True, ustar_limit=40, verbose=False):
    """Play matrix of L_n with every class at global budget b, decided by K.  Returns (val, meta, K, g)."""
    L, val_free, hc, hd = tables(n)
    t = time.time()
    K = BK.KTheory(cap=max(b, 1), ustar_limit=ustar_limit, filter_first=filter_first)
    if prune:
        K.prune = make_prune(K, L, hc, hd)
    g = [K.geno(s, b) for s in L.rep]
    contents = set()
    for x in g:
        for y in g:
            for a in K.atoms(x, y): contents.add(K.forms[a][1])
    t_build = time.time() - t
    live = [A for A in contents if not K.dead(A)]
    passes = K.solve(sorted(contents))
    t_solve = time.time() - t - t_build
    play = K.play_fn()
    Kn = len(g)
    val = np.array([[int(play(x, y)) for y in g] for x in g], np.int8)
    nchk, bad = K.soundness_check()
    # K-provable vs GL-true atoms (by count and mu-weighted over reader x, opponent y)
    mu = L.mu_canon / L.mu_canon.sum()
    nat, ak, al, af, aa, tt = L.arrays()
    gl_true = 0; k_true = 0; gl_w = 0.0; k_w = 0.0; unresolved = {}
    for i, x in enumerate(g):
        for j, y in enumerate(g):
            for a in K.atoms(x, y):
                A = K.forms[a][1]
                if K.prune is None: break
                pr = K.prune(A)
                if pr:
                    w = mu[i] * mu[j]
                    gl_true += 1; gl_w += w
                    if K.T.get(A, BK.INF) <= b:
                        k_true += 1; k_w += w
                    else:
                        unresolved.setdefault(L.rep[i], []).append(L.rep[j])
    ws = sorted(len(K.Ustar[A]) for A in K.Ustar) if K.Ustar else [0]
    meta = dict(n=n, b=b, passes=passes, n_contents=len(contents), n_live=len(live), n_forms=len(K.forms),
                sound_checked=nchk, sound_bad=len(bad), t_build=t_build, t_solve=t_solve, t=time.time() - t,
                gl_true_atoms=gl_true, k_true_atoms=k_true, gl_true_w=gl_w, k_true_w=k_w,
                ustar_max=ws[-1], ustar_mean=float(np.mean(ws)), filter_first=filter_first, ustar_limit=ustar_limit,
                prune=prune, diff_vs_free=int((val != val_free).sum()))
    meta['unresolved_by_reader'] = {k: len(v) for k, v in unresolved.items()}
    meta['unresolved_examples'] = {k: v[:4] for k, v in list(unresolved.items())[:60]}
    if verbose:
        print({k: v for k, v in meta.items() if not isinstance(v, dict)}, flush=True)
    return val, meta, K, g


def _ktable_job(j):
    n, b, ff, lim = j
    val, meta, K, g = ktable(n, b, filter_first=ff, ustar_limit=lim)
    np.save(os.path.join(KDIR, 'kval_n%d_b%d.npy' % (n, b)), val)
    json.dump(meta, open(os.path.join(KDIR, 'kmeta_n%d_b%d.json' % (n, b)), 'w'), indent=1)
    return meta


def cmd_ktables(a):
    jobs = [(a.n, b, True, a.ustar_limit) for b in a.budgets]
    jobs.sort(key=lambda j: -j[1])
    with Pool(a.workers) as pool:
        for m in pool.imap_unordered(_ktable_job, jobs):
            print('n=%d b=%d: contents %d live %d, passes %d, sound bad %d / %d, diff vs free %d, K/GL atoms %d/%d (w %.4f/%.4f), %.0fs (solve %.0fs)' % (
                m['n'], m['b'], m['n_contents'], m['n_live'], m['passes'], m['sound_bad'], m['sound_checked'], m['diff_vs_free'],
                m['k_true_atoms'], m['gl_true_atoms'], m['k_true_w'], m['gl_true_w'], m['t'], m['t_solve']), flush=True)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd')
    ap.add_argument('--workers', type=int, default=3)
    ap.add_argument('--n', type=int, default=8)
    ap.add_argument('--budgets', type=int, nargs='+', default=[3, 4, 6, 8, 12, 16, 24, 32, 54])
    ap.add_argument('--ustar_limit', type=int, default=40)
    a = ap.parse_args()
    {'ktables': cmd_ktables}[a.cmd](a)
