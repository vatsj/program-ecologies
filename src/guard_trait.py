"""The guard margin as a heritable trait (specs/2026-10-06-guard-trait.md; predictions/2026-10-06-guard-trait.md).

    python3 src/guard_trait.py catalogue --n 8 --b 16 [--workers 3]     # K closure, certificates, K_c4 search
    python3 src/guard_trait.py static | chain | sham | attrib | lottery | price | report

Genotype (source, g), g in {0, L}.  The reader's guard offset is part of its program semantics: a g = 0 reader's
level-k atoms read ~[]_b^k F, a g = L reader's read ~[]_{2b+8}^k F (offset b + 8, notes/k-cut.md §1.9).  A quoted
argument ^A of x is A at x's budget and x's guard (it is part of x's source).  A source with no level >= 1 atom
anywhere (quotes included) has a guard-free definition: its two genotypes are the same program (one K genotype),
so they are guard twins by construction.  Every cross-guard block is built from these mixed semantics: P[y, x]
unfolds to y's definition with y's guard, so an opponent's guard is part of the proposition the reader proves.

Calculus: K_c4 = K + Cut + UnfId + Dist+ (src/bounded_k.py option cut='c4'), b = 16, search cap 2b + 8 = 40.
Method (targeted, notes/k-cut.md §1.7 extended): K's mixed closure; extension-model certificates of the K misses,
with the high-budget rule below; the K_c4 search on the uncertified misses only.

High-budget rule (proved in runs/guard-trait.md §1): every content Y with (Y, e) in B_E satisfies
GL+Def |- erase(Box*E -> Y), Box*E = AND_{X in E} (X & []X) (Std contents are GL theorems; BoxEq images are
equivalences; a Dist+ output follows from its GL-valid premise, whose members A_i / []A_i follow from Box*E because
Box*E -> []Box*E in GL).  So a box query (Y, e) at any budget e is false in I_E when Y is not in Std (not GL-true, or
certified structural) and GL+Def does not prove erase(Box*E -> Y).  At budgets <= b + 1 Lemma E1's exact list is used
as before.
"""
import argparse, itertools, json, math, os, sys, time
import numpy as np
from collections import defaultdict
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(__file__))
import bounded_k as BK
import gl_proofs as G
import k_four as K4
import k_cut as KC
from gl_proofs import FP, FBOT, FTOP, FNOT, FAND, FOR, FIMP, FBOX
from conj4 import parse, src as psrc

INF = BK.INF
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS = os.path.join(ROOT, 'runs')
GDIR = os.path.join(RUNS, 'guard-trait')
os.makedirs(GDIR, exist_ok=True)


def gdep(t):
    """Does the source's definition depend on the guard (a level >= 1 atom anywhere, quotes included)?"""
    k = t[0]
    if k in ('C', 'D'): return False
    if k == 'not': return gdep(t[1])
    if k in ('and', 'or'): return gdep(t[1]) or gdep(t[2])
    _, kind, lev, form, arg = t
    return lev >= 1 or (arg is not None and gdep(arg))


# ====================================================================== mixed-guard calculus
class KTheoryM(KC.KTheoryC):
    """KTheoryC with a per-genotype guard: genotype key (tree, budget, g), g in {0, 1}; g = 1 reads its level-k
    guard at budget b + glong.  self.genos stays a list of (tree, budget) pairs (the prune and the erasure read only
    the source); self.gg holds each genotype's guard bit."""

    def __init__(self, *a, glong=24, **kw):
        super().__init__(*a, goff=0, **kw)
        self.glong = glong; self.gg = []

    def geno(self, s, b, g=0):
        ti = self.tree(s)
        t = self.trees[ti]
        if not BK.has_box(t): b = 0
        if not gdep(t): g = 0
        key = (ti, b, g)
        gid = self.geno_id.get(key)
        if gid is None:
            gid = len(self.genos); self.geno_id[key] = gid; self.genos.append((ti, b)); self.gg.append(g)
        return gid

    def name(self, gid):
        ti, b = self.genos[gid]
        s = psrc(self.trees[ti])
        s = s if b == 0 else '%s@%d' % (s, b)
        return s + ('/L' if self.gg[gid] else '')

    def phi(self, gx, gy):
        ti, b = self.genos[gx]; g = self.gg[gx]
        off = self.glong if g else 0

        def tr(t):
            k = t[0]
            if k == 'C': return self.TOP
            if k == 'D': return self.BOT
            if k == 'not': return self.neg(tr(t[1]))
            if k == 'and': return self.f((FAND, tr(t[1]), tr(t[2])))
            if k == 'or': return self.f((FOR, tr(t[1]), tr(t[2])))
            _, kind, lev, form, arg = t
            if form == 'ME': p, q = gy, gx
            elif form == 'THEM': p, q = gy, gy
            else: p, q = gy, self.geno(arg, b, g)
            s = self.P(p, q)
            if kind: s = self.neg(s)
            if lev:
                bb = self.BOT
                for _ in range(lev): bb = self.box(bb, b + off)
                s = self.f((FIMP, self.neg(bb), s))
            return self.box(s, b)
        return tr(self.trees[ti])


class CertifierM(KC.Certifier):
    """KC.Certifier with the high-budget rule (module docstring): box queries above b + 1 are decided false when the
    content is Std-false and not a GL+Def consequence of Box*E."""

    def __init__(self, K, b, four=False):
        super().__init__(K, b, four=four)
        self._imp = {}
        self.n_high = 0

    def glimp(self, E, Y):
        key = (E, Y)
        r = self._imp.get(key)
        if r is None:
            L = set()
            for X in E:
                ex = K4.erase(self.K, X, self.th, self._em)
                L.add(ex); L.add(self.th.box(ex))
            if len(self.orc.memo) > 400_000: self.orc.memo.clear()
            r = self._imp[key] = self.orc.prov((frozenset(L), frozenset([K4.erase(self.K, Y, self.th, self._em)])))
        return r

    def truth(self, f, E):
        K = self.K; t = K.forms[f]; k = t[0]
        if k != FBOX or t[2] <= self.b + 1:
            if k == FP: return self.truth(K.unfold(f), E)
            if k == FBOT: return False
            if k == FTOP: return True
            if k == FNOT:
                a = self.truth(t[1], E); return None if a is None else (not a)
            if k in (FAND, FOR, FIMP):
                a = self.truth(t[1], E)
                if k == FIMP: a = None if a is None else (not a)
                c = self.truth(t[2], E)
                if k == FAND:
                    if a is False or c is False: return False
                    return None if (a is None or c is None) else True
                if a is True or c is True: return True
                return None if (a is None or c is None) else False
            if self.ecl(E, t[1], t[2]): return True
            return self.std(t[1], t[2])
        Y, d = t[1], t[2]
        self.n_high += 1
        if self.ecl(E, Y, d): return True
        s = self.std(Y, d)
        if s is True: return True
        if s is False and not self.glimp(tuple(sorted(E)), Y): return False
        return None


# ====================================================================== the catalogue
def catalogue_genos(K, L, b):
    """Catalogue genotypes: (canonical source index, g) for every source and g in {0, 1}; their K genotype ids."""
    cat = [(c, g) for g in (0, 1) for c in range(len(L.rep))]
    kg = [K.geno(L.rep[c], b, g) for c, g in cat]
    return cat, kg


def build_K(n, b, glong, cut=None, ustar_limit=40):
    import k_at_n8 as KN
    L, val_free, hc, hd = KN.tables(n)
    K = KTheoryM(cap=max(b + glong, 1), ustar_limit=ustar_limit, filter_first=True, cut=cut, glong=glong)
    K.prune = KN.make_prune(K, L, hc, hd)
    cat, kg = catalogue_genos(K, L, b)
    return K, L, cat, kg


def contents_of(K, kg):
    ug = sorted(set(kg))
    contents = set(); atoms = defaultdict(list)
    for x in ug:
        for y in ug:
            for a in K.atoms(x, y):
                c = K.forms[a][1]; contents.add(c); atoms[c].append((x, y))
    return ug, contents, atoms


def play_table(K, kg, T=None):
    if T is not None:
        save = K.T; K.T = T
    play = K.play_fn()
    ug = sorted(set(kg)); pos = {g: i for i, g in enumerate(ug)}
    small = np.array([[int(play(x, y)) for y in ug] for x in ug], np.int8)
    if T is not None:
        K.T = save
    idx = np.array([pos[g] for g in kg])
    return small[np.ix_(idx, idx)]


def cmd_kclosure(a):
    """Step 1: K's mixed closure at cap b + glong; the play table; the K misses certified (high-budget rule); the
    uncertified misses written for the K_c4 search."""
    n, b = a.n, a.b; glong = b + 8
    t = time.time()
    K, L, cat, kg = build_K(n, b, glong)
    ug, contents, atoms = contents_of(K, kg)
    t_build = time.time() - t
    print('n=%d b=%d: %d catalogue genotypes, %d K genotypes, %d contents (%.0fs)' % (n, b, len(cat), len(ug), len(contents), t_build), flush=True)
    passes = K.solve(sorted(contents))
    t_solve = time.time() - t - t_build
    vK = play_table(K, kg)
    nchk, bad = K.soundness_check()
    if bad: nchk, bad = K4.closure_check(K)
    print('K solved (%.0fs), soundness %d / %d' % (t_solve, len(bad), nchk), flush=True)
    gl_true = [c for c in contents if K.prune(c)]
    miss = [c for c in gl_true if K.T.get(c, INF) > b]
    tc = time.time()
    cert = CertifierM(K, b, four=False)
    res = cert.run(miss)
    unc = [c for c in miss if res[c] is None]
    t_cert = time.time() - tc
    # which uncertified contents involve a long guard anywhere in their closure?
    def has_long(c, seen=None):
        st = [c]; seen = set()
        while st:
            f = st.pop()
            if f in seen: continue
            seen.add(f); tt = K.forms[f]
            if tt[0] == FBOX:
                if tt[2] > b + 1: return True
                st.append(tt[1])
            elif tt[0] == FP: st.append(K.unfold(f))
            elif tt[0] == FNOT: st.append(tt[1])
            elif tt[0] in (FAND, FOR, FIMP): st += [tt[1], tt[2]]
        return False
    unc_long = [c for c in unc if has_long(c)]
    mu = L.mu_canon / L.mu_canon.sum()
    meta = dict(n=n, b=b, glong=glong, cap=b + glong, n_catalogue=len(cat), n_kgenos=len(ug), n_contents=len(contents),
                passes=passes, t_build=t_build, t_solve=t_solve, t_cert=t_cert, sound_checked=nchk, sound_bad=len(bad),
                gl_true_contents=len(gl_true), K_derived_contents=len(gl_true) - len(miss), missing_contents=len(miss),
                certified_contents=len(miss) - len(unc), uncertified_contents=len(unc), uncertified_long=len(unc_long),
                cert_high_queries=cert.n_high, n_forms=len(K.forms))
    np.save(os.path.join(GDIR, 'vK_n%d_b%d.npy' % (n, b)), vK)
    cs = np.array(sorted(contents), np.int64)
    np.save(os.path.join(GDIR, 'kT_n%d_b%d.npy' % (n, b)), np.stack([cs, np.array([min(K.T.get(c, INF), 10**6) for c in cs], np.int64)]))
    json.dump(dict(meta=meta, cat=cat, kg=kg, names=[K.name(g) for g in range(len(K.genos))],
                   uncertified=[K.show(c) for c in unc], uncertified_long=[K.show(c) for c in unc_long],
                   n_atoms_unc=[len(atoms[c]) for c in unc]),
              open(os.path.join(GDIR, 'kclosure_n%d_b%d.json' % (n, b)), 'w'))
    print({k: v for k, v in meta.items()}, flush=True)
    # g = 0 block vs the published K table
    import k_at_n8 as KN
    nr = len(L.rep)
    try:
        ref = KN.load_val(n, b) if n == 8 else np.load(os.path.join(RUNS, 'k-four', 'K_g0_n%d_b%d.npy' % (n, b)))
        print('g = 0 block vs published K table: %d differing plays' % int((vK[:nr, :nr] != ref).sum()), flush=True)
    except Exception as e:
        print('no published reference:', e)


def _kc4_job(j):
    """K_c4 search on a chunk of uncertified goals (matched by printed form).  Returns {shown: T} for every goal
    derived within the cap, soundness, and the checker on every newly derived goal (witness replay)."""
    n, b, goals, seed = j
    glong = b + 8
    t = time.time()
    K, L, cat, kg = build_K(n, b, glong, cut='c4')
    ug = sorted(set(kg))
    want = set(goals); cmap = {}
    for x in ug:
        for y in ug:
            for a_ in K.atoms(x, y):
                c = K.forms[a_][1]
                s = K.show(c)
                if s in want: cmap[s] = c
    K.solve(sorted(set(cmap.values())))
    T = {s: int(K.T.get(c, INF)) for s, c in cmap.items() if K.T.get(c, INF) <= K.cap}
    nchk, bad = K.soundness_check()
    if bad: nchk, bad = K4.closure_check(K)
    newly = [s for s, v in T.items() if v <= b]
    ck = dict(goals=0, size_mismatch=0, dist=0, replayed=0, fail=0, nodes=0)
    for s in newly:
        c = cmap[s]
        try:
            sz, st = KC.check_goal(K, c)
            ck['goals'] += 1; ck['size_mismatch'] += int(sz != K.T[c])
            ck['dist'] += st['dist']; ck['replayed'] += st['replayed']; ck['nodes'] += st['nodes']
        except (AssertionError, ValueError, KeyError) as e:
            ck['fail'] += 1
    return dict(seed=seed, n_goals=len(goals), matched=len(cmap), T=T, sound_checked=nchk, sound_bad=len(bad),
                bad_examples=[K.show(x) for x in bad[:10]], checker=ck, t=time.time() - t, n_forms=len(K.forms))


def cmd_kc4(a):
    n, b = a.n, a.b
    d = json.load(open(os.path.join(GDIR, 'kclosure_n%d_b%d.json' % (n, b))))
    goals = sorted(d['uncertified'])
    rng = np.random.default_rng(0); perm = rng.permutation(len(goals))
    chunks = [[goals[i] for i in perm[k::a.chunks]] for k in range(a.chunks)]
    path = os.path.join(GDIR, 'kc4_n%d_b%d.json' % (n, b))
    out = json.load(open(path)) if os.path.exists(path) and not a.fresh else []
    done = {r['seed'] for r in out}
    jobs = [(n, b, ch, k) for k, ch in enumerate(chunks) if k not in done]
    print('%d goals in %d chunks, %d to run' % (len(goals), len(chunks), len(jobs)), flush=True)
    with Pool(min(a.workers, len(jobs) or 1)) as pool:
        for r in pool.imap_unordered(_kc4_job, jobs):
            out.append(r); json.dump(out, open(path, 'w'))
            print('chunk %d: %d goals, %d matched, %d derived within cap, %d within b, sound %d/%d, checker %s, %.0fs' % (
                r['seed'], r['n_goals'], r['matched'], len(r['T']), sum(1 for v in r['T'].values() if v <= b),
                r['sound_bad'], r['sound_checked'], r['checker'], r['t']), flush=True)


def patched_tables(n, b):
    """Rebuild the mixed catalogue's formulas (same construction order, so the same content ids), load K's values
    and the K_c4 search results, and return (vK, vKc4, info, (K, L, cat, kg))."""
    glong = b + 8
    K, L, cat, kg = build_K(n, b, glong)
    ug, contents, atoms = contents_of(K, kg)
    arr = np.load(os.path.join(GDIR, 'kT_n%d_b%d.npy' % (n, b)))
    assert len(arr[0]) == len(contents) and set(arr[0].tolist()) == contents
    K.T = {int(c): (int(v) if v < 10**6 else INF) for c, v in zip(arr[0], arr[1])}
    vK = play_table(K, kg)
    d = json.load(open(os.path.join(GDIR, 'kclosure_n%d_b%d.json' % (n, b))))
    rows = json.load(open(os.path.join(GDIR, 'kc4_n%d_b%d.json' % (n, b))))
    Tn = {}
    for r in rows: Tn.update(r['T'])
    unc = set(d['uncertified'])
    assert sum(r['n_goals'] for r in rows) == len(unc)
    byshow = {K.show(c): c for c in contents if K.T.get(c, INF) > b}
    T2 = dict(K.T); newly = []
    for s_, v in Tn.items():
        assert s_ in unc
        if v <= b and s_ in byshow:
            T2[byshow[s_]] = v; newly.append(byshow[s_])
    v4 = play_table(K, kg, T2)
    info = dict(newly_derived=len(newly), newly_examples=[K.show(c) for c in newly[:40]],
                newly_pairs=[(K.name(x), K.name(y)) for c in newly[:40] for x, y in atoms[c][:2]],
                derived_within_cap=sum(1 for v in Tn.values() if v < INF), sound_bad=sum(r['sound_bad'] for r in rows),
                sound_checked=sum(r['sound_checked'] for r in rows),
                checker={k: sum(r['checker'][k] for r in rows) for k in rows[0]['checker']} if rows else {})
    return vK, v4, info, (K, L, cat, kg)


def cmd_patch(a):
    vK, v4, info, (K, L, cat, kg) = patched_tables(a.n, a.b)
    np.save(os.path.join(GDIR, 'vKc4_n%d_b%d.npy' % (a.n, a.b)), v4)
    info['diff_vs_K'] = int((v4 != vK).sum())
    json.dump(info, open(os.path.join(GDIR, 'patch_n%d_b%d.json' % (a.n, a.b)), 'w'), indent=1)
    print({k: v for k, v in info.items() if 'examples' not in k and 'pairs' not in k})


def cmd_full(a):
    """Validation (small n): the full K_c4 closure over the mixed catalogue, compared with the targeted table."""
    n, b = a.n, a.b; glong = b + 8
    t = time.time()
    K, L, cat, kg = build_K(n, b, glong, cut='c4')
    ug, contents, atoms = contents_of(K, kg)
    K.solve(sorted(contents))
    vf = play_table(K, kg)
    nchk, bad = K.soundness_check()
    if bad: nchk, bad = K4.closure_check(K)
    vt = np.load(os.path.join(GDIR, 'vKc4_n%d_b%d.npy' % (n, b)))
    out = dict(n=n, b=b, full_vs_targeted=int((vf != vt).sum()), sound_bad=len(bad), sound_checked=nchk, t=time.time() - t,
               diffs=[(K.name(kg[i]), K.name(kg[j]), int(vt[i, j]), int(vf[i, j])) for i, j in np.argwhere(vf != vt)[:20]])
    np.save(os.path.join(GDIR, 'vKc4full_n%d_b%d.npy' % (n, b)), vf)
    json.dump(out, open(os.path.join(GDIR, 'full_n%d_b%d.json' % (n, b)), 'w'), indent=1)
    print(out)


def main():
    p = argparse.ArgumentParser()
    sp = p.add_subparsers(dest='cmd')
    q = sp.add_parser('kclosure'); q.add_argument('--n', type=int, default=8); q.add_argument('--b', type=int, default=16)
    q = sp.add_parser('kc4'); q.add_argument('--n', type=int, default=8); q.add_argument('--b', type=int, default=16)
    q.add_argument('--chunks', type=int, default=3); q.add_argument('--workers', type=int, default=3); q.add_argument('--fresh', action='store_true')
    for nm in ('patch', 'full'):
        q = sp.add_parser(nm); q.add_argument('--n', type=int, default=8); q.add_argument('--b', type=int, default=16)
    a = p.parse_args()
    {'kclosure': cmd_kclosure, 'kc4': cmd_kc4, 'patch': cmd_patch, 'full': cmd_full}[a.cmd](a)


if __name__ == '__main__':
    main()
