"""Proof length (specs/2026-10-05-proof-length.md; predictions/2026-10-05-proof-length.md).

Part A (static, exact): GLS+Def lengths on L_6 (every pair) and L_8 (named family, a mu-weighted sample of 5,000
pairs, every mutually cooperating establisher pair), the audit of the four box-fact tables, the proxy comparison,
siblings and the prudence ladder beyond L_8 (audited against src/conj4.py's trace evaluator).

    python3 src/proof_length_arm.py partA [--workers 3]
Writes runs/proof-length-partA.json (raw rows); `report` builds runs/proof-length.md / .json.
"""
import argparse, json, os, sys, time
import numpy as np
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(__file__))
import gl_proofs as G

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS = os.path.join(ROOT, 'runs')
OUT_A = os.path.join(RUNS, 'proof-length-partA.json')

FB = 'BOX(THEM(ME))'
PB = 'and(BOX(THEM(ME)),BOXD1(THEM(^D)))'
PSTAR = 'and(BOX1(THEM(ME)),not(BOX(THEM(ME))))'
FAMILY_L8 = [FB, 'BOX1(THEM(ME))', 'BOX(THEM(THEM))', 'BOX1(THEM(THEM))', 'BOX(THEM(^C))', 'BOX1(THEM(^C))', PB, PSTAR,
             'not(BOX(THEM(ME)))', 'BOX1(THEM(^not(BOX(THEM(ME)))))', 'BOX(THEM(^D))', 'BOX1(THEM(^D))', 'C', 'D',
             'BOXD(THEM(^C))', 'BOX(THEM(^BOX(THEM(ME))))', 'not(BOXD(THEM(^C)))']
LADDER = [FB, 'BOX1(THEM(ME))', PB, PSTAR,
          'and(BOX1(THEM(ME)),not(BOX(THEM(^C))))',                         # P2
          'and(and(BOX1(THEM(ME)),not(BOX(THEM(^C)))),BOXD2(THEM(^D)))',     # P12b
          'and(and(BOX1(THEM(ME)),not(BOX(THEM(ME)))),BOXD2(THEM(^D)))',     # P*1b
          'and(BOX(THEM(ME)),BOXD2(THEM(^D)))',                              # PB2
          'BOX(THEM(THEM))', 'BOX1(THEM(THEM))', 'BOX(THEM(^C))', 'BOX1(THEM(^C))']
ROOTS = ('C0', 'D0', 'C1', 'D1')


# ------------------------------------------------------------------ per-pair measurement
_W = {}


def _ctx(n):
    if n not in _W:
        if n is None:
            _W[n] = dict(th=None)
        else:
            L, val, hc, hd = G.box_tables(n)
            _W[n] = dict(L=L, val=val, hc=hc, hd=hd)
    return _W[n]


class Meas:
    def __init__(self):
        self.reset()

    def reset(self):
        self.th = G.Theory(); self.orc = G.Oracle(self.th); self.ms = G.MinSearch(self.th, self.orc)
        self.pid = {}

    def p(self, s):
        if s not in self.pid:
            self.pid[s] = self.th.prog(s)
        return self.pid[s]

    def root(self, S):
        t = time.time()
        r = self.ms.minimize(S)
        dt = time.time() - t
        if r is None:
            return None
        out = dict(size=r['c'][0] if r['c'] else None, loeb=r['c'][1] if r['c'] else None, certified=r['certified'],
                   expansions=r['expansions'], t=dt)
        if r['certified']:
            st = self.ms.stats(S)
            out.update(dag=st['dag'], height=st['height'], loeb_depth=st['loeb_depth'])
        else:
            out['lb'] = r['lb']
        return out

    def pair(self, xs, ys):
        th = self.th
        x, y = self.p(xs), self.p(ys)
        t = time.time()
        res = dict(x=xs, y=ys)
        for nm, S in G.roots_for(th, x, y):
            res[nm] = self.root(S)
        atoms = []
        for f, kind, lev, (pp, qq) in G.atom_formulas(th, x, y):
            S = (frozenset(), frozenset([f]))
            r = self.root(S)
            atoms.append(dict(kind=kind, lev=lev, prov=r is not None, size=r and r['size'], loeb=r and r['loeb'],
                              certified=(r is None) or r['certified']))
        res['atoms'] = atoms
        res['L_read'] = sum(a['size'] for a in atoms if a['prov'])
        res['read_certified'] = all(a['certified'] for a in atoms)
        res['t'] = time.time() - t
        res['phi_symbols'] = th.symbols(th.unfold(th.P(x, y)))
        return res


_M = None


def job(j):
    """j = (tag, n or None, list of (xsrc, ysrc))."""
    global _M
    if _M is None:
        _M = Meas()
    tag, n, pairs = j
    out = []
    for xs, ys in pairs:
        if len(_M.th.forms) > 400000:
            _M.reset()
        r = _M.pair(xs, ys)
        r['tag'] = tag; r['n'] = n
        out.append(r)
    return out


def audit_rows(rows, n):
    """Fill provability-vs-table agreement (n given) or vs conj4 trace (n None)."""
    if n is not None:
        c = _ctx(n); L = c['L']; idx = {s: i for i, s in enumerate(L.rep)}
        for r in rows:
            a, b = idx[r['x']], idx[r['y']]
            want = dict(C0=bool(c['hc'][0, a, b]), D0=bool(c['hd'][0, a, b]), C1=bool(c['hc'][1, a, b]), D1=bool(c['hd'][1, a, b]))
            r['val'] = int(c['val'][a, b])
            r['audit_bad'] = [k for k in ROOTS if want[k] != (r[k] is not None)]
    else:
        import conj4 as C4
        for r in rows:
            tr = C4.trace(C4.parse(r['x']), C4.parse(r['y']), 60)
            assert len(set(tr[30:])) == 1
            want = dict(C0=all(v == 1 for v in tr), D0=all(v == 0 for v in tr), C1=all(v == 1 for v in tr[1:]), D1=all(v == 0 for v in tr[1:]))
            r['val'] = tr[-1]
            r['audit_bad'] = [k for k in ROOTS if want[k] != (r[k] is not None)]


def chunks(tag, n, pairs, k=50):
    return [(tag, n, pairs[i:i + k]) for i in range(0, len(pairs), k)]


def partA(a):
    import modal as M
    jobs = []
    L6 = M.ModalLanguage(6)
    jobs += chunks('n6', 6, [(x, y) for x in L6.rep for y in L6.rep], 100)
    L8 = M.ModalLanguage(8)
    fam = [s for s in FAMILY_L8 if s in L8.rep]
    jobs += chunks('n8_family', 8, [(x, y) for x in fam for y in fam], 20)
    mu = L8.mu_canon / L8.mu_canon.sum()
    rng = np.random.default_rng(20261005)
    xs = rng.choice(len(mu), 5000, p=mu); ys = rng.choice(len(mu), 5000, p=mu)
    jobs += chunks('n8_sample', 8, [(L8.rep[i], L8.rep[j]) for i, j in zip(xs, ys)], 50)
    val8, _ = M.evaluate(L8)
    iD = L8.rep.index('D')
    est = [c for c in range(len(L8.rep)) if val8[c, c] == 1 and val8[c, iD] == 0]
    mce = [(L8.rep[p], L8.rep[q]) for p in est for q in est if val8[p, q] == 1 and val8[q, p] == 1]
    jobs += chunks('n8_mce', 8, mce, 100)
    # beyond L_8: the ladder, siblings, fakers (conj4)
    import conj4 as C4
    extra = list(LADDER)
    sib = {}
    for x in LADDER:
        K, y, z = C4.sibling(C4.parse(x), 60)
        sib[x] = dict(K=K, y=C4.src(y), z=C4.src(z))
        extra += [C4.src(y), C4.src(z)]
    extra = list(dict.fromkeys(extra + ['C', 'D']))
    jobs += chunks('ladder', None, [(x, y) for x in extra for y in extra], 20)
    t = time.time()
    rows = []
    jobs.sort(key=lambda j: (j[0] != 'ladder', j[0] != 'n8_family'))
    with Pool(a.workers) as pool:
        for out in pool.imap_unordered(job, jobs):
            rows += out
            if len(rows) % 2000 < len(out):
                print('%d rows, %.0fs' % (len(rows), time.time() - t), flush=True)
    for tag, n in (('n6', 6), ('n8_family', 8), ('n8_sample', 8), ('n8_mce', 8), ('ladder', None)):
        audit_rows([r for r in rows if r['tag'] == tag], n)
    json.dump(dict(rows=rows, siblings=sib, wall_s=time.time() - t), open(OUT_A, 'w'))
    bad = [r for r in rows if r['audit_bad']]
    print('done: %d rows, %d audit disagreements, %.0fs' % (len(rows), len(bad), time.time() - t))


def partA_uniform(a):
    """Addition (not in the spec): a uniform (not mu-weighted) sample of 5,000 L_8 pairs, because the mu-weighted
    sample is 89% constant opponents (v = 0) and leaves only 312 pairs for the proxy comparison."""
    import modal as M
    L8 = M.ModalLanguage(8)
    rng = np.random.default_rng(20261006)
    xs = rng.integers(len(L8.rep), size=5000); ys = rng.integers(len(L8.rep), size=5000)
    jobs = chunks('n8_uniform', 8, [(L8.rep[i], L8.rep[j]) for i, j in zip(xs, ys)], 50)
    d = json.load(open(OUT_A))
    d['rows'] = [r for r in d['rows'] if r['tag'] != 'n8_uniform']
    t = time.time(); rows = []
    with Pool(a.workers) as pool:
        for out in pool.imap_unordered(job, jobs):
            rows += out
    audit_rows(rows, 8)
    d['rows'] += rows
    json.dump(d, open(OUT_A, 'w'))
    print('uniform: %d rows, %d disagreements, %.0fs' % (len(rows), sum(1 for r in rows if r['audit_bad']), time.time() - t))


# ------------------------------------------------------------------ Part B, run 1: the budget grid
def _grid_cell(j):
    import bounded_k as BK
    px, py, bx, by = j
    K = BK.KTheory(cap=80)
    gx, gy = K.geno(px, bx), K.geno(py, by)
    ax = K.atoms(gx, gy); ay = K.atoms(gy, gx)
    passes = K.solve([K.forms[a][1] for a in ax + ay])
    play = K.play_fn()
    nchk, bad = K.soundness_check()
    return dict(px=px, py=py, bx=bx, by=by, xy=int(play(gx, gy)), yx=int(play(gy, gx)),
                Tx=[K.T.get(K.forms[a][1]) for a in ax], Ty=[K.T.get(K.forms[a][1]) for a in ay], passes=passes,
                sound_checked=nchk, sound_bad=len(bad))


def grid(a):
    B = list(range(2, 41))
    fams = [(FB, FB), ('BOX1(THEM(ME))', 'BOX1(THEM(ME))'), (FB, 'BOX1(THEM(ME))')]
    jobs = [(px, py, bx, by) for px, py in fams for bx in B for by in B]
    t = time.time()
    with Pool(a.workers) as pool:
        rows = pool.map(_grid_cell, jobs, chunksize=40)
    out = dict(rows=rows, wall_s=time.time() - t)
    json.dump(out, open(os.path.join(RUNS, 'proof-length-grid.json'), 'w'))
    for px, py in fams:
        R = [r for r in rows if r['px'] == px and r['py'] == py]
        asym = [(r['bx'], r['by'], r['xy'], r['yx']) for r in R if r['xy'] != r['yx']]
        diag = min([r['bx'] for r in R if r['bx'] == r['by'] and r['xy'] and r['yx']] or [None])
        off = sorted(set((min(r['bx'], r['by'])) for r in R if r['bx'] != r['by'] and r['xy'] and r['yx']))
        offmin = off[0] if off else None
        # is cooperation exactly {min(bx, by) >= threshold} off the diagonal?
        exact = all((r['xy'] and r['yx']) == (min(r['bx'], r['by']) >= offmin) for r in R if r['bx'] != r['by']) if offmin else None
        print(px, 'vs', py, 'asymmetric cells', len(asym), asym[:5], 'diag threshold', diag, 'off-diag min-threshold', offmin, 'exactly min-rule', exact,
              'soundness violations', sum(r['sound_bad'] for r in R), 'checked', sum(r['sound_checked'] for r in R))
    print('%.0fs' % (time.time() - t))


# ------------------------------------------------------------------ Part B, run 2: the bounded arm at n = 6
KVALS = os.path.join(RUNS, 'proof-length-karm.npz')


def _kval(b):
    """Play matrix of L_6 with every class at global budget b, decided by K; plus soundness and GL-comparison."""
    import bounded_k as BK
    import modal as M
    L = M.ModalLanguage(6)
    t = time.time()
    K = BK.KTheory(cap=max(b, 1))
    g = [K.geno(s, b) for s in L.rep]
    contents = set()
    for x in g:
        for y in g:
            for a in K.atoms(x, y): contents.add(K.forms[a][1])
    passes = K.solve(sorted(contents))
    play = K.play_fn()
    val = np.array([[int(play(x, y)) for y in g] for x in g], np.int8)
    nchk, bad = K.soundness_check()
    Ts = sorted(v for v in K.T.values() if v < BK.INF)
    return b, val, dict(b=b, passes=passes, sound_checked=nchk, sound_bad=len(bad), n_contents=len(contents),
                        T_hist=np.bincount(Ts).tolist() if Ts else [], t=time.time() - t)


def karm_vals(a):
    B = list(range(1, 41))
    out = {}; meta = []
    with Pool(a.workers) as pool:
        for b, val, m in pool.imap_unordered(_kval, B):
            out['b%d' % b] = val; meta.append(m)
            print('b=%d sound %d/%d bad, %.0fs' % (b, m['sound_bad'], m['sound_checked'], m['t']), flush=True)
    np.savez_compressed(KVALS, **out)
    json.dump(sorted(meta, key=lambda m: m['b']), open(os.path.join(RUNS, 'proof-length-karm-meta.json'), 'w'))


def _free6():
    import modal as M
    L = M.ModalLanguage(6); val, _ = M.evaluate(L)
    return L, val.astype(np.int8)


def matched_control(val_k, val_free, seed=20261005):
    """Random flips of the free table, matched to the K arm stratum by stratum: stratum = (opponent class y, free
    play C/D, reader has boxes); within each stratum, as many plays flipped as the K arm changed."""
    import modal as M
    L = M.ModalLanguage(6); nat = L.arrays()[0]
    rng = np.random.default_rng(seed)
    out = val_free.copy()
    K = len(nat)
    for y in range(K):
        for v in (0, 1):
            for hb in (0, 1):
                cells = [x for x in range(K) if val_free[x, y] == v and (nat[x] > 0) == hb]
                nch = sum(1 for x in cells if val_k[x, y] != val_free[x, y])
                if nch:
                    for x in rng.choice(cells, nch, replace=False):
                        out[x, y] = 1 - out[x, y]
    return out


def leak_test(val):
    """Drift-closure at n = 6: x self-cooperating; its mutual-cooperation component; closed iff no member is
    suckerable (cooperates with some z that defects on it)."""
    K = val.shape[0]
    S = [x for x in range(K) if val[x, x] == 1]
    comp = {}; comps = []
    for s in S:
        if s in comp: continue
        stack = [s]; mem = []; comp[s] = len(comps)
        while stack:
            a = stack.pop(); mem.append(a)
            for b in S:
                if b not in comp and val[a, b] == 1 and val[b, a] == 1:
                    comp[b] = len(comps); stack.append(b)
        comps.append(mem)
    suck = [x for x in range(K) if any(val[x, z] == 1 and val[z, x] == 0 for z in range(K))]
    closed = [c for c in comps if not any(m in suck for m in c)]
    return dict(n_selfcoop=len(S), n_components=len(comps), closed_components=closed, n_closed=len(closed))


def _arm_prov(val):
    import modal as M
    L = M.ModalLanguage(6)
    U, PCC = M.pd_payoffs(val, M.PD)
    prov = M.ModalProvider(U.astype(float), PCC, L.mu_canon, L.rep, L.bits_canon)
    prov.sizes = np.array([L.count_canon[m].sum() for m in prov.members])
    return prov


def _chain_cell(j):
    import modal as M
    from chain import Chain
    label, val, N = j
    t = time.time()
    prov = _arm_prov(val)
    names = prov.names; P = prov.PCC
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
    coop = [(v, q) for q, v in pis.items() if P[q, q] == 1 and q != iC]
    out = dict(label=label, N=N, n_classes=len(names), pcc=pcc, pi_D=pis.get(iD, 0.0), pi_C=pis.get(iC, 0.0), poly=poly,
               cut_flow=ch.cut_flow, indeterminate=len(ch.indeterminate), n_terminal=len(ch.terminal),
               support=[(ch.describe_state(k, lang), float(p)) for k, p in ch.support(1e-3)][:8], t=time.time() - t)
    if coop:
        v, qtop = max(coop)
        from cert_limN import top_exits
        e = top_exits(ch, prov, key_of[qtop])
        out.update(top_coop=names[qtop], pi_top=v, top_exit=e['top_exit'], top_exit_strict=e['top_exit_strict'],
                   top_exit_neutral=e['top_exit_neutral'], top_dest=e['top_dest'][:3])
    return out


BUDGETS_B = None


def _chosen(meta_vals):
    """6 budgets spanning K's minimal lengths: the budgets at which the n = 6 play table changes, thinned to 6."""
    keys = sorted(int(k[1:]) for k in meta_vals)
    brk = [b for b in keys[1:] if (meta_vals['b%d' % b] != meta_vals['b%d' % (b - 1)]).any()]
    return keys, brk


def karm_chain(a):
    vals = dict(np.load(KVALS))
    keys, brk = _chosen(vals)
    B = a.budgets
    L, vf = _free6()
    jobs = []
    for N in (1000, 10000, 30000):
        jobs.append(('free', vf, N))
        for b in B:
            jobs.append(('K b=%d' % b, vals['b%d' % b], N))
            jobs.append(('control b=%d' % b, matched_control(vals['b%d' % b], vf), N))
    t = time.time()
    with Pool(a.workers) as pool:
        rows = pool.map(_chain_cell, jobs, chunksize=1)
    static = {}
    for b in keys:
        v = vals['b%d' % b]
        lt = leak_test(v)
        static[b] = dict(diff_vs_free=int((v != vf).sum()), coop=int(v.sum()), n_closed=lt['n_closed'],
                         closed=[[L.rep[i] for i in c] for c in lt['closed_components']], n_selfcoop=lt['n_selfcoop'],
                         n_components=lt['n_components'])
    static['free'] = dict(diff_vs_free=0, coop=int(vf.sum()), **{k: v for k, v in leak_test(vf).items() if k != 'closed_components'})
    json.dump(dict(rows=rows, static=static, breakpoints=brk, budgets=B, wall_s=time.time() - t),
              open(os.path.join(RUNS, 'proof-length-karm-chain.json'), 'w'), indent=1, default=str)
    for r in sorted(rows, key=lambda r: (r['N'], r['label'])):
        print('%-14s N=%-6d P(C,C) %.4f pi(D) %.3f pi(C) %.3f top %s %.3f exit %.2e (strict %.2e) dest %s' % (
            r['label'], r['N'], r['pcc'], r['pi_D'], r['pi_C'], r.get('top_coop'), r.get('pi_top', 0), r.get('top_exit', 0), r.get('top_exit_strict', 0), r.get('top_dest')))
    print('breakpoints', brk)
    for b, s in static.items(): print(b, s)


def _lottery_job(j):
    import almost_all_seeds as AS
    label, val, N, I, rep = j
    import modal as M
    prov = _arm_prov(val)
    L = M.ModalLanguage(6)
    names = list(prov.names)
    U = np.ascontiguousarray(prov.Ufull, dtype=float); PCC = np.ascontiguousarray(prov.PCC, dtype=float)
    K = len(names)
    cls = np.zeros(len(L.funcs), np.int64)
    for k, mem in enumerate(prov.members):
        for c in mem: cls[c] = k
    iC = names.index('C')
    coop = [k for k in range(K) if PCC[k, k] >= 0.95 and k != iC]
    mu = L.mu_canon / L.mu_canon.sum()
    rng = np.random.default_rng([N, I, 10, rep, 2026104])        # same seeding as src/bounded_lottery.py: paired
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
    return dict(label=label, N=N, I=I, rep=rep, status=AS.STATUS[st], stop_gen=int(sg), pcc=cc, pay=pay,
                outcome=AS.outcome(cc, pay) if st in (1, 2, 3) else ('unresolved' if st == 4 else None),
                final={names[k]: int(v) for k, v in enumerate(glob) if v > 0}, t=time.time() - t)


def karm_lottery(a):
    import almost_all_seeds as AS
    vals = dict(np.load(KVALS))
    L, vf = _free6()
    arms = [('free', vf)] + [('K b=%d' % b, vals['b%d' % b]) for b in a.budgets]
    jobs = [(lab, v, N, I, rep) for lab, v in arms for N, I in ((100, 4), (100, 64)) for rep in range(20)]
    jobs.sort(key=lambda j: -j[3])
    t = time.time()
    with Pool(a.workers) as pool:
        rows = pool.map(_lottery_job, jobs, chunksize=1)
    summ = []
    for lab, _ in arms:
        for N, I in ((100, 4), (100, 64)):
            R = [r for r in rows if r['label'] == lab and r['N'] == N and r['I'] == I]
            res = [r for r in R if r['outcome'] not in ('unresolved', None)]
            k = sum(1 for r in res if r['outcome'] == 'efficient')
            lo, hi = AS.wilson(k, len(res))
            summ.append(dict(label=lab, N=N, I=I, n=len(res), efficient=k, frac=k / max(len(res), 1), wilson=[lo, hi],
                             unresolved=len(R) - len(res)))
            print('%-10s (%d, %d): efficient %d/%d = %.2f [%.2f, %.2f]' % (lab, N, I, k, len(res), k / max(len(res), 1), lo, hi), flush=True)
    json.dump(dict(rows=rows, summary=summ, wall_s=time.time() - t), open(os.path.join(RUNS, 'proof-length-karm-lottery.json'), 'w'), default=str)


# ------------------------------------------------------------------ Part B, run 3: per-program budgets with a price
KPAIRS = os.path.join(RUNS, 'proof-length-kpairs.npz')


def _kpair(j):
    """Plays of every L_6 class at budget bx against every class at budget by (and by against bx), by K."""
    import bounded_k as BK
    import modal as M
    bx, by = j
    L = M.ModalLanguage(6)
    t = time.time()
    K = BK.KTheory(cap=max(bx, by))
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


def kpairs(a):
    B = a.budgets
    jobs = [(bx, by) for i, bx in enumerate(B) for by in B[i:]]
    jobs.sort(key=lambda j: -(j[0] + j[1]))
    out = dict(np.load(KPAIRS)) if os.path.exists(KPAIRS) else {}
    jobs = [j for j in jobs if 'v%d_%d' % j not in out]
    sb = 0
    with Pool(a.workers) as pool:
        for bx, by, vxy, vyx, nchk, nbad, dt in pool.imap_unordered(_kpair, jobs):
            out['v%d_%d' % (bx, by)] = vxy; out['v%d_%d' % (by, bx)] = vyx; sb += nbad
            print('(%d, %d) sound bad %d / %d, %.0fs' % (bx, by, nbad, nchk, dt), flush=True)
            np.savez_compressed(KPAIRS, **out)
    print('soundness violations', sb)


def priced_val(B):
    """Genotypes: C, D unbudgeted; every non-constant class at each budget in B.  Returns val, base, gb."""
    import modal as M
    L = M.ModalLanguage(6); nat = L.arrays()[0]
    V = dict(np.load(KPAIRS))
    const = [c for c in range(len(nat)) if nat[c] == 0]
    nonc = [c for c in range(len(nat)) if nat[c] > 0]
    base = list(const) + [c for b in B for c in nonc]
    gb = [0] * len(const) + [b for b in B for c in nonc]
    G_ = len(base); val = np.zeros((G_, G_), np.int8)
    bref = B[0]
    for i in range(G_):
        for j in range(G_):
            bi = gb[i] if gb[i] else bref; bj = gb[j] if gb[j] else bref
            val[i, j] = V['v%d_%d' % (bi, bj)][base[i], base[j]]
    return val, np.array(base), np.array(gb), L


def _priced_cell(j):
    import modal as M
    from chain import Chain
    B, c, N = j
    val, base, gb, L = priced_val(B)
    U, PCC = M.pd_payoffs(val, M.PD)
    U = U.astype(float) - c * gb[:, None].astype(float)
    nb = len(B)
    nat = L.arrays()[0]
    mu = np.array([L.mu_canon[bc] / (1.0 if gb[g] == 0 else nb) for g, bc in enumerate(base)])
    names = [L.rep[bc] if gb[g] == 0 else '%s@%d' % (L.rep[bc], gb[g]) for g, bc in enumerate(base)]
    bits = np.array([L.bits_canon[bc] for bc in base])
    prov = M.ModalProvider(U, PCC, mu, names, bits)
    prov.sizes = np.ones(len(prov.names))
    lang = M.ClassLang(prov)
    t = time.time()
    ch = Chain(prov, N=N, w=0.3, verbose=False, eager_poly=False).explore()
    P = prov.PCC; nm = prov.names
    pcc = 0.0; pis = {}; poly = 0.0; key_of = {}
    for key, wgt in zip(ch.keys_list, ch.pi):
        ids, x, kd = ch.states[key]; ids = list(ids); x = np.asarray(x)
        pcc += wgt * float(x @ P[np.ix_(ids, ids)] @ x)
        if kd == 'mono':
            pis[ids[0]] = pis.get(ids[0], 0.0) + wgt; key_of[ids[0]] = key
        else:
            poly += wgt
    # pi by budget (class members may mix budgets: mu-weighted split) and by cooperation
    gid = {n_: g for g, n_ in enumerate(names)}
    byb = {}; coop_pi = 0.0
    for q, p in pis.items():
        mem = prov.members[q]
        w_ = np.array([mu[g] for g in mem]); w_ = w_ / w_.sum()
        for g, ww in zip(mem, w_):
            byb[str(int(gb[g]))] = byb.get(str(int(gb[g])), 0.0) + p * ww
        if P[q, q] == 1: coop_pi += p
    out = dict(B=list(B), c=c, N=N, pcc=pcc, pi_by_budget=byb, pi_selfcoop_mono=coop_pi, poly=poly,
               pi_D=pis.get(nm.index('D'), 0.0) if 'D' in nm else None, pi_C=pis.get(nm.index('C'), 0.0) if 'C' in nm else None,
               support=[(ch.describe_state(k, lang), float(p)) for k, p in ch.support(1e-3)][:8], cut_flow=ch.cut_flow,
               indeterminate=len(ch.indeterminate), t=time.time() - t)
    coop = [(v, q) for q, v in pis.items() if P[q, q] == 1 and nm[q] != 'C']
    if coop:
        from cert_limN import top_exits
        v, qtop = max(coop)
        e = top_exits(ch, prov, key_of[qtop])
        out.update(top_coop=nm[qtop], pi_top=v, top_exit=e['top_exit'], top_exit_strict=e['top_exit_strict'], top_dest=e['top_dest'][:3])
    return out


def priced(a):
    B = a.budgets
    jobs = [(B, c, 10000) for c in (0.0, 0.01, 0.1)]
    with Pool(a.workers) as pool:
        rows = pool.map(_priced_cell, jobs, chunksize=1)
    json.dump(rows, open(os.path.join(RUNS, 'proof-length-priced.json'), 'w'), indent=1, default=str)
    for r in rows:
        print('c=%g N=%d P(C,C) %.4f pi(D) %s pi(C) %s pi by budget %s top %s %.3f exit %s strict %s dest %s' % (
            r['c'], r['N'], r['pcc'], r['pi_D'], r['pi_C'], {k: round(v, 3) for k, v in r['pi_by_budget'].items()},
            r.get('top_coop'), r.get('pi_top', 0), r.get('top_exit'), r.get('top_exit_strict'), r.get('top_dest')))
        print('   support', r['support'][:5])


# ------------------------------------------------------------------ Part A report
def _proxy(n):
    import modal as M
    L = M.ModalLanguage(n)
    nat, ak, al, af, aa, tt = L.arrays()
    K = len(nat)
    val, w, last = M._evaluate_priced(nat, ak, al, af, aa, tt, np.zeros(K, np.int64), 200)
    v = nat[None, :].astype(float) * (1.0 + last.T.astype(float))     # v[x, y] = k(y) (1 + settle(y, x))
    return L, v


def _size(s):
    import conj4 as C4
    return C4.size(C4.parse(s))


def _depth(s):
    import conj4 as C4
    return G.nesting_depth(C4.parse(s))


def _lc(r):
    """Cost of cooperation: level-0 C proof if any, else level-1 (flagged)."""
    if r['C0']: return r['C0']['size'], r['C0']['loeb'], r['C0'].get('dag'), 0
    if r['C1']: return r['C1']['size'], r['C1']['loeb'], r['C1'].get('dag'), 1
    return None


def _lout(r):
    k = 'C0' if r['val'] == 1 else 'D0'
    if r[k]: return r[k]['size'], 0
    k = 'C1' if r['val'] == 1 else 'D1'
    if r[k]: return r[k]['size'], 1
    return None


def _ols(X, y):
    X = np.asarray(X, float); y = np.asarray(y, float)
    beta, res, rk, sv = np.linalg.lstsq(X, y, rcond=None)
    r = y - X @ beta; n, k = X.shape
    rss = float(r @ r); s2 = rss / max(n - k, 1)
    cov = s2 * np.linalg.inv(X.T @ X)
    se = np.sqrt(np.diag(cov))
    aic = n * np.log(rss / n) + 2 * k
    return dict(beta=beta.tolist(), se=se.tolist(), rss=rss, aic=float(aic), resid_sd=float(np.sqrt(rss / n)), n=n)


def reportA(a):
    from scipy.stats import spearmanr
    d = json.load(open(OUT_A))
    rows = d['rows']; sib = d['siblings']
    by = {}
    for r in rows: by.setdefault(r['tag'], []).append(r)
    out = dict(audit={}, cert={}, dist={}, proxy={}, scaling={}, family={}, siblings=[], ladder_self={})
    md = []
    # ---- audit and certification
    md += ['## Part A: GLS+Def on the free arm', '', '### Audit and certification', '',
           '| set | pairs | disagreements | provable roots | certified | neither at level 0 | neither at level 1 | search time per pair (mean / max s) |',
           '|---|---|---|---|---|---|---|---|']
    for tag in ('n6', 'n8_family', 'n8_sample', 'n8_uniform', 'n8_mce', 'ladder'):
        R = by[tag]
        prov = [r[k] for r in R for k in ROOTS if r[k]]
        cert = sum(1 for p in prov if p['certified'])
        n0 = sum(1 for r in R if not r['C0'] and not r['D0']); n1 = sum(1 for r in R if not r['C1'] and not r['D1'])
        bad = [(r['x'], r['y'], r['audit_bad']) for r in R if r['audit_bad']]
        ts = np.array([r['t'] for r in R])
        out['audit'][tag] = dict(pairs=len(R), disagreements=len(bad), bad=bad[:20], provable=len(prov), certified=cert,
                                 neither0=n0, neither1=n1, t_mean=float(ts.mean()), t_max=float(ts.max()))
        md.append('| %s | %d | %d | %d | %d (%.3f) | %d | %d | %.4f / %.2f |' % (tag, len(R), len(bad), len(prov), cert, cert / max(len(prov), 1), n0, n1, ts.mean(), ts.max()))
    md += ['', 'Audit: hc[0] ⇔ ⊢ P, hd[0] ⇔ P ⊢, hc[1] ⇔ ⊢ ¬□⊥ → P, hd[1] ⇔ ⊢ ¬□⊥ → ¬P against the evaluator\'s tables (n = 6, 8) '
           'or `src/conj4.py`\'s trace (ladder, siblings and fakers, levels ≤ 2). Certified = minimal size certified by iterative deepening.', '']
    # ---- distributions
    md += ['### Distributions of minimal sizes and Löb counts', '',
           '| set | root | n provable | size: min / median / mean / max | Λ: min / median / max | DAG/tree (mean) | height (mean) |', '|---|---|---|---|---|---|---|']
    for tag in ('n6', 'n8_sample', 'n8_uniform', 'n8_mce'):
        for k in ROOTS:
            P = [r[k] for r in by[tag] if r[k] and r[k]['certified']]
            if not P: continue
            s = np.array([p['size'] for p in P]); l = np.array([p['loeb'] for p in P])
            dg = np.array([p['dag'] / p['size'] for p in P]); h = np.array([p['height'] for p in P])
            out['dist']['%s_%s' % (tag, k)] = dict(n=len(P), size=[int(s.min()), float(np.median(s)), float(s.mean()), int(s.max())],
                                                    loeb=[int(l.min()), float(np.median(l)), int(l.max())], dag_ratio=float(dg.mean()),
                                                    hist_size=np.bincount(s).tolist(), hist_loeb=np.bincount(l).tolist())
            md.append('| %s | %s | %d | %d / %g / %.1f / %d | %d / %g / %d | %.3f | %.1f |' % (tag, k, len(P), s.min(), np.median(s), s.mean(), s.max(), l.min(), np.median(l), l.max(), dg.mean(), h.mean()))
    # ---- family table
    md += ['', '### Cost table: the prover family, the ladder, fakers', '',
           '| program | |x| | depth | L_C (self) | Λ | L_C¹ (self) | Λ¹ | L_read(x→x) | vs D: L_D¹ | vs ALLC: L_out |', '|---|---|---|---|---|---|---|---|---|---|']
    lad = {(r['x'], r['y']): r for r in by['ladder']}
    for x in LADDER + sorted(set(v['z'] for v in sib.values())):
        r = lad.get((x, x))
        if r is None: continue
        rD = lad.get((x, 'D')); rC = lad.get((x, 'C'))
        f = lambda p: '%d' % p['size'] if p else '∞'
        g = lambda p: '%d' % p['loeb'] if p else '—'
        loC = _lout(rC) if rC else None
        out['family'][x] = dict(size=_size(x), depth=_depth(x), C0=r['C0'], C1=r['C1'], L_read=r['L_read'], D1_vs_D=rD and rD['D1'], out_vs_C=loC)
        md.append('| `%s` | %d | %d | %s | %s | %s | %s | %d | %s | %s |' % (x, _size(x), _depth(x), f(r['C0']), g(r['C0']), f(r['C1']), g(r['C1']), r['L_read'],
                                                                     f(rD['D1']) if rD else '?', ('%d (lvl %d)' % loC) if loC else '∞'))
    # ---- siblings
    md += ['', '### Siblings: L(x → sibling) / L(x → x)', '',
           'y = or(x, ψ_K) (`src/conj4.py`). L_read sums the minimal sizes of x\'s true atoms against the opponent; L_out is the minimal size of x\'s actual outcome (level 0, else level 1).', '',
           '| x | K | L_read(x→x) | L_read(x→y) | ratio | diff | L_out(x→x) | L_out(x→y) | ratio | y cooperates with x (L_out(y→x)) |', '|---|---|---|---|---|---|---|---|---|---|']
    for x in LADDER:
        y = sib[x]['y']
        rxx, rxy, ryx = lad[(x, x)], lad[(x, y)], lad[(y, x)]
        if rxx['val'] != 1:
            continue
        a1, a2 = rxx['L_read'], rxy['L_read']
        o1, o2, o3 = _lout(rxx), _lout(rxy), _lout(ryx)
        row = dict(x=x, K=sib[x]['K'], read_self=a1, read_sib=a2, read_ratio=a2 / a1 if a1 else None, read_diff=a2 - a1,
                   out_self=o1, out_sib=o2, out_ratio=(o2[0] / o1[0]) if (o1 and o2) else None, y_to_x=o3, val_xy=rxy['val'], val_yx=ryx['val'])
        out['siblings'].append(row)
        md.append('| `%s` | %d | %d | %d | %s | %d | %s | %s | %s | %s |' % (x, sib[x]['K'], a1, a2, '%.2f' % (a2 / a1) if a1 else '—', a2 - a1,
                                                                    o1 and '%d (lvl %d)' % o1, o2 and '%d (lvl %d)' % o2,
                                                                    '%.2f' % (o2[0] / o1[0]) if (o1 and o2) else '—', o3 and '%d (lvl %d)' % o3))
    # ---- proxy comparison
    md += ['', '### Comparison with the stabilization proxy v(x, y) = k(y)·(1 + settle(y, x))', '',
           '| n | pairs with v > 0 | Spearman(v, L_read) | Spearman(v, L_out) over finite (n) | Spearman(v, L_read) among pairs with true atoms |', '|---|---|---|---|---|']
    for n, tags in ((6, ('n6',)), ('8s', ('n8_sample',)), ('8u', ('n8_uniform',)), (8, ('n8_family', 'n8_sample', 'n8_uniform', 'n8_mce'))):
        L, v = _proxy(6 if n == 6 else 8)
        idx = {s: i for i, s in enumerate(L.rep)}
        R = list({(r['x'], r['y']): r for t in tags for r in by[t]}.values())
        vv, lr, vo, lo, vt, lt = [], [], [], [], [], []
        for r in R:
            val_v = v[idx[r['x']], idx[r['y']]]
            if val_v <= 0: continue
            vv.append(val_v); lr.append(r['L_read'])
            if r['L_read'] > 0: vt.append(val_v); lt.append(r['L_read'])
            o = _lout(r)
            if o: vo.append(val_v); lo.append(o[0])
        s1 = spearmanr(vv, lr).correlation; s2 = spearmanr(vo, lo).correlation if len(vo) > 2 else float('nan')
        s3 = spearmanr(vt, lt).correlation if len(vt) > 2 else float('nan')
        out['proxy'][str(n)] = dict(n=len(vv), spearman_read=float(s1), spearman_out=float(s2), n_out=len(vo), spearman_read_true=float(s3), n_true=len(vt))
        md.append('| %s | %d | %.3f | %.3f (%d) | %.3f (%d) |' % ({6: '6', '8s': '8, mu-sample', '8u': '8, uniform sample', 8: '8, all sets (union)'}[n], len(vv), s1, s2, len(vo), s3, len(vt)))
        # largest disagreements (rank difference), n = 8
        if n == 8:
            from scipy.stats import rankdata
            rv = rankdata(vt) / len(vt); rl = rankdata(lt) / len(lt)
            Rt = [r for r in R if v[idx[r['x']], idx[r['y']]] > 0 and r['L_read'] > 0]
            dif = sorted(range(len(Rt)), key=lambda i: -abs(rv[i] - rl[i]))
            seen = set(); top = []
            for i in dif:
                key = (Rt[i]['x'], Rt[i]['y'])
                if key in seen: continue
                seen.add(key); top.append(dict(x=key[0], y=key[1], v=float(vt[i]), L_read=lt[i], rank_v=float(rv[i]), rank_L=float(rl[i])))
                if len(top) >= 8: break
            out['proxy']['top_disagreements'] = top
    md += ['', 'Largest rank disagreements at n = 8 (pairs with v > 0 and at least one true atom):', '',
           '| x | y | v | L_read | rank v | rank L |', '|---|---|---|---|---|---|']
    for t in out['proxy']['top_disagreements']:
        md.append('| `%s` | `%s` | %g | %d | %.2f | %.2f |' % (t['x'], t['y'], t['v'], t['L_read'], t['rank_v'], t['rank_L']))
    # ---- scaling among mutually cooperating establisher pairs
    md += ['', '### The cost of cooperation among mutually cooperating establisher pairs', '']
    for tag, n in (('n8_mce', 8), ('n6', 6)):
        R = by[tag]
        if tag == 'n6':
            import modal as M
            L6 = M.ModalLanguage(6); val6, _ = M.evaluate(L6); i6 = {s: i for i, s in enumerate(L6.rep)}; iD = i6['D']
            est = {s for s, i in i6.items() if val6[i, i] == 1 and val6[i, iD] == 0}
            R = [r for r in R if r['x'] in est and r['y'] in est and val6[i6[r['x']], i6[r['y']]] == 1 and val6[i6[r['y']], i6[r['x']]] == 1]
        pts = []
        for r in R:
            c = _lc(r)
            if c is None: continue
            pts.append((_size(r['x']) + _size(r['y']), max(_depth(r['x']), _depth(r['y'])), c[0], c[1], c[2], c[3], r['x'], r['y']))
        nn = np.array([p[0] for p in pts], float); dp = np.array([p[1] for p in pts]); Lc = np.array([p[2] for p in pts], float)
        lam = np.array([p[3] for p in pts]); dag = np.array([p[4] for p in pts], float); lev = np.array([p[5] for p in pts])
        lin = _ols(np.c_[np.ones_like(nn), nn], Lc); quad = _ols(np.c_[np.ones_like(nn), nn, nn ** 2], Lc)
        q, qse = quad['beta'][2], quad['se'][2]
        sp = spearmanr(nn, Lc).correlation; spd = spearmanr(dp, Lc).correlation
        viol1 = int((lam > dp + 1).sum()); viol3 = int((lam >= dp + 3).sum())
        fb = [p for p in pts if p[6] == FB and p[7] == FB]
        # residual structure: mean residual by (x-type) level and depth
        res = Lc - np.c_[np.ones_like(nn), nn] @ np.array(lin['beta'])
        by_lev = {int(k): float(res[lev == k].mean()) for k in np.unique(lev)}
        by_dep = {int(k): dict(n=int((dp == k).sum()), mean_L=float(Lc[dp == k].mean()), mean_lam=float(lam[dp == k].mean()), max_lam=int(lam[dp == k].max()))
                  for k in np.unique(dp)}
        out['scaling'][tag] = dict(n=len(pts), level1_share=float((lev == 1).mean()), linear=lin, quadratic=quad,
                                   quad_ci=[q - 1.96 * qse, q + 1.96 * qse], aic_prefers_quad=bool(quad['aic'] < lin['aic']),
                                   resid_sd_over_mean=lin['resid_sd'] / float(Lc.mean()), spearman_size=float(sp), spearman_depth=float(spd),
                                   lam_gt_depth1=viol1, lam_ge_depth3=viol3, max_lam_minus_depth=int((lam - dp).max()),
                                   fb_fb=fb[0][2:4] if fb else None, dag_over_tree=float((dag / Lc).mean()),
                                   resid_by_level=by_lev, by_depth=by_dep,
                                   worst=[dict(x=p[6], y=p[7], L=p[2], lam=p[3], depth=p[1]) for p in sorted(pts, key=lambda p: -(p[3] - p[1]))[:5]])
        S = out['scaling'][tag]
        md += ['**%s** (%d ordered pairs with a C proof; %.2f need level 1):' % (tag, len(pts), S['level1_share']), '',
               '- linear: L_C = %.2f + %.2f·(|x|+|y|) (se %.2f), residual sd / mean = %.2f; Spearman(L_C, |x|+|y|) = %.3f, Spearman(L_C, depth) = %.3f' % (
                   lin['beta'][0], lin['beta'][1], lin['se'][1], S['resid_sd_over_mean'], sp, spd),
               '- quadratic term %.3f, 95%% CI [%.3f, %.3f]; AIC linear %.1f, quadratic %.1f (%s)' % (q, S['quad_ci'][0], S['quad_ci'][1], lin['aic'], quad['aic'],
                                                                                          'prefers quadratic' if S['aic_prefers_quad'] else 'prefers linear'),
               '- Λ > depth + 1 in %d pairs; Λ ≥ depth + 3 in %d pairs; max Λ − depth = %d; FairBot–FairBot (L, Λ) = %s' % (viol1, viol3, S['max_lam_minus_depth'], S['fb_fb']),
               '- DAG/tree size ratio of the minimal derivations: %.3f; mean residual by level: %s' % (S['dag_over_tree'], by_lev),
               '- by nesting depth: %s' % ', '.join('d=%d: n %d, mean L %.1f, mean Λ %.2f, max Λ %d' % (k, v_['n'], v_['mean_L'], v_['mean_lam'], v_['max_lam']) for k, v_ in by_dep.items()),
               '']
    json.dump(out, open(os.path.join(RUNS, 'proof-length-partA-summary.json'), 'w'), indent=1, default=str)
    open(os.path.join(RUNS, 'proof-length-partA.md'), 'w').write('\n'.join(md) + '\n')
    print('\n'.join(md))


# ------------------------------------------------------------------ final report
def report(a):
    J = lambda f: json.load(open(os.path.join(RUNS, f))) if os.path.exists(os.path.join(RUNS, f)) else None
    A = J('proof-length-partA-summary.json'); grid_ = J('proof-length-grid.json'); kc = J('proof-length-karm-chain.json')
    kl = J('proof-length-karm-lottery.json'); kp = J('proof-length-priced.json'); km = J('proof-length-karm-meta.json')
    md = ['# Proof length: GLS+Def on the free arm, and the bounded calculus K', '',
          'Spec `specs/2026-10-05-proof-length.md`; predictions `predictions/2026-10-05-proof-length.md`; calculi, soundness and hand-checked '
          'derivations in `notes/proof-length.md`. Raw rows: `runs/proof-length-partA.json`, `runs/proof-length-grid.json`, '
          '`runs/proof-length-karm-*.json`, `runs/proof-length-priced.json`.', '']
    md += open(os.path.join(RUNS, 'proof-length-partA.md')).read().split('\n')
    md += ['## Part B: the bounded calculus K', '', '### Run 1: budget grid, b ∈ {2..40}²', '',
           '| pair | (C, D) cells | copy threshold (b_x = b_y) | distinct-budget rule | soundness violations / checked |', '|---|---|---|---|---|']
    rows = grid_['rows']; out = dict(partA=A, grid={})
    for px, py in ((FB, FB), ('BOX1(THEM(ME))', 'BOX1(THEM(ME))'), (FB, 'BOX1(THEM(ME))')):
        R = [r for r in rows if r['px'] == px and r['py'] == py]
        asym = sum(1 for r in R if r['xy'] != r['yx'])
        diag = min([r['bx'] for r in R if r['bx'] == r['by'] and r['xy'] and r['yx']] or [None])
        coop = [(r['bx'], r['by']) for r in R if r['bx'] != r['by'] and r['xy'] and r['yx']]
        mx = min(b for b, _ in coop); my = min(b for _, b in coop)
        rect = all((r['xy'] and r['yx']) == (r['bx'] >= mx and r['by'] >= my) for r in R if r['bx'] != r['by'])
        rule = ('min(b_x, b_y) ≥ %d' % mx) if (mx == my and rect) else ('b_x ≥ %d and b_y ≥ %d' % (mx, my) if rect else 'irregular')
        sb = sum(r['sound_bad'] for r in R); sc = sum(r['sound_checked'] for r in R)
        out['grid']['%s|%s' % (px, py)] = dict(asym=asym, copy_threshold=diag, rule=rule, sound_bad=sb, sound_checked=sc)
        md.append('| `%s` vs `%s` | %d | %s | %s | %d / %d |' % (px, py, asym, diag if px == py else '—', rule, sb, sc))
    md += ['', 'Payoffs per cell follow from the play (PD: both C → 0 each, both D → −1 each); no cell is (C, D), so no budget is exploited.', '']
    md += ['### Run 2: the n = 6 arm, every class at a global budget b (ε → 0 chain, w = 0.3; ε = 0 lottery)', '',
           'K soundness: %d violations in %d checked K-derived formulas over b = 1..40. Plays differing from the free arm by b: %s.' % (
               sum(m['sound_bad'] for m in km), sum(m['sound_checked'] for m in km),
               ', '.join('%s: %d' % (b, kc['static'][str(b)]['diff_vs_free']) for b in (1, 2, 3, 4, 6, 10, 16, 40))), '',
           '| arm | P(C,C) N = 10³ | 10⁴ | 3·10⁴ | π(all-D) at 3·10⁴ | top cooperative state (π) | its exit rate 10³ / 10⁴ / 3·10⁴ (strict share) | indeterminate | cut flow |', '|---|---|---|---|---|---|---|---|---|']
    labs = ['free'] + ['K b=%d' % b for b in kc['budgets']] + ['control b=%d' % b for b in kc['budgets']]
    out['chain'] = {}
    for l in labs:
        R = {r['N']: r for r in kc['rows'] if r['label'] == l}
        r3 = R[30000]
        out['chain'][l] = {str(N): dict(pcc=R[N]['pcc'], pi_D=R[N]['pi_D'], top=R[N].get('top_coop'), pi_top=R[N].get('pi_top'), exit=R[N].get('top_exit'),
                                        strict=R[N].get('top_exit_strict'), support=R[N]['support']) for N in R}
        md.append('| %s | %.4f | %.4f | %.4f | %.3f | `%s` (%.3f) | %s (%s) | %d | %.1e |' % (
            l, R[1000]['pcc'], R[10000]['pcc'], r3['pcc'], r3['pi_D'], r3.get('top_coop'), r3.get('pi_top', 0),
            ' / '.join('%.1e' % R[N].get('top_exit', 0) for N in (1000, 10000, 30000)),
            '%.2f' % (r3.get('top_exit_strict', 0) / r3['top_exit']) if r3.get('top_exit') else '—', r3['indeterminate'], r3['cut_flow']))
    md += ['', 'Support at N = 3·10⁴ (π ≥ 10⁻³): ' + '; '.join('%s: %s' % (l, ', '.join('%s %.3f' % (s, p) for s, p in out['chain'][l]['30000']['support'][:5]))
                                                             for l in ('free', 'K b=3', 'K b=6', 'K b=16')), '',
           'Control = the free table with plays flipped at random, matched to the K arm stratum by stratum (opponent class × free play × reader has boxes).', '',
           'Leak test (drift-closed components among self-cooperators, n = 6): ' + ', '.join('b=%s: %d' % (b, kc['static'][str(b)]['n_closed']) for b in range(1, 41)) + '; free: %d.' % kc['static']['free']['n_closed'], '']
    if kl:
        md += ['ε = 0 lottery, n = 6, mN = 1, 20 paired seeds per cell (seeding as `src/bounded_lottery.py`), efficient fraction with Wilson 95%:', '',
               '| arm | (N, I) = (100, 4) | (100, 64) |', '|---|---|---|']
        out['lottery'] = kl['summary']
        for l in ['free'] + ['K b=%d' % b for b in kc['budgets']]:
            S = {(s['N'], s['I']): s for s in kl['summary'] if s['label'] == l}
            md.append('| %s | %s |' % (l, ' | '.join('%d/%d = %.2f [%.2f, %.2f]%s' % (S[c]['efficient'], S[c]['n'], S[c]['frac'], S[c]['wilson'][0], S[c]['wilson'][1],
                                                                                   (' (%d unresolved)' % S[c]['unresolved']) if S[c]['unresolved'] else '') for c in ((100, 4), (100, 64)))))
        md.append('')
    if kp:
        md += ['### Run 3: per-program budgets with a price c·b per match (budgets {%s}, μ split equally across budgets, N = 10⁴)' % ', '.join(map(str, kp[0]['B'])), '',
               '| c | P(C,C) | π(all-D) | π(all-ALLC) | π by budget (0 = constants) | π on self-cooperating monomorphic states | top cooperative state (π) | its exit (strict) | top destinations |', '|---|---|---|---|---|---|---|---|---|']
        out['priced'] = kp
        for r in kp:
            md.append('| %g | %.4f | %.3f | %.3f | %s | %.3f | `%s` (%.3f) | %s (%s) | %s |' % (
                r['c'], r['pcc'], r['pi_D'] or 0, r['pi_C'] or 0, ', '.join('%s: %.3f' % (k, v) for k, v in sorted(r['pi_by_budget'].items(), key=lambda kv: int(kv[0]))),
                r['pi_selfcoop_mono'], r.get('top_coop'), r.get('pi_top', 0), '%.1e' % r['top_exit'] if r.get('top_exit') else '—',
                '%.1e' % r['top_exit_strict'] if r.get('top_exit') else '—', '; '.join('%s %s %.1e' % tuple(t) for t in (r.get('top_dest') or []))))
        md.append('')
    open(os.path.join(RUNS, 'proof-length.md'), 'w').write('\n'.join(md) + '\n')
    json.dump(out, open(os.path.join(RUNS, 'proof-length.json'), 'w'), indent=1, default=str)
    print('\n'.join(md[-60:]))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd')
    ap.add_argument('--workers', type=int, default=3)
    ap.add_argument('--budgets', type=int, nargs='+', default=[])
    a = ap.parse_args()
    {'partA': partA, 'partA_uniform': partA_uniform, 'reportA': reportA, 'grid': grid, 'karm_vals': karm_vals,
     'karm_chain': karm_chain, 'karm_lottery': karm_lottery, 'kpairs': kpairs, 'priced': priced, 'report': report}[a.cmd](a)
