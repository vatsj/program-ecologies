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


# ====================================================================== catalogue objects for the chain
W = 0.3


class Cat:
    """A catalogue: genotype table val (G x G), labels, sources, prior, kernel.  cat = [(source canon id, label)].
    prior_g = (p0, p1).  cost: G x G per-match cost on the row genotype (or None)."""

    def __init__(self, val, cat, L, prior_g, cost=None, names=None, gdeps=None, mu_src=None):
        import modal as M
        self.val = val; self.cat = cat; self.L = L; self.prior_g = prior_g
        U0, PCC = M.pd_payoffs(val, M.PD)
        self.U = U0.astype(float) - (cost if cost is not None else 0.0)
        self.PCC = PCC
        mc = L.mu_canon / L.mu_canon.sum() if mu_src is None else mu_src
        self.mu_src = mc
        self.src = np.array([c for c, g in cat]); self.lab = np.array([g for c, g in cat])
        self.mu = np.array([mc[c] * prior_g[g] for c, g in cat])
        self.names = names or ['%s%s' % (L.rep[c], '/L' if g else '') for c, g in cat]
        self.gdep = gdeps
        # index of the partner genotype (same source, other label)
        pos = {(c, g): i for i, (c, g) in enumerate(cat)}
        self.partner = np.array([pos.get((c, 1 - g), -1) for c, g in cat])
        R = np.round(self.U, 9)
        self.rowsig = [R[i].tobytes() + R[:, i].tobytes() for i in range(len(cat))]

    def twins(self):
        """(s, 1) genotypes whose rows and columns equal (s, 0)'s (payoff, costs included) -- under a permutation-
        free comparison: entries against every genotype identical."""
        R = np.round(self.U, 9); G_ = len(self.cat)
        tw = np.zeros(G_, bool)
        for i in range(G_):
            j = self.partner[i]
            if j < 0 or self.lab[i] != 1: continue
            if (R[i] == R[j]).all() and (R[:, i] == R[:, j]).all() and R[i, i] == R[j, j]:
                tw[i] = True
        return tw


def lump(cat, kernel):
    """Blocks of genotypes for the chain.  joint: behavioural classes (identical payoff rows and columns), exactly
    lumpable for a resident-independent kernel.  separate: label-pure behavioural classes refined until every member
    of a block has the same kernel row over blocks (strong lumpability).  Returns (blocks, block of genotype)."""
    G_ = len(cat.cat)
    if kernel == 'joint':
        init = [cat.rowsig[i] for i in range(G_)]
    else:
        init = [cat.rowsig[i] + bytes([int(cat.lab[i])]) for i in range(G_)]
    ids = {}; blk = np.array([ids.setdefault(k, len(ids)) for k in init])
    if kernel == 'separate':
        Km = kernel_matrix(cat)
        while True:
            nb = blk.max() + 1
            S = np.zeros((G_, nb))
            for j in range(nb):
                S[:, j] = Km[:, blk == j].sum(1)
            Sr = np.round(S, 12)
            keys = [(int(blk[i]), Sr[i].tobytes()) for i in range(G_)]
            ids = {}; nblk = np.array([ids.setdefault(k, len(ids)) for k in keys])
            if nblk.max() == blk.max():
                blk = nblk; break
            blk = nblk
    nb = blk.max() + 1
    blocks = [list(np.nonzero(blk == j)[0]) for j in range(nb)]
    return blocks, blk


def kernel_matrix(cat):
    """Separate kernel at genotype level: (s, g) -> (s', g) w.p. mu_src(s')/2, -> (s, g') w.p. prior(g')/2."""
    G_ = len(cat.cat)
    pos = {(c, g): i for i, (c, g) in enumerate(cat.cat)}
    Km = np.zeros((G_, G_))
    srcs = sorted(set(cat.src.tolist()))
    ms = np.array([cat.mu_src[c] for c in srcs]); ms = ms / ms.sum()
    for i, (c, g) in enumerate(cat.cat):
        for c2, m in zip(srcs, ms):
            Km[i, pos[(c2, g)]] += 0.5 * m
        for g2 in (0, 1):
            Km[i, pos[(c, g2)]] += 0.5 * cat.prior_g[g2]
    return Km


class KernelProvider:
    """chain.Chain provider over blocks with a (possibly resident-dependent) mutation kernel over blocks."""

    def __init__(self, U, PCC, kmat=None, mu=None):
        self.Ufull = np.round(np.asarray(U, float), 9); self.PCC = PCC
        self.K = self.Ufull.shape[0]
        self.kmat = kmat; self.mu = mu
        self.cur = mu if kmat is None else None
        self.R = np.arange(self.K)

    def set_state(self, ids, x):
        if self.kmat is not None:
            self.cur = np.asarray(x) @ self.kmat[list(ids)]

    def prepare(self, support): pass

    def U(self, ids, sup=None):
        ids = [int(p) for p in ids]; return self.Ufull[np.ix_(ids, ids)]

    def mutant_classes(self, support):
        cur = self.cur if self.cur is not None else (self.kmat.mean(0) if self.kmat is not None else self.mu)
        return [(c, [c], float(cur[c])) for c in range(self.K)]

    def blocks_for(self, support):
        si = np.array(list(support), int); R = self.R
        return self.Ufull[np.ix_(R, si)], self.Ufull[np.ix_(si, R)], self.Ufull[R, R], self.Ufull[np.ix_(si, si)]


def _make_kchain():
    from chain import Chain, fixation

    class KChain(Chain):
        """chain.Chain with a resident-dependent kernel (the provider's set_state) and zero-weight mutants skipped;
        every edge's kernel weight, fate share and k* are recorded for the log-domain solve."""

        def expand(self, key):
            if key in self.trans:
                return
            ids, x, kind = self.states[key]
            self.P.set_state(ids, x)
            ids = np.array(ids); x = np.array(x)
            N = self.N; m = len(ids); w = self.w
            classes = self.P.mutant_classes(ids)
            reps = np.array([c[0] for c in classes]); mu = np.array([c[2] for c in classes])
            rows, cols, diag, inner = self.P.blocks_for(ids)
            K = len(reps)
            in_sup = np.isin(reps, ids)
            if kind == 'poly':
                neutral_ext = np.zeros(K, bool)
            else:
                neutral_ext = (np.abs(rows - inner[0:1, :]) < 1e-7).all(axis=1) & (np.abs(cols - diag[None, :]) < 1e-7).all(axis=0)
            uaa = float(x @ inner @ x); uqa = rows @ x; uaq = cols.T @ x
            out = defaultdict(float); muts = defaultdict(lambda: defaultdict(float))
            if not hasattr(self, 'edges'): self.edges = {}; self.wstate = {}
            self.wstate[key] = float(mu.sum())
            for qi in range(K):
                q = int(reps[qi]); m_q = mu[qi]
                if m_q <= 0: continue
                if in_sup[qi]:
                    out[key] += m_q; muts[key][q] += m_q; continue
                if neutral_ext[qi]:
                    fl = [(1.0, self.mono(q), N)]
                else:
                    Uq = np.empty((m + 1, m + 1)); Uq[:m, :m] = inner; Uq[m, :m] = rows[qi]; Uq[:m, m] = cols[:, qi]; Uq[m, m] = diag[qi]
                    fl = self.fates(key, ids, x, q, Uq)
                if not fl:
                    continue
                stay = m_q
                for share, k2, kstar in fl:
                    rho = fixation(float(diag[qi]), float(uqa[qi]), float(uaq[qi]), uaa, N, w, int(kstar))
                    if k2 == key: continue
                    wgt = m_q * share * rho
                    out[k2] += wgt; muts[k2][q] += wgt; stay -= wgt
                    self.edge_rho[(key, k2, q)] = (rho, int(kstar), self.states[k2][2])
                    e = self.edges.get((key, k2, q))
                    sh = share + (e[1] if e else 0.0)
                    self.edges[(key, k2, q)] = (m_q, sh, int(kstar), float(diag[qi]), float(uqa[qi]), float(uaq[qi]), uaa)
                out[key] += max(stay, 0.0); muts[key][q] += max(stay, 0.0)
            z = sum(out.values())
            self.trans[key] = {k2: v / z for k2, v in out.items()}
            for k2, d in muts.items():
                for q, v in d.items():
                    self.trans_mut[(key, k2)][q] += v / z
    return KChain


def edge_logweights_k(ch, N, keys):
    import modal_dollar as MD
    pos = {k: i for i, k in enumerate(keys)}
    n = len(keys)
    LA = np.full((n, n), -np.inf); out_un = defaultdict(list)
    for (k1, k2, q), (m_q, share, kstar, uqq, uqa, uaq, uaa) in ch.edges.items():
        i = pos.get(k1)
        if i is None or share <= 0: continue
        lr = MD.log_fixation(uqq, uqa, uaq, uaa, N, W, int(kstar))
        lw = math.log(m_q) - math.log(ch.wstate[k1]) + math.log(min(share, 1.0)) + lr
        j = pos.get(k2)
        if j is None: out_un[k2].append((i, lw))
        else: LA[i, j] = MD._lae(LA[i, j], lw)
    return LA, out_un


def seeded_chain_k(prov, N, extra_states=(), log_theta=math.log(1e-12), max_states=6000, max_rounds=80):
    """modal_dollar.seeded_chain on KChain: every monomorphic state and every extra (deep) state expanded, one layer
    more after the seeded states, then expansion by relative inflow; log-domain GTH (reflecting boundary)."""
    import modal_dollar as MD
    KChain = _make_kchain()
    ch = KChain(prov, N=N, w=W, theta=1.0, max_states=10**9, eager_poly=True)
    for c in range(prov.K):
        ch.expand(ch.mono(c))
    seeded = []
    for ids, x in extra_states:
        k = ch.add_state(ids, x); ch.expand(k); seeded.append(k)
    for k in seeded:
        for k2 in list(ch.trans[k]):
            if k2 not in ch.trans: ch.expand(k2)
    for rnd in range(max_rounds):
        keys = list(ch.trans)
        LA, out_un = edge_logweights_k(ch, N, keys)
        lpi, lex = MD.solve_log(LA)
        inflow = {k2: np.logaddexp.reduce([lpi[i] + lw for i, lw in lst]) for k2, lst in out_un.items()}
        cand = [k for k, f in inflow.items() if f > log_theta]
        small = [f for f in inflow.values() if f <= log_theta]
        lcut = np.logaddexp.reduce(small) if small else -1e300
        if not cand or len(keys) >= max_states: break
        for k in sorted(cand, key=lambda k: -inflow[k])[:max(1, max_states - len(keys))]:
            ch.expand(k)
    return dict(ch=ch, keys=keys, lpi=lpi, LA=LA, log10_cut=float(lcut / math.log(10)), rounds=rnd + 1)


def run_chain(cat, kernel, N, label='', lazy=True, deep=True, rates=True):
    """The ε -> 0 chain on a catalogue under a kernel.  Returns a row with P(C,C), pi by genotype label (neutral /
    active), support, transitions, rates and audit outputs."""
    import modal_dollar as MD
    t = time.time()
    blocks, blk = lump(cat, kernel)
    nb = len(blocks)
    rep = [b[0] for b in blocks]
    Ub = cat.U[np.ix_(rep, rep)]; Pb = cat.PCC[np.ix_(rep, rep)]
    mub = np.array([cat.mu[b].sum() for b in blocks])
    if kernel == 'joint':
        prov = KernelProvider(Ub, Pb, mu=mub / mub.sum())
    else:
        Km = kernel_matrix(cat)
        kb = np.zeros((nb, nb))
        for j in range(nb):
            kb[:, j] = Km[rep][:, blocks[j]].sum(1)
        prov = KernelProvider(Ub, Pb, kmat=kb)
    d = dict(U=prov.Ufull, mu=(mub / mub.sum()), K=nb)
    deeps = MD.deep_states(d, max_types=2) if deep else []
    extra = [s for s in deeps if len(s[0]) > 1]
    res = seeded_chain_k(prov, N, extra_states=extra)
    ch, keys, lpi = res['ch'], res['keys'], res['lpi']
    pi = np.exp(lpi)
    # genotype-level split: joint -> within block prop. to mu (exact); separate -> blocks are label-pure, split by mu
    tw = cat.twins()
    gpi = np.zeros(len(cat.cat))
    pcc = 0.0; mono = defaultdict(float); poly = 0.0; supp = []
    for k, p in zip(keys, pi):
        ids, x, kind = ch.states[k]; ids = list(ids); x = np.asarray(x)
        pcc += p * float(x @ Pb[np.ix_(ids, ids)] @ x)
        for i, xi in zip(ids, x):
            mem = blocks[i]; w_ = cat.mu[mem] / cat.mu[mem].sum()
            gpi[mem] += p * xi * w_
        if len(ids) == 1: mono[ids[0]] += p
        else: poly += p
        if p >= 1e-3:
            supp.append((' + '.join('%s %.2f' % (cat.names[rep[i]], xi) for i, xi in zip(ids, x)), float(p)))
    lab1 = cat.lab == 1
    neutral = float(gpi[lab1 & tw].sum()); active = float(gpi[lab1 & ~tw].sum())
    tw1 = tw & (cat.lab == 1)
    pair_mass = float(gpi[tw1].sum() + gpi[cat.partner[tw1]].sum())
    selfc = np.array([cat.val[i, i] == 1 for i in range(len(cat.cat))])
    iC = [i for i, (c, g) in enumerate(cat.cat) if cat.L.rep[c] == 'C']
    coopmask = selfc.copy(); coopmask[iC] = False
    row = dict(label=label, kernel=kernel, N=N, prior=list(cat.prior_g), n_blocks=nb, pcc=float(pcc), poly=float(poly),
               pi_active_long=active, pi_neutral_long=neutral, pi_long=float(gpi[lab1].sum()),
               twin_pair_mass=pair_mass, allocation_twins=(neutral / pair_mass if pair_mass > 0 else float('nan')),
               coop_pi=float(gpi[coopmask].sum()), coop_long_active=float(gpi[coopmask & lab1 & ~tw].sum()),
               coop_long_neutral=float(gpi[coopmask & lab1 & tw].sum()), coop_g0=float(gpi[coopmask & ~lab1].sum()),
               pi_D=float(sum(gpi[i] for i, (c, g) in enumerate(cat.cat) if cat.L.rep[c] == 'D')),
               n_states=len(keys), n_deep_poly=len(extra), log10_cut=res['log10_cut'],
               support=sorted(supp, key=lambda s: -s[1])[:14],
               top_genotypes=[(cat.names[i], float(gpi[i]), bool(tw[i]) if lab1[i] else None) for i in np.argsort(-gpi)[:20]])
    # residual of pi on the explored generator
    LA = res['LA']
    A = np.exp(LA - LA[np.isfinite(LA)].max()); A[~np.isfinite(LA)] = 0.0
    row['residual'] = float(np.abs(pi @ A - pi * A.sum(1)).sum() / max((pi * A.sum(1)).sum(), 1e-300))
    row['gpi'] = gpi.tolist()
    if rates:
        row['rates'] = state_rates(ch, cat, blocks, rep, keys, pi, N)
    if lazy:
        KChain = _make_kchain()
        lch = KChain(prov, N=N, w=W, verbose=False, eager_poly=False).explore()
        lp = 0.0
        for key, wgt in zip(lch.keys_list, lch.pi):
            ids, x, kd = lch.states[key]; ids = list(ids); x = np.asarray(x)
            lp += wgt * float(x @ Pb[np.ix_(ids, ids)] @ x)
        sk = set(keys); lk = set(lch.keys_list); spi = dict(zip(keys, pi)); lpi_ = dict(zip(lch.keys_list, lch.pi))
        row['lazy'] = dict(pcc=float(lp), n_states=len(lk), only_seeded=len(sk - lk), only_lazy=len(lk - sk),
                           pi_only_seeded=float(sum(spi[k] for k in sk - lk)), pi_only_lazy=float(sum(lpi_[k] for k in lk - sk)),
                           cut_flow=float(lch.cut_flow))
    row['t'] = time.time() - t
    return row


def state_rates(ch, cat, blocks, rep, keys, pi, N, thresh=1e-3):
    """For every monomorphic state with pi >= thresh: total exit weight per mutation event (x N), its split strict /
    neutral / other, the top exits (mutant, destination, N rho, kind) with the mpmath Moran check of the largest; and
    the entry from D (N rho of the strongest D -> state mutant)."""
    U = ch.P.Ufull
    iD = [b for b, r in enumerate(rep) if cat.L.rep[cat.cat[r][0]] == 'D']
    kD = [ch.mono(b) for b in iD]
    out = []
    for k, p in zip(keys, pi):
        ids, x, kind = ch.states[k]
        if kind != 'mono' or p < thresh: continue
        a = ids[0]; uaa = U[a, a]
        ex = dict(strict=0.0, neutral=0.0, other=0.0); lst = []
        tot_w = ch.wstate[k]
        for (k1, k2, q), (m_q, share, kstar, uqq, uqa, uaq, _) in ch.edges.items():
            if k1 != k: continue
            rho = ch.edge_rho[(k1, k2, q)][0]
            wgt = m_q / tot_w * min(share, 1.0) * rho
            if U[q, a] > uaa + 1e-12: t_ = 'strict'
            elif max(abs(U[q, a] - uaa), abs(U[a, q] - uaa), abs(U[q, q] - uaa)) < 1e-12: t_ = 'neutral'
            else: t_ = 'other'
            ex[t_] += wgt
            lst.append((wgt, cat.names[rep[q]], describe(ch, cat, rep, k2), N * rho, t_, q, int(kstar)))
        lst.sort(key=lambda e: -e[0])
        tot = sum(ex.values())
        r = dict(state=cat.names[rep[a]], pi=float(p), N_exit=float(N * tot), exit_split={kk: float(v / tot) if tot else 0 for kk, v in ex.items()},
                 top_exits=[dict(w=float(e[0]), mutant=e[1], to=e[2], N_rho=float(e[3]), kind=e[4]) for e in lst[:5]])
        if lst:
            e = lst[0]; q = e[5]
            lr = KC.moran_log_rho(U[q, q], U[q, a], U[a, q], uaa, N, W, e[6])
            r['top_exit_mp_abs_err'] = float(abs(math.exp(lr) - e[3] / N))
        ent = [(ch.edge_rho[(k1, k2, q)][0], q) for (k1, k2, q) in ch.edges if k1 in kD and k2 == k and k not in kD]
        if ent:
            rho, q = max(ent)
            r['entry_from_D'] = dict(mutant=cat.names[rep[q]], N_rho=float(N * rho))
        out.append(r)
    return out


def describe(ch, cat, rep, key):
    ids, x, kind = ch.states[key]
    return ' + '.join('%s %.2f' % (cat.names[rep[i]], xi) for i, xi in zip(ids, x)) if kind == 'poly' else cat.names[rep[ids[0]]]


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
