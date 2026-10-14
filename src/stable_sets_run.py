"""Driver for the stable-sets-on-islands experiment (notes/stable-sets-on-islands.md).

    python3 src/stable_sets_run.py static              # enumeration -> runs/stable-sets-static.json
    python3 src/stable_sets_run.py validate            # kernel identity with sog_lottery.kern, costs -> runs/stable-sets-validate.json
    python3 src/stable_sets_run.py cell NAME [--procs 2]
    python3 src/stable_sets_run.py all [--procs 2]
Per-run summaries go to runs/stable_sets/<cell>.json; per-run class sequences to runs/stable_sets/<cell>/r<k>.npz
(not committed).
"""
import argparse, itertools, json, os, sys, time, zlib
from collections import Counter, defaultdict
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stable_sets as SS
import dollar3 as D

ROOT = SS.ROOT
OUT = SS.OUT
HS = (500, 1000, 2000, 10000)
HMAX = 10000

# ---------------------------------------------------------------- cells
CELLS = {}
for mN in (0, 1):
    CELLS['L%d' % mN] = dict(law='L', mN=mN, arm='weak', seedbase='L%d' % mN)
    CELLS['M%d' % mN] = dict(law='M', mN=mN, arm='modalPA', seedbase='L%d' % mN)     # paired with L
    CELLS['U%d' % mN] = dict(law='U', mN=mN, arm='weak')
    CELLS['A%d' % mN] = dict(law='A', mN=mN, arm='weak')
    CELLS['K%d' % mN] = dict(law='K', mN=mN, arm='weak')
    for g in (6, 8):
        CELLS['X%d-%d' % (g, mN)] = dict(law='X', g=g, mN=mN)
    for Nn in (50, 200):
        CELLS['L%d-N%d' % (mN, Nn)] = dict(law='L', mN=mN, arm='weak', N=Nn, runs=20)
for tg in ('fair', 'unequal', 'wasteful', 'grand'):
    CELLS['Fe-' + tg] = dict(law='Fe', target=tg, mN=0, arm='weak', runs=20)
    CELLS['Fr-' + tg] = dict(law='Fr', target=tg, mN=1, arm='weak', runs=20)
ORDER = ['L0', 'L1', 'M0', 'M1', 'K0', 'K1', 'U0', 'U1', 'A0', 'A1',
         'Fe-fair', 'Fe-unequal', 'Fe-wasteful', 'Fe-grand', 'Fr-fair', 'Fr-unequal', 'Fr-wasteful', 'Fr-grand',
         'L0-N50', 'L1-N50', 'L0-N200', 'L1-N200', 'X6-0', 'X6-1', 'X8-0', 'X8-1']


def run_seed(base, r):
    return (zlib.crc32(('stable-sets|%s|%d' % (base, r)).encode()) & 0x7fffffff)


# ---------------------------------------------------------------- static data (cached per process)
_ST = {}


def static_data(g=None):
    key = g or 'd3'
    if key in _ST:
        return _ST[key]
    if g is None:
        G = SS.dollar3_game(); gg = 6
    else:
        G = SS.ext_game(g); gg = g
    T = SS.Tables(G)
    X = G.R
    M = SS.dom_M(X, gg)
    ks, ok = SS.kernels(M)
    Etu = SS.eff_tu(X, gg); Ftu = SS.indirect(X, Etu); ftu, _ = SS.kernels(Ftu)
    Eg = SS.eff_game(G, X); Fg = SS.indirect(X, Eg); fg, _ = SS.kernels(Fg)
    d = dict(G=G, T=T, X=X, M=M, stable=ks, far_tu=ftu, far_game=fg, g=gg)
    _ST[key] = d
    return d


# ---------------------------------------------------------------- one run
def build_run(p, r):
    rng = np.random.default_rng(run_seed(p.get('seedbase', p['name']), r))
    I = p.get('I', 64); N = p.get('N', 100)
    if p['law'] == 'X':
        g = p['g']; n = 3 * (g - 1)
        law = np.ones(n) / n
        init = SS.draw_seeds(rng, I, N, [law] * 3)
        loc, U = SS.compress(init)
        J = SS.ext_joint(g, U)
        conds = [np.zeros(len(u), bool) for u in U]
        return loc, U, J, conds, I, N
    S, mu = SS.arm_data('weak')
    if p['law'] == 'U':
        laws = [SS.seed_law('U', s, cat=rng.choice(len(mu), 160, replace=False)) for s in range(3)]
    elif p['law'] in ('Fe', 'Fr'):
        laws = [SS.seed_law('L', s) for s in range(3)]
    else:
        laws = [SS.seed_law(p['law'], s) for s in range(3)]
    init = SS.draw_seeds(rng, I, N, laws)
    if p['law'] in ('Fe', 'Fr'):
        ci = SS.const_index(S.fs)
        tc = SS.target_constants(p['target'])
        if p['law'] == 'Fe':
            nb = int(round(0.25 * N))
            for i in range(I):
                for s in range(3):
                    if tc[s] is None: continue
                    # replace nb uniformly chosen founders by the target constant
                    pop = np.repeat(np.arange(init.shape[2]), init[i, s])
                    rng.shuffle(pop)
                    pop[:nb] = ci[tc[s]]
                    init[i, s] = np.bincount(pop, minlength=init.shape[2])
        else:
            for i in range(I // 2):
                for s in range(3):
                    if tc[s] is None: continue
                    init[i, s] = 0; init[i, s, ci[tc[s]]] = N
    loc, U = SS.compress(init)
    J = SS.joint_for(p['arm'], U)
    conds = [S.nat[s, U[s]] > 0 for s in range(3)]
    return loc, U, J, conds, I, N


def run_job(args):
    name, r = args
    p = dict(CELLS[name]); p['name'] = name
    st = static_data(p.get('g'))
    T = st['T']
    loc, U, J, conds, I, N = build_run(p, r)
    seed = run_seed(p.get('seedbase', name), r) % (2 ** 31)
    hrec = np.array([h for h in HS if h <= HMAX], np.int64)
    t0 = time.time()
    status, stop, counts, cls, eff, dist, ev, nev, nmig = SS.kern(J, T.PAY, T.VEC, T.ISMEM, T.TOT, loc, N, SS.W,
                                                                    p['mN'] / N, seed, HMAX, 10, hrec, 2000000)
    wall = time.time() - t0
    os.makedirs(os.path.join(OUT, name), exist_ok=True)
    np.savez_compressed(os.path.join(OUT, name, 'r%d.npz' % r), cls=cls, ev=ev, eff=eff, dist=dist.astype(np.float32),
                        U0=U[0], U1=U[1], U2=U[2], counts=counts)
    rec = analyse_run(p, st, cls, ev, eff, dist, conds, U, status, stop, I)
    rec.update(cell=name, run=r, seed=int(seed), status=int(status), stop_gen=int(stop), nev=int(nev),
               nmig=int(nmig), wall=wall, K=[len(u) for u in U])
    return rec


# ---------------------------------------------------------------- analysis
def analyse_run(p, st, cls, ev, eff, dist, conds, U, status, stop, I):
    T = st['T']; X = st['X']; nout = len(X); g = st['g']
    cat = T.cat
    Vstar = SS.symmetric_set(X, g)
    stable = st['stable']
    far_tu = set().union(*st['far_tu']) if st['far_tu'] else set()
    far_g = set().union(*st['far_game']) if st['far_game'] else set()
    myo = set().union(*stable) if stable else set()
    rec = dict(horizons={})
    for hi, h in enumerate(HS):
        c = cls[h]
        d = {}
        cnt = Counter(int(x) for x in c)
        lab = Counter()
        for k, v in cnt.items():
            if k < nout: lab[T.labels[k]] += v
            elif k == nout: lab['MM'] += v
            else: lab['MO'] += v
        d['labels'] = dict(lab)
        cats = Counter()
        for k, v in cnt.items():
            cats[cat[k] if k < nout else ('member-mixed' if k == nout else 'other-mixed')] += v
        d['cats'] = {k: v / I for k, v in cats.items()}
        support = {k for k in cnt if k < nout}
        d['support'] = sorted(T.labels[k] for k in support)
        d['coverage'] = bool(Vstar <= support)
        d['n_members_present'] = len(Vstar & support)
        d['selection'] = [i for i, V in enumerate(stable) if support <= V]
        d['rs_strong'] = bool(len(d['selection']) > 0)
        d['rs_strong_nomixed'] = bool(d['rs_strong'] and cnt.get(nout + 1, 0) == 0)
        d['rs_weak'] = d['coverage']
        d['far_not_myopic'] = sum(v for k, v in cnt.items() if k < nout and (k in far_tu) and (k not in myo)) / I
        d['far_game_not_myopic'] = sum(v for k, v in cnt.items() if k < nout and (k in far_g) and (k not in myo)) / I
        d['in_no_stable_set'] = sum(v for k, v in cnt.items() if k < nout and k not in myo) / I
        nn = [v for k, v in cnt.items() if k < nout]
        d['consensus'] = bool(len(cnt) == 1 and next(iter(cnt)) < nout)
        d['resolved'] = bool(status in (1, 5) and stop <= h)
        # member islands per pair (role symmetry)
        mp = Counter()
        for k, v in cnt.items():
            if k < nout and k in Vstar:
                mp[T.labels[k][:3]] += v
        d['member_pairs'] = dict(mp)
        # time window: last 250 generations
        win = cls[max(0, h - 249):h + 1]
        wc = Counter()
        for k, v in zip(*np.unique(win, return_counts=True)):
            wc[cat[k] if k < nout else ('member-mixed' if k == nout else 'other-mixed')] += v / win.size
        d['window_cats'] = dict(wc)
        d['efficiency'] = float(eff[hi].mean())
        ds = dist[hi]
        supp_n = (ds >= 0.01).sum(1)
        nonmem = (ds[:, [k for k in range(nout) if k not in Vstar]] >= 0.01).any(1)
        d['payoff_support_mean_size'] = float(supp_n.mean())
        d['islands_with_nonmember_support'] = float(nonmem.mean())
        # slot-3 role in pairs (tilted cell): among islands on a pair containing slot 3, how often slot 3 gets the low share
        s3 = [X[k] for k in support]
        low = 0; tot = 0
        for k, v in cnt.items():
            if k < nout and cat[k] in ('fair', 'unequal', 'wasteful') and X[k][2] > 0:
                other = max(X[k][0], X[k][1])
                tot += v
                if X[k][2] < other: low += v
        d['slot3_pair_islands'] = tot; d['slot3_low'] = low
        # discriminatory-line elements: three-positive efficient allocations (and the degenerate (2,2,2))
        d['grand_islands'] = sum(v for k, v in cnt.items() if k < nout and cat[k].startswith('grand')) / I
        d['grand_unequal_islands'] = sum(v for k, v in cnt.items() if k < nout and cat[k] == 'grand-unequal') / I
        d['slot3_at_c_disc'] = sum(v for k, v in cnt.items() if k < nout and cat[k] == 'grand-unequal'
                                    and X[k][2] < min(X[k][0], X[k][1])) / I
        rec['horizons'][str(h)] = d
    # transience: first generation an island's class is a member (censored at stop/H)
    first_mem = []
    for i in range(I):
        hit = np.nonzero(np.isin(cls[:, i], list(Vstar)))[0]
        first_mem.append(int(hit[0]) if len(hit) else -1)
    rec['first_member'] = first_mem
    # dwell of the first visit to grand / wasteful outcomes
    dw = dict(grand=[], wasteful=[])
    for i in range(I):
        seq = cls[:, i]
        for key in ('grand', 'wasteful'):
            mask = np.array([(k < nout and cat[k].startswith('grand')) if key == 'grand' else (k < nout and cat[k] == 'wasteful') for k in range(nout + 2)])
            m = mask[seq]
            hit = np.nonzero(m)[0]
            if len(hit):
                t0 = hit[0]; t1 = t0
                while t1 + 1 < len(seq) and m[t1 + 1]:
                    t1 += 1
                censored = (t1 == len(seq) - 1) or (t1 >= stop)
                dw[key].append((int(t1 - t0 + 1), bool(censored)))
    rec['dwell_first_visit'] = dw
    if p['mN'] > 0:
        rec['flips'] = flips(st, cls, ev, conds, I)
    if p['law'] == 'Fr':
        rec['forced'] = forced_stats(st, cls, p['target'], I)
    if p['law'] == 'Fe':
        tg = forced_target_index(st, p['target'])
        rec['forced'] = {str(h): float((cls[h] == tg).mean()) for h in HS}
    return rec


def forced_target_index(st, target):
    X = st['X']
    x = dict(fair=(3, 3, 0), unequal=(4, 2, 0), wasteful=(2, 2, 0), grand=(2, 2, 2))[target]
    return X.index(x)


def forced_stats(st, cls, target, I):
    tg = forced_target_index(st, target)
    nout = len(st['X'])
    res = []; ent = []; nxt = Counter()
    for i in range(I):
        seq = cls[:, i]
        if i < I // 2:
            if seq[0] != tg:
                res.append((0, False)); continue
            t = 0
            # residence: until the island's class differs from the target for 25 consecutive generations
            bad = 0; t_exit = None
            for u in range(1, len(seq)):
                if seq[u] != tg:
                    bad += 1
                    if bad >= SS.HELD:
                        t_exit = u - SS.HELD + 1; break
                else:
                    bad = 0
            if t_exit is None:
                res.append((len(seq) - 1, True))
            else:
                res.append((t_exit, False))
                hr = SS.held_runs(seq[t_exit:], nout)
                if hr:
                    nxt[st['T'].labels[hr[0][0]]] += 1
        else:
            hr = [h for h in SS.held_runs(seq, nout) if h[0] == tg]
            ent.append((hr[0][1], False) if hr else (len(seq) - 1, True))
    return dict(residence=res, entry=ent, exits_to=dict(nxt))


def flips(st, cls, ev, conds, I):
    T = st['T']; X = st['X']; nout = len(X); M = st['M']
    Vstar = SS.symmetric_set(X, st['g'])
    cat = T.cat
    ev_by = defaultdict(list)
    for e in ev:
        ev_by[int(e[1])].append(e)
    out = Counter(); trig = Counter(); seqs = []
    mm_total = 0; mm_outsider = 0; mm_any_mixed_other = 0
    steps_out = 0; steps_out_arrow = 0; steps_all = 0; steps_arrow = 0
    trig_by_type = defaultdict(Counter)
    for i in range(I):
        seq = cls[:, i]
        hr = SS.held_runs(seq, nout)
        evs = sorted(ev_by[i], key=lambda e: e[0])

        def dom_at(t):
            dd = [-1, -1, -1]
            for e in evs:
                if e[0] > t: break
                dd[int(e[2])] = int(e[4])
            return dd
        for (ca, a0, a1), (cb, b0, b1) in zip(hr, hr[1:]):
            if ca == cb:
                continue
            ta, tb = cat[ca], cat[cb]
            typ = ('member' if ca in Vstar else ta) + '->' + ('member' if cb in Vstar else tb)
            out[typ] += 1
            inter = SS.segments(seq, a1 + 1, b0)
            path = [ca] + [c for c, l in inter if c < nout] + [cb]
            path = [c for k_, c in enumerate(path) if k_ == 0 or c != path[k_ - 1]]
            for x_, y_ in zip(path, path[1:]):
                steps_all += 1; steps_arrow += int(M[y_, x_])
                if x_ not in Vstar:
                    steps_out += 1; steps_out_arrow += int(M[y_, x_])
            if ca in Vstar and cb in Vstar:
                mm_total += 1
                if any((c < nout and c not in Vstar) for c, l in inter):
                    mm_outsider += 1
                if any(c == nout + 1 for c, l in inter):
                    mm_any_mixed_other += 1
            da, db = dom_at(a0), dom_at(b0)
            cond = any(conds[s][k] for s in range(3) for k in (da[s], db[s]) if k >= 0)
            tr, nch = SS.trigger(evs, a0, b0, cond)
            trig[tr] += 1; trig_by_type[typ][tr] += 1
            if len(seqs) < 30:
                lab = lambda c: T.labels[c] if c < nout else ('MM' if c == nout else 'MO')
                seqs.append(dict(island=i, gen=int(b0), type=typ, trigger=tr,
                                 path=[lab(ca)] + ['%s×%d' % (lab(c), l) for c, l in inter] + [lab(cb)]))
    return dict(by_type=dict(out), triggers=dict(trig), triggers_by_type={k: dict(v) for k, v in trig_by_type.items()},
                member_member=mm_total, member_member_via_outsider=mm_outsider,
                member_member_via_other_mixed=mm_any_mixed_other,
                steps_out_of_nonmember=steps_out, steps_out_following_arrow=steps_out_arrow,
                steps_all=steps_all, steps_all_arrow=steps_arrow, examples=seqs, n=int(sum(out.values())))


# ---------------------------------------------------------------- cells
def run_cell(name, procs=2):
    from multiprocessing import Pool
    p = CELLS[name]
    nr = p.get('runs', 40)
    jobs = [(name, r) for r in range(nr)]
    t0 = time.time()
    if procs > 1:
        with Pool(procs) as pool:
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


# ---------------------------------------------------------------- static report
def static():
    out = {}
    G = SS.dollar3_game(); X = G.R
    M = SS.dom_M(X, 6); C, byC = SS.dom_C(G.nact, G.pay, X)
    ks, ok = SS.kernels(M); kc, _ = SS.kernels(C)
    bk = SS.brute_kernels(M)
    A = np.array(X); n = len(X)
    Eg = SS.eff_game(G, X)
    def myo_game(sizes):
        Dm = np.zeros((n, n), bool)
        for S in SS.COALS:
            if len(S) not in sizes: continue
            pref = np.all(A[:, None, list(S)] > A[None, :, list(S)], axis=2)
            Dm |= pref & Eg[S].T
        return Dm
    Mg = myo_game((1, 2, 3)); Mg1 = myo_game((1,))
    kg, _ = SS.kernels(Mg); kg1, _ = SS.kernels(Mg1)
    Etu = SS.eff_tu(X, 6); Ftu = SS.indirect(X, Etu); ftu, _ = SS.kernels(Ftu); Ztu = SS.lcs(X, Etu, Ftu)
    Fg = SS.indirect(X, Eg); fg, _ = SS.kernels(Fg); Zg = SS.lcs(X, Eg, Fg)
    lab = [SS.label(x) for x in X]
    L = lambda ks_: [[lab[v] for v in sorted(k)] for k in ks_]
    out['R'] = dict(outcomes=lab, n=n, C_equals_M=bool((C == M).all()), singleton_C=bool(byC[1].any()),
                    M_stable=L(ks), M_complete=ok, M_brute=L(bk), C_stable=L(kc), undominated=[lab[v] for v in range(n) if not M[:, v].any()],
                    game_eff_myopic_all=L(kg), game_eff_myopic_singletons=L(kg1),
                    farsighted_tu=L(ftu), lcs_tu=[lab[v] for v in np.nonzero(Ztu)[0]],
                    farsighted_game=L(fg), lcs_game=[lab[v] for v in np.nonzero(Zg)[0]])
    # membership table
    tab = []
    for v in range(n):
        tab.append(dict(outcome=lab[v], category=SS.category(X[v], 6), dominated_M=bool(M[:, v].any()),
                        dominators=[lab[u] for u in range(n) if M[u, v]],
                        in_M_sets=[k for k, V in enumerate(ks) if v in V], in_far_tu=[k for k, V in enumerate(ftu) if v in V],
                        in_far_game=[k for k, V in enumerate(fg) if v in V],
                        in_game_singleton_set=[k for k, V in enumerate(kg1) if v in V]))
    out['R']['membership'] = tab
    for name, Xg, g in [('G6=', SS.grid(6, True), 6), ('G6', SS.grid(6), 6), ('G8=', SS.grid(8, True), 8), ('G8', SS.grid(8), 8)]:
        Mx = SS.dom_M(Xg, g); kx, okx = SS.kernels(Mx)
        V = SS.symmetric_set(Xg, g)
        disc_lines = {}
        for k in range(3):
            for c in range(0, g):
                line = [j for j, x in enumerate(Xg) if x[k] == c and sum(x) == g]
                disc_lines['%d,%d' % (k + 1, c)] = dict(stable=SS.is_stable(Mx, line))
        lab_ = [SS.label(x) for x in Xg]
        out[name] = dict(n=len(Xg), stable=[[lab_[v] for v in sorted(k)] for k in kx], complete=okx,
                         symmetric_stable=SS.is_stable(Mx, V), exact_lines_stable=sum(v['stable'] for v in disc_lines.values()),
                         discriminatory_sets=sum(1 for kk in kx if any(m >= 3 for m in SS.discriminatory_counts(Xg, g, kk).values())))
    for g in (6, 8):
        Gx = SS.ext_game(g); Xx = Gx.R
        Mx = SS.dom_M(Xx, g); Cx, _ = SS.dom_C(Gx.nact, Gx.pay, Xx)
        kx, okx = SS.kernels(Mx); kcx, okc = SS.kernels(Cx)
        Ex = SS.eff_tu(Xx, g); Fx = SS.indirect(Xx, Ex); fx, okf = SS.kernels(Fx, cap=5000)
        Egx = SS.eff_game(Gx, Xx); Fgx = SS.indirect(Xx, Egx); fgx, okfg = SS.kernels(Fgx, cap=5000)
        lab_ = [SS.label(x) for x in Xx]
        out['R%dx' % g] = dict(n=len(Xx), C_subset_M=bool((Cx & ~Mx).sum() == 0), M_minus_C=int((Mx & ~Cx).sum()),
                               M_stable=[[lab_[v] for v in sorted(k)] for k in kx], C_stable=[[lab_[v] for v in sorted(k)] for k in kcx],
                               farsighted_tu_count=len(fx), farsighted_tu_complete=okf,
                               farsighted_tu_examples=[[lab_[v] for v in sorted(k)] for k in fx[:12]],
                               farsighted_game_count=len(fgx), farsighted_game_complete=okfg,
                               farsighted_game_examples=[[lab_[v] for v in sorted(k)] for k in fgx[:12]])
    # chicken
    pay = SS.chicken_game(); Xc = [(-10, -10), (2, -1), (-1, 2), (0, 0)]
    Cc, _ = SS.dom_C((2, 2), pay, Xc, players=2); kc2, _ = SS.kernels(Cc)
    out['chicken'] = dict(outcomes=['crash', 'R1', 'R2', 'swerve'], C_stable=[[['crash', 'R1', 'R2', 'swerve'][v] for v in sorted(k)] for k in kc2])
    json.dump(out, open(os.path.join(ROOT, 'runs', 'stable-sets-static.json'), 'w'), indent=1, default=_js)
    print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk not in ('membership',)} for k, v in out.items()}, indent=1, default=_js)[:6000])


# ---------------------------------------------------------------- validation: identity with sog_lottery.kern
def validate():
    import sog_lottery as SL
    res = []
    st = static_data(None); T = st['T']
    for (mN, law, H, I, N, sd) in [(0, 'L', 300, 8, 30, 1), (1, 'L', 200, 6, 30, 2), (1, 'K', 150, 8, 20, 3), (0, 'U', 200, 6, 25, 4)]:
        p = dict(law=law, mN=mN, arm='weak', I=I, N=N, name='val');
        loc, U, J, conds, I_, N_ = build_run(p, sd)
        ncode = T.PAY.shape[0]
        PAY4 = T.PAY.reshape(ncode, 1, 1, 3).copy()
        T4 = np.zeros((ncode, 1, 1, 27)); KEYT = np.arange(ncode, dtype=np.int64).reshape(ncode, 1, 1)
        K = loc.shape[2]
        LB = np.zeros((0, K), np.bool_); LW = np.zeros((0, K), np.bool_)
        checks = np.arange(1, H + 1, dtype=np.int64)
        seed = 1000 + sd
        a = SL.kern(np.ascontiguousarray(J.astype(np.int64)), np.zeros(K, np.int64), PAY4, T4, KEYT, LB, LW, loc, N, SS.W,
                    mN / N, seed, checks, min(H, 50), H // 2)
        b = SS.kern(J, T.PAY, T.VEC, T.ISMEM, T.TOT, loc, N, SS.W, mN / N, seed, H, 1, np.array([H], np.int64), 100000)
        same = bool(a[0] == b[0] or (a[0] == 4 and b[0] == 4)) and int(a[1]) == int(b[1]) and bool((a[2] == b[2]).all())
        res.append(dict(mN=mN, law=law, H=H, I=I, N=N, sog_status=int(a[0]), sog_stop=int(a[1]), status=int(b[0]),
                        stop=int(b[1]), counts_identical=bool((a[2] == b[2]).all()), identical=same, nmig=(int(a[8]), int(b[8]))))
        print(res[-1], flush=True)
    # costs
    cost = {}
    for name in ('L0', 'L1', 'X8-1'):
        t = time.time(); r = run_job((name, 999)); cost[name] = dict(wall=r['wall'], total=time.time() - t, K=r['K'],
                                                                     status=r['status'], stop=r['stop_gen'])
        print(name, cost[name], flush=True)
    json.dump(dict(identity=res, cost=cost), open(os.path.join(ROOT, 'runs', 'stable-sets-validate.json'), 'w'), indent=1,
              default=_js)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('what')
    ap.add_argument('name', nargs='?')
    ap.add_argument('--procs', type=int, default=2)
    a = ap.parse_args()
    if a.what == 'static':
        static()
    elif a.what == 'validate':
        validate()
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
