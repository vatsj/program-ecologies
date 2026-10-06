"""K with the 4-rule, and a frozen classifier for what a sound bounded prover loses (specs/2026-10-05-k-four.md;
predictions/2026-10-05-k-four.md; notes/k-four.md).

    python3 src/k_four.py repro            # K tables reproduce with the option off
    python3 src/k_four.py classify          # Part B on the K-disarmed label (frozen classifier)
    python3 src/k_four.py ktables --four mono --budgets ... [--goff 1]
    ...

The 4-rule itself is the `four` option of `src/bounded_k.py` (None / 'lit' / 'mono'); everything else lives here.
"""
import argparse, json, os, sys, time
import numpy as np
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(__file__))
import bounded_k as BK
import gl_proofs as G
from gl_proofs import FP, FBOT, FTOP, FNOT, FAND, FOR, FIMP, FBOX
from conj4 import parse, src as psrc

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS = os.path.join(ROOT, 'runs')
KDIR8 = os.path.join(RUNS, 'k-at-n8')
K4DIR = os.path.join(RUNS, 'k-four')
os.makedirs(K4DIR, exist_ok=True)

FB = 'BOX(THEM(ME))'
PB = 'and(BOX(THEM(ME)),BOXD1(THEM(^D)))'
PSTAR = 'and(BOX1(THEM(ME)),not(BOX(THEM(ME))))'
P2 = 'and(BOX1(THEM(ME)),not(BOX(THEM(^C))))'
P12B = 'and(and(BOX1(THEM(ME)),not(BOX(THEM(^C)))),BOXD2(THEM(^D)))'
PS1B = 'and(and(BOX1(THEM(ME)),not(BOX(THEM(ME)))),BOXD2(THEM(^D)))'
PB2 = 'and(BOX(THEM(ME)),BOXD2(THEM(^D)))'


# ====================================================================== Part B: the frozen classifier
# Frozen at the commit that introduces it (predictions/2026-10-05-k-four.md, "Classifier, frozen"); evaluated only
# afterwards.  Do not edit the functions in this section after the freeze; a change is a new classifier with a new name.

def _subformulas(th, f, out):
    out.add(f)
    t = th.forms[f]
    for a in t[1:]:
        if t[0] != FP:
            _subformulas(th, a, out)
    return out


def _is_guard(th, f):
    """f = ~[]^k F with k >= 1."""
    F = th.forms
    if F[f][0] != FNOT: return False
    g = F[f][1]; k = 0
    while F[g][0] == FBOX:
        k += 1; g = F[g][1]
    return k >= 1 and F[g][0] == FBOT


def con_under_box(th, f):
    """True iff f has a syntactic subformula []C (no unfolding) such that C has a guard ~[]^k F (k >= 1) as a
    subformula: a Con statement under a box."""
    for s in _subformulas(th, f, set()):
        if th.forms[s][0] == FBOX:
            if any(_is_guard(th, u) for u in _subformulas(th, th.forms[s][1], set())):
                return True
    return False


class Classifier:
    """C_spec (primary, the spec's): for an eligible pair (invader z, resident x), take the minimal (size, Loeb)
    GLS+Def derivation (cut-free, src/gl_proofs.py MinSearch) of z's free-arm play against x at the lowest level k
    (0, 1, 2) at which it is provable (C: |- ~[]^k F -> P_zx, k = 0: |- P_zx; D: |- ~[]^k F -> ~P_zx, k = 0:
    P_zx |-), and flag the pair iff some GLR (Loeb-rule) application in it has
      (G) a Goedel-sentence premise: a boxed formula []B on the left of the GLR premise (the diagonal or the boxed
          context) with B in {P_uu, phi(P_uu), ~P_uu, ~phi(P_uu)} for some program u, B of the polarity of u's
          free-arm self-play (true at the stable world) and B not GL-provable at level 0 (Oracle: |- B fails); or
      (C) a Con statement under a box: some formula of the GLR premise sequent has a subformula []C whose C contains
          a guard ~[]^k F (k >= 1).
    C_pair (secondary, descriptive): the same flag on either play of the invasion (z vs x, or x vs z).
    Uncertified minimal searches fall back to the oracle's greedy derivation and are counted as such."""

    def __init__(self, maxlev=2, cap=2_000_000, W=60):
        self.maxlev = maxlev; self.cap = cap; self.W = W
        self._trace = {}

    def free_play(self, u, v):
        import conj4 as C4
        key = (u, v)
        if key not in self._trace:
            tr = C4.trace(parse(u), parse(v), self.W)
            self._trace[key] = int(tr[-1])
        return self._trace[key]

    def root(self, th, orc, x, y, play):
        p = th.P(x, y)
        for k in range(self.maxlev + 1):
            if play == 1:
                S = (frozenset(), frozenset([p])) if k == 0 else (frozenset(), frozenset([th.con_guard(k, p)]))
            else:
                S = (frozenset([p]), frozenset()) if k == 0 else (frozenset(), frozenset([th.con_guard(k, th.neg(p))]))
            if orc.prov(S):
                return k, S
        return None, None

    def derivation(self, th, orc, S):
        ms = G.MinSearch(th, orc, cap=self.cap)
        r = ms.minimize(S)
        if r is not None and r['certified']:
            return dtree(ms, S), dict(size=r['c'][0], loeb=r['c'][1], certified=True)
        d = greedy_tree(th, orc, S)
        return d, dict(size=_tsize(d), loeb=_tloeb(d), certified=False)

    def triggers(self, th, orc, d):
        """Walk the derivation; return (flagG, flagC, trigger descriptions).  Only hypotheses *used* in the GLR
        premise's subtree count (a formula is used if it, or for a boxed hypothesis []B also B, is principal in some
        rule or closes some initial sequent of that subtree); the premise's goal A always counts."""
        inv = {}
        for P_, D_ in th.defn.items():
            inv.setdefault(D_, []).append(P_)
        progname = {i: psrc(t) for i, t in enumerate(th.progs)}
        F = th.forms
        gG = False; gC = False; out = []

        def selfplay(B):
            pol = 1
            if F[B][0] == FNOT:
                pol = 0; B = F[B][1]
            cands = [B] if F[B][0] == FP else inv.get(B, [])
            for P_ in cands:
                t = F[P_]
                if t[0] == FP and t[1] == t[2]:
                    return t[1], pol
            return None

        def walk(t):
            """Returns the set of principal / closing formulas of the subtree."""
            nonlocal gG, gC
            S, lab, ch = t
            L, R = S
            U = set()
            if lab == 'Ax':
                U |= {a for a in L & R if F[a][0] in (FP, FBOX)}
                if th.BOT in L: U.add(th.BOT)
                if th.TOP in R: U.add(th.TOP)
            elif lab == 'GLR':
                U |= {a for a in R if F[a][0] == FBOX and F[a][1] in ch[0][0][1]}
            elif lab != 'Del':
                cl = set().union(*[c[0][0] for c in ch]); cr = set().union(*[c[0][1] for c in ch])
                U |= (L - cl) | (R - cr)
            sub = set()
            for c in ch:
                sub |= walk(c)
            if lab == 'GLR':
                pL, pR = ch[0][0]
                for a in pL:
                    if F[a][0] != FBOX: continue
                    B = F[a][1]
                    if a not in sub and B not in sub: continue
                    sp = selfplay(B)
                    if sp is not None:
                        u, pol = sp
                        if self.free_play(progname[u], progname[u]) == pol and not orc.prov((frozenset(), frozenset([B]))):
                            gG = True; out.append(('G', th.show(a, progname)))
                for a in list(pL) + list(pR):
                    if (a in pR or a in sub) and con_under_box(th, a):
                        gC = True; out.append(('C', th.show(a, progname))); break
            return U | sub
        walk(d)
        return gG, gC, out[:6]

    def classify_play(self, x, y):
        """Flag for x's free-arm play against y."""
        th = G.Theory(); xi = th.prog(x); yi = th.prog(y); orc = G.Oracle(th)
        play = self.free_play(x, y)
        k, S = self.root(th, orc, xi, yi, play)
        if S is None:
            return dict(play=play, level=None, flag=False, flagG=False, flagC=False, note='no proof at level <= %d' % self.maxlev)
        d, info = self.derivation(th, orc, S)
        gG, gC, trig = self.triggers(th, orc, d)
        return dict(play=play, level=k, flag=bool(gG or gC), flagG=bool(gG), flagC=bool(gC), triggers=trig, **info)

    def classify(self, z, x):
        a = self.classify_play(z, x)
        b = self.classify_play(x, z)
        return dict(spec=a, reverse=b, flag_spec=a['flag'], flag_pair=bool(a['flag'] or b['flag']))


def dtree(ms, S):
    """MinSearch's minimal derivation as a (seq, label, children) tree, keeping 'Del' (weakening, cost 0) nodes."""
    e = ms.exact[S]
    return (S, e[2], [dtree(ms, p) for p in e[3]])


def greedy_tree(th, orc, S):
    """The oracle's own derivation as a (seq, label, children) tree (eager invertible rules, first GLR that works)."""
    if G.is_axiom(th, *S):
        return (S, 'Ax', [])
    rules = [(tuple((frozenset(p[0]), frozenset(p[1])) for p in prem), glr, lab) for prem, glr, lab in G.expand(th, S)]
    for prem, glr, lab in rules:
        if not glr and all(orc.prov(p) for p in prem):
            return (S, lab, [greedy_tree(th, orc, p) for p in prem])
    for prem, glr, lab in rules:
        if glr and orc.prov(prem[0]):
            return (S, lab, [greedy_tree(th, orc, prem[0])])
    raise ValueError('not provable')


def _tsize(d):
    return (d[1] != 'Del') + sum(_tsize(c) for c in d[2])


def _tloeb(d):
    return (d[1] == 'GLR') + sum(_tloeb(c) for c in d[2])

# ====================================================================== end of the frozen section


# ====================================================================== K+4 tables
class KTheoryG(BK.KTheory):
    """KTheory with the level-k guard read `goff` budgets up: BOXk at budget b reads [](~[]_{b+goff}^k F -> s, b).
    goff = 0 is K's convention exactly (notes/proof-length.md §3).  An exploratory variant (predictions, X-arm)."""

    def __init__(self, *a, goff=0, **kw):
        super().__init__(*a, **kw)
        self.goff = goff

    def phi(self, gx, gy):
        if self.goff == 0:
            return super().phi(gx, gy)
        ti, b = self.genos[gx]

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
            else: p, q = gy, self.geno(arg, b)
            s = self.P(p, q)
            if kind: s = self.neg(s)
            if lev:
                bb = self.BOT
                for _ in range(lev): bb = self.box(bb, b + self.goff)
                s = self.f((FIMP, self.neg(bb), s))
            return self.box(s, b)
        return tr(self.trees[ti])


def closure_check(K, rounds=4):
    """Soundness check with every box content of every flagged formula solved (the plain check reads an unsolved
    box content as unprovable, which can only produce false alarms).  Returns (n_checked, violations)."""
    for _ in range(rounds):
        n, bad = K.soundness_check()
        if not bad:
            return n, []
        new = set()
        for A in bad:
            st = [A]; seen = set()
            while st:
                f = st.pop()
                if f in seen: continue
                seen.add(f); t = K.forms[f]
                if t[0] == FBOX:
                    if t[1] not in K.T: new.add(t[1])
                    st.append(t[1])
                elif t[0] == FNOT: st.append(t[1])
                elif t[0] in (FAND, FOR, FIMP): st += [t[1], t[2]]
        if not new:
            return n, bad
        K.solve(sorted(new))
    return K.soundness_check()


def ktable4(n, b, four, goff=0, ustar_limit=40):
    """K(+4) play matrix of L_n at global budget b (src/k_at_n8.py's ktable with the 4-rule option and the guard
    offset)."""
    import k_at_n8 as KN
    L, val_free, hc, hd = KN.tables(n)
    t = time.time()
    K = KTheoryG(cap=max(b + goff, 1), ustar_limit=ustar_limit, filter_first=True, four=four, goff=goff)
    K.prune = KN.make_prune(K, L, hc, hd)
    g = [K.geno(s, b) for s in L.rep]
    contents = set()
    for x in g:
        for y in g:
            for a in K.atoms(x, y): contents.add(K.forms[a][1])
    passes = K.solve(sorted(contents))
    play = K.play_fn()
    val = np.array([[int(play(x, y)) for y in g] for x in g], np.int8)
    nchk, bad = K.soundness_check()
    meta = dict(n=n, b=b, four=four, goff=goff, passes=passes, n_contents=len(contents), sound_checked=nchk,
                sound_bad=len(bad), t=time.time() - t, diff_vs_free=int((val != val_free).sum()))
    return val, meta, K, g


def kpath(n, b, four, goff=0):
    tag = 'K' if four is None else ('K4' if four == 'lit' else 'K4m')
    return os.path.join(K4DIR, '%s_g%d_n%d_b%d.npy' % (tag, goff, n, b))


def _ktable4_job(j):
    n, b, four, goff = j
    val, meta, K, g = ktable4(n, b, four, goff)
    np.save(kpath(n, b, four, goff), val)
    json.dump(meta, open(kpath(n, b, four, goff).replace('.npy', '.json'), 'w'), indent=1)
    return meta


def load4(n, b, four, goff=0):
    if four is None and goff == 0 and n == 8 and os.path.exists(os.path.join(KDIR8, 'kval_n8_b%d.npy' % b)):
        return np.load(os.path.join(KDIR8, 'kval_n8_b%d.npy' % b))
    return np.load(kpath(n, b, four, goff))


def cmd_repro(a):
    """The option off reproduces the published K tables exactly (n = 8 against runs/k-at-n8/, n = 6 against
    k_at_n8.ktable)."""
    import k_at_n8 as KN
    out = []
    jobs = [(8, b, None, 0) for b in a.budgets]
    with Pool(a.workers) as pool:
        for m in pool.imap_unordered(_ktable4_job, jobs):
            v = np.load(kpath(8, m['b'], None, 0)); ref = np.load(os.path.join(KDIR8, 'kval_n8_b%d.npy' % m['b']))
            m['identical_to_published'] = bool((v == ref).all()); m['n_diff'] = int((v != ref).sum())
            out.append(m); print(m, flush=True)
    for b in (4, 16, 40):
        v0, m0, _, _ = KN.ktable(6, b, prune=True, filter_first=True)
        v1, m1, _, _ = ktable4(6, b, None)
        out.append(dict(n=6, b=b, identical=bool((v0 == v1).all()), sound_bad=m1['sound_bad']))
        print(out[-1], flush=True)
    json.dump(out, open(os.path.join(K4DIR, 'repro.json'), 'w'), indent=1)


# ====================================================================== dense sweeps on the named family
LADDER5 = [PB2, PSTAR, P2, P12B, PS1B]
NAMED = LADDER5 + [PB, FB, 'BOX1(THEM(ME))', 'BOX(THEM(THEM))', 'BOX1(THEM(THEM))', 'C', 'D']


def sweep_family():
    fk = json.load(open(os.path.join(RUNS, 'k-at-n8-fakers.json')))
    godel = sorted(z for z, g in fk['godel'].items() if g)
    victims = sorted({x for z in godel for x in fk['fakers'][z]})
    progs = list(dict.fromkeys(NAMED + godel + victims))
    return progs, godel, {z: fk['fakers'][z] for z in godel}


def family4(progs, b, four, goff=0, W=60):
    """K(+4m) plays among a family at global budget b (trace-pruned as k_at_n8.family_table), with the plain and
    closure soundness checks, and the exact minimal sizes of every self-play atom content."""
    import k_at_n8 as KN
    import modal as M
    t = time.time()
    K = KTheoryG(cap=max(b + goff, 1), filter_first=True, four=four, goff=goff)
    K.prune = KN.make_prune_trace(K, W)
    g = [K.geno(s, b) for s in progs]
    contents = set()
    for x in g:
        for y in g:
            for a in K.atoms(x, y): contents.add(K.forms[a][1])
    K.solve(sorted(contents))
    play = K.play_fn()
    val = np.array([[int(play(x, y)) for y in g] for x in g], np.int8)
    nchk, bad = K.soundness_check()
    if bad:
        nchk, bad = closure_check(K)
    wit = {}
    for s, x in zip(progs, g):
        wit[s] = [(K.show(a), int(min(K.T.get(K.forms[a][1], BK.INF), 10 ** 6)), K.forms[a][2]) for a in K.atoms(x, x)]
    return val, dict(b=b, four=four, goff=goff, sound_checked=nchk, sound_bad=len(bad), n_contents=len(contents),
                     t=time.time() - t), wit


def _sweep_job(j):
    progs, b, four, goff = j
    val, meta, wit = family4(progs, b, four, goff)
    return b, four, goff, val.tolist(), meta, wit


def cmd_sweep(a):
    import modal as M
    progs, godel, vict = sweep_family()
    idx = {s: i for i, s in enumerate(progs)}
    cfgs = [(None if f == 'K' else f, int(g)) for f, g in (c.split('/') for c in a.configs)]
    jobs = [(progs, b, f, g) for f, g in cfgs for b in range(a.bmin, a.bmax + 1)]
    path = os.path.join(K4DIR, 'sweep.json')
    out = json.load(open(path)) if os.path.exists(path) else dict(progs=progs, godel=godel, victims=vict, cells={})
    jobs = [j for j in jobs if '%s/%d/%d' % (j[2], j[3], j[1]) not in out['cells']]
    jobs.sort(key=lambda j: -j[1])
    with Pool(a.workers) as pool:
        for b, f, g, val, meta, wit in pool.imap_unordered(_sweep_job, jobs):
            v = np.array(val); U, _ = M.pd_payoffs(v, M.PD)
            selfc = {s: int(v[idx[s], idx[s]]) for s in NAMED}
            rearmed = {z: [x for x in vict[z] if x in idx and U[idx[z], idx[x]] > U[idx[x], idx[x]] + 1e-12] for z in godel}
            out['cells']['%s/%d/%d' % (f, g, b)] = dict(meta=meta, self=selfc, rearmed={z: xs for z, xs in rearmed.items() if xs},
                                                         witness={s: wit[s] for s in NAMED}, val=val)
            json.dump(out, open(path, 'w'))
            print('%s/g%d b=%d sound %d/%d self %s rearmed %d %.0fs' % (f, g, b, meta['sound_bad'], meta['sound_checked'],
                  ''.join(str(selfc[s]) for s in NAMED), sum(1 for xs in rearmed.values() if xs), meta['t']), flush=True)


# ====================================================================== Part B: evaluation of the frozen classifier
def eligible(n, residents, vf, labels):
    """Eligible pairs (z, x): x a supported self-cooperator, z strictly invades x in the free arm.  labels: dict
    name -> play table; returns list of dict(z, x, <label>: disarmed?)."""
    import modal as M
    Uf, _ = M.pd_payoffs(vf, M.PD)
    Us = {k: M.pd_payoffs(v, M.PD)[0] for k, v in labels.items()}
    out = []
    for x in residents:
        for z in range(vf.shape[0]):
            if Uf[z, x] > Uf[x, x] + 1e-12:
                r = dict(z=int(z), x=int(x))
                for k, U in Us.items():
                    r[k] = bool(not (U[z, x] > U[x, x] + 1e-12))
                out.append(r)
    return out


def confusion(flags, labels):
    tp = sum(1 for f, l in zip(flags, labels) if f and l); fp = sum(1 for f, l in zip(flags, labels) if f and not l)
    fn = sum(1 for f, l in zip(flags, labels) if not f and l); tn = sum(1 for f, l in zip(flags, labels) if not f and not l)
    return dict(tp=tp, fp=fp, fn=fn, tn=tn, precision=tp / (tp + fp) if tp + fp else None,
                recall=tp / (tp + fn) if tp + fn else None, n=len(flags))


def _classify_job(j):
    z, x = j
    t = time.time()
    r = Classifier().classify(z, x)
    r['t'] = time.time() - t
    return z, x, r


def cmd_classify(a):
    """C_spec and C_pair on the eligible catalogue against the given labels (pair and class level)."""
    import k_at_n8 as KN
    n = a.n
    L, vf, hc, hd = KN.tables(n)
    vf = vf.astype(np.int8)
    idx = {s: i for i, s in enumerate(L.rep)}
    if n == 8:
        res = [idx[s] for s in json.load(open(os.path.join(RUNS, 'k-at-n8-fakers.json')))['supported_selfcoop']]
    else:
        res = [idx[s] for s in json.load(open(os.path.join(K4DIR, 'n6_residents.json')))['residents']]
    labels = {}
    for lab in a.labels:
        four, b = lab.split('@'); b = int(b)
        labels[lab] = load4(n, b, None if four == 'K' else ('lit' if four == 'K4' else 'mono'))
    el = eligible(n, res, vf, labels)
    path = os.path.join(K4DIR, 'classify_n%d.json' % n)
    old = json.load(open(path)) if os.path.exists(path) else {}
    cache = {(r['z'], r['x']): r['clf'] for r in old.get('pairs', [])}
    todo = [(L.rep[r['z']], L.rep[r['x']]) for r in el if (r['z'], r['x']) not in cache]
    with Pool(a.workers) as pool:
        for z, x, r in pool.imap_unordered(_classify_job, todo, chunksize=2):
            cache[(idx[z], idx[x])] = r
    for r in el:
        r['clf'] = cache[(r['z'], r['x'])]
        r['zname'] = L.rep[r['z']]; r['xname'] = L.rep[r['x']]
    out = dict(n=n, residents=[L.rep[x] for x in res], n_pairs=len(el), labels=a.labels, pairs=el, confusion={})
    for lab in a.labels:
        for which in ('flag_spec', 'flag_pair'):
            f = [r['clf'][which] for r in el]; l = [r[lab] for r in el]
            out['confusion']['%s|%s|pair' % (lab, which)] = confusion(f, l)
            zs = sorted({r['z'] for r in el})
            fz = [any(r['clf'][which] for r in el if r['z'] == z) for z in zs]
            lz = [any(r[lab] for r in el if r['z'] == z) for z in zs]
            out['confusion']['%s|%s|class' % (lab, which)] = confusion(fz, lz)
        for part in ('flagG', 'flagC'):
            f = [r['clf']['spec'][part] for r in el]; l = [r[lab] for r in el]
            out['confusion']['%s|spec.%s|pair' % (lab, part)] = confusion(f, l)
    out['uncertified'] = sum(1 for r in el if not r['clf']['spec'].get('certified', True))
    out['no_root'] = sum(1 for r in el if r['clf']['spec'].get('level') is None)
    json.dump(out, open(path, 'w'), indent=1, default=str)
    for k, v in out['confusion'].items():
        print(k, v)
    print('uncertified', out['uncertified'], 'no root', out['no_root'])


# ====================================================================== Part B: misclassified pairs
class RestrictedSearch(G.MinSearch):
    """Exact minimal GLS+Def derivations in which no GLR premise keeps a triggering hypothesis: every GLR premise drops
    (weakens away) its G-trigger boxes []B (and their contents B) and its Con-under-box formulas; a GLR whose goal or
    diagonal triggers is not allowed.  Since an unused hypothesis can always be weakened away, this finds a derivation
    with no *used* trigger iff one exists (within the size bound)."""

    def __init__(self, th, oracle, clf, cap=2_000_000):
        super().__init__(th, oracle, cap=cap)
        self.clf = clf
        self._trig = {}
        self.progname = {}

    def trig(self, a):
        r = self._trig.get(a)
        if r is None:
            th = self.th; F = th.forms
            r = con_under_box(th, a)
            if not r and F[a][0] == FBOX:
                B = F[a][1]; pol = 1; Bp = B
                if F[Bp][0] == FNOT: pol = 0; Bp = F[Bp][1]
                cands = [Bp] if F[Bp][0] == FP else [P_ for P_, D_ in th.defn.items() if D_ == Bp]
                for P_ in cands:
                    t = F[P_]
                    if t[0] == FP and t[1] == t[2]:
                        u = psrc(th.progs[t[1]])
                        if self.clf.free_play(u, u) == pol and not self.oracle.prov((frozenset(), frozenset([B]))):
                            r = True; break
            self._trig[a] = r
        return r

    def rules(self, S):
        out = []
        F = self.th.forms
        for prem, glr, lab in G.expand_nf(self.th, S):
            if lab == 'GLR':
                (pL, pR), = prem
                goal = next(iter(pR)); diag = next(a for a in pL if F[a][0] == FBOX and F[a][1] == goal and a in S[1])
                if self.trig(diag) or con_under_box(self.th, goal):
                    continue
                drop = {a for a in pL if a != diag and self.trig(a)}
                drop |= {F[a][1] for a in drop if F[a][0] == FBOX}
                prem = ((pL - drop, pR),)
            out.append((prem, glr, lab))
        return out

    def solve(self, S, bound):
        e = self.exact.get(S)
        if e is not None:
            return e if e[0] <= bound else None
        if self.lb.get(S, 1) > bound:
            return None
        th = self.th
        if G.is_axiom(th, *S):
            e = (1, 0, 'Ax', ()); self.exact[S] = e
            return e if bound >= 1 else None
        if not self.oracle.prov(S):
            self.lb[S] = self.INF
            return None
        self.count += 1
        if self.count > self.cap:
            raise G.Abort()
        best = None; newlb = self.INF
        for prem, glr, lab in self.rules(S):
            prem = tuple((frozenset(p[0]), frozenset(p[1])) for p in prem)
            if not all(self.oracle.prov(p) for p in prem):
                continue
            w = 0 if lab == 'Del' else 1
            lbs = [self._lbv(p) for p in prem]
            capb = bound if best is None else best[0]
            rl = w + sum(lbs)
            if rl > capb:
                newlb = min(newlb, rl); continue
            tot = w; tl = glr; ok = True
            for i, p in enumerate(prem):
                rest = sum(lbs[i + 1:])
                r = self.solve(p, capb - tot - rest)
                if r is None:
                    ok = False
                    newlb = min(newlb, tot + self._lbv(p) + rest)
                    break
                tot += r[0]; tl += r[1]
            if ok and (best is None or (tot, tl) < best[:2]):
                best = (tot, tl, lab, prem)
        if best is not None:
            self.exact[S] = best
            return best
        self.lb[S] = max(self.lb.get(S, 1), newlb)
        return None


def alt_untriggered(z, x, cap=2_000_000):
    """For z's free-arm play against x: (minimal size, minimal untriggered size within twice it, certified)."""
    C = Classifier()
    th = G.Theory(); zi = th.prog(z); xi = th.prog(x); orc = G.Oracle(th)
    play = C.free_play(z, x)
    k, S = C.root(th, orc, zi, xi, play)
    if S is None:
        return None
    ms = G.MinSearch(th, orc, cap=cap); r0 = ms.minimize(S)
    rs = RestrictedSearch(th, orc, C, cap=cap)
    try:
        r1 = rs.minimize(S, max_size=2 * r0['c'][0])
    except Exception as e:
        r1 = dict(error=str(e))
    if r1 is not None and r1.get('certified') is False:
        r1 = dict(c=None, certified=False, lb=r1.get('lb'))     # the greedy fallback is unrestricted: not a witness
    return dict(level=k, min=r0['c'], min_certified=r0['certified'], untriggered=r1)


def erase(K, f, th, memo=None):
    """A K formula with budgets erased, as a GLS+Def formula in th."""
    if memo is None: memo = {}
    if f in memo: return memo[f]
    t = K.forms[f]; k = t[0]
    if k == FP:
        r = th.P(th.prog(psrc(K.trees[K.genos[t[1]][0]])), th.prog(psrc(K.trees[K.genos[t[2]][0]])))
    elif k == FBOT: r = th.BOT
    elif k == FTOP: r = th.TOP
    elif k == FNOT: r = th.neg(erase(K, t[1], th, memo))
    elif k == FBOX: r = th.box(erase(K, t[1], th, memo))
    else: r = th.f((k, erase(K, t[1], th, memo), erase(K, t[2], th, memo)))
    memo[f] = r
    return r


def lost_atoms(z, x, b=16, four=None, bmax_extra=10, W=60):
    """GL-true atoms of the three plays deciding the invasion (z vs x, x vs z, x vs x) that are K-false at budget b;
    for each, its GL length L and the first global budget b' in (b, 2L + bmax_extra] at which it is K-true, if any
    (finite-budget) or None (structural)."""
    import k_at_n8 as KN
    def build(bb):
        K = KTheoryG(cap=bb, filter_first=True, four=four)
        K.prune = KN.make_prune_trace(K, W)
        gz, gx = K.geno(z, bb), K.geno(x, bb)
        plays = [(gz, gx), (gx, gz), (gx, gx)]
        cont = [[K.forms[a][1] for a in K.atoms(p, q)] for p, q in plays]
        K.solve(sorted({c for cs in cont for c in cs}))
        return K, cont
    K, cont = build(b)
    th = G.Theory(); orc = G.Oracle(th)
    out = []
    for pi, cs in enumerate(cont):
        for ai, A in enumerate(cs):
            if K.T.get(A, BK.INF) <= b: continue
            gA = erase(K, A, th)
            if not orc.prov((frozenset(), frozenset([gA]))): continue
            r = G.MinSearch(th, orc).minimize((frozenset(), frozenset([gA])))
            out.append(dict(play=('zx', 'xz', 'xx')[pi], atom=ai, content=K.show(A), L=r['c'][0], L_certified=r['certified']))
    for o in out:
        hi = 2 * o['L'] + bmax_extra
        o['finite_budget_at'] = None
        for bb in range(b + 1, hi + 1):
            K2, cont2 = build(bb)
            A = cont2[('zx', 'xz', 'xx').index(o['play'])][o['atom']]
            if K2.T.get(A, BK.INF) <= bb:
                o['finite_budget_at'] = bb; break
        o['searched_to'] = hi
    return out


def _mis_job(j):
    z, x, kind, label_four = j
    t = time.time()
    r = dict(z=z, x=x, kind=kind)
    r['alt'] = alt_untriggered(z, x)
    r['lost'] = lost_atoms(z, x, four=label_four)
    r['t'] = time.time() - t
    return r


def cmd_misclass(a):
    path = os.path.join(K4DIR, 'classify_n%d.json' % a.n)
    clf = json.load(open(path))
    four = None if a.label.startswith('K@') else 'mono'
    jobs = []
    for r in clf['pairs']:
        f = r['clf']['flag_spec']; l = r[a.label]
        if f != l:
            jobs.append((r['zname'], r['xname'], 'FP' if f else 'FN', four))
    if a.also_tp:
        jobs += [(r['zname'], r['xname'], 'TP', four) for r in clf['pairs'] if r['clf']['flag_spec'] and r[a.label]]
    outp = os.path.join(K4DIR, 'misclass_n%d_%s.json' % (a.n, a.label.replace('@', '')))
    rows = json.load(open(outp)) if os.path.exists(outp) else []
    done = {(r['z'], r['x']) for r in rows}
    jobs = [j for j in jobs if (j[0], j[1]) not in done]
    with Pool(a.workers) as pool:
        for r in pool.imap_unordered(_mis_job, jobs):
            rows.append(r); json.dump(rows, open(outp, 'w'), indent=1, default=str)
            alt = r['alt'] and r['alt']['untriggered']
            print(r['kind'], r['z'], 'vs', r['x'], 'alt', alt and alt.get('c'), 'lost', [(o['play'], o['L'], o['finite_budget_at']) for o in r['lost']], '%.0fs' % r['t'], flush=True)


# ====================================================================== static analysis, catalogue, chain, Part C
def cmd_ktables(a):
    four = None if a.four == 'K' else a.four
    jobs = [(a.n, b, four, a.goff) for b in a.budgets]
    jobs.sort(key=lambda j: -j[1])
    with Pool(a.workers) as pool:
        for m in pool.imap_unordered(_ktable4_job, jobs):
            print({k: v for k, v in m.items()}, flush=True)


def partition(val):
    """Canonical classes grouped by identical row and column (behavioural classes of an arm)."""
    key = {}
    for i in range(val.shape[0]):
        key.setdefault((val[i].tobytes(), val[:, i].tobytes()), []).append(i)
    return sorted(key.values())


def split_merge(va, vb, mu, names):
    """Groups of canonical classes that are one behavioural class in arm a but several in arm b (splits a -> b) and
    vice versa (merges), with aggregate source-level mass."""
    pa = partition(va); pb = partition(vb)
    ca = {i: k for k, g in enumerate(pa) for i in g}; cb = {i: k for k, g in enumerate(pb) for i in g}
    splits = []
    for g in pa:
        parts = sorted({cb[i] for i in g})
        if len(parts) > 1:
            splits.append(dict(members=[names[i] for i in g][:6], n=len(g), mu=float(mu[g].sum()), into=len(parts)))
    merges = []
    for g in pb:
        parts = sorted({ca[i] for i in g})
        if len(parts) > 1:
            merges.append(dict(members=[names[i] for i in g][:6], n=len(g), mu=float(mu[g].sum()), from_=len(parts)))
    return dict(n_classes_a=len(pa), n_classes_b=len(pb), splits=splits, merges=merges)


def cmd_static(a):
    """Per K+4m table: plays vs K and vs free, soundness, self-cooperators, leak test, named self-play, splits and
    merges against K, restored cooperators and restored exploiters."""
    import k_at_n8 as KN
    import modal as M
    n = a.n
    L, vf, hc, hd = KN.tables(n)
    vf = vf.astype(np.int8)
    idx = {s: i for i, s in enumerate(L.rep)}
    mu = L.mu_canon / L.mu_canon.sum()
    res = [idx[s] for s in json.load(open(os.path.join(RUNS, 'k-at-n8-fakers.json')))['supported_selfcoop']] if n == 8 else []
    out = {}
    for b in a.budgets:
        vk = load4(n, b, None)
        row = {}
        for four in ('lit', 'mono'):
            p = kpath(n, b, four, a.goff)
            if not os.path.exists(p): continue
            v = np.load(p); m = json.load(open(p.replace('.npy', '.json')))
            if a.goff:
                vk_ = load4(n, b, None, a.goff) if os.path.exists(kpath(n, b, None, a.goff)) else None
            else:
                vk_ = vk
            r = dict(meta=m, diff_vs_K=int((v != vk_).sum()) if vk_ is not None else None, diff_vs_free=int((v != vf).sum()),
                     selfcoop=int(sum(v[i, i] for i in range(len(v)))), leak=KN.leak_test(v)['n_closed'])
            if vk_ is not None:
                ch = np.argwhere(v != vk_)
                r['changed_pairs'] = [(L.rep[i], L.rep[j], int(vk_[i, j]), int(v[i, j])) for i, j in ch[:40]]
                r['changed_mu'] = float(sum(mu[i] * mu[j] for i, j in ch))
                r['restored_coop'] = [L.rep[i] for i in range(len(v)) if v[i, i] == 1 and vk_[i, i] == 0]
                Uk, _ = M.pd_payoffs(vk_, M.PD); U4, _ = M.pd_payoffs(v, M.PD)
                rex = {}
                for x in res:
                    if v[x, x] != 1: continue
                    for z in range(len(v)):
                        if U4[z, x] > U4[x, x] + 1e-12 and not (Uk[z, x] > Uk[x, x] + 1e-12):
                            rex.setdefault(L.rep[z], []).append(L.rep[x])
                r['restored_exploiters'] = rex
                r['split_merge_vs_K'] = split_merge(vk_, v, mu, L.rep)
            if n == 8:
                named = [s for s in NAMED if s in idx]
                r['named_self'] = {s: int(v[idx[s], idx[s]]) for s in named}
            row[four] = r
        out[str(b)] = row
        print(b, {f: {k: r[k] for k in ('diff_vs_K', 'diff_vs_free', 'selfcoop', 'leak')} for f, r in row.items()}, flush=True)
    json.dump(out, open(os.path.join(K4DIR, 'static_n%d_g%d.json' % (n, a.goff)), 'w'), indent=1, default=str)


def _cross4(j):
    bx, by, four = j
    import k_at_n8 as KN
    L, vf, hc, hd = KN.tables(8)
    t = time.time()
    K = KTheoryG(cap=max(bx, by), filter_first=True, four=four)
    K.prune = KN.make_prune(K, L, hc, hd)
    gx = [K.geno(s, bx) for s in L.rep]; gy = [K.geno(s, by) for s in L.rep]
    contents = set()
    for x in gx:
        for y in gy:
            for a in K.atoms(x, y) + K.atoms(y, x): contents.add(K.forms[a][1])
    K.solve(sorted(contents))
    play = K.play_fn()
    vxy = np.array([[int(play(x, y)) for y in gy] for x in gx], np.int8)
    vyx = np.array([[int(play(y, x)) for x in gx] for y in gy], np.int8)
    nchk, bad = K.soundness_check()
    if bad: nchk, bad = closure_check(K)
    tag = 'K4m' if four == 'mono' else 'K'
    np.save(os.path.join(K4DIR, '%s_cross_n8_%d_%d.npy' % (tag, bx, by)), vxy); np.save(os.path.join(K4DIR, '%s_cross_n8_%d_%d.npy' % (tag, by, bx)), vyx)
    return bx, by, nchk, len(bad), time.time() - t


def cmd_catalogue(a):
    """Leak test on the n = 8 cross-budget catalogue over the budgets under K+4m; plays changed against K's
    published cross-budget blocks."""
    import k_at_n8 as KN
    B = a.budgets
    L, vf, hc, hd = KN.tables(8)
    jobs = [(B[i], B[k], 'mono') for i in range(len(B)) for k in range(i + 1, len(B))]
    with Pool(a.workers) as pool:
        for bx, by, nchk, nbad, dt in pool.imap_unordered(_cross4, jobs):
            print('(%d, %d) sound bad %d / %d, %.0fs' % (bx, by, nbad, nchk, dt), flush=True)
    nat = L.arrays()[0]
    const = [c for c in range(len(nat)) if nat[c] == 0]; nonc = [c for c in range(len(nat)) if nat[c] > 0]
    geno = [(c, 0) for c in const] + [(c, b) for b in B for c in nonc]
    G_ = len(geno); val = np.zeros((G_, G_), np.int8)
    blocks = {}; diffK = {}
    for bx in B:
        for by in B:
            if bx == by:
                blocks[(bx, by)] = load4(8, bx, 'mono')
            else:
                blocks[(bx, by)] = np.load(os.path.join(K4DIR, 'K4m_cross_n8_%d_%d.npy' % (bx, by)))
                kp = os.path.join(KDIR8, 'kcross_n8_%d_%d.npy' % (bx, by))
                if os.path.exists(kp):
                    ref = np.load(kp); ch = np.argwhere(ref != blocks[(bx, by)])
                    diffK['%d_%d' % (bx, by)] = dict(n=int(len(ch)), examples=[(L.rep[i], L.rep[j], int(ref[i, j]), int(blocks[(bx, by)][i, j])) for i, j in ch[:20]])
    for i, (ci, bi) in enumerate(geno):
        for j, (cj, bj) in enumerate(geno):
            val[i, j] = blocks[(bi or B[0], bj or B[0])][ci, cj]
    lt = KN.leak_test(val)
    out = dict(budgets=B, n_genotypes=G_, n_selfcoop=lt['n_selfcoop'], n_components=lt['n_components'], n_closed=lt['n_closed'],
               sizes=lt['sizes'], diff_vs_K_cross=diffK)
    json.dump(out, open(os.path.join(K4DIR, 'catalogue8.json'), 'w'), indent=1)
    print(out)


def chain_rows(jobs, path, workers):
    import k_at_n8 as KN
    rows = json.load(open(path)) if os.path.exists(path) else []
    done = {(r['label'], r['N']) for r in rows}
    jobs = [j for j in jobs if (j[0], j[3]) not in done]
    jobs.sort(key=lambda j: -j[3])
    with Pool(workers) as pool:
        for r in pool.imap_unordered(KN.chain_cell, jobs):
            rows.append(r)
            json.dump(rows, open(path, 'w'), indent=1, default=str)
            print('%-40s N=%-6d P(C,C) %.4f pi(D) %.3f top %s %.3f exit %.2e (strict %.2e) n_terminal %d indet %d cut %.1e (%.0fs)' % (
                r['label'], r['N'], r['pcc'], r['pi_D'], r.get('top_coop'), r.get('pi_top', 0), r.get('top_exit', 0), r.get('top_exit_strict', 0),
                r['n_terminal'], r['indeterminate'], r['cut_flow'], r['t']), flush=True)
    return rows


def cmd_chain(a):
    jobs = []
    for b in a.budgets:
        v = load4(8, b, 'mono', a.goff)
        for N in a.Ns:
            jobs.append(('K4m b=%d g=%d' % (b, a.goff), 8, v, N, None))
        if a.goff:
            vk = load4(8, b, None, a.goff)
            for N in a.Ns:
                jobs.append(('K b=%d g=%d' % (b, a.goff), 8, vk, N, None))
    chain_rows(jobs, os.path.join(K4DIR, 'chain.json'), a.workers)


def cmd_n6res(a):
    """n = 6 held-out residents: self-cooperators with pi >= 1e-3 in the n = 6 free or K b = 16 chain at N = 10^4."""
    import k_at_n8 as KN
    L, vf, hc, hd = KN.tables(6)
    if not os.path.exists(kpath(6, 16, None)):
        _ktable4_job((6, 16, None, 0))
    vk = load4(6, 16, None)
    rows = chain_rows([('n6 free', 6, vf.astype(np.int8), 10000, None), ('n6 K b=16', 6, vk, 10000, None)],
                      os.path.join(K4DIR, 'chain_n6.json'), 2)
    idx = {s: i for i, s in enumerate(L.rep)}
    sup = set()
    for r in rows:
        for nm, p in r['pi_mono'].items():
            if p >= 1e-3:
                for c in r['canon_members'].get(nm, [idx[nm]]): sup.add(L.rep[c])
    res = sorted(s for s in sup if vf[idx[s], idx[s]] == 1 and s != 'C')
    json.dump(dict(residents=res), open(os.path.join(K4DIR, 'n6_residents.json'), 'w'), indent=1)
    print(res)


def cmd_partc(a):
    """Matched table interventions at n = 8, N = 10^4 (b = 16)."""
    import k_at_n8 as KN
    L, vf, hc, hd = KN.tables(8)
    vf = vf.astype(np.int8)
    idx = {s: i for i, s in enumerate(L.rep)}
    clf = json.load(open(os.path.join(K4DIR, 'classify_n8.json')))
    flagged = sorted({r['z'] for r in clf['pairs'] if r['clf']['flag_spec']})
    keep = [i for i in range(len(L.rep)) if i not in set(flagged)]
    st = json.load(open(os.path.join(K4DIR, 'static_n8_g0.json')))[str(a.b)]['mono']
    vk = load4(8, a.b, None); v4 = load4(8, a.b, 'mono')
    rc = [idx[s] for s in st['restored_coop']]; rx = [idx[s] for s in st['restored_exploiters']]
    def graft(rows_):
        v = vk.copy()
        for i in rows_:
            v[i, :] = v4[i, :]; v[:, i] = v4[:, i]
        return v
    jobs = [('C(i) free minus C_spec-flagged', 8, vf, a.N, keep),
            ('C(ii) K + restored cooperators', 8, graft(rc), a.N, None),
            ('C(iii) K + restored exploiters', 8, graft(rx), a.N, None)]
    rows = chain_rows(jobs, os.path.join(K4DIR, 'partc.json'), a.workers)
    meta = dict(flagged=[L.rep[i] for i in flagged], mu_flagged=float(L.mu_canon[flagged].sum() / L.mu_canon.sum()),
                restored_coop=st['restored_coop'], restored_exploiters=list(st['restored_exploiters']))
    json.dump(meta, open(os.path.join(K4DIR, 'partc_meta.json'), 'w'), indent=1)
    print(meta)


def cmd_lottery(a):
    import k_at_n8 as KN
    jobs = [('K4m b=%d' % a.b, 8, load4(8, a.b, 'mono'), a.N, a.I, rep) for rep in range(a.reps)]
    path = os.path.join(K4DIR, 'lottery.json')
    rows = json.load(open(path)) if os.path.exists(path) else []
    with Pool(a.workers) as pool:
        for r in pool.imap_unordered(KN.lottery_job, jobs):
            rows.append(r); json.dump(rows, open(path, 'w'), indent=1, default=str)
            print(r['label'], r['rep'], r['outcome'], r['status'], r['stop_gen'], flush=True)


# ====================================================================== report
def _jl(p):
    p = os.path.join(K4DIR, p) if not os.path.isabs(p) else p
    return json.load(open(p)) if os.path.exists(p) else None


def _fmt(x, f='%.4f'):
    return '—' if x is None else (f % x)


def cmd_report(a):
    import k_at_n8 as KN
    L8 = KN.tables(8)[0]
    md = []; J = {}
    w = md.append
    w('# K with the 4-rule, and a frozen classifier for what a sound bounded prover loses\n')
    w('Spec `specs/2026-10-05-k-four.md`; predictions `predictions/2026-10-05-k-four.md`; notes `notes/k-four.md` (§1: encoding, '
      'cost recurrence, soundness proof; Lemmas V, V′, G). Code: the `four` option of `src/bounded_k.py`, everything else '
      '`src/k_four.py`. Raw rows in `runs/k-four/`. ε → 0 chain numbers are at the stated N; the lottery is ε = 0 at '
      '(N, I) = (100, 64). K+4 = the spec\'s literal rule; K+4m = its monotone closure (cases i–iv); X-arm = guard read one '
      'budget up (exploratory, not in the spec).\n')
    rep = _jl('repro.json')
    if rep:
        J['repro'] = rep
        w('## 0. Reproduction with the option off\n')
        w('| n | b | identical to the published K table | soundness violations |\n|---|---|---|---|')
        for r in rep:
            w('| %d | %d | %s | %s |' % (r['n'], r['b'], r.get('identical_to_published', r.get('identical')), r['sound_bad']))
        w('')
    # tables
    for n in (6, 8):
        st = _jl('static_n%d_g0.json' % n)
        if not st: continue
        J['static_n%d' % n] = st
        w('## 1.%s K+4 tables at n = %d\n' % ('a' if n == 6 else 'b', n))
        w('| b | rule | time (s) | soundness: violations / checked | plays ≠ free | plays ≠ K | μ²-weight of changed plays | self-cooperators | restored cooperators | restored exploiters | drift-closed components |')
        w('|---|---|---|---|---|---|---|---|---|---|---|')
        for b in sorted(st, key=int):
            for four, r in st[b].items():
                m = r['meta']
                w('| %s | %s | %.0f | %d / %d | %d | %s | %s | %d | %d | %d | %d |' % (
                    b, 'K+4' if four == 'lit' else 'K+4m', m['t'], m['sound_bad'], m['sound_checked'], r['diff_vs_free'],
                    r['diff_vs_K'], _fmt(r.get('changed_mu'), '%.2e'), r['selfcoop'], len(r.get('restored_coop', [])),
                    len(r.get('restored_exploiters', {})), r['leak']))
        w('')
        for b in sorted(st, key=int):
            for four, r in st[b].items():
                if r.get('changed_pairs'):
                    w('- b = %s, %s: changed plays vs K (reader, opponent, K, new): %s' % (b, four, '; '.join('`%s` vs `%s` %d→%d' % t for t in r['changed_pairs'][:12])))
                sm = r.get('split_merge_vs_K')
                if sm and (sm['splits'] or sm['merges']):
                    w('  - classes K %d → %d; splits: %s; merges: %s' % (sm['n_classes_a'], sm['n_classes_b'],
                      '; '.join('%s (n %d, μ %.2e, into %d)' % (s['members'][0], s['n'], s['mu'], s['into']) for s in sm['splits'][:6]) or 'none',
                      '; '.join('%s (n %d, μ %.2e, from %d)' % (s['members'][0], s['n'], s['mu'], s['from_']) for s in sm['merges'][:6]) or 'none'))
                if r.get('restored_exploiters'):
                    w('  - restored exploiters: %s' % '; '.join('`%s` → %s' % (z, ', '.join('`%s`' % x for x in xs[:3])) for z, xs in list(r['restored_exploiters'].items())[:10]))
                if r.get('restored_coop'):
                    w('  - restored cooperators: %s' % ', '.join('`%s`' % s for s in r['restored_coop'][:12]))
        w('')
        if n == 8:
            named = None
            rows = []
            for b in sorted(st, key=int):
                r = st[b].get('mono')
                if r and r.get('named_self'):
                    named = list(r['named_self']); rows.append((b, r['named_self']))
            if named:
                w('Named self-play in K+4m at n = 8 (1 = C): ' + '; '.join('b = %s: %s' % (b, ''.join(str(d[s]) for s in named)) for b, d in rows))
                w('(order: %s)\n' % ', '.join('`%s`' % s for s in named))
    for g in (1,):
        st = _jl('static_n8_g%d.json' % g)
        if st:
            J['static_n8_g%d' % g] = st
    sw = _jl('sweep.json')
    if sw:
        J['sweep'] = {k: dict(meta=v['meta'], self=v['self'], rearmed=v['rearmed'], witness=v['witness']) for k, v in sw['cells'].items()}
        w('## 2. Dense sweeps on the named family (b = 4…40)\n')
        w('Family: %d programs (the five Con/4-axiom cooperators, PrudentBot, FairBot, `BOX1(THEM(ME))`, `BOX(THEM(THEM))`, '
          '`BOX1(THEM(THEM))`, C, D, the 21 Gödel-sentence fakers and their free-arm victims). b\\* = first b at which the program '
          'self-cooperates; witness = the exact minimal sizes T of its self-play atom contents at b\\* (each witnessed by a derivation; '
          'at b\\* − 1 at least one exceeds the budget).\n' % len(sw['progs']))
        cfgs = sorted({k.rsplit('/', 1)[0] for k in sw['cells']})
        w('| program | ' + ' | '.join('b\\* %s' % c.replace('None', 'K').replace('mono', 'K+4m').replace('/0', '').replace('/1', ', guard +1') for c in cfgs) + ' |')
        w('|---|' + '---|' * len(cfgs))
        bstar = {}
        for s in NAMED:
            cells = []
            for c in cfgs:
                bs = sorted(int(k.rsplit('/', 1)[1]) for k in sw['cells'] if k.startswith(c + '/'))
                hit = next((b for b in bs if sw['cells']['%s/%d' % (c, b)]['self'][s]), None)
                bstar[(s, c)] = hit
                if hit is None:
                    cells.append('never (≤ %d)' % max(bs))
                else:
                    wit = sw['cells']['%s/%d' % (c, hit)]['witness'][s]
                    cells.append('%d [T = %s]' % (hit, ', '.join(str(t[1]) if t[1] < 10 ** 6 else '∞' for t in wit)))
            w('| `%s` | %s |' % (s, ' | '.join(cells)))
        w('')
        w('Gödel sentences re-armed (strictly invading a free-arm victim in the family table), max over b: ' + '; '.join(
            '%s: %d' % (c.replace('None', 'K').replace('mono', 'K+4m'), max(len(sw['cells'][k]['rearmed']) for k in sw['cells'] if k.startswith(c + '/'))) for c in cfgs))
        viol = sum(v['meta']['sound_bad'] for v in sw['cells'].values()); chk = sum(v['meta']['sound_checked'] for v in sw['cells'].values())
        w('\nSoundness over all sweep cells: %d violations / %d checked formulas.\n' % (viol, chk))
        J['bstar'] = {'%s|%s' % k: v for k, v in bstar.items()}
    cat = _jl('catalogue8.json')
    if cat:
        J['catalogue8'] = cat
        w('## 3. Cross-budget catalogue at n = 8 under K+4m (b ∈ %s)\n' % cat['budgets'])
        w('%d genotypes, %d self-cooperators in %d component(s), %d closed. Plays changed against K\'s published cross-budget blocks: %s.\n' % (
            cat['n_genotypes'], cat['n_selfcoop'], cat['n_components'], cat['n_closed'],
            '; '.join('%s: %d (%s)' % (k, v['n'], '; '.join('`%s` vs `%s` %d→%d' % tuple(e) for e in v['examples'][:6])) for k, v in cat['diff_vs_K_cross'].items())))
    ch = _jl('chain.json')
    pub = json.load(open(os.path.join(RUNS, 'k-at-n8-chain.json')))
    if ch:
        rows = [r for r in pub if r['label'] in ('free', 'K b=16', 'K b=54')] + ch
        J['chain'] = ch
        w('## 4. The lim_N chain at n = 8 (PD, w = 0.3)\n')
        w('| arm | P(C,C) N = 10³ | 10⁴ | 3·10⁴ | π(all-D) 3·10⁴ | top state (π) 3·10⁴ | top exit 10³ / 10⁴ / 3·10⁴ | exit slope | strict share | ALLC share | entry N·ρ (10⁴) | classes | terminal / indeterminate / cut |')
        w('|---|---|---|---|---|---|---|---|---|---|---|---|---|')
        labs = list(dict.fromkeys(r['label'] for r in rows))
        for lab in labs:
            rr = {r['N']: r for r in rows if r['label'] == lab}
            Ns = sorted(rr)
            ex = [rr[N].get('top_exit') for N in Ns]
            slope = np.polyfit(np.log(Ns), np.log(ex), 1)[0] if len(Ns) >= 2 and all(ex) else None
            top = rr[Ns[-1]]
            w('| %s | %s | %s | %s | %.3f | `%s` (%.3f) | %s | %s | %.3f | %.2f | %s | %d | %d / %d / %.0e |' % (
                lab, _fmt(rr.get(1000, {}).get('pcc')), _fmt(rr.get(10000, {}).get('pcc')), _fmt(rr.get(30000, {}).get('pcc')),
                top['pi_D'], top.get('top_coop'), top.get('pi_top', 0), ' / '.join(_fmt(e, '%.2e') for e in ex), _fmt(slope, '%.2f'),
                top.get('top_exit_strict', 0) / top['top_exit'] if top.get('top_exit') else 0, top.get('allc_share', float('nan')),
                _fmt((rr.get(10000, {}).get('entry') or {}).get('N_rho'), '%.1f'), top['n_classes'], top['n_terminal'], top['indeterminate'], top['cut_flow']))
        w('')
        for lab in labs:
            rr = [r for r in rows if r['label'] == lab and r['N'] == 30000]
            if rr:
                w('- %s, support at 3·10⁴: %s' % (lab, ', '.join('%s %.3f' % (s, p) for s, p in rr[0]['support'][:8])))
        w('')
        for lab in labs:
            rr = [r for r in rows if r['label'] == lab and r['N'] == 10000]
            if rr and rr[0].get('exits'):
                w('- %s, top `%s` exits at 10⁴: %s' % (lab, rr[0]['top_coop'], '; '.join('`%s` %.1e N·ρ %.2f Δ %g/%g/%g' % (
                    e['mutant'], e['w'], e['N_rho'] or 0, e['d_vs_res'], e['d_res_vs'], e['d_self']) for e in rr[0]['exits'][:3])))
        w('')
    clf = {}
    for n in (8, 6):
        c = _jl('classify_n%d.json' % n)
        if c:
            clf[n] = c
    if clf:
        w('## 5. The frozen classifier\n')
        w('C_spec (primary) and C_pair (secondary) as frozen in commit 6001721; positive = disarmed (invasion gone). Pair level is primary.\n')
        w('| n | label | classifier | level | TP | FP | FN | TN | precision | recall |\n|---|---|---|---|---|---|---|---|---|---|')
        for n, c in clf.items():
            for k, v in c['confusion'].items():
                lab, which, lev = k.split('|')
                w('| %d | %s | %s | %s | %d | %d | %d | %d | %s | %s |' % (n, lab, which, lev, v['tp'], v['fp'], v['fn'], v['tn'], _fmt(v['precision'], '%.2f'), _fmt(v['recall'], '%.2f')))
            w('')
            w('n = %d: %d eligible pairs; %d without a proof of the invader\'s play at level ≤ 2; %d uncertified.\n' % (n, c['n_pairs'], c['no_root'], c['uncertified']))
        J['classify'] = {n: dict(confusion=c['confusion'], n_pairs=c['n_pairs'], no_root=c['no_root']) for n, c in clf.items()}
    ph = _jl('posthoc_n8.json')
    if ph:
        J['posthoc'] = ph
        w('Post-hoc variants (declared after seeing the frozen result; descriptive only): %s\n' % '; '.join('%s: %s' % (k, v) for k, v in ph.items()))
    for lab in ('K16', 'K4m16'):
        mc = _jl('misclass_n8_%s.json' % lab)
        if not mc: continue
        J['misclass_' + lab] = mc
        w('**Misclassified and true-positive pairs, label %s** (FN: disarmed, not flagged; FP: flagged, not disarmed; TP: both). Lost atoms: GL-true atoms of z vs x, x vs z, x vs x that are K-false at b = 16, with GL length L and the first budget ≤ 2L + 10 at which K proves them (structural if none). Alternative: minimal size of a GL derivation of z\'s play with no used trigger, searched to twice the minimum.\n' % lab)
        kinds = {}
        for r in mc:
            kinds.setdefault(r['kind'], []).append(r)
        for kd, rs in kinds.items():
            nfin = sum(1 for r in rs if any(o['finite_budget_at'] for o in r['lost']))
            nstr = sum(1 for r in rs if r['lost'] and not any(o['finite_budget_at'] for o in r['lost']))
            nnone = sum(1 for r in rs if not r['lost'])
            nalt = sum(1 for r in rs if r['alt'] and r['alt']['untriggered'] and r['alt']['untriggered'].get('c'))
            w('- %s: %d pairs; lost atoms structural in %d, some finite-budget in %d, no lost GL-true atom in %d; untriggered alternative within 2× in %d.' % (kd, len(rs), nstr, nfin, nnone, nalt))
        w('')
        for r in mc:
            alt = r['alt'] and r['alt']['untriggered']
            w('  - %s `%s` vs `%s`: min %s, untriggered %s; lost %s' % (r['kind'], r['z'], r['x'], r['alt'] and r['alt']['min'], alt and alt.get('c'),
              ', '.join('%s L=%d %s' % (o['play'], o['L'], ('finite at %d' % o['finite_budget_at']) if o['finite_budget_at'] else 'structural (≤ %d)' % o['searched_to']) for o in r['lost']) or 'none'))
        w('')
    pc = _jl('partc.json'); pm = _jl('partc_meta.json')
    if pc:
        J['partc'] = dict(rows=pc, meta=pm)
        ref = {r['label']: r['pcc'] for r in pub if r['N'] == 10000}
        r4 = [r for r in (ch or []) if r['label'] == 'K4m b=16 g=0' and r['N'] == 10000]
        if r4: ref['K4m b=16'] = r4[0]['pcc']
        w('## 6. Part C: matched table interventions (n = 8, N = 10⁴, b = 16)\n')
        w('| arm | P(C,C) | − free | − K | − K+4m | top state |\n|---|---|---|---|---|---|')
        for lab in ('free', 'K b=16', 'K4m b=16'):
            if lab in ref:
                w('| %s | %.4f | %+.4f | %+.4f | %s |  |' % (lab, ref[lab], ref[lab] - ref['free'], ref[lab] - ref['K b=16'], _fmt(ref[lab] - ref['K4m b=16'], '%+.4f') if 'K4m b=16' in ref else '—'))
        for r in pc:
            w('| %s | %.4f | %+.4f | %+.4f | %s | `%s` |' % (r['label'], r['pcc'], r['pcc'] - ref['free'], r['pcc'] - ref['K b=16'],
              _fmt(r['pcc'] - ref['K4m b=16'], '%+.4f') if 'K4m b=16' in ref else '—', r.get('top_coop')))
        gap = ref['K b=16'] - ref['free']
        ci = [r for r in pc if r['label'].startswith('C(i)')]
        if ci:
            w('\nRecovered share of the K − free gap by (i): %.3f (gap %.4f). Flagged classes deleted: %d (μ %.4f).\n' % ((ci[0]['pcc'] - ref['free']) / gap, gap, len(pm['flagged']), pm['mu_flagged']))
    lot = _jl('lottery.json')
    if lot:
        J['lottery'] = lot
        res = [r for r in lot if r['outcome'] not in (None, 'unresolved')]
        k = sum(1 for r in res if r['outcome'] == 'efficient')
        w('## 7. Lottery\n\nK+4m b = 16, (100, 64), mN = 1, 20 paired seeds: efficient %d/%d (unresolved %d).\n' % (k, len(res), len(lot) - len(res)))
    open(os.path.join(RUNS, 'k-four.md'), 'w').write('\n'.join(md) + '\n')
    json.dump(J, open(os.path.join(RUNS, 'k-four.json'), 'w'), indent=1, default=str)
    print('\n'.join(md))


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest='cmd')
    p = sp.add_parser('repro'); p.add_argument('--budgets', type=int, nargs='+', default=[4, 8, 16]); p.add_argument('--workers', type=int, default=3)
    p = sp.add_parser('classify'); p.add_argument('--n', type=int, default=8); p.add_argument('--labels', nargs='+', default=['K@16'])
    p.add_argument('--workers', type=int, default=3)
    p = sp.add_parser('ktables'); p.add_argument('--n', type=int, default=8); p.add_argument('--budgets', type=int, nargs='+', required=True)
    p.add_argument('--four', default='mono'); p.add_argument('--goff', type=int, default=0); p.add_argument('--workers', type=int, default=3)
    p = sp.add_parser('static'); p.add_argument('--n', type=int, default=8); p.add_argument('--budgets', type=int, nargs='+', required=True)
    p.add_argument('--goff', type=int, default=0)
    p = sp.add_parser('catalogue'); p.add_argument('--budgets', type=int, nargs='+', default=[4, 16]); p.add_argument('--workers', type=int, default=1)
    p = sp.add_parser('chain'); p.add_argument('--budgets', type=int, nargs='+', default=[16, 54]); p.add_argument('--Ns', type=int, nargs='+', default=[1000, 10000, 30000])
    p.add_argument('--goff', type=int, default=0); p.add_argument('--workers', type=int, default=3)
    p = sp.add_parser('n6res')
    p = sp.add_parser('report')
    p = sp.add_parser('misclass'); p.add_argument('--n', type=int, default=8); p.add_argument('--label', default='K@16')
    p.add_argument('--also_tp', action='store_true'); p.add_argument('--workers', type=int, default=3)
    p = sp.add_parser('partc'); p.add_argument('--b', type=int, default=16); p.add_argument('--N', type=int, default=10000); p.add_argument('--workers', type=int, default=3)
    p = sp.add_parser('lottery'); p.add_argument('--b', type=int, default=16); p.add_argument('--N', type=int, default=100); p.add_argument('--I', type=int, default=64)
    p.add_argument('--reps', type=int, default=20); p.add_argument('--workers', type=int, default=3)
    p = sp.add_parser('sweep'); p.add_argument('--configs', nargs='+', default=['K/0', 'mono/0']); p.add_argument('--bmin', type=int, default=4)
    p.add_argument('--bmax', type=int, default=40); p.add_argument('--workers', type=int, default=3)
    a = ap.parse_args()
    globals()['cmd_' + a.cmd](a)


if __name__ == '__main__':
    main()
