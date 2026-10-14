"""Driver for the dominance-contracts experiment (notes/dominance-contracts.md).

    python3 src/dominance_contracts_run.py static           # -> runs/dominance-contracts-static.json
    python3 src/dominance_contracts_run.py validate         # identity with stable_sets.kern, jump checks, costs
    python3 src/dominance_contracts_run.py assays [--procs 3]   # forced edge assays -> runs/dominance_contracts/assays.json
    python3 src/dominance_contracts_run.py cell NAME [--procs 3]
    python3 src/dominance_contracts_run.py all [--procs 3] [NAMES]
Per-run summaries go to runs/dominance_contracts/<cell>.json; per-run arrays to runs/dominance_contracts/<cell>/r<k>.npz
(not committed).
"""
import argparse, itertools, json, os, sys, time, zlib
from collections import Counter, defaultdict
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stable_sets as SS
import stable_sets_run as SR
import dollar3 as D
import dominance_contracts as DC

ROOT = SS.ROOT
OUT = os.path.join(ROOT, 'runs', 'dominance_contracts')
HS = (500, 1000, 2000, 10000)
MINRUN = 5

# ---------------------------------------------------------------- cells
CELLS = {}
for mN in (0, 1):
    base = 'L%d' % mN
    CELLS['B%d' % mN] = dict(mN=mN, nu=0.0, H=10000, seedbase=base)
    CELLS['D1-%d' % mN] = dict(mN=mN, nu=0.1, H=10000, seedbase=base)
    CELLS['D2-%d' % mN] = dict(mN=mN, nu=0.01, H=2000, seedbase=base)
    CELLS['D3-%d' % mN] = dict(mN=mN, nu=0.1, beta=0.25, H=2000, seedbase=base)
    CELLS['D3p-%d' % mN] = dict(mN=mN, nu=0.1, beta=0.5, H=2000, seedbase=base)
    CELLS['D4-%d' % mN] = dict(mN=mN, nu=0.1, menu='G', H=2000, seedbase=base)
    CELLS['R1pub-%d' % mN] = dict(mN=mN, nu=0.1, fr=0.5, consent='public', H=10000, seedbase=base)
    CELLS['R1priv-%d' % mN] = dict(mN=mN, nu=0.1, fr=0.5, consent='private', H=2000, seedbase=base)
    CELLS['R1blind-%d' % mN] = dict(mN=mN, nu=0.1, fr=0.5, consent='blind', H=2000, seedbase=base)
    CELLS['R2-%d' % mN] = dict(mN=mN, nu=0.1, fr=1.0, consent='public', H=10000, seedbase=base)
    for Nn in (50, 200):
        nb = 'L%d-N%d' % (mN, Nn)
        CELLS['B%d-N%d' % (mN, Nn)] = dict(mN=mN, nu=0.0, H=10000, seedbase=nb, N=Nn, runs=20)
        CELLS['D1-%d-N%d' % (mN, Nn)] = dict(mN=mN, nu=0.1, H=10000, seedbase=nb, N=Nn, runs=20)
        CELLS['R1pub-%d-N%d' % (mN, Nn)] = dict(mN=mN, nu=0.1, fr=0.5, consent='public', H=10000, seedbase=nb, N=Nn, runs=20)
        CELLS['R1priv-%d-N%d' % (mN, Nn)] = dict(mN=mN, nu=0.1, fr=0.5, consent='private', H=2000, seedbase=nb, N=Nn, runs=20)
ORDER = ['B0', 'B1', 'D1-0', 'D1-1', 'R1pub-0', 'R1pub-1', 'R2-0', 'R2-1', 'R1priv-0', 'R1priv-1', 'R1blind-0',
         'R1blind-1', 'D3-0', 'D3-1', 'D4-0', 'D4-1', 'B0-N50', 'B1-N50', 'B0-N200', 'B1-N200',
         'D1-0-N50', 'D1-1-N50', 'D1-0-N200', 'D1-1-N200', 'R1pub-0-N50', 'R1pub-1-N50', 'R1pub-0-N200',
         'R1pub-1-N200', 'R1priv-0-N50', 'R1priv-1-N50', 'R1priv-0-N200', 'R1priv-1-N200',
         'D3p-0', 'D3p-1', 'D2-0', 'D2-1']

_T = {}


def tables():
    if 'T' not in _T:
        _T['T'] = SS.Tables(SS.dollar3_game())
    return _T['T']


def build(p, r):
    """founders exactly as stable_sets_run.build_run for law L (same generator, same draws), then the refusal bits
    and carried contracts from the same generator."""
    I = p.get('I', 64); N = p.get('N', 100)
    rng = np.random.default_rng(SR.run_seed(p['seedbase'], r))
    laws = [SS.seed_law('L', s) for s in range(3)]
    init = SS.draw_seeds(rng, I, N, laws)
    loc, U = SS.compress(init)
    st = DC.Setup(loc, U, fr=p.get('fr', 0.0), pcar=0.1 if p.get('menu') == 'G' else 0.0, rng=rng)
    return st, I, N


def run_job(args):
    name, r = args
    p = dict(CELLS[name]); p['name'] = name
    T = tables()
    st, I, N = build(p, r)
    H = p['H']
    seed = SR.run_seed(p['seedbase'], r) % (2 ** 31)
    hrec = np.array([h for h in HS if h <= H], np.int64)
    t0 = time.time()
    out = DC.run_kernel(st, T, N, p['mN'], seed, H, hrec, nu=p['nu'], menu_g=(p.get('menu') == 'G'),
                        beta=p.get('beta', 1.0), consent=DC.CONSENT[p.get('consent', 'none')])
    wall = time.time() - t0
    status, stop, tcount, cls, eff, dist, ev, nev, nmig, cev, ncev, cnt, rfreq, menus, pend, pcount = out
    os.makedirs(os.path.join(OUT, name), exist_ok=True)
    np.savez_compressed(os.path.join(OUT, name, 'r%d.npz' % r), cls=cls, ev=ev, cev=cev, cnt=cnt,
                        rfreq=rfreq[::5].astype(np.float16), menus=menus[::5], pend=pend, eff=eff,
                        dist=dist.astype(np.float32))
    rec = analyse(p, st, T, out, I, N, H)
    rec.update(cell=name, run=r, seed=int(seed), status=int(status), stop_gen=int(stop), nev=int(nev), nmig=int(nmig),
               ncev=int(ncev), wall=wall, K=[len(u) for u in st.U], ntypes=[int(x) for x in st.ntypes])
    return rec


# ---------------------------------------------------------------- analysis
CATS = ('member', 'unequal', 'wasteful', 'grand', 'disagreement')


def catof(T, c, nout):
    if c == nout: return 'member-mixed'
    if c > nout: return 'other-mixed'
    x = T.cat[c]
    if x == 'fair': return 'member'
    if x.startswith('grand'): return 'grand'
    return x


def settled(seq, nout, minlen=MINRUN):
    out = []
    t = 0; L = len(seq)
    while t < L:
        c = seq[t]; u = t
        while u + 1 < L and seq[u + 1] == c:
            u += 1
        if c < nout and u - t + 1 >= minlen:
            if out and out[-1][0] == c:
                out[-1] = (c, out[-1][1], u)        # a short spell between two runs of one class: merge
            else:
                out.append((int(c), t, u))
        t = u + 1
    return out


def analyse(p, st, T, out, I, N, H):
    status, stop, tcount, cls, eff, dist, ev, nev, nmig, cev, ncev, cnt, rfreq, menus, pend, pcount = out
    X = T.R; nout = len(X)
    V = set(SS.symmetric_set(X, 6))
    hs = [h for h in HS if h <= H]
    rec = dict(horizons={})
    for hi, h in enumerate(hs):
        c = cls[h]
        cc = Counter(catof(T, int(x), nout) for x in c)
        d = dict(cats={k: v / I for k, v in cc.items()})
        d['occupancy'] = cc.get('member', 0) / I
        d['member_or_mixed'] = (cc.get('member', 0) + cc.get('member-mixed', 0)) / I
        d['support_strict'] = bool(all((int(x) in V) or int(x) == nout for x in c))
        d['support_ss'] = bool({int(x) for x in c if x < nout} <= V)
        d['coverage'] = bool(V <= {int(x) for x in c})
        d['consensus'] = bool(len(set(int(x) for x in c)) == 1 and c[0] < nout)
        d['efficiency'] = float(eff[hi].mean())
        win = cls[max(0, h - 249):h + 1]
        d['window_occupancy'] = float(np.isin(win, list(V)).mean())
        d['labels'] = {T.labels[k] if k < nout else ('MM' if k == nout else 'MO'): v for k, v in Counter(int(x) for x in c).items()}
        if rfreq is not None and rfreq.shape[0] > 0:
            rr = rfreq[min(h // 10, rfreq.shape[0] - 1)]
            d['r_mean'] = float(rr.mean())
            d['r_by_slot'] = [float(rr[:, s].mean()) for s in range(3)]
        rec['horizons'][str(h)] = d
    # contract counters
    rec['counts'] = dict(zip(['draws', 'null', 'empty_menu', 'guarded', 'refused', 'installed', 'infeasible', 'overflow'],
                             [int(v) for v in cnt.sum(0)]))
    # events by island
    inst_by = defaultdict(list)
    cev_rows = cev
    for row in cev_rows:
        if int(row[3]) == 2:
            inst_by[int(row[1])].append(int(row[0]))
    evb = defaultdict(list)
    for e in ev:
        evb[int(e[1])].append(e)
    # settled transitions and triggers
    trans = Counter(); trig = Counter(); entries = Counter(); exits = Counter()
    trans_by_trig = defaultdict(Counter)
    same_member = 0; other_member = 0
    member_gen = 0; member_exit = Counter()
    cycles = Counter(); revisits = 0; nsettled = 0
    circ = Counter()
    for i in range(I):
        seq = cls[:H + 1, i]
        sr = settled(seq, nout)
        nsettled += len(sr)
        insts = sorted(inst_by.get(i, []))
        for (ca, a0, a1) in sr:
            if ca in V:
                member_gen += a1 - a0 + 1
        last_member = None; pending_exit = False
        for (ca, a0, a1), (cb, b0, b1) in zip(sr, sr[1:]):
            A = catof(T, ca, nout); B = catof(T, cb, nout)
            tr = trigger_of(insts, evb.get(i, []), a1, b0)
            trans[(A, B)] += 1; trig[tr] += 1; trans_by_trig[tr][(A, B)] += 1
            circ[(A, B)] += 1
            if ca not in V and cb in V:
                entries[tr] += 1
            if ca in V and cb not in V:
                exits[tr] += 1; member_exit[tr] += 1
            if ca in V and cb in V:
                member_exit['member->member:' + tr] += 1
        # same-member returns: member run, then >= 1 non-member run, then the next member run
        prev_m = None; left = False
        for (ca, a0, a1) in sr:
            if ca in V:
                if prev_m is not None and left:
                    if ca == prev_m: same_member += 1
                    else: other_member += 1
                prev_m = ca; left = False
            else:
                if prev_m is not None:
                    left = True
        # minimal directed cycles on outcomes
        oc = [c for c, _, _ in sr]
        for j in range(len(oc)):
            seen = {oc[j]}
            for l in range(j + 1, len(oc)):
                if oc[l] == oc[j]:
                    pat = '>'.join(catof(T, x, nout)[0].upper() for x in oc[j:l + 1])
                    cycles[pat if len(pat) <= 13 else 'long'] += 1
                    revisits += 1
                    break
                if oc[l] in seen:
                    break
                seen.add(oc[l])
    rec['transitions'] = {'%s>%s' % k: v for k, v in trans.items()}
    rec['transitions_by_trigger'] = {t: {'%s>%s' % k: v for k, v in c.items()} for t, c in trans_by_trig.items()}
    rec['triggers'] = dict(trig)
    rec['entries_into_V'] = dict(entries)
    rec['exits_from_V'] = dict(exits)
    rec['member_exit'] = dict(member_exit)
    rec['member_gens'] = int(member_gen)
    rec['same_member_return'] = [same_member, other_member]
    rec['cycles'] = dict(cycles.most_common(15))
    rec['revisits'] = revisits; rec['nsettled'] = nsettled
    # contract jump matrix (classified at the event and one generation after)
    jm = Counter(); guard_stats = Counter()
    for row in cev_rows:
        g = int(row[0]); i = int(row[1])
        if int(row[3]) == 2 and g + 1 <= H:
            jm[(catof(T, int(cls[g, i]), nout), catof(T, int(cls[g + 1, i]), nout))] += 1
        if row[10] > 0:
            guard_stats['guarded'] += 1
            guard_stats['refused' if int(row[3]) == 1 else 'went_through'] += 1
            if row[8] == 1 or row[9] == 1: guard_stats['drawn_carrier'] += 1
            if row[17] > 0 or row[18] > 0: guard_stats['carriers_present'] += 1
    rec['jumps'] = {'%s>%s' % k: v for k, v in jm.items()}
    rec['guard'] = dict(guard_stats)
    # beta < 1 fates by edge class
    if len(pend):
        fates = defaultdict(Counter)
        for q in pend:
            row = int(q[0])
            kap = int(cev_rows[row, 2]) if row < len(cev_rows) else -1
            pre = catof(T, int(q[9]), nout)
            xc = catof(T, T.ridx[DC.contract_x(kap)], nout) if kap >= 0 else '?'
            st_ = ['open', 'joint', 'lost', 'one-sided', 'timeout', 'superseded'][int(q[7])]
            fates['%s>%s' % (pre, xc)][st_] += 1
        rec['fates'] = {k: dict(v) for k, v in fates.items()}
    # refusal
    if p.get('fr', 0.0) > 0.0:
        traj = rfreq[::5].mean(axis=(1, 2))
        rec['r_traj'] = [round(float(v), 4) for v in traj]
        rec['r_change'] = float(rfreq[min(H // 10, rfreq.shape[0] - 1)].mean() - rfreq[0].mean())
        isl = []
        hs_isl = [h for h in hs if h in (2000, 10000)]
        for h in hs_isl:
            rr = rfreq[min(h // 10, rfreq.shape[0] - 1)]
            win = cls[max(0, h - 249):h + 1]
            share = np.isin(win, list(V)).mean(0)
            rows_ = []
            for i in range(I):
                b = [float(rr[i, s]) for s in range(3)]
                c = int(cls[h, i])
                prot_pub = prot_priv = None
                if c in V:
                    pr = [s for s in range(3) if X[c][s] > 0]; k = [s for s in range(3) if X[c][s] == 0][0]
                    fixed = all(v in (0.0, 1.0) for v in b)
                    if fixed:
                        prot_pub = bool(b[k] == 1.0 or (b[pr[0]] == 1.0 and b[pr[1]] == 1.0))
                        prot_priv = bool(b[pr[0]] == 1.0 and b[pr[1]] == 1.0)
                rows_.append(dict(bits=[round(v, 3) for v in b], share=float(share[i]), cls=c, prot_pub=prot_pub,
                                  prot_priv=prot_priv))
            isl.append(rows_)
        rec['islands'] = {str(h): v for h, v in zip(hs_isl, isl)}
    # menus
    if p.get('menu') == 'G':
        pc_ = np.vectorize(lambda v: bin(int(v)).count('1'))
        sizes = pc_(menus[::5])
        rec['menu_size'] = [round(float(v), 3) for v in sizes.mean(1)]
        cov = []
        for j in range(0, menus.shape[0], 5):
            g = j * 10
            if g > H: break
            vals = []
            for i in range(I):
                c = int(cls[g, i])
                if c >= nout: continue
                dm = [k for k in range(DC.NCON) if DC.proposed(k, X[c])]
                if not dm: continue
                vals.append(sum((int(menus[j, i]) >> k) & 1 for k in dm) / len(dm))
            cov.append(round(float(np.mean(vals)), 4) if vals else None)
        rec['menu_coverage'] = cov
    return rec


def trigger_of(insts, evs, a1, b0, tol=1e-9):
    for g in insts:
        if a1 <= g < b0:
            return 'contract'
    rows = [e for e in evs if a1 < e[0] <= b0 and e[4] >= 0]
    if not rows:
        return 'conditional/none'
    causes = [int(e[6]) for e in rows]
    if 2 in causes:
        return 'contract residue'
    if 1 in causes:
        return 'migration'
    ds = [e[7] for e in rows if not np.isnan(e[7])]
    if ds and all(abs(d) <= tol for d in ds):
        return 'drift'
    if any(d > tol for d in ds):
        return 'strict P'
    return 'other'


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
              default=_js)
    print(name, 'done in %.0fs' % (time.time() - t0), flush=True)


def _js(o):
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, (np.floating,)): return float(o)
    if isinstance(o, (np.bool_,)): return bool(o)
    if isinstance(o, (set, frozenset)): return sorted(o)
    if isinstance(o, np.ndarray): return o.tolist()
    raise TypeError(type(o))


# ---------------------------------------------------------------- static
def static():
    T = tables(); G = SS.dollar3_game(); X = G.R; n = len(X)
    M = SS.dom_M(X, 6); V = SS.symmetric_set(X, 6)
    lab = [SS.label(x) for x in X]; cat = T.cat
    Q, nprop, mult = DC.generator(X)
    pg = DC.stationary(Q)
    P = DC.uniform_successor(X, M); pu = DC.stationary(P)
    summ = lambda pi: {c: round(float(sum(pi[k] for k in range(n) if cat[k] == c)), 6) for c in sorted(set(cat))}
    Qa = Q.copy()
    for v in V:
        Qa[v] = 0; Qa[v, v] = 1
    ht = DC.hitting_times(Qa, V)
    ev = np.sort(np.abs(np.linalg.eigvals(Q)))[::-1]
    smr = DC.same_member_return(Q, V)
    out = dict(contracts=[DC.contract_label(k) for k in range(DC.NCON)],
               nprop={lab[y]: int(nprop[y]) for y in range(n)},
               multiplicity_max=int(mult.max()),
               generator_stationary={lab[k]: round(float(pg[k]), 6) for k in range(n)},
               generator_V=round(float(pg[list(V)].sum()), 6), generator_by_cat=summ(pg),
               uniform_successor_V=round(float(pu[list(V)].sum()), 6), uniform_successor_by_cat=summ(pu),
               second_eigenvalue=float(ev[1]), relaxation_draws=float(1 / (1 - ev[1])),
               hitting_draws={lab[k]: round(float(v), 3) for k, v in ht.items()},
               same_member_return={lab[k]: round(float(v), 4) for k, v in smr.items()})
    # thresholds for every dominating edge, every constant realization of y
    pay = G.pay
    th = defaultdict(list)
    idx = {x: k for k, x in enumerate(X)}
    for a in itertools.product(range(9), repeat=3):
        y = tuple(int(v) for v in pay[a]); yi = idx[y]
        if not (lab[yi].startswith('P12') or y == (2, 2, 2) or a == (8, 8, 8)):
            continue
        for k in range(DC.NCON):
            if not DC.proposed(k, y):
                continue
            bs, bf = DC.thresholds(pay, a, k)
            th['%s>%s' % (lab[yi], lab[idx[DC.contract_x(k)]])].append(dict(third=D.act_name(2, a[2]), static=bs, flow=bf))
    out['thresholds'] = th
    summary = {}
    for e, rows in th.items():
        ss = [r['static'] for r in rows]; ff = [r['flow'] for r in rows]
        summary[e] = dict(n=len(rows), static_max=max([v for v in ss if v is not None], default=None),
                          static_none=sum(v is None for v in ss),
                          flow_max=max([v for v in ff if v is not None], default=None),
                          flow_min=min([v for v in ff if v is not None], default=None), flow_none=sum(v is None for v in ff))
    out['threshold_summary'] = summary
    mem_exits = [v for e, v in summary.items() if e.startswith('P12:3|3>')]
    out['member_exit_flow_max'] = max(v['flow_max'] for v in mem_exits)
    out['member_exit_static_max'] = max(v['static_max'] for v in mem_exits)
    json.dump(out, open(os.path.join(ROOT, 'runs', 'dominance-contracts-static.json'), 'w'), indent=1, default=_js)
    print(json.dumps({k: v for k, v in out.items() if k not in ('thresholds',)}, indent=1, default=_js)[:5000])


# ---------------------------------------------------------------- forced edge assays
def assay_job(args):
    ykey, kap, beta, reps = args
    T = tables(); G = SS.dollar3_game(); X = G.R
    S, mu = SS.arm_data('weak'); ci = SS.const_index(S.fs)
    lo = D.local_of
    if ykey == 'X':
        prof = [(8, 8, 8)]
    elif ykey == 'G':
        prof = [(6, 6, 6)]
    else:
        a, b = ykey
        prof = [(lo(0, 1, a - 2), lo(1, 0, b - 2), k3) for k3 in range(9)]
    U = [np.array(sorted(ci[l] for l in range(9)), np.int64) for _ in range(3)]
    pos = {x: j for j, x in enumerate(U[0])}
    N = 100
    I = len(prof) * reps
    init = np.zeros((I, 3, 9), np.int64)
    for i in range(I):
        a = prof[i % len(prof)]
        for s in range(3):
            init[i, s, pos[ci[a[s]]]] = N
    st = DC.Setup(init, U)
    Sx, d0, d1 = DC.CONTRACTS[kap]
    CS, CD, CACT = DC.contract_arrays()
    nb = int(round(beta * N))
    tc = st.tc0.copy()
    for i in range(I):
        a = prof[i % len(prof)]
        for z, s in enumerate(Sx):
            k = pos[ci[a[s]]]
            t = st.tid(s, k, int(CACT[kap, z]), 0, -1)
            tc[i, s, k] -= nb; tc[i, s, t] += nb
    st.tc0 = tc
    y = tuple(int(v) for v in G.pay[prof[0]]); x = DC.contract_x(kap)
    seed = zlib.crc32(('assay|%s|%d|%d' % (ykey, kap, int(round(beta * 100)))).encode()) & 0x7fffffff
    out = DC.run_kernel(st, T, N, 0, seed, 4000, np.array([4000], np.int64), nu=0.0, stop_closed=True)
    cls = out[3]; stop = out[1]; pcount = out[15]
    fin = cls[stop]
    res = Counter()
    by_third = defaultdict(Counter)
    for i in range(I):
        c = int(fin[i])
        ov = [int(pcount[i, s, st.Kmax:].sum()) for s in Sx]
        lab = 'joint' if c == T.ridx[x] else ('reversal' if c == T.ridx[y] else 'other')
        side = 'both' if ov[0] == N and ov[1] == N else ('none' if ov[0] == 0 and ov[1] == 0 else
                                                          ('one' if N in ov and 0 in ov else 'poly'))
        res[lab] += 1; res['ov_' + side] += 1
        by_third[D.act_name(2, prof[i % len(prof)][2])][lab] += 1
    # immediate payoffs (sixths) at installation for the first realization
    c_ = {Sx[0]: int(CACT[kap, 0]), Sx[1]: int(CACT[kap, 1])}
    f = DC._fits(G.pay, prof[0], Sx, c_, {Sx[0]: beta, Sx[1]: beta})
    imm = {str(s + 1): dict(installed=round(f[s][1], 3), resident=round(f[s][0], 3)) for s in Sx}
    return dict(y=SS.label(y), x=SS.label(x), contract=DC.contract_label(kap), beta=beta, islands=I, stop=int(stop),
                status=int(out[0]), res=dict(res), by_third={k: dict(v) for k, v in by_third.items()}, immediate=imm)


def assays(procs=3):
    from multiprocessing import Pool
    G = SS.dollar3_game()
    ys = [(3, 3), (4, 2), (2, 4), (3, 2), (2, 3), (2, 2), 'G', 'X']
    jobs = []
    for yk in ys:
        if yk == 'G': y = (2, 2, 2)
        elif yk == 'X': y = (0, 0, 0)
        else: y = (yk[0], yk[1], 0)
        for kap in range(DC.NCON):
            if DC.proposed(kap, y):
                for beta in (0.25, 0.4, 0.5, 0.6, 0.75):
                    jobs.append((yk, kap, beta, 25 if yk not in ('G', 'X') else 200))
    t0 = time.time()
    with Pool(procs) as pool:
        res = pool.map(assay_job, jobs, chunksize=1)
    os.makedirs(OUT, exist_ok=True)
    json.dump(dict(rows=res, wall=time.time() - t0), open(os.path.join(OUT, 'assays.json'), 'w'), indent=1, default=_js)
    print('assays done in %.0fs' % (time.time() - t0))


# ---------------------------------------------------------------- validation
def validate():
    T = tables()
    res = []
    for (mN, law, H, I, N, sd) in [(0, 'L', 300, 8, 30, 1), (1, 'L', 200, 6, 30, 2), (1, 'K', 150, 8, 20, 3), (0, 'U', 200, 6, 25, 4)]:
        p = dict(law=law, mN=mN, arm='weak', I=I, N=N, name='val')
        loc, U, J, conds, I_, N_ = SR.build_run(p, sd)
        seed = 1000 + sd; hrec = np.array([H], np.int64)
        a = SS.kern(J, T.PAY, T.VEC, T.ISMEM, T.TOT, loc, N, SS.W, mN / N, seed, H, 10, hrec, 100000)
        st = DC.Setup(loc, U)
        b = DC.run_kernel(st, T, N, mN, seed, H, hrec, nu=0.0)
        K = loc.shape[2]
        same = bool(a[0] == b[0] and a[1] == b[1] and (a[2] == b[2][:, :, :K]).all() and (a[3] == b[3]).all()
                    and a[8] == b[8])
        res.append(dict(mN=mN, law=law, H=H, I=I, N=N, identical=same, status=int(b[0]), stop=int(b[1])))
        print(res[-1], flush=True)
    # bit-identity of the full baseline cells with the stored stable-sets runs (first 6 runs of each)
    base = {}
    for mN in (0, 1):
        ss = json.load(open(os.path.join(ROOT, 'runs', 'stable_sets', 'L%d.json' % mN)))['runs']
        ok = 0
        for r in range(6):
            rec = run_job(('B%d' % mN, r))
            a = ss[r]
            same = (rec['stop_gen'] == a['stop_gen'] and rec['status'] == a['status'] and rec['nmig'] == a['nmig'] and
                    all(rec['horizons'][h]['labels'] == {k: v for k, v in a['horizons'][h]['labels'].items()}
                        for h in a['horizons']))
            ok += same
        base['L%d' % mN] = ok
        print('baseline L%d identical runs %d/6' % (mN, ok), flush=True)
    # costs
    cost = {}
    for name in ('D1-0', 'D1-1', 'R1pub-0', 'R1pub-1', 'D3-1', 'D4-1'):
        t = time.time(); r = run_job((name, 999))
        cost[name] = dict(wall=r['wall'], total=time.time() - t, H=CELLS[name]['H'], counts=r['counts'],
                          ntypes=r['ntypes'])
        print(name, cost[name], flush=True)
    json.dump(dict(identity=res, baseline=base, cost=cost), open(os.path.join(ROOT, 'runs', 'dominance-contracts-validate.json'), 'w'),
              indent=1, default=_js)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('what')
    ap.add_argument('name', nargs='?')
    ap.add_argument('--procs', type=int, default=3)
    a = ap.parse_args()
    if a.what == 'static':
        static()
    elif a.what == 'validate':
        validate()
    elif a.what == 'assays':
        assays(a.procs)
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
