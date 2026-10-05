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


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd')
    ap.add_argument('--workers', type=int, default=3)
    a = ap.parse_args()
    {'partA': partA, 'partA_uniform': partA_uniform, 'reportA': reportA}[a.cmd](a)
