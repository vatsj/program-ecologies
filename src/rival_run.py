"""Rival cooperative networks under spatial structure: lazy-priced modal arm, n = 8, PD, w = 0.3.
Predictions: predictions/2026-10-01-rival-networks.md.

    python3 src/rival_run.py rates      # R1 + R2: per-mutant hitting/fixation probabilities on graphs (ε-free)
    python3 src/rival_run.py domain     # R3: FB vs P* half split, no mutation (ε-free)
    python3 src/rival_run.py wmchain    # well-mixed full ε→0 chain at the graph sizes (reference)
    python3 src/rival_run.py abm        # R4: finite-ε agent-based runs (approach rates only)
    python3 src/rival_run.py report     # runs/rival_networks.md / .json

At most 3 worker processes (shared machine).
"""
import json, os, sys, time
import numpy as np
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(__file__))
from graph_rates import torus, hypercube
from graph_rates_run import wilson
from rival_kernels import _invade_fix, _domain, _abm
import rival_static as RS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = 0.3
CS = (0.0, 0.01, 0.1)
GRAPHS = [('torus', 16), ('torus', 32), ('torus', 64), ('hypercube', 6), ('hypercube', 8), ('hypercube', 10)]
WORKERS = 3
OUT = lambda f: os.path.join(ROOT, 'runs', f)
REQUIRED = [('P*|FB', 'P*-net', 'FB-net'), ('FB|P*', 'FB-net', 'P*-net'), ('ALLC|FB', 'exploitable', 'FB-net'),
            ('ALLC|P*', 'exploitable', 'P*-net'), ('D|FB', 'D-type', 'FB-net'), ('D|P*', 'D-type', 'P*-net'),
            ('FB|D', 'FB-net', 'D-type'), ('P*|D', 'P*-net', 'D-type'), ('D|ALLC', 'D-type', 'exploitable')]


def graph(kind, size):
    return torus(size) if kind == 'torus' else hypercube(size)


_CACHE = {}


def setup(c):
    if c not in _CACHE:
        prov = RS.load(c); nw = RS.networks(prov); reps = RS.reps_for(prov, nw)
        _CACHE[c] = (prov, nw, reps)
    return _CACHE[c]


def bkey(U, q, r):
    """Block (u_qq, u_qr, u_rq, u_rr), rounded."""
    return tuple(float(x) for x in np.round([U[q, q], U[q, r], U[r, q], U[r, r]], 9))


# ------------------------------------------------------------------------------------ R1 + R2
def block_jobs():
    """Every distinct 2x2 block between a resident of the partially lumped chain and any class,
    every c.  Tier 0: the requested pairs and P*'s shadow; tier 1: primary representatives;
    tier 2: the other residents of the expanded set."""
    tier = {}
    def add(b, t):
        tier[b] = min(t, tier.get(b, 9))
    for c in CS:
        prov, nw, reps = setup(c); U = prov.Ufull
        for name, ml, rl in REQUIRED:
            add(bkey(U, reps[ml], reps[rl]), 0)
        add(bkey(U, prov.names.index('not(BOX(THEM(ME)))'), reps['P*-net']), 0)
        for rl, r in reps.items():
            for q in range(len(nw['mu'])):
                if q != r: add(bkey(U, q, r), 1)
        for r in RS.expanded_residents(prov, nw):
            for q in range(len(nw['mu'])):
                if q != r: add(bkey(U, q, r), 2)
    J = []
    for kind, size in GRAPHS:
        N = size * size if kind == 'torus' else 1 << size
        for b, t in tier.items():
            if t == 2 and N > 1024:          # the expanded set is not run at torus side 64 (cost)
                continue
            J.append((kind, size, b, t == 0, t, N))
    J.sort(key=lambda j: (j[4], -j[5]))
    return [j[:5] for j in J]


def rate_job(j):
    kind, size, b, required, tier = j
    nb = graph(kind, size); N = nb.shape[0]
    qq, qr, rq, rr = b
    t0 = time.time()
    neutral = max(abs(qq - rr), abs(qr - rr), abs(rq - rr)) < 1e-12
    out = dict(graph=kind, size=size, N=N, block=b, required=required, tier=tier, neutral=neutral)
    if neutral and not (required and N <= 256):
        out.update(analytic=True, half=0, lost=0, und=0, trials=0, fx=0, la=0, ua=0,
                   rho_half=2.0 / N, lo=2.0 / N, hi=2.0 / N, pfix=0.5, time_s=0.0)
        return out
    U2 = np.array([[rr, rq], [qr, qq]], float)
    if tier == 0:
        target, tcap, tmax = 20, (400 if N <= 1024 else 1200), 100000
    else:                                   # 2*10^4 trials bound a zero block below 2e-4 (< 2/N at N = 4,096)
        target, tcap, tmax = 10, (200 if N <= 1024 else 300), 20000
    cap = max(500, 2 * N); cont = 4 * N
    h = l = u = fx = la = ua = 0; tr = 0; batch = 0
    while True:
        r = _invade_fix(U2, nb, W, 2000, cap, cont, max(0, target - (fx + la + ua)), 1000 + 7919 * batch + 31 * size)
        h += r[0]; l += r[1]; u += r[2]; fx += r[3]; la += r[4]; ua += r[5]; tr += 2000; batch += 1
        if h >= target or tr >= tmax or time.time() - t0 > tcap:
            break
    dec = h + l
    lo, hi = wilson(h, dec)
    dd = fx + la
    out.update(analytic=False, half=h, lost=l, und=u, trials=tr, fx=fx, la=la, ua=ua,
               rho_half=h / dec if dec else float('nan'), lo=lo, hi=hi,
               pfix=(fx / dd) if dd else float('nan'), time_s=time.time() - t0)
    return out


def run_rates():
    J = block_jobs()
    path = OUT('rival_rates.json')
    done = {}
    if os.path.exists(path):
        for r in json.load(open(path)):
            done[(r['graph'], r['size'], tuple(r['block']))] = r
    J = [j for j in J if (j[0], j[1], j[2]) not in done]
    rows = list(done.values())
    print('%d block jobs to run (%d cached)' % (len(J), len(rows)), flush=True)
    with Pool(WORKERS) as pool:
        for r in pool.imap_unordered(rate_job, J):
            rows.append(r)
            print('%s %d %s: half %d/%d rho %.3e [%.1e, %.1e] pfix %s (%.0fs)%s' % (
                r['graph'], r['size'], r['block'], r['half'], r['trials'], r['rho_half'], r['lo'], r['hi'],
                '%.2f' % r['pfix'] if r['pfix'] == r['pfix'] else '-', r['time_s'], ' analytic' if r['analytic'] else ''), flush=True)
            json.dump(rows, open(path, 'w'), indent=0)


# ------------------------------------------------------------------------------------ R3
def split_init(kind, size):
    """1 = FB on half the graph: rows y < side/2 (torus), top bit 0 (hypercube)."""
    if kind == 'torus':
        N = size * size; init = np.zeros(N, np.int64)
        for s in range(N):
            if s // size < size // 2: init[s] = 1
    else:
        N = 1 << size; init = np.array([1 if not (s >> (size - 1)) & 1 else 0 for s in range(N)], np.int64)
    return init


DOMAIN_REPS = {('torus', 16): 400, ('torus', 32): 200, ('torus', 64): 60, ('hypercube', 6): 400, ('hypercube', 8): 200, ('hypercube', 10): 100}


def disc_init(size, inside):
    """Torus: 1 on a disc of radius side/4 (the disc type), 0 elsewhere."""
    N = size * size; init = np.zeros(N, np.int64); c0 = size / 2.0
    for s in range(N):
        x, y = s % size, s // size
        if (x + 0.5 - c0) ** 2 + (y + 0.5 - c0) ** 2 <= (size / 4.0) ** 2: init[s] = 1
    return init


def domain_job(j):
    """start 'band': type 1 = FB on half the graph, first passage at 3N/4 (FB) or N/4 (P*).
    start 'disc-PS' / 'disc-FB': type 1 = the disc type (P* or FB) on a disc of radius side/4
    in a sea of the other; first passage at N/2 (disc grows) or 0 (disc lost)."""
    c, kind, size, rep0, nrep, start = j
    prov, nw, reps = setup(c); U = prov.Ufull
    iF, iP = reps['FB-net'], reps['P*-net']
    a, b = (iP, iF) if start == 'disc-PS' else (iF, iP)                      # 1 = a, 0 = b
    U2 = np.array([[U[b, b], U[b, a]], [U[a, b], U[a, a]]], float)
    nb = graph(kind, size); N = nb.shape[0]
    side_like = size if kind == 'torus' else (1 << size) ** 0.5
    cap = int(max(5000, 15 * side_like ** 2)) if kind == 'torus' else 20000
    cont = cap
    every = max(1, int(side_like)) if kind == 'torus' else 5
    nrec = (cap + cont) // every + 2
    if start == 'band':
        init = split_init(kind, size); lo, hi = N // 4, 3 * N // 4
    else:
        init = disc_init(size, a); lo, hi = 0, N // 2
    res = []
    t0 = time.time()
    for k in range(rep0, rep0 + nrep):
        first, tf, fix, tfx, rc, rx = _domain(U2, nb, W, init, cap, cont, every, nrec, 50000 + 101 * k + size, lo, hi)
        n = int((rc >= 0).sum())
        if first != 0:                       # keep records up to first passage only
            n = min(n, int(tf // every) + 1)
        res.append(dict(first=int(first), t_first=tf, fix=int(fix), t_fix=tfx, cnt=rc[:n].tolist(), cross=rx[:n].tolist()))
    return dict(c=c, graph=kind, size=size, N=N, deg=nb.shape[1], start=start, init_count=int(init.sum()), every=every,
                cap=cap, cont=cont, runs=res, time_s=time.time() - t0)


def run_domain():
    J = []
    for kind, size in GRAPHS:
        R = DOMAIN_REPS[(kind, size)]; chunk = max(10, R // 10)
        for c in CS:
            for r0 in range(0, R, chunk):
                J.append((c, kind, size, r0, min(chunk, R - r0), 'band'))
    for size, R in ((32, 100), (64, 40)):
        for c in CS:
            for start in ('disc-PS', 'disc-FB'):
                for r0 in range(0, R, 10):
                    J.append((c, 'torus', size, r0, min(10, R - r0), start))
    J.sort(key=lambda j: -(j[2] ** 2 if j[1] == 'torus' else 1 << j[2]))
    rows = []
    with Pool(WORKERS) as pool:
        for r in pool.imap_unordered(domain_job, J):
            rows.append(r)
            ff = [x['first'] for x in r['runs']]
            print('domain %s c=%g %s %d: type-1 first %d, other first %d, undecided %d (%.0fs)' % (
                r['start'], r['c'], r['graph'], r['size'], ff.count(1), ff.count(-1), ff.count(0), r['time_s']), flush=True)
            json.dump(rows, open(OUT('rival_domain.json'), 'w'))


# ------------------------------------------------------------------------------------ R3b: controlled fronts
FRONT_X = (0.0, 0.01, 0.02, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4)


def front_job(j):
    from rival_kernels import _front
    c, kind, size, x, reps, gens = j
    prov, nw, r = setup(c); U = prov.Ufull
    ids = [r['P*-net'], r['FB-net'], r['exploitable']]                 # 0 = P*, 1 = FB, 2 = ALLC
    U3 = np.ascontiguousarray(U[np.ix_(ids, ids)])
    nb = graph(kind, size); N = nb.shape[0]
    sp = split_init(kind, size)                                        # 1 = FB half
    every = 50
    out = []; fronts = []
    t0 = time.time()
    for k in range(reps):
        rng = np.random.default_rng(900 + 37 * k + int(1000 * x) + size)
        init = np.where(sp == 1, np.where(rng.random(N) < x, 2, 1), 0).astype(np.int64)
        rec = _front(U3, nb, W, init, gens, every, 0, 7000 + 13 * k + size)
        out.append(rec[:, 0].tolist()); fronts.append(rec[:, 4:7].tolist())
    return dict(c=c, graph=kind, size=size, N=N, x=x, every=every, gens=gens, ps=out, front=fronts, time_s=time.time() - t0)


def run_front():
    J = []
    for kind, size, gens in (('torus', 64, 4000), ('hypercube', 10, 2000)):
        for c in CS:
            for x in FRONT_X:
                J.append((c, kind, size, x, 20, gens))
    rows = []
    with Pool(WORKERS) as pool:
        for r in pool.imap_unordered(front_job, J):
            rows.append(r)
            ps = np.array(r['ps'])
            print('front c=%g %s %d x=%.2f: P* share %.3f -> %.3f (%.0fs)' % (r['c'], r['graph'], r['size'], r['x'],
                  ps[:, 0].mean() / r['N'], ps[:, -1].mean() / r['N'], r['time_s']), flush=True)
            json.dump(rows, open(OUT('rival_front.json'), 'w'))


# ------------------------------------------------------------------------------------ well-mixed chain
def wm_job(j):
    from priced_limN import cell
    c, N = j
    r = cell(('wm', 8, c, 0, N, 'per', 'lazy'))
    return r


def run_wmchain():
    J = [(c, N) for c in CS for N in (256, 1024, 4096)]
    rows = []
    with Pool(WORKERS) as pool:
        for r in pool.imap_unordered(wm_job, J):
            rows.append(r)
            print('wm chain c=%g N=%d: P(C,C) %.4f support %s (%.0fs)' % (r['c'], r['N'], r['pcc'], r['support'][:4], r['time_s']), flush=True)
            json.dump(rows, open(OUT('rival_wmchain.json'), 'w'), indent=1, default=str)


# ------------------------------------------------------------------------------------ R4
LABS = ('D-type', 'FB-net', 'P*-net', 'exploitable', 'other-coop')


def abm_job(j):
    kind, size, c, eps, start, seed, gens, every = j
    prov, nw, reps = setup(c); U = np.ascontiguousarray(prov.Ufull); A = np.ascontiguousarray(prov.ACT)
    lab = np.array([LABS.index(l) for l in nw['lab']], np.int64)
    mu = nw['mu'].copy()
    if start.endswith('noALLC'):                 # control: the ALLC class is never supplied by mutation
        mu[reps['exploitable']] = 0.0
    if start.endswith('CDonly'):                 # control: mutation supplies only ALLC and D
        keep = np.zeros_like(mu); keep[reps['exploitable']] = mu[reps['exploitable']]; keep[reps['D-type']] = mu[reps['D-type']]
        mu = keep
    cdf = np.cumsum(mu) / mu.sum()
    nb = graph(kind, size); N = nb.shape[0]
    if start.startswith('allD'):
        init = np.full(N, reps['D-type'], np.int64)
    else:
        sp = split_init(kind, size)
        init = np.where(sp == 1, reps['FB-net'], reps['P*-net']).astype(np.int64)
    t0 = time.time()
    rec, grid = _abm(U, A, lab, len(LABS), cdf, nb, W, eps, gens, every, init, seed, reps['FB-net'], reps['P*-net'], reps['exploitable'])
    return dict(graph=kind, size=size, N=N, c=c, eps=eps, start=start, seed=seed, gens=gens, every=every,
                rec=rec.tolist(), time_s=time.time() - t0)


def abm_jobs(gens_t=200000, gens_h=100000):
    J = []
    for kind, size, gens, seeds in (('torus', 128, gens_t, (1, 2, 3, 4)), ('hypercube', 14, gens_h, (1, 2))):
        for c in (0.01, 0.0, 0.1):
            for start in ('allD', 'split'):
                for seed in seeds:
                    J.append((kind, size, c, 1e-3, start, seed, gens, 100))
        for start in ('allD', 'split'):
            J.append((kind, size, 0.1, 1e-4, start, 1, gens, 100))
        J.append((kind, size, 0.01, 1e-3, 'split-noALLC', 1, gens // 4, 100))      # control: no ALLC supply
    J.append(('torus', 128, 0.01, 1e-3, 'split-CDonly', 1, gens_t // 4, 100))       # control: only ALLC and D supplied
    for seed in (1, 2, 3):                                                          # small-system seeds
        J.append(('torus', 64, 0.01, 1e-3, 'split', seed, 50000, 100))
    return J


def run_abm():
    J = abm_jobs()
    J.sort(key=lambda j: (j[0] != 'hypercube', j[2] != 0.01))
    rows = []
    with Pool(WORKERS) as pool:
        for r in pool.imap_unordered(abm_job, J):
            rows.append(r)
            rec = np.array(r['rec']); h = len(rec) // 2
            print('abm %s %d c=%g eps=%g %s seed %d: P(C,C) 2nd half %.3f, FB-net %.3f P*-net %.3f ALLC %.3f, MD %.4f (rival border %.4f) (%.0fs)' % (
                r['graph'], r['size'], r['c'], r['eps'], r['start'], r['seed'], rec[h:, 1].mean(), rec[h:, 12].mean(), rec[h:, 13].mean(),
                rec[h:, 10].mean(), rec[h:, 2].mean(), rec[h:, 3].mean(), r['time_s']), flush=True)
            json.dump(rows, open(OUT('rival_abm.json'), 'w'))


# ------------------------------------------------------------------------------------ report
def _load(f):
    """runs/<f>, or runs/<f>.gz (the committed, rounded copy of the agent-based records)."""
    import gzip
    p = OUT(f)
    if os.path.exists(p):
        return json.load(open(p))
    if os.path.exists(p + '.gz'):
        return json.load(gzip.open(p + '.gz', 'rt'))
    return []


def rate_table():
    return {(r['graph'], r['size'], tuple(r['block'])): r for r in _load('rival_rates.json')}


def rho_fix(r, upper=False):
    """Fixation-probability estimate from a rate row: P(half) * P(fix | half).  With no half-successes,
    0; in the 'upper' variant, half the Wilson upper bound, but only for blocks with >= 10^4 trials
    (under-sampled zero blocks stay at 0, so they cannot set the band).  P(fix|half) from decided
    continuations, else 1/2."""
    if r is None:
        return float('nan')
    if r['analytic']:
        return 1.0 / r['N']
    if r['half'] == 0:
        return 0.5 * r['hi'] if (upper and r['trials'] >= 10000) else 0.0
    pf = r['pfix'] if r['pfix'] == r['pfix'] else 0.5
    return r['rho_half'] * pf


def lumped_graph(c, kind, size, T, upper=False, partial=False, prior_swap=False):
    """Lumped chain (five primary representatives) or, with partial=True, the partially lumped
    chain over the expanded resident set.  A block missing for a non-primary resident (tier 2 at
    torus side 64) is replaced by the same mutant's block against its label's primary
    representative.  prior_swap: P*-net members get prior mass scaled so that the label's total
    equals FB-net's (a control on the 4,300x prior).
    Returns (pi by label, rates by label pair, missing blocks, fallbacks, absorbing-in-sample states)."""
    prov, nw, reps = setup(c); U = prov.Ufull
    if prior_swap:
        nw = dict(nw); mu = nw['mu'].copy(); lab = nw['lab']
        ps = lab == 'P*-net'; fb = lab == 'FB-net'
        mu[ps] *= mu[fb].sum() / mu[ps].sum(); nw['mu'] = mu
    missing = set(); fall = set()
    def fn(q, r):
        b = bkey(U, q, r); row = T.get((kind, size, b))
        if row is None:
            rp = reps[nw['lab'][r]]
            if q != rp and r != rp:
                row = T.get((kind, size, bkey(U, q, rp)))
                if row is not None:
                    fall.add(b); return rho_fix(row, upper)
            missing.add(b); return 0.0
        return rho_fix(row, upper)
    if partial:
        by, per, Q, S = RS.partial_pi(prov, nw, fn)
        absorbing = [prov.names[S[i]] for i in range(len(S)) if Q[i].sum() == 0]
        R = {}
        for i, a in enumerate(S):
            for j, b in enumerate(S):
                if Q[i, j] > 0:
                    k = (nw['lab'][a], nw['lab'][b])
                    if k[0] != k[1]: R[k] = R.get(k, 0.0) + Q[i, j] * per[prov.names[a]] / max(1e-300, by[nw['lab'][a]])
        return by, R, len(missing), len(fall), absorbing
    R = RS.lumped_rates(prov, nw, fn, reps)
    absorbing = [l for l in RS.LABELS if sum(v for (a, b), v in R.items() if a == l) == 0]
    return RS.lumped_pi(R), R, len(missing), len(fall), absorbing


def report():
    T = rate_table()
    L = ['# Rival cooperative networks under spatial structure (lazy pricing, n = 8, PD, w = 0.3)', '',
         'Predictions: `predictions/2026-10-01-rival-networks.md`. R1–R3 are ε-free; R4 is finite ε (approach rates only).', '']
    summary = {}
    # ---- R1
    L += ['## R1: per-mutant rates on graphs (ε-free)', '',
          'ρ = P(single mutant reaches N/2) [95% Wilson]; P(fix|½) from up to 20 continued successes; well-mixed = Moran hitting N/2.', '',
          '| pair | c | graph | N | ρ (graph) | successes / trials | P(fix \\| ½) | ρ·N/2 | well-mixed ρ |', '|---|---|---|---|---|---|---|---|---|']
    pairs = REQUIRED + [('P*-shadow|P*', None, 'P*-net')]
    r1 = []
    for name, ml, rl in pairs:
        for c in CS:
            prov, nw, reps = setup(c); U = prov.Ufull
            q = reps[ml] if ml else prov.names.index('not(BOX(THEM(ME)))'); r = reps[rl]
            b = bkey(U, q, r)
            for kind, size in GRAPHS:
                row = T.get((kind, size, b))
                if row is None: continue
                N = row['N']; wmv = RS.wm(U, q, r, N, N // 2)
                pf = row['pfix']
                L.append('| %s | %g | %s %d | %d | %.3g [%.2g, %.2g]%s | %d / %d | %s | %.3g | %.2g |' % (
                    name, c, kind, size, N, row['rho_half'], row['lo'], row['hi'], ' (analytic)' if row['analytic'] else '',
                    row['half'], row['trials'], '%.2f (%d/%d)' % (pf, row['fx'], row['fx'] + row['la']) if pf == pf and not row['analytic'] else ('0.5' if row['analytic'] else '—'),
                    row['rho_half'] * N / 2, wmv))
                r1.append(dict(pair=name, c=c, graph=kind, size=size, N=N, rho=row['rho_half'], lo=row['lo'], hi=row['hi'],
                               half=row['half'], trials=row['trials'], pfix=pf, wm=wmv))
    summary['R1'] = r1
    # ---- R2
    wmc = {(r['c'], r['N']): r for r in _load('rival_wmchain.json')}
    L += ['', '## R2: lumped spatial chain over labels (ε→0, approximate)', '',
          'π over labels from Σ μ(q)·ρ_fix(q | representative); ρ_fix = P(half)·P(fix|half) on the graph. "upper" sets every zero-success block to half its Wilson upper bound.', '',
          '| c | graph | N | chain | π D-type | π FB-net | π P*-net | π exploitable | π other-coop | self-coop | self-coop (upper) | prior swap: π FB-net / π P*-net | missing / fallback blocks | absorbing in sample |', '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    r2 = []
    for c in CS:
        for kind, size in GRAPHS:
            N = size * size if kind == 'torus' else 1 << size
            for partial in (False, True):
                pi, R, miss, fall, absb = lumped_graph(c, kind, size, T, partial=partial)
                piu = lumped_graph(c, kind, size, T, upper=True, partial=partial)[0]
                pis = lumped_graph(c, kind, size, T, partial=partial, prior_swap=True)[0]
                sc = 1 - pi['D-type']; scu = 1 - piu['D-type']
                L.append('| %g | %s %d | %d | %s | %.4f | %.4f | %.4f | %.4f | %.4f | %.4f | %.4f | %.3f / %.3f | %d / %d | %s |' % (
                    c, kind, size, N, 'partial (16 residents)' if partial else 'lumped (5)', pi['D-type'], pi['FB-net'], pi['P*-net'],
                    pi['exploitable'], pi['other-coop'], sc, scu, pis['FB-net'], pis['P*-net'], miss, fall, ', '.join(absb) or '—'))
                r2.append(dict(c=c, graph=kind, size=size, N=N, chain='partial' if partial else 'lumped', pi=pi, pi_upper=piu, pi_prior_swap=pis,
                               missing=miss, fallback=fall, absorbing=absb, flux={'%s->%s' % k: v for k, v in R.items()}))
    L += ['', 'Transition structure (rate per mutation event out of each representative, by destination label):', '']
    for d in r2:
        fl = d['flux']
        parts = []
        for src in RS.LABELS:
            outs = sorted([(k.split('->')[1], v) for k, v in fl.items() if k.startswith(src + '->') and v > 0], key=lambda t: -t[1])
            parts.append('%s → %s' % (src, ', '.join('%s %.1e' % t for t in outs[:3])))
        L.append('- %s, c = %g, %s %d: %s' % (d['chain'], d['c'], d['graph'], d['size'], '; '.join(parts)))
    L += ['', 'Well-mixed reference: lumped chain vs full ε→0 chain (`wmchain`).', '',
          '| c | N | lumped self-coop | lumped FB-net / P*-net | full chain P(C,C) | full chain support |', '|---|---|---|---|---|---|']
    for c in CS:
        prov, nw, reps = setup(c); U = prov.Ufull
        for N in (256, 1024, 4096):
            pi = RS.lumped_pi(RS.lumped_rates(prov, nw, lambda q, r: RS.wm(U, q, r, N, N), reps))
            pp, _, _, _ = RS.partial_pi(prov, nw, lambda q, r: RS.wm(U, q, r, N, N))
            f = wmc.get((c, N))
            L.append('| %g | %d | %.4f (partial %.4f) | %.3f / %.3f (partial %.3f / %.3f) | %s | %s |' % (c, N, 1 - pi['D-type'], 1 - pp['D-type'],
                     pi['FB-net'], pi['P*-net'], pp['FB-net'], pp['P*-net'],
                     '%.4f' % f['pcc'] if f else '—', '; '.join('%s %.3f' % tuple(s) for s in f['support'][:4]) if f else '—'))
            summary.setdefault('wm', []).append(dict(c=c, N=N, lumped=pi, full=f['pcc'] if f else None))
    summary['R2'] = r2
    # ---- R3
    D = _load('rival_domain.json')
    L += ['', '## R3: domain competition FB vs P*, no mutation (ε-free)', '',
          'band: half split (torus: straight, two borders; hypercube: subcube); type 1 = FB; first passage at 3N/4 (FB) or N/4 (P*). '
          'disc-PS / disc-FB: a disc of radius side/4 of P* (FB) in a sea of the other; first passage at N/2 (disc grows) or 0 (disc lost). '
          'Velocity (Wald ratio): Σ(type-1 count change) / Σ(generations × mean type-1/type-0 edge count), over records before first passage, '
          'i.e. type-1 gain per cross edge per generation; first-order flat-border value for FB at c = 10⁻² is 9.2·10⁻⁴, at 10⁻¹ 9.1·10⁻³. '
          'Interface: fraction of undirected edges joining the two types (all mutual defection).', '',
          '| start | c | graph | N | runs | P(type 1 first) [95%] | other first | undecided | median t_first | P(fix agrees \\| first) | velocity per cross edge | interface at t=0 | mean interface before first passage |',
          '|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    agg = {}
    for blk in D:
        k = (blk.get('start', 'band'), blk['c'], blk['graph'], blk['size'])
        a_ = agg.setdefault(k, dict(runs=[], N=blk['N'], deg=blk['deg'], every=blk['every']))
        a_['runs'] += blk['runs']
    r3 = []
    for (start, c, kind, size), a_ in sorted(agg.items(), key=lambda kv: (kv[0][0], kv[0][2], kv[0][3], kv[0][1])):
        runs = a_['runs']; N = a_['N']; E = N * a_['deg'] / 2; ev = a_['every']
        ff = np.array([x['first'] for x in runs]); n = len(runs)
        nf = int((ff == 1).sum()); npf = int((ff == -1).sum()); nu = int((ff == 0).sum())
        lo, hi = wilson(nf, nf + npf)
        tf = [x['t_first'] for x in runs if x['first'] != 0]
        cons = [x['fix'] == x['first'] for x in runs if x['first'] != 0 and x['fix'] != 0]
        sd = 0.0; st = 0.0; inter = []
        for x in runs:
            cnt = np.array(x['cnt']); cr = np.array(x['cross'])
            m = len(cnt)                                   # records strictly before first passage
            if m < 2: continue
            sd += cnt[m - 1] - cnt[0]; st += (m - 1) * ev * cr[:m].mean()
            inter.append(cr[:m].mean() / E)
        vel = sd / st if st > 0 else float('nan')
        i0 = runs[0]['cross'][0] / E if runs[0]['cross'] else float('nan')
        L.append('| %s | %g | %s %d | %d | %d | %.3f [%.2f, %.2f] | %d | %d | %.0f | %s | %.2e | %.4f | %.4f |' % (
            start, c, kind, size, N, n, nf / max(1, nf + npf), lo, hi, npf, nu, np.median(tf) if tf else float('nan'),
            '%.3f (%d)' % (np.mean(cons), len(cons)) if cons else '—', vel, i0, np.mean(inter) if inter else float('nan')))
        r3.append(dict(start=start, c=c, graph=kind, size=size, N=N, runs=n, p_first=nf / max(1, nf + npf), lo=lo, hi=hi, other_first=npf,
                       undecided=nu, t_first_median=float(np.median(tf)) if tf else None, p_fix_given_first=float(np.mean(cons)) if cons else None,
                       velocity_per_edge=float(vel), interface0=i0, interface_mean=float(np.mean(inter)) if inter else None))
    summary['R3'] = r3
    # ---- R3b controlled fronts
    F = _load('rival_front.json')
    if F:
        L += ['', '## R3b: controlled fronts, P* against an FB half seeded with ALLC at density x, no mutation (ε-free)', '',
              'Velocity = mean P* count gain per generation / border length (torus: 2·side rows/gen; hypercube: share/gen), over the first 500 generations and over the whole run (20 replicates). Static threshold x*(c) = 4c/(3+4c) = 0 / 0.013 / 0.118.', '',
              '| c | graph | x | v (first 500 gen) ± se | v (whole run) ± se | P* share at end | ALLC share of FB-side front, first 500 gen | same, whole run |', '|---|---|---|---|---|---|---|---|']
        r3b = []
        for r in sorted(F, key=lambda r: (r['graph'], r['c'], r['x'])):
            ps = np.array(r['ps']); ev = r['every']; N = r['N']
            norm = 2 * r['size'] if r['graph'] == 'torus' else N
            k = min(ps.shape[1] - 1, 500 // ev)
            v1 = (ps[:, k] - ps[:, 0]) / (k * ev) / norm
            v2 = (ps[:, -1] - ps[:, 0]) / ((ps.shape[1] - 1) * ev) / norm
            fr = np.array(r['front'])                       # reps x records x 3 (front counts of P*, FB, ALLC)
            xf1 = fr[:, :k + 1, 2].sum() / max(1, fr[:, :k + 1, 1:].sum()); xf2 = fr[:, :, 2].sum() / max(1, fr[:, :, 1:].sum())
            L.append('| %g | %s %d | %.2f | %.2e ± %.1e | %.2e ± %.1e | %.3f | %.3f | %.3f |' % (r['c'], r['graph'], r['size'], r['x'], v1.mean(), v1.std() / np.sqrt(len(v1)),
                     v2.mean(), v2.std() / np.sqrt(len(v2)), ps[:, -1].mean() / N, xf1, xf2))
            r3b.append(dict(c=r['c'], graph=r['graph'], x=r['x'], v500=float(v1.mean()), v500_se=float(v1.std() / np.sqrt(len(v1))),
                            v=float(v2.mean()), v_se=float(v2.std() / np.sqrt(len(v2))), end=float(ps[:, -1].mean() / N)))
        summary['R3b'] = r3b
    # ---- R4
    A = _load('rival_abm.json')
    L += ['', '## R4: agent-based runs at finite ε (approach rates, not π)', '',
          'Torus side 128 and hypercube d = 14 (N = 16,384), death-birth, mutation from μ. Second-half means. x = ALLC / (ALLC + FB-net). MD = mutual-defection edge fraction; welfare lost = MD × (R − P) = MD.', '',
          '| graph | c | ε | start | seed | P(C,C) | FB-net | P*-net | exploitable | D-type | x | x at front (whole run) | MD total | MD rival border | MD with D end | MD rival border / D end while both nets ≥ 0.1 (gens) | max rival-border MD | interaction welfare loss | cost per edge | first gen P*-net > 0.9 | first gen P*-net > 0.01 |',
          '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    r4 = []
    for r in sorted(A, key=lambda r: (r['graph'], r['c'], r['eps'], r['start'], r['seed'])):
        rec = np.array(r['rec']); h = len(rec) // 2; s = rec[h:]
        x = s[:, 10].mean() / max(1e-12, s[:, 10].mean() + s[:, 12].mean())
        fa, ff, ft = rec[:, 16], rec[:, 17], rec[:, 18]          # front: ALLC, FB-net, all (/N)
        live = ft > 0
        xfront = float(fa[live].sum() / max(1e-12, fa[live].sum() + ff[live].sum())) if live.any() else float('nan')
        iwl = float((s[:, 6] - s[:, 7]).mean())                  # interaction welfare loss f_DD + (f_CD + f_DC)/2
        both = (rec[:, 12] >= 0.1) & (rec[:, 13] >= 0.1)
        mdb_both = float(rec[both, 3].mean()) if both.any() else float('nan')
        mdd_both = float(rec[both, 4].mean()) if both.any() else float('nan')
        g90 = rec[rec[:, 13] > 0.9, 0]; g01 = rec[rec[:, 13] > 0.01, 0]
        row = dict(graph=r['graph'], size=r['size'], c=r['c'], eps=r['eps'], start=r['start'], seed=r['seed'], pcc=s[:, 1].mean(),
                   fbnet=s[:, 12].mean(), psnet=s[:, 13].mean(), expl=s[:, 14].mean(), dtype=s[:, 11].mean(), x=x,
                   md=s[:, 2].mean(), md_border=s[:, 3].mean(), md_d=s[:, 4].mean(), cost=s[:, 7].mean(),
                   x_front=xfront, iwl=iwl, md_border_both=mdb_both, md_d_both=mdd_both, gens_both=int(both.sum()) * r['every'],
                   g90=float(g90[0]) if len(g90) else None, g01=float(g01[0]) if len(g01) else None,
                   md_border_max=float(rec[:, 3].max()), traj=rec[::max(1, len(rec) // 20)][:, [0, 1, 2, 3, 4, 10, 11, 12, 13, 14]].tolist())
        r4.append(row)
        L.append('| %s | %g | %g | %s | %d | %.3f | %.3f | %.3f | %.3f | %.3f | %.3f | %.3f | %.4f | %.4f | %.4f | %.4f / %.4f (%d) | %.4f | %.4f | %.4f | %s | %s |' % (
            '%s %d' % (r['graph'], r['size']), r['c'], r['eps'], r['start'], r['seed'], row['pcc'], row['fbnet'], row['psnet'], row['expl'], row['dtype'], x, xfront,
            row['md'], row['md_border'], row['md_d'], mdb_both, mdd_both, row['gens_both'], row['md_border_max'], iwl, row['cost'], '%.0f' % row['g90'] if row['g90'] else '—', '%.0f' % row['g01'] if row['g01'] else '—'))
    L += ['', 'Trajectories (every 5% of the run): generation, P(C,C), MD, MD rival border, MD with D end, ALLC, D-type, FB-net, P*-net, exploitable.', '']
    for row in r4:
        L.append('- %s %d c=%g ε=%g %s seed %d: %s' % (row['graph'], row['size'], row['c'], row['eps'], row['start'], row['seed'],
                 ' | '.join('g%d: cc %.2f FB %.2f P* %.2f ALLC %.2f D %.2f bMD %.4f' % (t[0], t[1], t[7], t[8], t[5], t[6], t[3]) for t in row['traj'])))
    summary['R4'] = [{k: v for k, v in row.items() if k != 'traj'} for row in r4]
    open(OUT('rival_networks.md'), 'w').write('\n'.join(L) + '\n')
    json.dump(summary, open(OUT('rival_networks.json'), 'w'), indent=1, default=float)
    print('\n'.join(L))


if __name__ == '__main__':
    {'rates': run_rates, 'domain': run_domain, 'front': run_front, 'wmchain': run_wmchain, 'abm': run_abm, 'report': report}[sys.argv[1]]()
