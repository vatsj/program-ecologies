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


def _make_prune(K, fact, nlev):
    """prune(A) for KTheory: False iff erase(A) is known not GL+Def-provable (None when the formula is not of a
    recognized shape).  Shapes: P_xy (C at level 0), ~P_xy (D at level 0), ~[]^k F -> P_xy (C at level k),
    ~[]^k F -> ~P_xy (D at level k), a definition phi(P_xy) (C at level 0 for P_xy), F (never), T (always).
    fact(gx, gy, kind, lev) -> bool or None (kind 0 = C, 1 = D)."""
    F = K.forms

    def boxbot_k(f):
        k = 0
        while F[f][0] == FBOX:
            k += 1; f = F[f][1]
        return k if F[f][0] == FBOT else None

    def onP(f, kind, lev):
        t = F[f]
        if t[0] != FP: return None
        return fact(t[1], t[2], kind, lev)

    def prune(A):
        t = F[A]; k = t[0]
        if k == FBOT: return False
        if k == FTOP: return True
        if k == FP: return onP(A, 0, 0)
        if k == FNOT and F[t[1]][0] == FP: return onP(t[1], 1, 0)
        if k == FIMP and F[t[1]][0] == FNOT:
            lev = boxbot_k(F[t[1]][1])
            if lev is not None and 1 <= lev < nlev:
                s_ = t[2]
                if F[s_][0] == FP: return onP(s_, 0, lev)
                if F[s_][0] == FNOT and F[F[s_][1]][0] == FP: return onP(F[s_][1], 1, lev)
        Ps = K.inv.get(A)
        if Ps: return onP(Ps[0], 0, 0)
        return None
    return prune


def make_prune(K, L, hc, hd):
    """GL facts from the free arm's box-fact tables (canonical classes of L_n)."""
    canon = {psrc(parse(s)): i for i, s in enumerate(L.rep)}
    tcanon = {}

    def cid(g):
        ti, b = K.genos[g]
        c = tcanon.get(ti)
        if c is None:
            c = tcanon[ti] = canon.get(psrc(K.trees[ti]), -1)
        return c

    def fact(gx, gy, kind, lev):
        a, b = cid(gx), cid(gy)
        if a < 0 or b < 0: return None
        return bool((hd if kind else hc)[lev, a, b])
    return _make_prune(K, fact, hc.shape[0])


def make_prune_trace(K, W=60, nlev=3):
    """GL facts from src/conj4.py's independent trace evaluator (any program, levels < nlev): C at level L iff the
    trace is C at every world >= L (the audit's rule, RESULTS "Proof length")."""
    import conj4 as C4

    def fact(gx, gy, kind, lev):
        tr = C4.trace(K.trees[K.genos[gx][0]], K.trees[K.genos[gy][0]], W)
        want = 0 if kind else 1
        return all(v == want for v in tr[lev:])
    return _make_prune(K, fact, nlev)


def family_table(progs, b, W=60):
    """K plays among a named family (programs outside L_8 allowed) at global budget b, pruned by the trace evaluator;
    with the soundness check."""
    t = time.time()
    K = BK.KTheory(cap=max(b, 1), filter_first=True)
    K.prune = make_prune_trace(K, W)
    g = [K.geno(s, b) for s in progs]
    contents = set()
    for x in g:
        for y in g:
            for a in K.atoms(x, y): contents.add(K.forms[a][1])
    K.solve(sorted(contents))
    play = K.play_fn()
    val = np.array([[int(play(x, y)) for y in g] for x in g], np.int8)
    nchk, bad = K.soundness_check()
    return val, dict(b=b, sound_checked=nchk, sound_bad=len(bad), n_contents=len(contents), t=time.time() - t)


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


# ------------------------------------------------------------------ static analysis of a table
def leak_test(val):
    """proof_length_arm.leak_test, vectorized for n = 8: components of mutual cooperation among self-cooperators;
    closed iff no member cooperates with some class that defects on it."""
    K = val.shape[0]
    S = [x for x in range(K) if val[x, x] == 1]
    Sset = set(S)
    mutual = (val == 1) & (val.T == 1)
    comp = {}; comps = []
    for s0 in S:
        if s0 in comp: continue
        stack = [s0]; mem = []; comp[s0] = len(comps)
        while stack:
            a = stack.pop(); mem.append(a)
            for b in np.nonzero(mutual[a])[0]:
                b = int(b)
                if b in Sset and b not in comp:
                    comp[b] = len(comps); stack.append(b)
        comps.append(mem)
    suck = ((val == 1) & (val.T == 0)).any(1)
    closed = [c for c in comps if not suck[c].any()]
    return dict(n_selfcoop=len(S), n_components=len(comps), closed_components=closed, n_closed=len(closed),
                sizes=sorted((len(c) for c in comps), reverse=True)[:5])


def load_val(n, b):
    if b == 'free':
        return tables(n)[1].astype(np.int8)
    return np.load(os.path.join(KDIR, 'kval_n%d_b%d.npy' % (n, b)))


NAMED = [FB, 'BOX1(THEM(ME))', 'BOX(THEM(THEM))', 'BOX1(THEM(THEM))', 'BOX(THEM(^C))', 'BOX1(THEM(^C))', PB, PSTAR,
         'not(BOX(THEM(ME)))', 'not(BOX(THEM(THEM)))', 'BOX1(THEM(^not(BOX(THEM(ME)))))', 'C', 'D']


def cmd_static(a):
    """Per budget: soundness, GL comparison, named-class plays, leak test; table-change map."""
    L, vf, hc, hd = tables(8)
    idx = {s: i for i, s in enumerate(L.rep)}
    named = [s for s in NAMED if s in idx]
    out = dict(budgets=a.budgets, missing_named=[s for s in NAMED if s not in idx], meta={}, named={}, leak={}, changes={})
    prev = None
    for b in ['free'] + a.budgets:
        v = load_val(8, b)
        if b != 'free':
            out['meta'][str(b)] = json.load(open(os.path.join(KDIR, 'kmeta_n8_b%d.json' % b)))
        lt = leak_test(v)
        out['leak'][str(b)] = dict(n_selfcoop=lt['n_selfcoop'], n_components=lt['n_components'], n_closed=lt['n_closed'], sizes=lt['sizes'],
                                   closed=[[L.rep[i] for i in c][:10] for c in lt['closed_components']][:10])
        out['named'][str(b)] = {x: {y: int(v[idx[x], idx[y]]) for y in named} for x in named}
        if b != 'free' and prev is not None:
            out['changes'][str(b)] = int((v != prev[1]).sum())
        if b != 'free':
            prev = (b, v)
    json.dump(out, open(os.path.join(RUNS, 'k-at-n8-static.json'), 'w'), indent=1)
    for b in ['free'] + a.budgets:
        m = out['meta'].get(str(b), {})
        print(b, 'leak', out['leak'][str(b)]['n_closed'], 'selfcoop', out['leak'][str(b)]['n_selfcoop'], 'diff vs free', m.get('diff_vs_free'),
              'change vs prev', out['changes'].get(str(b)), 'K/GL', m.get('k_true_atoms'), m.get('gl_true_atoms'), 't', m.get('t') and round(m['t']))
        print('   self:', {x: out['named'][str(b)][x][x] for x in named})


# ------------------------------------------------------------------ the lim_N chain
def build_prov(n, val, keep=None):
    import modal as M
    L = tables(n)[0]
    U, PCC = M.pd_payoffs(val, M.PD)
    K = len(L.rep)
    idx = np.arange(K) if keep is None else np.array(sorted(keep))
    prov = M.ModalProvider(U[np.ix_(idx, idx)].astype(float), PCC[np.ix_(idx, idx)], L.mu_canon[idx], [L.rep[i] for i in idx], L.bits_canon[idx])
    prov.sizes = np.array([L.count_canon[idx[m]].sum() for m in prov.members])
    prov.canon = [[int(idx[c]) for c in m] for m in prov.members]
    return prov


def chain_cell(j):
    import modal as M
    from chain import Chain
    from cert_limN import top_exits
    label, n, val, N, keep = j
    t = time.time()
    prov = build_prov(n, val, keep)
    names = prov.names; P = prov.PCC; U = prov.Ufull
    lang = M.ClassLang(prov)
    ch = Chain(prov, N=N, w=0.3, verbose=False, eager_poly=False).explore()
    pcc = 0.0; pis = {}; key_of = {}; poly = 0.0
    for key, wgt in zip(ch.keys_list, ch.pi):
        ids, x, kd = ch.states[key]; ids = list(ids); x = np.asarray(x)
        pcc += wgt * float(x @ P[np.ix_(ids, ids)] @ x)
        if kd == 'mono':
            pis[ids[0]] = pis.get(ids[0], 0.0) + wgt; key_of[ids[0]] = key
        else:
            poly += wgt
    iD = names.index('D'); iC = names.index('C')
    out = dict(label=label, n=n, N=N, n_classes=len(names), pcc=pcc, pi_D=pis.get(iD, 0.0), pi_C=pis.get(iC, 0.0), poly=poly,
               cut_flow=ch.cut_flow, indeterminate=len(ch.indeterminate), n_terminal=len(ch.terminal), n_states=len(ch.trans),
               support=[(ch.describe_state(k, lang), float(p)) for k, p in ch.support(1e-3)][:10],
               pi_mono={names[q]: float(v) for q, v in sorted(pis.items(), key=lambda kv: -kv[1]) if v >= 1e-4})
    coop = [(v, q) for q, v in pis.items() if P[q, q] == 1 and q != iC]
    out['pi_selfcoop'] = float(sum(v for v, q in coop))
    if coop:
        v, qtop = max(coop)
        e = top_exits(ch, prov, key_of[qtop])
        out.update(top_coop=names[qtop], pi_top=v, **e)
        kT, kD = key_of[qtop], key_of.get(iD)
        ent = [(q, r) for (a_, b_, q), r in ch.edge_rho.items() if a_ == kD and b_ == kT]
        if ent:
            q, r = max(ent, key=lambda t_: t_[1][0])
            out['entry'] = dict(mutant=names[q], rho=float(r[0]), N_rho=float(N * r[0]))
        ex = []
        for b_, pr in ch.trans.get(kT, {}).items():
            if b_ == kT: continue
            for q, mw in ch.trans_mut[(kT, b_)].items():
                r = ch.edge_rho.get((kT, b_, q))
                ex.append(dict(mutant=names[q], to=ch.describe_state(b_, lang), w=float(mw), rho=r and float(r[0]), N_rho=r and float(N * r[0]),
                               d_vs_res=float(U[q, qtop] - U[qtop, qtop]), d_res_vs=float(U[qtop, q] - U[qtop, qtop]), d_self=float(U[q, q] - U[qtop, qtop])))
        out['exits'] = sorted(ex, key=lambda e_: -e_['w'])[:6]
    inv = {}
    for v, q in coop:
        if v < 1e-3: continue
        uaa = U[q, q]
        inv[names[q]] = [names[z] for z in range(len(names)) if U[z, q] > uaa + 1e-12]
    out['strict_invaders'] = inv
    out['canon_members'] = {names[q]: prov.canon[q][:20] for q in pis if pis[q] >= 1e-3}
    out['t'] = time.time() - t
    return out


def cmd_chain(a):
    jobs = []
    for b in a.budgets:
        for N in a.Ns:
            jobs.append(('K b=%d' % b, 8, load_val(8, b), N, None))
    if 'free' in a.arms:
        for N in a.Ns:
            jobs.append(('free', 8, load_val(8, 'free'), N, None))
    if 'control' in a.arms:
        keep = json.load(open(os.path.join(RUNS, 'k-at-n8-fakers.json')))['keep']
        for N in a.Ns:
            jobs.append(('faker-removal control', 8, load_val(8, 'free'), N, keep))
    jobs.sort(key=lambda j: -j[3])
    path = os.path.join(RUNS, 'k-at-n8-chain.json')
    rows = json.load(open(path)) if os.path.exists(path) else []
    done = {(r['label'], r['N']) for r in rows}
    jobs = [j for j in jobs if (j[0], j[3]) not in done]
    with Pool(a.workers) as pool:
        for r in pool.imap_unordered(chain_cell, jobs):
            rows.append(r)
            json.dump(rows, open(path, 'w'), indent=1, default=str)
            print('%-24s N=%-6d P(C,C) %.4f pi(D) %.3f top %s %.3f exit %.2e (strict %.2e) n_terminal %d indet %d cut %.1e (%.0fs)' % (
                r['label'], r['N'], r['pcc'], r['pi_D'], r.get('top_coop'), r.get('pi_top', 0), r.get('top_exit', 0), r.get('top_exit_strict', 0),
                r['n_terminal'], r['indeterminate'], r['cut_flow'], r['t']), flush=True)


def cmd_fakers(a):
    """Faker identification (predictions, design choice 5) from the free and K b = ref chains at N = 10^4."""
    L, vf, hc, hd = tables(8)
    rows = json.load(open(os.path.join(RUNS, 'k-at-n8-chain.json')))
    idx = {s: i for i, s in enumerate(L.rep)}
    import modal as M
    Uf, _ = M.pd_payoffs(vf, M.PD)
    vk = load_val(8, a.ref)
    Uk, _ = M.pd_payoffs(vk, M.PD)
    sup = set()
    for r in rows:
        if r['N'] == 10000 and r['label'] in ('free', 'K b=%d' % a.ref):
            for nm, p in r['pi_mono'].items():
                if p >= 1e-3:
                    for c in r['canon_members'].get(nm, [idx[nm]]): sup.add(L.rep[c])
    selfc = [idx[s] for s in sup if vf[idx[s], idx[s]] == 1 and s != 'C']
    fakers = {}
    for x in selfc:
        for z in range(len(L.rep)):
            if Uf[z, x] > Uf[x, x] + 1e-12 and not (Uk[z, x] > Uk[x, x] + 1e-12):
                fakers.setdefault(L.rep[z], []).append(L.rep[x])
    godel = {z: bool(vf[idx[z], idx[z]] == 1 and not hc[0, idx[z], idx[z]]) for z in fakers}
    keep = [i for i in range(len(L.rep)) if L.rep[i] not in fakers]
    out = dict(ref=a.ref, supported_selfcoop=[L.rep[x] for x in selfc], fakers=fakers, godel=godel, keep=keep,
               mu_removed=float(sum(L.mu_canon[idx[z]] for z in fakers) / L.mu_canon.sum()))
    json.dump(out, open(os.path.join(RUNS, 'k-at-n8-fakers.json'), 'w'), indent=1)
    print('supported self-cooperators', out['supported_selfcoop'])
    for z, xs in fakers.items(): print('faker', z, 'Godel' if godel[z] else '', '->', xs)
    print('mu removed', out['mu_removed'])


# ------------------------------------------------------------------ lemma sharing: four cost columns
def _measure_root(th, orc, S, cuts, cap, cut_cap=None):
    """nocut and cut minima with DAG measures.  An aborted cut search reports its certified lower bound and the upper
    bound min(cut-free minimum, oracle derivation) (a cut-free derivation is a cut derivation), flagged uncertified."""
    import gl_proofs as G
    out = {}
    for tag, cs in (('nocut', None), ('cut', cuts)):
        ms = G.MinSearch(th, orc, cap=cap if cs is None else (cut_cap or cap), cuts=cs)
        t = time.time()
        r = ms.minimize(S)
        if r is None:
            return None
        d = dict(size=r['c'][0] if r['c'] else None, loeb=r['c'][1] if r['c'] else None, certified=r['certified'], t=time.time() - t)
        if r['certified']:
            dm = ms.dag_sizes(S); d.update(exact=dm['exact'], subs=dm['subsumption'])
        else:
            d['lb'] = r['lb']
            if tag == 'cut' and out.get('nocut', {}).get('certified'):
                n0 = out['nocut']
                if d['size'] is None or n0['size'] <= d['size']:
                    d.update(size=n0['size'], loeb=n0['loeb'], exact=n0.get('exact'), subs=n0.get('subs'), ub_from='nocut')
                if d['lb'] >= n0['size']:
                    d['certified'] = True
        out[tag] = d
    return out


def measure_pair(xs, ys, cap=2_000_000, atoms=True, cut_cap=300_000):
    """Four measures (tree/no cut, tree/cut, DAG exact, DAG subsumption on each) for the roots C0, C1 of (x, y) and,
    with atoms, for each of x's box atoms against y (L_read sums the true ones)."""
    import gl_proofs as G
    th = G.Theory(); x = th.prog(xs); y = th.prog(ys); orc = G.Oracle(th)
    R = dict(G.roots_for(th, x, y))
    seqs = [R['C0'], R['C1']]
    at = []
    if atoms:
        for f, kind, lev, _ in G.atom_formulas(th, x, y):
            at.append((frozenset(), frozenset([f])))
    cuts = G.cut_closure(th, seqs + at)
    res = dict(x=xs, y=ys, n_cuts=len(cuts))
    for nm in ('C0', 'C1'):
        res[nm] = _measure_root(th, orc, (frozenset(R[nm][0]), frozenset(R[nm][1])), cuts, cap, cut_cap)
    if atoms:
        res["atoms"] = [_measure_root(th, orc, S, cuts, cap, cut_cap) for S in at]
    return res


def _lread(res, tag, key):
    tot = 0; ok = True
    for a in res['atoms']:
        if a is None: continue
        d = a[tag]
        if not d['certified']: ok = False
        tot += d[key] if d.get(key) is not None else d['size']
    return tot, ok


def _sharing_job(j):
    return measure_pair(j[0], j[1])


def cmd_sharing(a):
    """Cost table in four columns (tree/no cut, tree/cut, DAG/no cut, DAG/cut; DAG exact and subsumption), siblings."""
    import conj4 as C4
    from proof_length_arm import LADDER
    rows = []
    progs = list(LADDER) + ['not(BOX(THEM(ME)))', 'BOX(THEM(^BOX(THEM(ME))))']
    jobs = [(x, x) for x in progs]
    sib = {}
    for x in LADDER:
        K, y, z = C4.sibling(C4.parse(x), 60)
        sib[x] = C4.src(y)
        jobs.append((x, sib[x]))
    t = time.time()
    path = os.path.join(RUNS, 'k-at-n8-sharing.json')
    # cheapest first (by the published cut-free size of x's self-proof), saved as they come
    order = {x: i for i, x in enumerate(['BOX(THEM(ME))', 'BOX(THEM(THEM))', 'BOX1(THEM(ME))', 'BOX1(THEM(THEM))', 'BOX(THEM(^C))',
                                         'BOX1(THEM(^C))', 'not(BOX(THEM(ME)))', 'BOX(THEM(^BOX(THEM(ME))))'])}
    jobs.sort(key=lambda j: (order.get(j[0], 50), j[0] != j[1], len(j[0])))
    with Pool(a.workers) as pool:
        for r in pool.imap_unordered(_sharing_job, jobs):
            rows.append(r)
            json.dump(dict(rows=rows, siblings=sib, wall_s=time.time() - t), open(path, 'w'), indent=1)
            print('done', r['x'][:50], r['y'][:40], '%.0fs' % (time.time() - t), flush=True)
    for r in rows:
        for nm in ('C0', 'C1'):
            m = r[nm]
            if m:
                print(r['x'][:50], 'vs', r['y'][:30] if r['y'] != r['x'] else 'self', nm,
                      'tree %s(%s) cut %s(%s)%s DAGex %s/%s DAGsub %s/%s' % (m['nocut']['size'], m['nocut']['loeb'], m['cut']['size'], m['cut']['loeb'],
                                                                        '' if m['cut']['certified'] else '*', m['nocut'].get('exact'), m['cut'].get('exact'),
                                                                        m['nocut'].get('subs'), m['cut'].get('subs')), flush=True)


def _mce_job(pairs):
    out = []
    for xs, ys in pairs:
        r = measure_pair(xs, ys, cap=a_cap, atoms=False)
        out.append(dict(x=xs, y=ys, C0=r['C0'], C1=r['C1']))
    return out


a_cap = 1_000_000


def cmd_mce(a):
    """Scaling on the n = 8 mutually cooperating establisher pairs under each measure."""
    import modal as M
    L8 = M.ModalLanguage(8); val8, _ = M.evaluate(L8)
    iD = L8.rep.index('D')
    est = [c for c in range(len(L8.rep)) if val8[c, c] == 1 and val8[c, iD] == 0]
    mce = [(L8.rep[p], L8.rep[q]) for p in est for q in est if val8[p, q] == 1 and val8[q, p] == 1]
    if a.limit: mce = mce[:a.limit]
    chunks = [mce[i:i + 50] for i in range(0, len(mce), 50)]
    rows = []; t = time.time()
    with Pool(a.workers) as pool:
        for out in pool.imap_unordered(_mce_job, chunks):
            rows += out
            if len(rows) % 1000 < 50: print(len(rows), '%.0fs' % (time.time() - t), flush=True)
    json.dump(dict(rows=rows, wall_s=time.time() - t), open(os.path.join(RUNS, 'k-at-n8-mce.json'), 'w'))
    print('done', len(rows), '%.0fs' % (time.time() - t))


# ------------------------------------------------------------------ prices in K (n = 6, per-program budgets)
PB_BUDGETS = [2, 3, 4, 6, 10, 16]
KPAIRS = os.path.join(RUNS, 'proof-length-kpairs.npz')


def _kpair_pruned(j):
    """proof_length_arm._kpair with the GL-erasure prune (cross-budget plays of L_6)."""
    bx, by = j
    L, vf, hc, hd = tables(6)
    t = time.time()
    K = BK.KTheory(cap=max(bx, by), filter_first=True)
    K.prune = make_prune(K, L, hc, hd)
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
    return bx, by, vxy, vyx, nchk, len(bad), time.time() - t


def cmd_kpairs(a):
    B = PB_BUDGETS
    old = dict(np.load(KPAIRS)) if os.path.exists(KPAIRS) else {}
    jobs = [(bx, by) for i, bx in enumerate(B) for by in B[i:]]
    out = {}; sb = 0; nchk_tot = 0; agree = []
    with Pool(a.workers) as pool:
        for bx, by, vxy, vyx, nchk, nbad, dt in pool.imap_unordered(_kpair_pruned, jobs):
            k1, k2 = 'v%d_%d' % (bx, by), 'v%d_%d' % (by, bx)
            if k1 in old:
                agree.append(((bx, by), bool((old[k1] == vxy).all() and (old[k2] == vyx).all())))
            out[k1] = vxy; out[k2] = vyx; sb += nbad; nchk_tot += nchk
            print('(%d, %d) sound bad %d / %d, %.0fs' % (bx, by, nbad, nchk, dt), flush=True)
    np.savez_compressed(KPAIRS, **out)
    print('soundness violations', sb, 'of', nchk_tot, '; agreement with the unpruned cells already computed:', agree)
    json.dump(dict(sound_bad=sb, sound_checked=nchk_tot, agree_unpruned=agree), open(os.path.join(KDIR, 'kpairs_meta.json'), 'w'))


def price_matrix(schedule, c, N, val, base, gb, copy='a'):
    """Per-match cost on the reader i against opponent j (constants pay nothing).  Imposed schedules:
    per-match c*b; amortized c*b/N; cache c*b*k/N with k = 2 classes present during a single-mutant invasion (so on
    the chain's transitions cache(c) = amortized(2c); k = 1 in a monomorphic state, which no fixation probability
    sees); lazy c*b against opponents that are neither constants nor copies, copy = (a) identical budgeted program,
    (b) same source at any budget, (c) extensionally identical play (same row and column of the play table)."""
    G_ = len(base)
    b = gb.astype(float)
    if schedule == 'per-match':
        return np.repeat((c * b)[:, None], G_, 1)
    if schedule == 'amortized':
        return np.repeat((c * b / N)[:, None], G_, 1)
    if schedule == 'cache':
        return np.repeat((2 * c * b / N)[:, None], G_, 1)
    if schedule == 'lazy':
        const = gb == 0
        if copy == 'a':
            same = np.eye(G_, dtype=bool)
        elif copy == 'b':
            same = base[:, None] == base[None, :]
        else:
            sig = {}
            key = [val[i].tobytes() + val[:, i].tobytes() for i in range(G_)]
            ids = np.array([sig.setdefault(k, len(sig)) for k in key])
            same = ids[:, None] == ids[None, :]
        cost = c * b[:, None] * np.ones((1, G_))
        cost[:, const] = 0.0
        cost[same] = 0.0
        return cost
    raise ValueError(schedule)


def priced_cell(j):
    import modal as M
    from chain import Chain
    from proof_length_arm import priced_val
    from cert_limN import top_exits
    schedule, c, N, copy = j
    B = PB_BUDGETS
    val, base, gb, L = priced_val(B)
    U0, PCC = M.pd_payoffs(val, M.PD)
    cost = price_matrix(schedule, c, N, val, base, gb, copy)
    U = U0.astype(float) - cost
    nb = len(B)
    mu = np.array([L.mu_canon[bc] / (1.0 if gb[g] == 0 else nb) for g, bc in enumerate(base)])
    names = [L.rep[bc] if gb[g] == 0 else '%s@%d' % (L.rep[bc], gb[g]) for g, bc in enumerate(base)]
    bits = np.array([L.bits_canon[bc] for bc in base])
    prov = M.ModalProvider(U, PCC, mu, names, bits)
    prov.sizes = np.ones(len(prov.names))
    lang = M.ClassLang(prov)
    t = time.time()
    ch = Chain(prov, N=N, w=0.3, verbose=False, eager_poly=False).explore()
    P = prov.PCC; nm = prov.names; Uf = prov.Ufull
    pcc = 0.0; pis = {}; poly = 0.0; key_of = {}
    for key, wgt in zip(ch.keys_list, ch.pi):
        ids, x, kd = ch.states[key]; ids = list(ids); x = np.asarray(x)
        pcc += wgt * float(x @ P[np.ix_(ids, ids)] @ x)
        if kd == 'mono':
            pis[ids[0]] = pis.get(ids[0], 0.0) + wgt; key_of[ids[0]] = key
        else:
            poly += wgt
    byb = {}; byb_coop = {}; coop_pi = 0.0; by_src = {}
    for q, p in pis.items():
        mem = prov.members[q]
        w_ = np.array([mu[g] for g in mem]); w_ = w_ / w_.sum()
        for g, ww in zip(mem, w_):
            kb = str(int(gb[g]))
            byb[kb] = byb.get(kb, 0.0) + p * ww
            if P[q, q] == 1 and nm[q] != 'C':
                byb_coop[kb] = byb_coop.get(kb, 0.0) + p * ww
        if P[q, q] == 1 and nm[q] != 'C': coop_pi += p
        by_src[nm[q]] = by_src.get(nm[q], 0.0) + p
    zc = sum(byb_coop.values()) or 1.0
    # mutation mass by behavioural class: the classes' mu (prov.classes carries normalized mu)
    mclass = sorted(((nm[i], float(cl[2])) for i, cl in enumerate(prov.classes)), key=lambda t_: -t_[1])[:8]
    mu_coop = float(sum(cl[2] for i, cl in enumerate(prov.classes) if P[i, i] == 1 and nm[i] != 'C'))
    out = dict(schedule=schedule, c=c, N=N, copy=copy, pcc=pcc, pi_by_budget=byb, budget_given_coop={k: v / zc for k, v in byb_coop.items()},
               pi_selfcoop_mono=coop_pi, poly=poly, pi_D=pis.get(nm.index('D'), 0.0), pi_C=pis.get(nm.index('C'), 0.0),
               support=[(ch.describe_state(k, lang), float(p)) for k, p in ch.support(1e-3)][:10], cut_flow=ch.cut_flow,
               indeterminate=len(ch.indeterminate), n_terminal=len(ch.terminal), mu_classes_top=mclass, mu_selfcoop=mu_coop,
               n_classes=len(nm))
    top_states = sorted(((v, q) for q, v in pis.items() if P[q, q] == 1 and nm[q] != 'C'), reverse=True)
    if top_states:
        v, qtop = top_states[0]
        e = top_exits(ch, prov, key_of[qtop])
        out.update(top_coop=nm[qtop], pi_top=v, **e)
        out['top_budget_share'] = max(out['budget_given_coop'].values()) if out['budget_given_coop'] else 0.0
        iD = nm.index('D'); kD = key_of.get(iD)
        edges = []
        for v2, q2 in top_states[:3]:
            kT = key_of[q2]; uaa = Uf[q2, q2]
            for b_, pr in ch.trans.get(kT, {}).items():
                if b_ == kT: continue
                for q, mw in ch.trans_mut[(kT, b_)].items():
                    r = ch.edge_rho.get((kT, b_, q))
                    d = float(Uf[q, q2] - uaa)
                    edges.append(dict(kind='exit', resident=nm[q2], pi_res=v2, mutant=nm[q], w=float(mw), delta=d, N_delta=N * d,
                                      rho=r and float(r[0]), fix_ratio=r and float(N * r[0]),
                                      c_b=float(c * max(gb[g] for g in prov.members[q2])) if schedule != 'none' else 0.0))
            ent = [(q, r) for (a_, b_, q), r in ch.edge_rho.items() if a_ == kD and b_ == kT]
            if ent:
                q, r = max(ent, key=lambda t_: t_[1][0])
                d = float(Uf[q, iD] - Uf[iD, iD])
                edges.append(dict(kind='entry', resident='D', mutant=nm[q], target=nm[q2], delta=d, N_delta=N * d, rho=float(r[0]), fix_ratio=float(N * r[0])))
        edges.sort(key=lambda e_: -(e_.get('w') or 0))
        out['edges'] = edges[:12]
    out['t'] = time.time() - t
    return out


def cmd_priced(a):
    jobs = []
    for c in (0.01, 0.1, 1.0):
        for N in (1000, 10000, 30000):
            jobs.append(('amortized', c, N, 'a'))
    for c in (0.01, 0.1):
        jobs.append(('cache', c, 10000, 'a'))
        jobs.append(('lazy', c, 10000, 'a'))
    jobs += [('lazy', 0.1, 10000, 'b'), ('lazy', 0.1, 10000, 'c'), ('per-match', 0.01, 10000, 'a'), ('amortized', 0.0, 10000, 'a')]
    path = os.path.join(RUNS, 'k-at-n8-priced.json')
    rows = json.load(open(path)) if os.path.exists(path) else []
    done = {(r['schedule'], r['c'], r['N'], r['copy']) for r in rows}
    jobs = [j for j in jobs if j not in done]
    with Pool(a.workers) as pool:
        for r in pool.imap_unordered(priced_cell, jobs):
            rows.append(r)
            json.dump(rows, open(path, 'w'), indent=1, default=str)
            print('%-10s c=%-5g N=%-6d copy=%s P(C,C) %.4f pi(D) %.3f pi(C) %.3f coop-budget %s top %s %.3f exit %.2e strict %.2e (%.0fs)' % (
                r['schedule'], r['c'], r['N'], r['copy'], r['pcc'], r['pi_D'], r['pi_C'],
                {k: round(v, 3) for k, v in sorted(r['budget_given_coop'].items(), key=lambda kv: int(kv[0]))},
                r.get('top_coop'), r.get('pi_top', 0), r.get('top_exit', 0), r.get('top_exit_strict', 0), r['t']), flush=True)


def _cutcheck_job(pairs):
    import gl_proofs as G
    L = tables(6)[0]
    out = []
    for c, d in pairs:
        th = G.Theory(); x = th.prog(L.rep[c]); y = th.prog(L.rep[d]); orc = G.Oracle(th)
        R = G.roots_for(th, x, y)
        cuts = G.cut_closure(th, [s for _, s in R])
        ms1 = G.MinSearch(th, orc, cuts=cuts); ms0 = G.MinSearch(th, orc)
        gn = G.Graph(th, [s for _, s in R], oracle=orc, nf=True, cuts=cuts, cap=400000, time_cap=60)
        ga = G.Graph(th, [s for _, s in R], oracle=orc, nf=False, cuts=cuts, cap=200000, time_cap=20)
        row = dict(c=int(c), d=int(d), nf_fit=gn.complete, all_fit=ga.complete, roots={})
        for nm, S in R:
            r1 = ms1.minimize(S); r0 = ms0.minimize(S)
            if r1 is None:
                row['roots'][nm] = None; continue
            d1 = ms1.dag_sizes(S) if r1['certified'] else {}
            d0 = ms0.dag_sizes(S)
            row['roots'][nm] = dict(cut=list(r1['c']), cert=r1['certified'], nocut=list(r0['c']),
                                    knuth_nf=list(gn.result(S)) if gn.complete else None,
                                    knuth_all=list(ga.result(S)) if ga.complete else None,
                                    exact0=d0['exact'], subs0=d0['subsumption'], exact1=d1.get('exact'), subs1=d1.get('subsumption'))
        out.append(row)
    return out


def cmd_cutcheck(a):
    L = tables(6)[0]
    K = len(L.rep)
    pairs = [(c, d) for c in range(K) for d in range(K)]
    chunks = [pairs[i:i + 40] for i in range(0, len(pairs), 40)]
    rows = []; t = time.time()
    with Pool(a.workers) as pool:
        for out in pool.imap_unordered(_cutcheck_job, chunks):
            rows += out
            if len(rows) % 400 < 40: print(len(rows), '%.0fs' % (time.time() - t), flush=True)
    mism_nf = mism_all = n_nf = n_all = unc = 0
    for r in rows:
        for nm, v in r['roots'].items():
            if v is None: continue
            if not v['cert']: unc += 1
            if v['knuth_nf'] is not None:
                n_nf += 1; mism_nf += v['knuth_nf'] != v['cut']
            if v['knuth_all'] is not None:
                n_all += 1; mism_all += v['knuth_all'] != v['cut']
    summ = dict(pairs=len(rows), roots_nf=n_nf, mismatch_nf=mism_nf, roots_all=n_all, mismatch_all=mism_all, uncertified=unc,
                pairs_nf_fit=sum(r['nf_fit'] for r in rows), pairs_all_fit=sum(r['all_fit'] for r in rows), wall_s=time.time() - t)
    json.dump(dict(summary=summ, rows=rows), open(os.path.join(RUNS, 'k-at-n8-cutcheck.json'), 'w'))
    print(summ)


# ------------------------------------------------------------------ the eps = 0 lottery at n = 8
def lottery_job(j):
    """As proof_length_arm._lottery_job, for L_n (seeding: iid from mu, paired across arms by seed)."""
    import almost_all_seeds as AS
    label, n, val, N, I, rep = j
    L = tables(n)[0]
    prov = build_prov(n, val)
    names = list(prov.names)
    U = np.ascontiguousarray(prov.Ufull, dtype=float); PCC = np.ascontiguousarray(prov.PCC, dtype=float)
    K = len(names)
    cls = np.zeros(len(L.rep), np.int64)
    for k, mem in enumerate(prov.canon):
        for c in mem: cls[c] = k
    iC = names.index('C')
    coop = [k for k in range(K) if PCC[k, k] >= 0.95 and k != iC]
    mu = L.mu_canon / L.mu_canon.sum()
    rng = np.random.default_rng([N, I, n, rep, 2026104])
    init = np.zeros((I, K), np.int64)
    for i in range(I):
        cnt = rng.multinomial(N, mu)
        np.add.at(init[i], cls, cnt)
    coopmask = np.zeros(K, np.bool_); coopmask[coop] = True
    t = time.time()
    res = AS._run(U, PCC, init, N, AS.W, 1.0 / N, 100000, 20, 100003 * rep + 7 * N + I + 1000 + 99991, iC, coopmask)
    st, sg, counts, isl_cc, isl_pay = res[:5]
    cc = float(isl_cc.mean()); pay = float(isl_pay.mean())
    glob = counts.sum(0)
    return dict(label=label, n=n, N=N, I=I, rep=rep, status=AS.STATUS[st], stop_gen=int(sg), pcc=cc, pay=pay,
                outcome=AS.outcome(cc, pay) if st in (1, 2, 3) else ('unresolved' if st == 4 else None),
                final={names[k]: int(v) for k, v in enumerate(glob) if v > 0}, t=time.time() - t)


def cmd_lottery(a):
    import almost_all_seeds as AS
    arms = [('free', load_val(8, 'free'))] + [('K b=%d' % b, load_val(8, b)) for b in a.budgets]
    jobs = [(lab, 8, v, 100, 64, rep) for lab, v in arms for rep in range(a.reps)]
    path = os.path.join(RUNS, 'k-at-n8-lottery.json')
    t = time.time(); rows = []
    with Pool(a.workers) as pool:
        for r in pool.imap_unordered(lottery_job, jobs, chunksize=1):
            rows.append(r)
            json.dump(dict(rows=rows), open(path, 'w'), default=str)
            print(r['label'], r['rep'], r['outcome'], r['status'], '%.0fs' % r['t'], flush=True)
    summ = []
    for lab, _ in arms:
        R = [r for r in rows if r['label'] == lab]
        res = [r for r in R if r['outcome'] not in ('unresolved', None)]
        k = sum(1 for r in res if r['outcome'] == 'efficient')
        lo, hi = AS.wilson(k, len(res))
        summ.append(dict(label=lab, n=len(res), efficient=k, frac=k / max(len(res), 1), wilson=[lo, hi], unresolved=len(R) - len(res)))
        print('%-8s efficient %d/%d [%.2f, %.2f], unresolved %d' % (lab, k, len(res), lo, hi, len(R) - len(res)))
    json.dump(dict(rows=rows, summary=summ, wall_s=time.time() - t), open(path, 'w'), default=str)


def cmd_family(a):
    """Named family beyond L_8 (P2, the level-2 ladder, Conjecture-4 siblings and fakers): K plays at each budget."""
    import conj4 as C4
    from proof_length_arm import LADDER
    progs = list(LADDER) + ['not(BOX(THEM(ME)))', 'not(BOX(THEM(THEM)))', 'BOX1(THEM(^not(BOX(THEM(ME)))))']
    sib = {}
    for x in LADDER:
        K_, y, z = C4.sibling(C4.parse(x), 60)
        sib[x] = dict(y=C4.src(y), z=C4.src(z))
        progs += [C4.src(y), C4.src(z)]
    progs = list(dict.fromkeys(progs + ['C', 'D']))
    out = dict(progs=progs, siblings=sib, tables={}, meta={})
    for b in a.budgets:
        v, m = family_table(progs, b)
        out['tables'][str(b)] = v.tolist(); out['meta'][str(b)] = m
        print('b=%d sound %d/%d contents %d %.0fs' % (b, m['sound_bad'], m['sound_checked'], m['n_contents'], m['t']), flush=True)
        json.dump(out, open(os.path.join(RUNS, 'k-at-n8-family.json'), 'w'), indent=1)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd')
    ap.add_argument('--workers', type=int, default=3)
    ap.add_argument('--n', type=int, default=8)
    ap.add_argument('--budgets', type=int, nargs='+', default=[3, 4, 6, 8, 12, 16, 24, 32, 54])
    ap.add_argument('--ustar_limit', type=int, default=40)
    ap.add_argument('--Ns', type=int, nargs='+', default=[1000, 10000, 30000])
    ap.add_argument('--arms', nargs='*', default=[])
    ap.add_argument('--ref', type=int, default=16)
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--reps', type=int, default=20)
    a = ap.parse_args()
    {'ktables': cmd_ktables, 'static': cmd_static, 'chain': cmd_chain, 'fakers': cmd_fakers, 'sharing': cmd_sharing,
     'mce': cmd_mce, 'priced': cmd_priced, 'lottery': cmd_lottery, 'family': cmd_family,
     'cutcheck': cmd_cutcheck, 'kpairs': cmd_kpairs}[a.cmd](a)
