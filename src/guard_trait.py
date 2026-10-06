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


def opath(name):
    """Output path; test runs at another n ($GT_N) get a prefix."""
    nn = int(os.environ.get('GT_N', 8))
    return os.path.join(GDIR, name if nn == 8 else 'n%d_%s' % (nn, name))


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

    def solve(self, targets, max_passes=200):
        """bounded_k.KTheory.solve plus the JLoeb sibling closure: an instance (S, b) of total size v concludes every
        member of S (the rule's conclusion is any A_i), but the candidate rule searches S only from one member, so a
        member's own search can miss it (found at n = 8: P[x, y] derived by an instance containing a content x's
        atom needs, while that content's own search failed, making the computed table inconsistent).  After each
        fixpoint, every member of a recorded instance gets J <= v, and the fixpoint is resumed until nothing moves.
        Values only decrease and every value is witnessed by the instance, so this is sound and more complete."""
        while True:
            r = super().solve(targets, max_passes)
            changed = False
            for A, w in list(self.Jw.items()):
                if not w: continue
                S, b = w; v = self.J.get(A, INF)
                if v >= INF: continue
                for s in S:
                    if self.J.get(s, INF) > v:
                        self.J[s] = v; self.Jw[s] = w; self.goalsJ.add(s); self.goalsT.add(s); changed = True
            if not changed:
                return r
            self.n_sibling = getattr(self, 'n_sibling', 0) + 1

    def _dist(self, L, B, c, memo):
        """bounded_k.KTheory._dist with two value-preserving accelerations (the search is otherwise unchanged):
        (i) a cache per phase memo (within one memo the T/J/M values are fixed, and the side effects -- premise
        registration -- are idempotent); (ii) GL pruning by weakening: if erase(Pi_max |- B) is not GL-valid for the
        union Pi_max of every content and box a choice could use, no subset is GL-valid, so every choice of the
        instance (and, for the full left set, every instance) is skipped exactly as seq_prune would skip it."""
        if self.cut is None or self.seq_prune is None:
            return super()._dist(L, B, c, memo)
        from itertools import combinations, product
        F = self.forms
        lb = tuple(sorted((F[x][2], F[x][1], x) for x in L if F[x][0] == FBOX))
        key = ('dist', lb, B, c)
        r = memo.get(key)
        if r is not None:
            return r
        best = INF
        feas = [h for h in lb if h[0] + 2 <= c]           # a hypothesis alone already costs a + 1 (+1 for the rule)
        if feas:
            allPi = frozenset(f for a, A, x in feas for f in ((A,) if self.cut == 'c' else (A, x)))
            if self.seq_prune(allPi, B) is False:
                feas = []
        for k in range(1, min(self.dist_arity, len(feas)) + 1):
            for H in combinations(feas, k):
                if sum(a for a, _, _ in H) + k + 1 > c: continue
                PiH = frozenset(f for a, A, x in H for f in ((A,) if self.cut == 'c' else (A, x)))
                if self.seq_prune(PiH, B) is False: continue
                opts = [((A,),) if self.cut == 'c' else ((A,), (x,), (A, x)) for a, A, x in H]
                for choice in product(*opts):
                    Pi = frozenset(f for ch in choice for f in ch)
                    charge = 0
                    for (a, A, x), ch in zip(H, choice):
                        if A in ch: charge += a + 1
                        if x in ch: charge += a + 2
                    if self.cut == 'c': charge = sum(a for a, _, _ in H) + k
                    if charge + 1 > c: continue
                    if self.seq_prune(Pi, B) is False: continue
                    sv = self.m(Pi, frozenset([B]), memo)
                    if sv >= INF: continue
                    self.mp.setdefault(B, set()).add((Pi, tuple(sorted(H)), choice))
                    self.goalsT.add(B)
                    for a, A, x in H: self.goalsT.add(A)
                    if sv + charge <= c: best = min(best, 1 + sv)
        memo[key] = best
        return best

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


def build_K(n, b, glong, cut=None, ustar_limit=40, cap=None):
    """KTheoryM on L_n's catalogue.  cap = b by default, in K and in K_c4: plays read only whether an atom content
    has a derivation of size <= b; sizes are additive and monotone (every sub-derivation, Nec premise, JLoeb premise,
    Dist+ premise and lemma-cut leaf of a size-<= b derivation has size <= b), and the Dist+ side condition
    d >= s + charges compares premise sizes with the right box's *budget* d (e.g. 2b + 8), not with the cap.  So every
    value <= b is exact at cap b.  (src/k_cut.py's long-guard family sweep used cap 2b + 8; the n = 6 validation
    compares the two.)"""
    import k_at_n8 as KN
    L, val_free, hc, hd = KN.tables(n)
    if cap is None: cap = b
    K = KTheoryM(cap=max(cap, 1), ustar_limit=ustar_limit, filter_first=True, cut=cut, glong=glong)
    K.prune = KN.make_prune(K, L, hc, hd)
    cat, kg = catalogue_genos(K, L, b)
    return K, L, cat, kg


BLOCKS = ('00', 'LL', '0L', 'L0')


def block_genos(L, kg, blk):
    nr = len(L.rep)
    bx, by = (0 if blk[0] == '0' else 1), (0 if blk[1] == '0' else 1)
    return [kg[bx * nr + c] for c in range(nr)], [kg[by * nr + c] for c in range(nr)]


def contents_block(K, gx, gy):
    contents = set(); atoms = defaultdict(list)
    for x in sorted(set(gx)):
        for y in sorted(set(gy)):
            for a in K.atoms(x, y):
                c = K.forms[a][1]; contents.add(c); atoms[c].append((x, y))
    return contents, atoms


def block_play(K, gx, gy, T=None):
    if T is not None:
        save = K.T; K.T = T
    play = K.play_fn()
    out = np.array([[int(play(x, y)) for y in gy] for x in gx], np.int8)
    if T is not None:
        K.T = save
    return out


def play_table(K, kg, T=None):
    return block_play(K, kg, kg, T)


def has_long(K, c, b):
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


def _kclosure_job(j):
    """One block of the mixed catalogue: K's closure (cap b), its play subtable, soundness, the K misses certified
    (Lemma E1 at budgets <= b + 1, Lemma H above), the uncertified misses written for the K_c4 search."""
    n, b, blk = j
    glong = b + 8
    t = time.time()
    K, L, cat, kg = build_K(n, b, glong)
    gx, gy = block_genos(L, kg, blk)
    contents, atoms = contents_block(K, gx, gy)
    t_build = time.time() - t
    passes = K.solve(sorted(contents))
    t_solve = time.time() - t - t_build
    vb = block_play(K, gx, gy)
    nchk, bad = K.soundness_check()
    if bad: nchk, bad = K4.closure_check(K)
    gl_true = [c for c in contents if K.prune(c)]
    miss = [c for c in gl_true if K.T.get(c, INF) > b]
    tc = time.time()
    cert = CertifierM(K, b, four=False)
    res = cert.run(miss)
    unc = [c for c in miss if res[c] is None]
    t_cert = time.time() - tc
    unc_long = [c for c in unc if has_long(K, c, b)]
    meta = dict(n=n, b=b, block=blk, glong=glong, cap=K.cap, n_kgenos=len(K.genos), n_contents=len(contents), passes=passes,
                t_build=t_build, t_solve=t_solve, t_cert=t_cert, sound_checked=nchk, sound_bad=len(bad),
                gl_true_contents=len(gl_true), K_derived_contents=len(gl_true) - len(miss), missing_contents=len(miss),
                certified_contents=len(miss) - len(unc), uncertified_contents=len(unc), uncertified_long=len(unc_long),
                cert_high_queries=cert.n_high, n_forms=len(K.forms))
    np.save(os.path.join(GDIR, 'vK_n%d_b%d_%s.npy' % (n, b, blk)), vb)
    cs = np.array(sorted(contents), np.int64)
    np.save(os.path.join(GDIR, 'kT_n%d_b%d_%s.npy' % (n, b, blk)), np.stack([cs, np.array([min(K.T.get(c, INF), 10**6) for c in cs], np.int64)]))
    json.dump(dict(meta=meta, uncertified=[K.show(c) for c in unc], uncertified_long=[K.show(c) for c in unc_long],
                   n_atoms_unc=[len(atoms[c]) for c in unc]),
              open(os.path.join(GDIR, 'kclosure_n%d_b%d_%s.json' % (n, b, blk)), 'w'))
    meta['t'] = time.time() - t
    return meta


def cmd_kclosure(a):
    import k_at_n8 as KN
    n, b = a.n, a.b
    L = KN.tables(n)[0]
    K = KTheoryM(cap=b, glong=b + 8)
    cat, kg = catalogue_genos(K, L, b)
    json.dump(dict(cat=cat, kg=kg, names=[K.name(g) for g in range(len(K.genos))]),
              open(os.path.join(GDIR, 'kclosure_n%d_b%d.json' % (n, b)), 'w'))
    jobs = [(n, b, blk) for blk in (a.blocks or BLOCKS)
            if not os.path.exists(os.path.join(GDIR, 'kclosure_n%d_b%d_%s.json' % (n, b, blk)))]
    with Pool(min(a.workers, max(len(jobs), 1)), maxtasksperchild=1) as pool:
        for m in pool.imap_unordered(_kclosure_job, jobs):
            print(m, flush=True)
    if os.path.exists(os.path.join(GDIR, 'vK_n%d_b%d_00.npy' % (n, b))):
        v00 = np.load(os.path.join(GDIR, 'vK_n%d_b%d_00.npy' % (n, b)))
        ref = KN.load_val(n, b) if n == 8 else np.load(os.path.join(RUNS, 'k-cut', 'K_g0_n%d_b%d.npy' % (n, b)))
        print('g = 0 block vs published K table: %d differing plays' % int((v00 != ref).sum()), flush=True)


def _kc4_job(j):
    """K_c4 search (cap b + glong) on a chunk of one block's uncertified goals (matched by printed form).  Returns
    {shown: T} for every goal derived within the cap, soundness, and the independent checker on every goal derived
    within b (Lemma C witnesses replayed with the reader's budget and the opponent's genotype)."""
    n, b, blk, goals, seed = j
    glong = b + 8
    t = time.time()
    K, L, cat, kg = build_K(n, b, glong, cut='c4')
    gx, gy = block_genos(L, kg, blk)
    want = set(goals); cmap = {}
    rp = os.path.join(GDIR, 'relevant_n%d_b%d_%s.json' % (n, b, blk))
    where = json.load(open(rp)).get('where', {}) if os.path.exists(rp) else {}
    if all(g in where for g in goals):
        pairs = sorted({tuple(where[g]) for g in goals})        # one witnessing pair per goal: build only those atoms
        it = ((gx[cx], gy[cy]) for cx, cy in pairs)
    else:
        it = ((x, y) for x in sorted(set(gx)) for y in sorted(set(gy)))
    for x, y in it:
        for a_ in K.atoms(x, y):
            c = K.forms[a_][1]
            s = K.show(c)
            if s in want: cmap[s] = c
    K.solve(sorted(set(cmap.values())))
    T = {s: int(K.T.get(c, INF)) for s, c in cmap.items() if K.T.get(c, INF) <= K.cap}
    # every other uncertified content of the block that this closure derived within b (any derivation found anywhere
    # is a K_c4 derivation; the patch takes the minimum over chunks)
    unc_all = set(json.load(open(os.path.join(GDIR, 'kclosure_n%d_b%d_%s.json' % (n, b, blk))))['uncertified'])
    extra = {}
    for c, v in list(K.T.items()):
        if v <= b and K.forms[c][0] != FP:
            s = K.show(c)
            if s in unc_all and s not in T: extra[s] = int(v); cmap.setdefault(s, c)
    T.update(extra)
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
    return dict(seed=seed, block=blk, n_goals=len(goals), goals=list(goals), matched=len(cmap), T=T, sound_checked=nchk, sound_bad=len(bad),
                bad_examples=[K.show(x) for x in bad[:10]], checker=ck, t=time.time() - t, n_forms=len(K.forms), n_extra=len(extra), n_sibling=getattr(K, 'n_sibling', 0))


def _relevant_job(j):
    """Uncertified contents that can change a play.  K_c4 contains K, so a K-true atom stays true; an uncertified
    K-false atom is unknown; a certified one stays false.  A pair whose play is decided under Kleene's three-valued
    evaluation with every uncertified atom unknown cannot change, whatever the search finds; the goals are the
    uncertified contents of the atoms of the undecided pairs.  Unsearched uncertified contents keep K's value, which
    by construction changes no play."""
    n, b, blk = j
    K, L, cat, kg = build_K(n, b, b + 8)
    gx, gy = block_genos(L, kg, blk)
    contents, atoms = contents_block(K, gx, gy)
    arr = np.load(os.path.join(GDIR, 'kT_n%d_b%d_%s.npy' % (n, b, blk)))
    K.T = {int(c): (int(v) if v < 10**6 else INF) for c, v in zip(arr[0], arr[1])}
    d = json.load(open(os.path.join(GDIR, 'kclosure_n%d_b%d_%s.json' % (n, b, blk))))
    unc_s = set(d['uncertified'])
    unc = {c for c in contents if K.T.get(c, INF) > b and K.show(c) in unc_s}
    F = K.forms
    memo = {}

    def tv(f, x, y):
        t = F[f]; k = t[0]
        if k == FBOT: return False
        if k == FTOP: return True
        if k == FNOT:
            r = tv(t[1], x, y); return None if r is None else (not r)
        if k in (FAND, FOR):
            p, q = tv(t[1], x, y), tv(t[2], x, y)
            if k == FAND:
                if p is False or q is False: return False
                return None if (p is None or q is None) else True
            if p is True or q is True: return True
            return None if (p is None or q is None) else False
        if k == FBOX:
            c = t[1]
            if c in unc: return None
            return K.T.get(c, INF) <= t[2]
        raise ValueError(k)
    mc = L.mu_canon / L.mu_canon.sum()
    srcx = {}; srcy = {}
    for c_, g_ in enumerate(gx): srcx.setdefault(g_, c_)
    for c_, g_ in enumerate(gy): srcy.setdefault(g_, c_)
    goals = set(); undecided = 0; pairs = 0
    w2 = defaultdict(float); w1 = defaultdict(float); where = {}
    for x in sorted(set(gx)):
        for y in sorted(set(gy)):
            pairs += 1
            if tv(K.phi(x, y), x, y) is None:
                undecided += 1
                mx, my = mc[srcx[x]], mc[srcy[y]]
                for a_ in K.atoms(x, y):
                    c = F[a_][1]
                    if c in unc:
                        s_ = K.show(c); goals.add(s_)
                        w2[s_] += mx * my; w1[s_] = max(w1[s_], max(mx, my))
                        if s_ not in where: where[s_] = (srcx[x], srcy[y])
    return blk, sorted(goals), dict(pairs=pairs, undecided_pairs=undecided, uncertified=len(unc), relevant=len(goals),
                                    w2=dict(w2), w1=dict(w1), where=where)


def cmd_relevant(a):
    jobs = [(a.n, a.b, blk) for blk in BLOCKS]
    with Pool(min(a.workers, 4)) as pool:
        for blk, goals, st in pool.imap_unordered(_relevant_job, jobs):
            json.dump(dict(goals=goals, **st), open(os.path.join(GDIR, 'relevant_n%d_b%d_%s.json' % (a.n, a.b, blk)), 'w'))
            print(blk, {k: v for k, v in st.items() if k not in ('w1', 'w2', 'where')}, flush=True)


def goals_of(n, b, blk):
    p = os.path.join(GDIR, 'relevant_n%d_b%d_%s.json' % (n, b, blk))
    if os.path.exists(p): return sorted(json.load(open(p))['goals'])
    return sorted(json.load(open(os.path.join(GDIR, 'kclosure_n%d_b%d_%s.json' % (n, b, blk))))['uncertified'])


def cmd_kc4(a):
    """K_c4 search on the relevant goals, in tiers of decreasing weight w1 (the largest source mu among the undecided
    pairs a goal enters), chunked per block; every run appends to kc4_n*_b*.json and skips goals already searched.
    Unsearched relevant goals keep K's value; their weight is reported as the residual."""
    n, b = a.n, a.b
    path = os.path.join(GDIR, 'kc4_n%d_b%d.json' % (n, b))
    out = json.load(open(path)) if os.path.exists(path) and not a.fresh else []
    searched = {(r['block'], g) for r in out for g in r.get('goals', [])}
    seed0 = max([r['seed'] for r in out], default=-1) + 1
    jobs = []; wtop = {}
    for blk in BLOCKS:
        d = json.load(open(os.path.join(GDIR, 'relevant_n%d_b%d_%s.json' % (n, b, blk))))
        w1 = d.get('w1', {}); w2 = d.get('w2', {})
        goals = [g for g in d['goals'] if (blk, g) not in searched and w1.get(g, 1.0) >= a.wmin]
        goals.sort(key=lambda g: (-w1.get(g, 1.0), -w2.get(g, 0.0), g))
        for k in range(0, len(goals), a.chunk_size):
            j = (n, b, blk, goals[k:k + a.chunk_size], seed0 + len(jobs))
            wtop[j[4]] = w1.get(j[3][0], 1.0)
            jobs.append(j)
    jobs.sort(key=lambda j: -wtop[j[4]])
    print('%d chunks to run (wmin %g)' % (len(jobs), a.wmin), [(j[2], len(j[3])) for j in jobs], flush=True)
    with Pool(min(a.workers, len(jobs) or 1), maxtasksperchild=1) as pool:
        for r in pool.imap_unordered(_kc4_job, jobs):
            out.append(r); json.dump(out, open(path, 'w'))
            print('block %s chunk %d: %d goals, %d matched, %d derived within cap, %d within b, sound %d/%d, checker %s, %.0fs' % (
                r['block'], r['seed'], r['n_goals'], r['matched'], len(r['T']), sum(1 for v in r['T'].values() if v <= b),
                r['sound_bad'], r['sound_checked'], r['checker'], r['t']), flush=True)


def patched_tables(n, b):
    """Per block: rebuild the formulas (same construction order, so the same content ids), load K's values and the
    K_c4 search results, recompute the plays.  Returns (vK, vKc4, info) on the full catalogue."""
    import k_at_n8 as KN
    glong = b + 8
    L = KN.tables(n)[0]; nr = len(L.rep)
    p4 = os.path.join(GDIR, 'kc4_n%d_b%d.json' % (n, b))
    rows = json.load(open(p4)) if os.path.exists(p4) else []
    vK = np.zeros((2 * nr, 2 * nr), np.int8); v4 = vK.copy()
    info = dict(blocks={})
    for blk in BLOCKS:
        K, L, cat, kg = build_K(n, b, glong)
        gx, gy = block_genos(L, kg, blk)
        contents, atoms = contents_block(K, gx, gy)
        arr = np.load(os.path.join(GDIR, 'kT_n%d_b%d_%s.npy' % (n, b, blk)))
        assert len(arr[0]) == len(contents) and set(arr[0].tolist()) == contents
        K.T = {int(c): (int(v) if v < 10**6 else INF) for c, v in zip(arr[0], arr[1])}
        vb = block_play(K, gx, gy)
        assert (vb == np.load(os.path.join(GDIR, 'vK_n%d_b%d_%s.npy' % (n, b, blk)))).all()
        d = json.load(open(os.path.join(GDIR, 'kclosure_n%d_b%d_%s.json' % (n, b, blk))))
        R = [r for r in rows if r['block'] == blk]
        unc = set(goals_of(n, b, blk)); unc_all = set(d['uncertified'])
        done_g = {g for r in R for g in r.get('goals', [])}
        assert done_g <= unc
        rel = json.load(open(os.path.join(GDIR, 'relevant_n%d_b%d_%s.json' % (n, b, blk))))
        resid = sorted(unc - done_g)
        resid_w1 = max([rel.get('w1', {}).get(g, 0.0) for g in resid], default=0.0)
        resid_w2 = float(sum(rel.get('w2', {}).get(g, 0.0) for g in resid))
        Tn = {}
        for r in R:
            for s_, v in r['T'].items(): Tn[s_] = min(v, Tn.get(s_, INF))
        byshow = {K.show(c): c for c in contents if K.T.get(c, INF) > b}
        T2 = dict(K.T); newly = []
        for s_, v in Tn.items():
            assert s_ in unc_all
            if v <= b and s_ in byshow:
                T2[byshow[s_]] = v; newly.append(byshow[s_])
        v4b = block_play(K, gx, gy, T2)
        bx, by = (0 if blk[0] == '0' else 1), (0 if blk[1] == '0' else 1)
        vK[bx * nr:(bx + 1) * nr, by * nr:(by + 1) * nr] = vb
        v4[bx * nr:(bx + 1) * nr, by * nr:(by + 1) * nr] = v4b
        info['blocks'][blk] = dict(meta=d['meta'], newly_derived=len(newly), derived_within_cap=sum(1 for v in Tn.values() if v < INF),
                                   newly_examples=[K.show(c) for c in newly[:30]],
                                   newly_pairs=[(K.name(x), K.name(y)) for c in newly[:30] for x, y in atoms[c][:1]],
                                   diff_vs_K=int((v4b != vb).sum()),
                                   sound_bad=sum(r['sound_bad'] for r in R), sound_checked=sum(r['sound_checked'] for r in R),
                                   checker={k: sum(r['checker'][k] for r in R) for k in R[0]['checker']} if R else {},
                                   t_kc4=sum(r['t'] for r in R), searched=len(done_g), relevant=len(unc),
                                   unsearched=len(resid), unsearched_max_w1=resid_w1, unsearched_w2=resid_w2)
    return vK, v4, info


def cmd_patch(a):
    vK, v4, info = patched_tables(a.n, a.b)
    np.save(os.path.join(GDIR, 'vK_n%d_b%d.npy' % (a.n, a.b)), vK)
    np.save(os.path.join(GDIR, 'vKc4_n%d_b%d.npy' % (a.n, a.b)), v4)
    info['diff_vs_K'] = int((v4 != vK).sum())
    json.dump(info, open(os.path.join(GDIR, 'patch_n%d_b%d.json' % (a.n, a.b)), 'w'), indent=1)
    print('diff vs K', info['diff_vs_K'], {k: (v['newly_derived'], v['diff_vs_K'], v['sound_bad'], v['checker']) for k, v in info['blocks'].items()})


def cmd_full(a):
    """Validation (small n): the full K_c4 closure over the mixed catalogue, compared with the targeted table."""
    n, b = a.n, a.b; glong = b + 8
    t = time.time()
    K, L, cat, kg = build_K(n, b, glong, cut='c4')
    ug = sorted(set(kg)); contents, atoms = contents_block(K, ug, ug)
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


# ====================================================================== arms
PRIORS = {'u': (0.5, 0.5), '91': (0.9, 0.1)}
_BASE = {}


def base(n=None, b=16):
    """(val of the mixed K_c4 table, catalogue list, L, gdep per source).  n defaults to $GT_N or 8 (6 for tests)."""
    n = n or int(os.environ.get('GT_N', 8))
    if (n, b) not in _BASE:
        import k_at_n8 as KN
        L = KN.tables(n)[0]
        d = json.load(open(os.path.join(GDIR, 'kclosure_n%d_b%d.json' % (n, b))))
        v = np.load(os.path.join(GDIR, 'vKc4_n%d_b%d.npy' % (n, b)))
        cat = [tuple(x) for x in d['cat']]
        gd = np.array([gdep(parse(s)) for s in L.rep])
        _BASE[(n, b)] = (v, cat, L, gd)
    return _BASE[(n, b)]


def erased_index(cat):
    pos = {(c, g): i for i, (c, g) in enumerate(cat)}
    return np.array([pos[(c, 0)] for c, g in cat])


def faker_partner_sets(v, cat):
    """Newly enabled fakers and cooperative partners (design choice 8)."""
    import modal as M
    U, _ = M.pd_payoffs(v, M.PD)
    e = erased_index(cat); lab = np.array([g for c, g in cat])
    Ue = U[np.ix_(e, e)]
    inv = U > np.diag(U)[None, :] + 1e-12           # inv[z, x]: z strictly invades x
    inv_e = Ue > np.diag(Ue)[None, :] + 1e-12
    new_inv = inv & ~inv_e
    fakers = sorted(set(np.nonzero(new_inv.any(1))[0].tolist()))
    mut = (v == 1) & (v.T == 1); mut_e = mut[np.ix_(e, e)]
    new_mut = mut & ~mut_e
    fs = set(fakers)
    partners = [z for z in np.nonzero(new_mut.any(1))[0].tolist() if lab[z] == 1 and z not in fs]
    return fakers, partners, new_inv, new_mut


def price_cost(cat, gd, c, N, b=16):
    """Amortized c (2b + 8) / N per match for every g = L genotype whose source reads a guard."""
    G_ = len(cat)
    cost = np.zeros((G_, G_))
    for i, (s, g) in enumerate(cat):
        if g == 1 and gd[s]:
            cost[i, :] = c * (2 * b + 8) / N
    return cost


def make_cat(arm, prior, N=10000):
    """Catalogues: 'mixed' (the (source, g) table), 'g0' / 'L' (one guard population, guard-free sources included),
    'sham' (the g = 0 block with a label that changes nothing), 'delF' / 'delP' / 'delFP' (attribution: newly
    enabled fakers / partners / both deleted, prior weight 0), 'price:c'."""
    v, cat, L, gd = base()
    pg = PRIORS[prior]
    nr = len(L.rep)
    if arm in ('g0', 'L'):
        lab = 0 if arm == 'g0' else 1
        ii = [i for i, (c, g) in enumerate(cat) if g == lab]
        return Cat(v[np.ix_(ii, ii)], [cat[i] for i in ii], L, (1.0, 0.0) if lab == 0 else (0.0, 1.0))
    if arm == 'sham':
        ii = [i for i, (c, g) in enumerate(cat) if g == 0]
        v0 = v[np.ix_(ii, ii)]
        pos = {c: k for k, (c, g) in enumerate(cat[i] for i in ii)}
        vs = np.zeros_like(v)
        idx = np.array([pos[c] for c, g in cat])
        vs = v0[np.ix_(idx, idx)]
        C = Cat(vs, cat, L, pg)
        C.names = ['%s%s' % (L.rep[c], '/h' if g else '') for c, g in cat]
        return C
    if arm.startswith('price:'):
        c = float(arm.split(':')[1])
        return Cat(v, cat, L, pg, cost=price_cost(cat, gd, c, N))
    C = Cat(v, cat, L, pg)
    if arm in ('delF', 'delP', 'delFP'):
        fk, pt, _, _ = faker_partner_sets(v, cat)
        dele = (fk if arm in ('delF', 'delFP') else []) + (pt if arm in ('delP', 'delFP') else [])
        keep = [i for i in range(len(cat)) if i not in set(dele)]
        C2 = Cat(v[np.ix_(keep, keep)], [cat[i] for i in keep], L, pg)
        # a deleted genotype's partner loses its partner index; Cat recomputes partners on the kept list
        C2.deleted = [C.names[i] for i in dele]
        return C2
    return C


def _chain_job(j):
    arm, kernel, prior, N = j
    C = make_cat(arm, prior, N)
    kern = kernel if arm not in ('g0', 'L') else 'joint'
    r = run_chain(C, kern, N, label='%s %s %s' % (arm, kernel, prior))
    r.update(arm=arm, kernel_req=kernel, prior_key=prior)
    if hasattr(C, 'deleted'): r['deleted'] = C.deleted
    r['names'] = C.names
    return r


def cmd_chain(a):
    path = opath('chains.json')
    rows = json.load(open(path)) if os.path.exists(path) else []
    done = {(r['arm'], r['kernel_req'], r['prior_key'], r['N']) for r in rows}
    jobs = []
    for spec in a.cells:
        arm, kernel, prior, N = spec.split(',')
        if (arm, kernel, prior, int(N)) not in done:
            jobs.append((arm, kernel, prior, int(N)))
    print('%d jobs' % len(jobs), flush=True)
    with Pool(min(a.workers, max(len(jobs), 1))) as pool:
        for r in pool.imap_unordered(_chain_job, jobs):
            rows.append(r); json.dump(rows, open(path, 'w'), default=str)
            print('%-28s N=%-6d P(C,C) %.6f pi(D) %.3f active-L %.4f neutral-L %.4f alloc %.4f coop(g0/Lneu/Lact) %.3f/%.3f/%.3f blocks %d states %d deep %d resid %.1e lazy %s (%.0fs)' % (
                r['label'], r['N'], r['pcc'], r['pi_D'], r['pi_active_long'], r['pi_neutral_long'], r['allocation_twins'],
                r['coop_g0'], r['coop_long_neutral'], r['coop_long_active'], r['n_blocks'], r['n_states'], r['n_deep_poly'],
                r['residual'], r.get('lazy', {}).get('pcc'), r['t']), flush=True)
            print('    support:', r['support'][:6], flush=True)


# ====================================================================== static screening
CORE0_DEFAULT = ['BOX(THEM(ME))', 'BOX1(THEM(ME))', 'and(BOX(THEM(ME)),BOXD1(THEM(^D)))', 'BOX(THEM(THEM))', 'BOX1(THEM(THEM))']


def chain_core(arm, N=10000, prior='u', kernel='joint', thresh=1e-3):
    """Supported self-cooperators (pi >= thresh) of a chain row in chains.json, as genotype names."""
    path = opath('chains.json')
    if not os.path.exists(path): return None
    for r in json.load(open(path)):
        if r['arm'] == arm and r['N'] == N and r['prior_key'] == prior and r['kernel_req'] == kernel:
            names = r['names']; gpi = np.array(r['gpi'])
            return [(names[i], float(gpi[i])) for i in np.argsort(-gpi) if gpi[i] >= thresh]
    return None


def cmd_static(a):
    import modal as M
    from chain import fixation
    v, cat, L, gd = base()
    C = Cat(v, cat, L, PRIORS['u'])
    U = C.U; names = C.names; G_ = len(cat); lab = C.lab; mu = C.mu
    e = erased_index(cat)
    pos = {nm: i for i, nm in enumerate(names)}
    tw = C.twins()
    out = {}
    # -- table summary
    nr = len(L.rep)
    i0 = np.nonzero(lab == 0)[0]; i1 = np.nonzero(lab == 1)[0]
    v0 = v[np.ix_(i0, i0)]
    nn = int(os.environ.get('GT_N', 8))
    pKc = os.path.join(RUNS, 'k-cut', 'Kc_g0_n%d_b16.npy' % nn)
    vKc = np.load(pKc) if os.path.exists(pKc) else None
    import k_at_n8 as KN
    vK = KN.load_val(8, 16) if nn == 8 else np.load(os.path.join(RUNS, 'k-cut', 'K_g0_n%d_b16.npy' % nn))
    mc = L.mu_canon / L.mu_canon.sum()
    def mu2(mask_pairs):
        return float(sum(mc[i] * mc[j] for i, j in mask_pairs))
    out['g0_block'] = dict(diff_vs_K=int((v0 != vK).sum()), diff_vs_Kc=(int((v0 != vKc).sum()) if vKc is not None else None),
                           mu2_vs_Kc=(mu2(np.argwhere(v0 != vKc)) if vKc is not None else None),
                           changed_vs_Kc=[(L.rep[i], L.rep[j], int(vKc[i, j]), int(v0[i, j])) for i, j in np.argwhere(v0 != vKc)[:20]] if vKc is not None else None)
    vLL = v[np.ix_(i1, i1)]
    out['LL_block'] = dict(diff_vs_g0=int((vLL != v0).sum()), mu2=mu2(np.argwhere(vLL != v0)))
    out['cross'] = dict(g0_reader_vs_L=int((v[np.ix_(i0, i1)] != v0).sum()), L_reader_vs_g0=int((v[np.ix_(i1, i0)] != v0).sum()))
    # -- twins
    act = [i for i in i1 if not tw[i]]
    out['twins'] = dict(n_long=len(i1), n_twins=int(tw.sum()), n_active=len(act), n_guard_free=int((~gd).sum()),
                        mu_active=float(mc[[cat[i][0] for i in act]].sum()), mu_twin=float(mc[[cat[i][0] for i in i1 if tw[i]]].sum()),
                        active_examples=[names[i] for i in sorted(act, key=lambda i: -mu[i])[:40]])
    # -- action-change table
    tab = defaultdict(float); cnt = defaultdict(int); bydir = defaultdict(float)
    ex = defaultdict(list)
    for x in range(G_):
        for y in range(G_):
            if lab[x] == 0 and lab[y] == 0: continue
            xb, yb = e[x], e[y]
            if v[x, y] == v[xb, yb]: continue
            new_x, new_y = v[x, y], v[y, x]
            if new_x == 1 and new_y == 1: k = 'enabled cooperation (new mutual C)'
            elif new_x == 1 and new_y == 0: k = 'x newly suckered (enabled exploitation by y)'
            elif new_x == 0 and new_y == 1: k = 'x newly exploits y (enabled exploitation by x)'
            else: k = 'protection (new mutual D)'
            w_ = mu[x] * mu[y]
            tab[k] += w_; cnt[k] += 1
            bydir['%s reader, %s opponent' % ('L' if lab[x] else '0', 'L' if lab[y] else '0')] += w_
            if len(ex[k]) < 12: ex[k].append((names[x], names[y], int(v[xb, yb]), int(v[x, y]), int(v[y, x])))
    expl = tab['x newly suckered (enabled exploitation by y)'] + tab['x newly exploits y (enabled exploitation by x)']
    out['action_changes'] = dict(weight=dict(tab), count=dict(cnt), by_direction=dict(bydir), examples=dict(ex),
                                 enabled_cooperation=tab['enabled cooperation (new mutual C)'], enabled_exploitation=expl,
                                 ratio_coop_to_expl=(tab['enabled cooperation (new mutual C)'] / expl if expl > 0 else float('inf')))
    # -- P*-type sources (cooperate with themselves only at g = L) and fakers acting only against g = L readers
    pstar = [L.rep[c] for c in range(nr) if v[pos.get(L.rep[c] + '/L', 0), pos.get(L.rep[c] + '/L', 0)] == 1 and v[c, c] == 0 and gd[c]]
    fk, pt, new_inv, new_mut = faker_partner_sets(v, cat)
    vict = defaultdict(list)
    for z, x in np.argwhere(new_inv):
        vict[names[z]].append(names[x])
    only_vs_L = {nm: vs[:8] for nm, vs in vict.items() if all(vv.endswith('/L') for vv in vs)}
    godel, con, _ = KC.faker_sets()
    gset = set(godel) | set(con)
    gc_new = sorted({names[z].replace('/L', '') for z in fk if names[z].replace('/L', '') in gset})
    out['pstar_type'] = dict(n=len(pstar), mu=float(sum(mc[L.rep.index(s)] for s in pstar)), sources=pstar[:60])
    out['fakers'] = dict(n=len(fk), mu=float(mu[fk].sum()), names=[names[z] for z in sorted(fk, key=lambda z: -mu[z])][:60],
                         victims={names[z]: vict[names[z]][:8] for z in sorted(fk, key=lambda z: -mu[z])[:30]},
                         only_vs_L_readers=len(only_vs_L), godel_con_classes_newly_invading=gc_new, n_godel_con=len(gc_new))
    out['partners'] = dict(n=len(pt), mu=float(mu[pt].sum()), names=[names[z] for z in sorted(pt, key=lambda z: -mu[z])][:60])
    named = ['and(BOX1(THEM(ME)),not(BOX(THEM(ME))))', 'and(BOX1(THEM(ME)),not(BOX(THEM(^C))))', 'BOX(THEM(ME))', 'BOX1(THEM(ME))',
             'and(BOX(THEM(ME)),BOXD1(THEM(^D)))', 'BOX(THEM(THEM))', 'BOX1(THEM(THEM))', 'not(BOX(THEM(ME)))', 'C', 'D']
    out['named_self'] = {s: dict(g0=int(v[pos[s], pos[s]]) if s in pos else None,
                                 gL=int(v[pos[s + '/L'], pos[s + '/L']]) if s + '/L' in pos else None) for s in named}
    out['named_cross'] = {x: {y: int(v[pos[x], pos[y]]) for y in [n_ for s in named[:7] for n_ in (s, s + '/L') if n_ in pos]}
                          for x in [n_ for s in named[:7] for n_ in (s, s + '/L') if n_ in pos]}
    # -- cores (from the reference chains if present)
    core0 = chain_core('g0') or [(s, None) for s in CORE0_DEFAULT]
    coreL = chain_core('L') or []
    out['core0'] = core0; out['coreL'] = coreL
    sc = [i for i in range(G_) if v[i, i] == 1 and L.rep[cat[i][0]] != 'C']
    iD = pos['D']
    est = [i for i in sc if v[i, iD] == 0]
    out['establishers'] = dict(n=len(est), mu=float(mu[est].sum()), n_g0=sum(1 for i in est if lab[i] == 0),
                               n_L=sum(1 for i in est if lab[i] == 1), n_L_active=sum(1 for i in est if lab[i] == 1 and not tw[i]))
    def core_ids(core, labv):
        ids = []
        for nm, p in core:
            if nm in pos and nm != 'D' and nm != 'C' and v[pos[nm], pos[nm]] == 1: ids.append(pos[nm])
        return ids
    c0 = core_ids(core0, 0); cL = core_ids(coreL, 1)
    def incompatible(a_, b_):
        mutD = v[a_, b_] == 0 and v[b_, a_] == 0
        return bool(mutD or U[a_, b_] > U[b_, b_] + 1e-12 or U[b_, a_] > U[a_, a_] + 1e-12)
    out['incompatible_core_pairs'] = [(names[a_], names[b_]) for a_ in c0 for b_ in cL if a_ != b_ and incompatible(a_, b_)]
    for tagc, core in (('core0', c0), ('coreL', cL)):
        if not core: continue
        riv = [r_ for r_ in est if r_ not in core and any(v[r_, k] == 0 and v[k, r_] == 0 for k in core)]
        coopc = [i for i in sc if not (U[i] == U[pos['C']]).all()]
        def bridges(r_):
            return [bb for bb in coopc if all(v[bb, k] == 1 and v[k, bb] == 1 for k in core) and v[bb, r_] == 1 and v[r_, bb] == 1]
        rv = sorted(riv, key=lambda i: -mu[i])
        out['rivals_' + tagc] = dict(core=[names[i] for i in core], n=len(riv), mu=float(mu[riv].sum()),
                                     n_active_long=sum(1 for i in riv if lab[i] == 1 and not tw[i]),
                                     top=[(names[i], float(mu[i]), len(bridges(i))) for i in rv[:20]],
                                     bridgeless=[names[i] for i in rv if not bridges(i)][:20],
                                     bridgeless_mu=float(sum(mu[i] for i in rv if not bridges(i))),
                                     strict_invaders=[(names[z], names[k]) for k in core for z in range(G_) if U[z, k] > U[k, k] + 1e-12][:30])
    # -- four encounter payoffs and exact N rho for core guard mutants (g = L mutant in a g = 0 resident, same source)
    enc = []
    for s in ['BOX(THEM(ME))', 'BOX1(THEM(ME))', 'and(BOX(THEM(ME)),BOXD1(THEM(^D)))', 'BOX(THEM(THEM))', 'BOX1(THEM(THEM))',
              'and(BOX1(THEM(ME)),not(BOX(THEM(ME))))'] + [nm for nm, p in core0 if nm not in CORE0_DEFAULT and '/L' not in nm]:
        if s not in pos or s + '/L' not in pos: continue
        r0, m1 = pos[s], pos[s + '/L']
        four = dict(rr=float(U[r0, r0]), rm=float(U[r0, m1]), mr=float(U[m1, r0]), mm=float(U[m1, m1]))
        row = dict(source=s, guard_free=not gd[cat[r0][0]], twin=bool(tw[m1]), **four)
        for N in (1000, 10000):
            row['N_rho_%d' % N] = float(N * fixation(four['mm'], four['mr'], four['rm'], four['rr'], N, W, N))
        enc.append(row)
    out['four_encounters'] = enc
    # P*_L against the g = 0 core
    ps = 'and(BOX1(THEM(ME)),not(BOX(THEM(ME))))/L'
    out['pstarL_invades_core0'] = [names[k] for k in c0 if U[pos[ps], k] > U[k, k] + 1e-12] if ps in pos else None
    out['pstarL_vs_core0'] = {names[k]: (int(v[pos[ps], k]), int(v[k, pos[ps]])) for k in c0} if ps in pos else None
    json.dump(out, open(opath('static.json'), 'w'), indent=1, default=str)
    for k_ in ('g0_block', 'LL_block', 'cross', 'twins', 'pstar_type', 'partners', 'establishers'):
        print(k_, {kk: vv for kk, vv in out[k_].items() if not isinstance(vv, list) or len(vv) < 8} if isinstance(out[k_], dict) else out[k_])
    print('action changes', {k_: (round(vv, 12), out['action_changes']['count'][k_]) for k_, vv in out['action_changes']['weight'].items()},
          'ratio coop/expl %.3f' % out['action_changes']['ratio_coop_to_expl'])
    print('fakers', out['fakers']['n'], out['fakers']['mu'], 'godel/con newly invading', out['fakers']['n_godel_con'])
    print('four encounters', enc)
    print('P*_L invades core0:', out['pstarL_invades_core0'])


# ====================================================================== lottery (eps = 0)
def lottery_job(j):
    """eps = 0 islands at (N, I) = (100, 64), mN = 1, genotype level (no lumping, so holders keep their guard).
    Pairing: island founders' sources are drawn iid from mu_canon with the same seed in every arm; in the mixed arm
    each founder's guard label is then drawn from the prior with an independent stream."""
    import almost_all_seeds as AS
    arm, prior, N, I, rep = j
    v, cat, L, gd = base()
    if arm == 'g0':
        C = make_cat('g0', 'u')
    else:
        C = make_cat('mixed', prior)
    U = np.ascontiguousarray(C.U, dtype=float); PCC = np.ascontiguousarray(C.PCC, dtype=float)
    G_ = len(C.cat)
    pos = {(c, g): i for i, (c, g) in enumerate(C.cat)}
    nr = len(L.rep)
    mc = L.mu_canon / L.mu_canon.sum()
    rng = np.random.default_rng([N, I, 8, rep, 2026106])
    rngg = np.random.default_rng([N, I, 8, rep, 61])
    pg = PRIORS[prior]
    init = np.zeros((I, G_), np.int64)
    for i in range(I):
        cnt = rng.multinomial(N, mc)
        for c in np.nonzero(cnt)[0]:
            if arm == 'g0':
                init[i, pos[(c, 0)]] += cnt[c]
            else:
                k1 = rngg.binomial(cnt[c], pg[1])
                init[i, pos[(c, 0)]] += cnt[c] - k1; init[i, pos[(c, 1)]] += k1
    iC = pos[(L.rep.index('C'), 0)]
    coop = np.array([PCC[k, k] >= 0.95 and L.rep[C.cat[k][0]] != 'C' for k in range(G_)])
    t = time.time()
    res = AS._run(U, PCC, init, N, AS.W, 1.0 / N, 100000, 20, 100003 * rep + 7 * N + I + 1000 + 99991, iC, coop)
    st, sg, counts, isl_cc, isl_pay, first_noC, ext_C, lost_b, lost_a, tr_cc, tr_np, loss_log = res
    cc = float(isl_cc.mean()); pay = float(isl_pay.mean())
    tw = C.twins()
    holders = []
    for i in range(I):
        cw = counts[i] * coop
        if cw.sum() * 2 < N:
            holders.append(None); continue
        k = int(np.argmax(cw)); c, g = C.cat[k]
        holders.append(dict(name=C.names[k], g=int(g), twin=bool(tw[k]) if g == 1 else None, guard_free=not bool(gd[c])))
    est = int(np.argmax(tr_cc >= 0.9)) * 20 if (tr_cc >= 0.9).any() else None
    glob = counts.sum(0)
    return dict(arm=arm, prior=prior, N=N, I=I, rep=rep, status=AS.STATUS[st], stop_gen=int(sg), pcc=cc, pay=pay,
                outcome=AS.outcome(cc, pay) if st in (1, 2, 3) else ('unresolved' if st == 4 else None),
                n_eff_islands=int((isl_cc >= 0.95).sum()), holders=holders,
                establish_gen=est, allc_extinct_gen=int(ext_C), first_noC_median=float(np.median(first_noC[first_noC > 0])) if (first_noC > 0).any() else None,
                lost_before=int(lost_b), lost_after=int(lost_a), coexist_until=int(sg),
                final={C.names[k]: int(x) for k, x in enumerate(glob) if x > 0}, t=time.time() - t)


def cmd_lottery(a):
    import almost_all_seeds as AS
    path = opath('lottery.json')
    rows = json.load(open(path))['rows'] if os.path.exists(path) else []
    done = {(r['arm'], r['prior'], r['rep']) for r in rows}
    cells = [('g0', 'u'), ('mixed', 'u'), ('mixed', '91')]
    jobs = [(arm, pr, 100, 64, rep) for arm, pr in cells for rep in range(a.reps) if (arm, pr, rep) not in done]
    with Pool(a.workers) as pool:
        for r in pool.imap_unordered(lottery_job, jobs, chunksize=1):
            rows.append(r); json.dump(dict(rows=rows), open(path, 'w'), default=str)
            print(r['arm'], r['prior'], r['rep'], r['outcome'], r['status'], r['n_eff_islands'], '%.0fs' % r['t'], flush=True)
    summ = []
    for arm, pr in cells:
        R = sorted([r for r in rows if r['arm'] == arm and r['prior'] == pr], key=lambda r: r['rep'])
        res = [r for r in R if r['outcome'] not in ('unresolved', None)]
        k = sum(1 for r in res if r['outcome'] == 'efficient')
        lo, hi = AS.wilson(k, len(res))
        H = [h for r in R for h in r['holders'] if h]
        nL_act = sum(1 for h in H if h['g'] == 1 and not h['twin']); nL_tw = sum(1 for h in H if h['g'] == 1 and h['twin'])
        n0 = sum(1 for h in H if h['g'] == 0)
        summ.append(dict(arm=arm, prior=pr, n=len(res), efficient=k, frac=k / max(len(res), 1), wilson=[lo, hi], censored=len(R) - len(res),
                         holders=len(H), holders_g0=n0, holders_L_active=nL_act, holders_L_twin=nL_tw,
                         share_g0=n0 / max(len(H), 1), share_L_active=nL_act / max(len(H), 1), share_L_by_bit=(nL_act + nL_tw) / max(len(H), 1),
                         mean_eff_islands=float(np.mean([r['n_eff_islands'] for r in R])) if R else None,
                         mean_stop=float(np.mean([r['stop_gen'] for r in R])) if R else None,
                         losses=sum(r['lost_before'] + r['lost_after'] for r in R)))
        print(summ[-1], flush=True)
    # paired differences against g0 (per seed: efficient indicator; and efficient-island fraction)
    pairs = {}
    by = {(r['arm'], r['prior'], r['rep']): r for r in rows}
    for pr in ('u', '91'):
        d1 = []; d2 = []
        for rep in range(a.reps):
            r0 = by.get(('g0', 'u', rep)); r1 = by.get(('mixed', pr, rep))
            if r0 is None or r1 is None: continue
            d1.append(int(r1['outcome'] == 'efficient') - int(r0['outcome'] == 'efficient'))
            d2.append((r1['n_eff_islands'] - r0['n_eff_islands']) / 64)
        if d1:
            m1 = float(np.mean(d1)); s1 = float(np.std(d1, ddof=1) / np.sqrt(len(d1))) if len(d1) > 1 else 0.0
            m2 = float(np.mean(d2)); s2 = float(np.std(d2, ddof=1) / np.sqrt(len(d2))) if len(d2) > 1 else 0.0
            pairs[pr] = dict(n=len(d1), diff_efficient=m1, ci95=[m1 - 1.96 * s1, m1 + 1.96 * s1],
                             diff_island_frac=m2, ci95_island=[m2 - 1.96 * s2, m2 + 1.96 * s2], discordant=sum(1 for x in d1 if x != 0))
    print(pairs)
    json.dump(dict(rows=rows, summary=summ, paired=pairs), open(path, 'w'), default=str, indent=1)


def cmd_collect(a):
    """runs/guard-trait.json: block metas, relevance, patch summary, static screening, chain rows (without the
    per-genotype vectors), lottery summary."""
    n, b = 8, 16
    out = dict(blocks={}, relevant={})
    for blk in BLOCKS:
        p = os.path.join(GDIR, 'kclosure_n%d_b%d_%s.json' % (n, b, blk))
        if os.path.exists(p): out['blocks'][blk] = json.load(open(p))['meta']
        p = os.path.join(GDIR, 'relevant_n%d_b%d_%s.json' % (n, b, blk))
        if os.path.exists(p): out['relevant'][blk] = {k: v for k, v in json.load(open(p)).items() if k != 'goals'}
    for nm, key in (('patch_n8_b16.json', 'patch'), ('static.json', 'static'), ('lottery.json', 'lottery')):
        p = os.path.join(GDIR, nm)
        if os.path.exists(p):
            d = json.load(open(p))
            if key == 'lottery': d = {k: v for k, v in d.items() if k != 'rows'}
            out[key] = d
    p = os.path.join(GDIR, 'chains.json')
    if os.path.exists(p):
        out['chains'] = [{k: v for k, v in r.items() if k not in ('gpi', 'names')} for r in json.load(open(p))]
    for nm in ('scaling.json', 'n6_validation.json'):
        p = os.path.join(GDIR, nm)
        if os.path.exists(p): out[nm.replace('.json', '')] = json.load(open(p))
    json.dump(out, open(os.path.join(RUNS, 'guard-trait.json'), 'w'), indent=1, default=str)
    print('wrote runs/guard-trait.json', list(out))


def main():
    p = argparse.ArgumentParser()
    sp = p.add_subparsers(dest='cmd')
    q = sp.add_parser('kclosure'); q.add_argument('--n', type=int, default=8); q.add_argument('--b', type=int, default=16)
    q.add_argument('--blocks', nargs='*'); q.add_argument('--workers', type=int, default=2)
    q = sp.add_parser('kc4'); q.add_argument('--n', type=int, default=8); q.add_argument('--b', type=int, default=16)
    q.add_argument('--wmin', type=float, default=0.0); q.add_argument('--chunk-size', type=int, default=400)
    q.add_argument('--workers', type=int, default=3); q.add_argument('--fresh', action='store_true')
    for nm in ('patch', 'full'):
        q = sp.add_parser(nm); q.add_argument('--n', type=int, default=8); q.add_argument('--b', type=int, default=16)
    q = sp.add_parser('chain'); q.add_argument('--cells', nargs='+'); q.add_argument('--workers', type=int, default=3)
    sp.add_parser('static'); sp.add_parser('collect')
    q = sp.add_parser('relevant'); q.add_argument('--n', type=int, default=8); q.add_argument('--b', type=int, default=16)
    q.add_argument('--workers', type=int, default=2)
    q = sp.add_parser('lottery'); q.add_argument('--reps', type=int, default=20); q.add_argument('--workers', type=int, default=3)
    a = p.parse_args()
    {'kclosure': cmd_kclosure, 'kc4': cmd_kc4, 'patch': cmd_patch, 'full': cmd_full, 'chain': cmd_chain,
     'static': cmd_static, 'lottery': cmd_lottery, 'relevant': cmd_relevant, 'collect': cmd_collect}[a.cmd](a)


if __name__ == '__main__':
    main()
