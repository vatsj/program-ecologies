"""Driver for the farsighted-refusal experiment (notes/farsighted-refusal.md).

    python3 src/farsighted_refusal_run.py static [--procs 3]   # certified fixed points per delta -> runs/farsighted-refusal-static.json
    python3 src/farsighted_refusal_run.py validate             # identity with D1 / R2, reader = gKR, forced chain = static
    python3 src/farsighted_refusal_run.py forced               # forced starts, U-gKR(0.99), mN = 0
    python3 src/farsighted_refusal_run.py cell NAME [--procs 3]
    python3 src/farsighted_refusal_run.py all [--procs 3] [NAMES]
Per-run summaries go to runs/farsighted_refusal/<cell>.json; per-run arrays to runs/farsighted_refusal/<cell>/r<k>.npz
(not committed).
"""
import argparse, json, os, sys, time, zlib
from collections import Counter, defaultdict
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stable_sets as SS
import stable_sets_run as SR
import dominance_contracts as DC
import dominance_contracts_run as DR
import farsighted_refusal as F

ROOT = SS.ROOT
OUT = os.path.join(ROOT, 'runs', 'farsighted_refusal')
STATIC = os.path.join(ROOT, 'runs', 'farsighted-refusal-static.json')
HS = (500, 1000, 2000, 10000)
DELTAS = (0.5, 0.8, 0.9, 0.95, 0.99)

# ---------------------------------------------------------------- cells
CELLS = {}
def _c(name, guards, assign, mN, H, **kw):
    d = dict(guards=guards, assign=assign, mN=mN, H=H, seedbase='L%d' % mN, nu=0.1)
    d.update(kw)
    CELLS[name] = d

for mN in (0, 1):
    _c('D1r-%d' % mN, ['g0'], None, mN, 10000)                                    # baseline D1 rerun (bit check)
    _c('R2r-%d' % mN, ['g0', 'gV'], ('bit', 1.0, 1), mN, 10000)                    # baseline R2 rerun (bit check)
    _c('Ug1-%d' % mN, ['g0', 'g1'], ('bit', 1.0, 1), mN, 10000)
    _c('UKR90-%d' % mN, ['g0', 'gKR0.9'], ('bit', 1.0, 1), mN, 10000)
    _c('UKR99-%d' % mN, ['g0', 'gKR0.99'], ('bit', 1.0, 1), mN, 10000)
    _c('Uread99-%d' % mN, ['g0', 'read0.99'], ('bit', 1.0, 1), mN, 10000)
    _c('MKR-%d' % mN, ['g0', 'gKR0.99'], ('bit', 0.5, 1), mN, 10000)
    for Nn in (50, 200):
        _c('UKR99-%d-N%d' % (mN, Nn), ['g0', 'gKR0.99'], ('bit', 1.0, 1), mN, 2000, N=Nn, runs=20,
           seedbase='L%d-N%d' % (mN, Nn))
_c('Ug1x-0', ['g0', 'g1x'], ('bit', 1.0, 1), 0, 2000)
_c('C3-1', ['g0', 'gV', 'gKR0.99'], ('mix', [0, 1, 2], [1 / 3, 1 / 3, 1 / 3]), 1, 10000)
_c('C3read-1', ['g0', 'gKR0.99', 'read0.99'], ('mix', [0, 1, 2], [1 / 3, 1 / 3, 1 / 3]), 1, 10000)
_c('Mread-1', ['g0', 'gKR0.99', 'read0.99'], ('mix', [1, 2], [0.5, 0.5]), 1, 2000)
_c('Mg1-1', ['g0', 'g1'], ('bit', 0.5, 1), 1, 2000)
_c('Mg1-0', ['g0', 'g1'], ('bit', 0.5, 1), 0, 2000)
_c('Mu-1', ['g0', 'gKRu'], ('bit', 0.5, 1), 1, 2000)
_c('Rare-1', ['g0', 'gKR0.99'], ('bit', 0.05, 1), 1, 2000)

ORDER = ['D1r-0', 'R2r-0', 'Ug1-0', 'Ug1x-0', 'UKR90-0', 'UKR99-0', 'Uread99-0', 'MKR-0', 'Mg1-0',
         'D1r-1', 'R2r-1', 'Ug1-1', 'UKR90-1', 'UKR99-1', 'Uread99-1', 'MKR-1', 'C3-1', 'C3read-1', 'Mread-1',
         'Mg1-1', 'Mu-1', 'Rare-1', 'UKR99-0-N50', 'UKR99-0-N200', 'UKR99-1-N50', 'UKR99-1-N200']


# ---------------------------------------------------------------- guards
_G = {}


def static_data():
    if 'S' not in _G:
        _G['S'] = json.load(open(STATIC))
    return _G['S']


def kr_table(dkey):
    """the default fixed point's member-level table and W at delta = dkey ('0.9', '0.99', or 'u' for the
    unequal-absorbing program)."""
    if dkey in _G:
        return _G[dkey]
    S = static_data()
    if dkey == 'u':
        ent = S['unequal_program']
        d = ent['delta']; acc = np.array(ent['acc'], np.int8)
    else:
        d = float(dkey); acc = np.array(S['deltas'][dkey]['default']['acc'], np.int8)
    W = F.values(acc, d)
    T = F.table_from_W(W)
    # the table restricted to proposed pairs must be the fixed point
    for j in range(F.NP):
        assert bool(T[F.PY[j], F.PK[j], 0] and T[F.PY[j], F.PK[j], 1]) == bool(acc[j])
    _G[dkey] = (T, d, W, acc)
    return _G[dkey]


def guard_arrays(names):
    NG = len(names)
    GKIND = np.zeros(NG, np.int64)
    GTAB = np.ones((NG, F.NX, F.NCON, 2), np.bool_)
    KRTAB = np.ones((F.NX, F.NCON, 2), np.bool_)
    rdelta = 0.99
    kr = None
    for g, n in enumerate(names):
        if n == 'g0':
            GTAB[g] = F.table_g0()
        elif n == 'gV':
            GTAB[g] = F.table_gV()
        elif n == 'g1':
            GTAB[g] = F.table_g1('y')
        elif n == 'g1x':
            GTAB[g] = F.table_g1('x')
        elif n.startswith('gKR') or n == 'gKRu':
            key = 'u' if n == 'gKRu' else n[3:]
            T, d, W, acc = kr_table(key)
            GTAB[g] = T
            assert kr in (None, key); kr = key
        elif n.startswith('read'):
            key = n[4:]
            T, d, W, acc = kr_table(key)
            GKIND[g] = 1
            GTAB[g] = T          # unused by the kernel for readers (decisions are computed), kept for reporting
            assert kr in (None, key); kr = key
        else:
            raise KeyError(n)
    if kr is not None:
        T, d, W, acc = kr_table(kr)
        KRTAB[:] = T; rdelta = d
    return dict(GKIND=GKIND, GTAB=GTAB, KRTAB=KRTAB, rdelta=rdelta, NG=NG)


# ---------------------------------------------------------------- one run
def build(p, r):
    I = p.get('I', 64); N = p.get('N', 100)
    rng = np.random.default_rng(SR.run_seed(p['seedbase'], r))
    laws = [SS.seed_law('L', s) for s in range(3)]
    init = SS.draw_seeds(rng, I, N, laws)
    loc, U = SS.compress(init)
    st = F.Setup(loc, U, len(p['guards']), assign=p['assign'], rng=rng)
    return st, I, N


def run_job(args):
    name, r = args
    p = dict(CELLS[name]); p['name'] = name
    T = DR.tables()
    st, I, N = build(p, r)
    H = p['H']
    seed = SR.run_seed(p['seedbase'], r) % (2 ** 31)
    hrec = np.array([h for h in HS if h <= H], np.int64)
    ga = guard_arrays(p['guards'])
    t0 = time.time()
    out = F.run_fkern(st, T, N, p['mN'], seed, H, hrec, ga, nu=p['nu'])
    wall = time.time() - t0
    status, stop, tcount, cls, eff, dist, ev, nev, nmig, cev, ncev, cnt, gfreq, refby, nsolve, pcount = out
    os.makedirs(os.path.join(OUT, name), exist_ok=True)
    np.savez_compressed(os.path.join(OUT, name, 'r%d.npz' % r), cls=cls, cev=cev.astype(np.float32),
                        gfreq=gfreq[::5].astype(np.float16), eff=eff, dist=dist.astype(np.float32))
    rec = analyse(p, st, T, out, I, N, H)
    rec.update(cell=name, run=r, seed=int(seed), status=int(status), stop_gen=int(stop), nev=int(nev), nmig=int(nmig),
               ncev=int(ncev), wall=wall, ntypes=[int(x) for x in st.ntypes], nsolve=int(nsolve))
    return rec


def _dk_tuple(out, I):
    """the dkern-shaped tuple DR.analyse expects (cev padded to 20 columns; no bits, menus or pending fates)."""
    status, stop, tcount, cls, eff, dist, ev, nev, nmig, cev, ncev, cnt, gfreq, refby, nsolve, pcount = out
    c20 = np.zeros((cev.shape[0], 20))
    c20[:, :8] = cev[:, :8]
    c20[:, 8] = -1; c20[:, 9] = -1
    c20[:, 10] = cev[:, 10]
    return (status, stop, tcount, cls, eff, dist, ev, nev, nmig, c20, ncev, cnt, np.zeros((0, I, 3)),
            np.zeros((0, I), np.int64), np.zeros((0, 10), np.int64), pcount)


def analyse(p, st, T, out, I, N, H):
    status, stop, tcount, cls, eff, dist, ev, nev, nmig, cev, ncev, cnt, gfreq, refby, nsolve, pcount = out
    rec = DR.analyse(dict(fr=0.0), st, T, _dk_tuple(out, I), I, N, H)
    rec.pop('guard', None)
    names = p['guards']; NG = len(names)
    X = T.R; nout = len(X); V = sorted(SS.symmetric_set(X, 6))
    hs = [h for h in HS if h <= H]
    rec['counts'] = dict(zip(['draws', 'null', '_', 'consulted', 'refused', 'installed', 'infeasible', 'overflow'],
                             [int(v) for v in cnt.sum(0)]))
    rec['counts'].pop('_')
    rec['refused_by'] = {names[g]: int(refby[:, g].sum()) for g in range(NG)}
    for hi, h in enumerate(hs):
        d = rec['horizons'][str(h)]
        am = dist[hi].argmax(1)
        d['modal_occupancy'] = float(np.isin(am, V).mean())
        d['modal_labels'] = {T.labels[k]: v for k, v in Counter(int(x) for x in am).items()}
        gf = gfreq[min(h // 10, gfreq.shape[0] - 1)]          # (I, 3, NG)
        d['guard_mean'] = {names[g]: float(gf[:, :, g].mean()) for g in range(NG)}
        # placement on member islands: member slots vs the excluded slot
        pl = defaultdict(list)
        for i in range(I):
            c = int(cls[h, i])
            if c in V:
                ex = [s for s in range(3) if X[c][s] == 0][0]
                for s in range(3):
                    for g in range(NG):
                        pl[(names[g], 'excluded' if s == ex else 'member')].append(float(gf[i, s, g]))
        d['placement'] = {'%s|%s' % k: float(np.mean(v)) for k, v in pl.items()}
    rec['guard_traj'] = {names[g]: [round(float(v), 4) for v in gfreq[::5, :, :, g].mean(axis=(1, 2))] for g in range(NG)}
    hl = hs[-1]
    g0f = gfreq[0]; gHf = gfreq[min(hl // 10, gfreq.shape[0] - 1)]
    rec['guard_change'] = {names[g]: float(gHf[:, :, g].mean() - g0f[:, :, g].mean()) for g in range(NG)}
    if 2000 <= H:
        g2 = gfreq[200]
        rec['guard_change_2000'] = {names[g]: float(g2[:, :, g].mean() - g0f[:, :, g].mean()) for g in range(NG)}
    # guard-outcome association: island guard frequency at a window start vs member time-share in the window
    if NG > 1:
        assoc = {}
        for g in range(1, NG):
            if names[g] == 'g0':
                continue
            rows = []
            for w0 in range(0, min(H, 10000), 250):
                w1 = min(w0 + 250, H)
                f0 = gfreq[w0 // 10, :, :, g].mean(1)
                share = np.isin(cls[w0:w1 + 1], V).mean(0)
                if f0.std() > 1e-9 and share.std() > 1e-9:
                    rows.append((w0, round(float(np.corrcoef(f0, share)[0, 1]), 4)))
                else:
                    rows.append((w0, None))
            assoc[names[g]] = rows
        rec['assoc'] = assoc
        rec['rescue'] = rescue(cls, cev, gfreq, names, V, nout, H)
    # contract events by modal outcome category and decision
    dec = Counter()
    for row in cev:
        y = int(row[5]); stt = int(row[3])
        dec[('member' if y in V else T.cat[y]) + '|' + ('refused' if stt == 1 else 'installed')] += 1
    rec['decisions'] = dict(dec)
    return rec


def rescue(cls, cev, gfreq, names, V, nout, H):
    """the dominance-contracts decomposition: per island and 50-generation window, the change of the island's mean
    frequency of each non-base guard by the window's contract events (consulted & refused / consulted & installed /
    installed without consultation / none) and the island's state at the window start (member or not)."""
    ev = defaultdict(set)
    for row in cev:
        g, i, stt, need = int(row[0]), int(row[1]), int(row[3]), row[10] > 0
        w = g // 50
        if need and stt == 1: ev[(i, w)].add('refused')
        elif need and stt == 2: ev[(i, w)].add('consulted-through')
        elif stt == 2: ev[(i, w)].add('unconsulted-install')
    I = cls.shape[1]
    out = {}
    nw = min(H, gfreq.shape[0] * 10 - 10) // 50
    for g in range(1, len(names)):
        tot = defaultdict(lambda: [0.0, 0])
        for w in range(nw):
            a = gfreq[w * 5, :, :, g].mean(1); b = gfreq[(w + 1) * 5, :, :, g].mean(1)
            for i in range(I):
                mem = (cls[w * 50, i] in V) or cls[w * 50, i] == nout
                e = ev.get((i, w), set())
                kind = ('consulted-through' if 'consulted-through' in e else ('refused' if 'refused' in e else
                        ('unconsulted-install' if 'unconsulted-install' in e else 'none')))
                key = ('member' if mem else 'non-member') + '|' + kind
                tot[key][0] += float(b[i] - a[i]); tot[key][1] += 1
        out[names[g]] = {k: [round(v[0] / I, 5), v[1]] for k, v in sorted(tot.items())}
    return out


# ---------------------------------------------------------------- cells
def run_cell(name, procs=3):
    from multiprocessing import Pool
    p = CELLS[name]
    nr = p.get('runs', 40)
    jobs = [(name, r) for r in range(nr)]
    t0 = time.time()
    if procs > 1:
        with Pool(procs, maxtasksperchild=8) as pool:
            recs = pool.map(run_job, jobs, chunksize=1)
    else:
        recs = [run_job(j) for j in jobs]
    recs.sort(key=lambda r: r['run'])
    os.makedirs(OUT, exist_ok=True)
    json.dump(dict(cell=name, params=p, runs=recs, wall=time.time() - t0), open(os.path.join(OUT, name + '.json'), 'w'),
              default=DR._js)
    print(name, 'done in %.0fs' % (time.time() - t0), flush=True)


# ---------------------------------------------------------------- static
FAIR_BITS = [j for j in range(F.NP) if F.PY[j] in F.V]
SUBTREE_CAP = 100_000


def fair_reps():
    """canonical S3 representatives of the 64 assignments of the six member-exit bits."""
    import itertools
    seen = {}
    for bits in itertools.product((0, 1), repeat=len(FAIR_BITS)):
        A = [0] * F.NP
        for j, b in zip(FAIR_BITS, bits):
            A[j] = b
        key = F.canon(tuple(A))
        seen.setdefault(key, bits)
    return sorted(seen.values())


def subtree_job(args):
    d, bits, cap = args
    fixed = np.where(F.ACTIVE_CORE, -1, 0).astype(np.int8)
    for j, b in zip(FAIR_BITS, bits):
        fixed[j] = b
    t0 = time.time()
    cs = F.CoreSearch(d, maxnodes=cap).run(fixed)
    return dict(delta=d, bits=list(bits), nodes=cs.nodes, complete=cs.complete, wall=time.time() - t0,
                solutions=[list(a) for a, _, _ in cs.solutions], weak=[list(a) for a, _, _ in cs.weak])


def sample_job(args):
    d, k0, n = args
    rng = np.random.default_rng(1000 + k0)
    found = set()
    for trial in range(n):
        A = np.where(F.ACTIVE_CORE, rng.integers(0, 2, F.NP), 0).astype(np.int8)
        for it in range(3000):
            B = F.best_response(F.values(A, d)); B[~F.ACTIVE_CORE] = 0
            diff = np.nonzero(B != A)[0]
            if len(diff) == 0:
                found.add(tuple(int(v) for v in A)); break
            j = rng.choice(diff); A = A.copy(); A[j] = B[j]
    return d, sorted(found)


def extend_core(acc, d, weak=True):
    """complete a core fixed point with every consistent level-2 / (0,0,0) decision set (exact)."""
    import itertools
    Wc = F.exact_values(tuple(acc), d)
    l2 = [F.local_solutions(y, Wc, d, weak=weak) for y in F.LEVEL2]
    out = []
    for combo in itertools.product(*l2):
        A = list(acc); W2 = [list(r) for r in Wc]
        for (js, S_, k2, Wy) in combo:
            for a, j in enumerate(js):
                A[j] = S_[a]
            W2[int(F.PY[js[0]])] = Wy
        for (js, S_, k3, Wy) in F.local_solutions(F.LEVEL3[0], W2, d, weak=weak):
            A3 = list(A)
            for a, j in enumerate(js):
                A3[j] = S_[a]
            st, mmin, ties = F.exact_check(tuple(A3), d)
            if st is not None:
                out.append((tuple(A3), st, mmin, ties))
    return out


def static(procs=3):
    from multiprocessing import Pool
    t0 = time.time()
    reps = fair_reps()
    jobs = [(d, bits, SUBTREE_CAP) for d in DELTAS for bits in reps]
    zs = [(d, k, 300) for d in DELTAS for k in range(5)]
    with Pool(procs, maxtasksperchild=4) as pool:
        sub = pool.map(subtree_job, jobs, chunksize=1)
        smp = pool.map(sample_job, zs, chunksize=1)
    seeded = F.seeded_distribution()
    z3 = [g for g, (pi, _, _, _) in enumerate(F.PERMS) if pi in ((0, 1, 2), (1, 2, 0), (2, 0, 1))]
    out = dict(deltas={}, subtree_cap=SUBTREE_CAP, fair_reps=[list(b) for b in reps])
    for d in DELTAS:
        rows = [r for r in sub if r['delta'] == d]
        complete = all(r['complete'] for r in rows)
        core = set()
        corew = set()
        for r in rows:
            for a in r['solutions']:
                for g in range(6):
                    core.add(tuple(_perm(a, g)))
            for a in r['weak']:
                for g in range(6):
                    corew.add(tuple(_perm(a, g)))
        sampled = set()
        for dd, f in smp:
            if dd == d:
                sampled.update(f)
        sub_inv = {}
        for nm, grp in (('S3', list(range(6))), ('Z3', z3)):
            r = F.subgroup_fixed_points(d, grp)
            sub_inv[nm] = dict(n_orbits=r['n_orbits'], solutions=len(r['solutions']), weak=len(r['weak']))
            for a, _, _ in r['solutions']:
                for g in range(6):
                    core.add(tuple(_perm(list(a), g)))
        # sampled core fixed points must be in the list when the list is complete
        missing = [a for a in sampled if a not in core]
        for a in missing:
            for g in range(6):
                core.add(tuple(_perm(list(a), g)))
        full = []; weakfull = []
        for a in sorted(core):
            for A3, st, mmin, ties in extend_core(a, d):
                (full if st == 'strict' else weakfull).append((A3, mmin, ties))
        for a in sorted(corew):
            for A3, st, mmin, ties in extend_core(a, d):
                if st == 'weak':
                    weakfull.append((A3, mmin, ties))
        orbits = {}
        for acc, mmin, ties in full:
            orbits.setdefault(F.canon(acc), []).append((acc, mmin, ties))
        dp = F.default_policy(d)
        defacc = tuple(int(v) for v in dp['A']) if dp['A'] is not None else None
        sols = set(a for a, _, _ in full)
        if defacc is None:
            defacc = min(sols, key=lambda a: (F.NP - sum(a), tuple(-v for v in a))); dp['rule'] = 'hamming'
        # cross-check initializations: all-refuse and 20 random starts (simultaneous best responses)
        xc = []
        rng = np.random.default_rng(7)
        starts = [('all-refuse', np.zeros(F.NP, np.int8))] + [('random%d' % k, rng.integers(0, 2, F.NP).astype(np.int8))
                                                              for k in range(20)]
        for lab, A in starts:
            seen = set()
            for it in range(2000):
                B = F.best_response(F.values(A, d))
                if np.array_equal(A, B):
                    break
                if B.tobytes() in seen:
                    A = None; break
                seen.add(B.tobytes()); A = B
            xc.append(dict(start=lab, fixed=None if A is None else bool(tuple(int(v) for v in A) in sols)))
        orb_out = []
        for c, mem in orbits.items():
            acc = mem[0][0]
            D = F.describe(np.array(acc), d, seeded)
            orb_out.append(dict(size=len(mem), acc=list(acc), min_margin_exact=float(min(m for _, m, _ in mem)),
                                ties=int(max(t for _, _, t in mem)), describe=D,
                                default=(defacc in [m[0] for m in mem]), members=[list(m[0]) for m in mem]))
        orb_out.sort(key=lambda o: (-o['default'], -o['describe']['n_accept']))
        Dd = F.describe(np.array(defacc), d, seeded)
        st_def, mm_def, ties_def = F.exact_check(defacc, d)
        out['deltas'][str(d)] = dict(
            delta=d, complete=complete, subtrees=[dict(bits=r['bits'], nodes=r['nodes'], complete=r['complete'],
                                                       wall=round(r['wall'], 1), n_core=len(r['solutions']))
                                                  for r in rows],
            core_fixed_points=len(core), sampled_core=len(sampled), sampled_missing_from_search=len(missing),
            subgroup=sub_inv, n_fixed_points=len(full), n_orbits=len(orbits), n_weak=len(weakfull),
            weak_examples=[list(w[0]) for w in weakfull[:5]],
            default=dict(acc=list(defacc), rule=dp['rule'], iterations=dp.get('iterations'), flips=dp.get('flips'),
                         simultaneous=dp.get('simultaneous'), in_list=defacc in sols, exact=st_def,
                         min_margin_exact=float(mm_def), ties=int(ties_def), describe=Dd),
            crosscheck=xc, orbits=orb_out)
    out['g1_freezing'] = dict(g1=F.freezing_set(F.table_g1('y')), g1x=F.freezing_set(F.table_g1('x')),
                              gV=F.freezing_set(F.table_gV()))
    out['exposure'] = {F.LAB[y]: [bool(F.exposed(F.X[y], i)) for i in range(3)] for y in range(F.NX)}
    out['seeded'] = {F.LAB[y]: round(float(v), 5) for y, v in enumerate(seeded)}
    cand = []
    for d in DELTAS:
        for o in out['deltas'][str(d)]['orbits']:
            if any(F.CAT[F.LAB.index(l)] == 'unequal' for l in o['describe']['absorbing']):
                cand.append((d, o))
    if cand:
        # frozen choice: the highest delta, then the orbit with most accepted contracts; its listed representative
        d, o = sorted(cand, key=lambda t: (-t[0], -t[1]['describe']['n_accept']))[0]
        out['unequal_program'] = dict(delta=d, acc=o['acc'], absorbing=o['describe']['absorbing'])
    out['wall'] = time.time() - t0
    json.dump(out, open(STATIC, 'w'), indent=1, default=DR._js)
    for d in DELTAS:
        r = out['deltas'][str(d)]
        print(d, 'complete', r['complete'], 'fixed points', r['n_fixed_points'], 'orbits', r['n_orbits'], 'weak',
              r['n_weak'], 'default', r['default']['rule'], r['default']['describe']['absorbing'], 'sampled missing',
              r['sampled_missing_from_search'], flush=True)


def _perm(acc, g):
    pmap = F.PERMS[g][3]
    B = [0] * F.NP
    for j in range(F.NP):
        B[pmap[j]] = acc[j]
    return B


# ---------------------------------------------------------------- forced starts
def forced(dkey='0.99', reps=3, H=2000, nper=12):
    """islands started at every outcome (constant profiles realizing it, up to nper per outcome, reps islands each),
    universal gKR(delta), mN = 0, nu = 0.1."""
    T = DR.tables(); G = SS.dollar3_game()
    S_, mu = SS.arm_data('weak'); ci = SS.const_index(S_.fs)
    groups = defaultdict(list)
    for a in np.ndindex(9, 9, 9):
        groups[F.RIDX[tuple(int(v) for v in G.pay[a])]].append(a)
    rng = np.random.default_rng(11)
    prof = []; youts = []
    for y in range(F.NX):
        lst = groups[y]
        pick = [lst[k] for k in rng.choice(len(lst), min(nper, len(lst)), replace=False)]
        for a in pick:
            for _ in range(reps):
                prof.append(a); youts.append(y)
    U = [np.array(sorted(ci[l] for l in range(9)), np.int64) for _ in range(3)]
    pos = {x: j for j, x in enumerate(U[0])}
    N = 100; I = len(prof)
    init = np.zeros((I, 3, 9), np.int64)
    for i, a in enumerate(prof):
        for s in range(3):
            init[i, s, pos[ci[a[s]]]] = N
    names = ['g0', 'gKR' + dkey]
    st = F.Setup(init, U, 2, assign=('bit', 1.0, 1), rng=None)
    ga = guard_arrays(names)
    seed = zlib.crc32(('forced|%s' % dkey).encode()) & 0x7fffffff
    out = F.run_fkern(st, T, N, 0, seed, H, np.array([H], np.int64), ga, nu=0.1, stop_closed=False)
    cls = out[3]
    V = sorted(SS.symmetric_set(T.R, 6))
    res = {}
    T_, d, W, acc = kr_table(dkey)
    Q = F.event_chain(acc)
    for y in range(F.NX):
        idx = [i for i in range(I) if youts[i] == y]
        fin = cls[H, idx]
        first = []
        for i in idx:
            hit = np.nonzero(np.isin(cls[:, i], V))[0]
            first.append(int(hit[0]) if len(hit) else None)
        # static prediction: P(in V at H) with 0.1 events per generation (binomial thinning of events)
        p0 = np.zeros(F.NX); p0[y] = 1.0
        Qg = 0.9 * np.eye(F.NX) + 0.1 * Q
        pH = p0 @ np.linalg.matrix_power(Qg, H)
        res[F.LAB[y]] = dict(islands=len(idx), in_V=float(np.isin(fin, V).mean()),
                             final={T.labels[k]: v for k, v in Counter(int(x) for x in fin).items()},
                             left_start=float(np.mean([any(cls[:, i] != y) for i in idx])),
                             first_V_median=float(np.median([f for f in first if f is not None])) if any(
                                 f is not None for f in first) else None,
                             static_in_V=float(pH[V].sum()))
    json.dump(dict(delta=dkey, H=H, reps=reps, nper=nper, results=res), open(os.path.join(OUT, 'forced_%s.json' % dkey), 'w'),
              indent=1, default=DR._js)
    for k, v in res.items():
        print(k, v['islands'], 'in V %.3f (static %.3f)' % (v['in_V'], v['static_in_V']), 'left %.2f' % v['left_start'],
              v['first_V_median'])


# ---------------------------------------------------------------- validation
def same_as_stored(rec, a, consent=True):
    """identity with a stored dominance-contracts run (D1 had no consent step, so its 'guarded' count, the gV guard
    firing without consequence, is not compared)."""
    keys = ('draws', 'null', 'refused', 'installed', 'infeasible')
    ca = a['counts']; cb = rec['counts']
    same_counts = all(ca[k] == cb[k] for k in keys) and (not consent or ca['guarded'] == cb['consulted'])
    return (rec['stop_gen'] == a['stop_gen'] and rec['status'] == a['status'] and rec['nmig'] == a['nmig'] and
            same_counts and all(rec['horizons'][h]['labels'] == a['horizons'][h]['labels'] for h in a['horizons']))


def validate(nruns=6):
    res = {}
    for mine, theirs in (('D1r-0', 'D1-0'), ('R2r-0', 'R2-0'), ('D1r-1', 'D1-1'), ('R2r-1', 'R2-1')):
        st = json.load(open(os.path.join(ROOT, 'runs', 'dominance_contracts', theirs + '.json')))['runs']
        ok = 0
        for r in range(nruns):
            rec = run_job((mine, r))
            ok += same_as_stored(rec, st[r], consent=mine.startswith('R2'))
        res[mine] = '%d/%d' % (ok, nruns)
        print(mine, 'identical to stored', theirs, res[mine], flush=True)
    # reader = gKR draw for draw (universal), first nruns runs at both mN
    for mN in (0, 1):
        ok = 0
        for r in range(nruns):
            a = run_job(('UKR99-%d' % mN, r)); b = run_job(('Uread99-%d' % mN, r))
            same = (a['stop_gen'] == b['stop_gen'] and a['nmig'] == b['nmig'] and a['counts'] == b['counts'] and
                    all(a['horizons'][h]['labels'] == b['horizons'][h]['labels'] for h in a['horizons']))
            ok += same
        res['read=gKR-%d' % mN] = '%d/%d' % (ok, nruns)
        print('reader = gKR at mN =', mN, res['read=gKR-%d' % mN], flush=True)
    # costs
    cost = {}
    for name in ('UKR99-0', 'UKR99-1', 'C3read-1', 'MKR-1'):
        t = time.time(); r = run_job((name, 999))
        cost[name] = dict(wall=r['wall'], H=CELLS[name]['H'], counts=r['counts'], nsolve=r['nsolve'], ntypes=r['ntypes'])
        print(name, cost[name], flush=True)
    json.dump(dict(identity=res, cost=cost), open(os.path.join(ROOT, 'runs', 'farsighted-refusal-validate.json'), 'w'),
              indent=1, default=DR._js)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('what')
    ap.add_argument('name', nargs='?')
    ap.add_argument('--procs', type=int, default=3)
    a = ap.parse_args()
    if a.what == 'static':
        static(a.procs)
    elif a.what == 'validate':
        validate()
    elif a.what == 'forced':
        forced(a.name or '0.99')
    elif a.what == 'cell':
        run_cell(a.name, a.procs)
    elif a.what == 'all':
        for nm in ORDER:
            if a.name and nm not in a.name.split(','):
                continue
            if os.path.exists(os.path.join(OUT, nm + '.json')):
                print('skip', nm, flush=True); continue
            run_cell(nm, a.procs)


if __name__ == '__main__':
    main()
