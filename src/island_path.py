"""A path in (N, I, mN) on which islands nucleate independently and rival networks still resolve.
Spec specs/2026-10-05-island-path.md (reviewed, reviews/2026-10-05-island-path-gpt-6.1-sol.md);
predictions predictions/2026-10-05-island-path.md.

Kernel: rival_islands._kern (exact skipping, lumping, ancestry labels), with the propagule option kprop added there
(kprop = 1 is the single-migrant kernel draw for draw; tests/check_rival_kernel_identity.py).  Modal arm, n = 9,
PD, w = 0.3, eps = 0, iid seeds from the length prior, complete island graph, horizon 1e5 generations of I*N births.

Definitions (spec, [after review]):
  nucleation event   first check at which an island is certified (locally frozen, every present class cooperative);
                     the holder (plurality class) is then a certified cooperator.  T_nuc(N) = median nucleation time
                     over nucleating islands in m = 0 iid runs (I = 16), distribution reported.
  boundary path      mN(N) = 0.3 * N / T_nuc(N).
  q (holder form)    sum over runs of islands whose horizon holder has local ancestry (island established with >= 0.5
                     of the holder class local-labelled, and the horizon holder is that class up to exact lumping),
                     divided by the same count in the m = 0 reference with the same initial seeds (same N, I, rep).
                     Measured on iid runs only.  q_est (the rival run's form: local establishments / m = 0) reported too.
  both-present       both rival networks (tags 1, 2) hold >= 1 island (holder rule) at the horizon or stop.
  separation loss    first check at which tag 1 or tag 2 holds no island; hazard = losses / sum over runs of the
                     integral of min(held_A, held_B) dt up to the loss (per minority-island-generation).
  invasion           a strong-holder change (a class reaching >= 0.9 of an island) between different tags.
  global resolution  every island held by one tag at the horizon or stop.
  propagule          kprop offspring drawn without replacement (fitness-weighted per individual) from one uniformly
                     chosen other island replace kprop uniformly chosen residents of the recipient at once; donors keep
                     theirs; mN/kprop events per island-generation.

    python3 src/island_path.py static              # statics -> runs/island-path-static.json
    python3 src/island_path.py validate            # unskipped reference + default-kernel regression -> runs/island-path-validate.json
    python3 src/island_path.py run --exp E         # E in cal, path, pathq, nat, prop, propq, bridge
    python3 src/island_path.py calib               # T_nuc and the boundary -> runs/island-path-calib.json
    python3 src/island_path.py merge               # merge test on N = 200 both-present end states
    python3 src/island_path.py report              # runs/island-path.md and runs/island-path.json
"""
import argparse, gzip, json, math, os, sys, time
from collections import Counter, defaultdict
import numpy as np
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(__file__))
from numba import njit
import rival_islands as R

RUNS = R.RUNS
W = R.W
GENS = 100000
SALT = 20261006
BRIDGE = 'BOX1(THEM(THEM))'
PAIRNAME = {0: 'pair 1 (bridge)', 2: 'pair 3 (P*, no bridge)'}
CALIB = os.path.join(RUNS, 'island-path-calib.json')
EXPS = ('cal', 'path', 'pathq', 'nat', 'prop', 'propq', 'bridge', 'time')
PRESETS = ('iid', 'AB', 'ABbridge', 'bridge', 'AAbridge')


# ------------------------------------------------------------------ seeds and initial states
def seeds(exp, N, I, mN, k, rep, pair, preset):
    """Initial state depends only on (N, I, rep, pair, preset): m = 0 references, k cells and the path share it."""
    pc = PRESETS.index(preset); pn = 9 if pair is None else pair
    rs = [SALT, N, I, rep, pn, pc]
    ss = (1000003 * rep + 7919 * EXPS.index(exp) + 104729 * pc + 13 * N + 17 * I + int(round(mN * 1000)) + 31 * k
          + 101 * (pn + 1) + SALT) % (2 ** 31 - 1)
    return rs, ss


def build_init(d, N, I, pair, preset, rng):
    if preset in ('iid', 'AB'):
        return R.build_init(d, N, I, pair, preset, rng)
    K = len(d['mu'])
    A = d['idx'][R.PAIRS[pair][0]]; B = d['idx'][R.PAIRS[pair][1]]; X = d['idx'][BRIDGE]
    init = np.zeros((I, K), np.int64); pre = np.zeros(I, np.int64)
    for i in range(I):
        init[i] = rng.multinomial(N, d['mu'])
    fill = {'ABbridge': (A, B, X), 'bridge': (X,), 'AAbridge': (A, A, X)}[preset]
    for i, c in enumerate(fill):
        init[i] = 0; init[i, c] = N; pre[i] = 1
    return init, pre, A, B


def boundary():
    c = json.load(open(CALIB))
    return {int(k): v for k, v in c['mN_boundary'].items()}


# ------------------------------------------------------------------ one run
def integ(trace, col_a, col_b, t_end):
    """Integral of min(held_A, held_B) dt over [0, t_end] from check rows (piecewise constant, left value; the
    interval before the first check uses the first row)."""
    g = trace[:, 0]; m = np.minimum(trace[:, col_a], trace[:, col_b])
    tot = 0.0; prev_t = 0.0; prev_v = m[0] if len(m) else 0.0
    for t, v in zip(g, m):
        if t > t_end:
            break
        tot += prev_v * (t - prev_t); prev_t = t; prev_v = v
    tot += prev_v * max(0.0, t_end - prev_t)
    return float(tot)


def job(j):
    exp, N, I, mN, k, rep, gens, pair, preset = j
    d = R.cls(9); nm = d['names']
    rs, ss = seeds(exp, N, I, mN, k, rep, pair, preset)
    rng = np.random.default_rng(rs)
    init, pre, A, B = build_init(d, N, I, pair, preset, rng)
    t0 = time.time()
    sup, U, PCC, coop, tag = R.restrict(d, init, A, B)
    li = np.ascontiguousarray(init[:, sup]); K = len(sup)
    rr = np.random.default_rng(ss); r1 = rr.random(K); r2 = rr.random(K)
    iDl = int(np.searchsorted(sup, d['iD'])) if d['iD'] in set(sup.tolist()) else -1
    o = R._kern(U, PCC, coop, tag, li, N, W, mN / N, ss, R.checks_schedule(gens), True, iDl, r1, r2, pre, int(k))
    (st, sg, counts, isl_cc, isl_pay, trace, t_ext, held_zero, parent, t_est, e_arr, e_arrC, e_arrD, e_imm, e_hold, e_hloc,
     t90, a90, imm90, h90, hl90, arr_all, loss_log, nloss, first_sep, sep_a, sep_b, nsepchk, tr_log, ntr, mig_ct) = o
    G = lambda x: nm[int(sup[x])] if x >= 0 else None
    root = np.arange(K)
    for x in range(K):
        r_ = x
        while parent[r_] != r_: r_ = parent[r_]
        root[x] = r_
    glob = counts.sum(0)
    hold = np.array([R.holder(counts[i]) for i in range(I)])
    htag = tag[hold]
    estd = t_est >= 0; bg = pre == 0
    loc_est = estd & (e_hloc >= 0.5)
    loc_end = loc_est & (root[np.maximum(e_hold, 0)] == hold)
    x = glob / glob.sum(); pr = np.nonzero(x)[0]
    cf = float(x[pr] @ PCC[np.ix_(pr, pr)] @ x[pr])
    r = dict(exp=exp, n=9, N=N, I=I, mN=mN, k=int(k), rep=rep, gens=gens, pair=pair, preset=preset,
             status=R.STATUS[int(st)], stop_gen=int(sg), pcc=float(isl_cc.mean()), pay=float(isl_pay.mean()), cf_cross_pcc=cf,
             isl_eff=int((isl_cc >= 0.95).sum()),
             held_final={str(t): int((htag == t).sum()) for t in range(4)},
             t_ext=[float(v) for v in t_ext], held_zero=[int(v) for v in held_zero],
             n_bg=int(bg.sum()), n_est_bg=int((estd & bg).sum()), n_loc_est_bg=int((loc_est & bg).sum()),
             n_loc_end_bg=int((loc_end & bg).sum()), n_hold_coop=int(coop[hold].sum()),
             mig_ct=mig_ct.tolist(), n_tr=int(ntr), time_s=0.0)
    # invasions: strong-holder changes between tags, by direction (old tag, new tag); old = -1 for a first strong holder
    inv = Counter(); nuc = Counter()
    for g_, i_, a_, b_ in tr_log:
        if a_ < 0:
            nuc[int(tag[b_])] += 1
        elif tag[a_] != tag[b_]:
            inv['%d>%d' % (tag[a_], tag[b_])] += 1
    r['inv'] = dict(inv); r['first_strong'] = {str(t): v for t, v in nuc.items()}
    if pair is not None:
        hz = [v for v in (held_zero[1], held_zero[2]) if v >= 0]
        tl = min(hz) if hz else None
        r['loss_t'] = tl
        r['loss_net'] = None if tl is None else (1 if held_zero[1] == tl else 2)
        r['expo'] = integ(trace, 3, 4, tl if tl is not None else float(sg))
        r['expo_A'] = float(np.sum(np.diff(np.concatenate([[0.0], trace[:, 0]])) * trace[:, 3]))
        r['expo_B'] = float(np.sum(np.diff(np.concatenate([[0.0], trace[:, 0]])) * trace[:, 4]))
        g_ = trace[:, 0]
        grid = sorted(set(int(np.searchsorted(g_, v)) for v in np.unique(np.round(np.logspace(1, 5, 41)))))
        grid = [q for q in grid if q < len(trace)]
        r['trace'] = trace[grid][:, [0, 3, 4, 12, 7, 9]].round(3).tolist()     # g, heldA, heldB, heldBridge, ncert, cc
    # natural-run timing: first establishment, first immigrant-founded establishment, first rival establishment
    order = sorted([i for i in range(I) if estd[i] and bg[i]], key=lambda i: t_est[i])
    r['t_first_est'] = int(t_est[order[0]]) if order else -1
    r['t_first_imm'] = next((int(t_est[i]) for i in order if e_hloc[i] < 0.5), -1)
    t2 = -1; seen = []
    for i in order:
        h = int(e_hold[i])
        if any(U[h, s_] == -1 and U[s_, h] == -1 for s_ in seen):
            t2 = int(t_est[i]); break
        seen.append(h)
    r['t_rival_est'] = t2
    if exp in ('nat', 'time'):
        hc = sorted({int(h) for i, h in enumerate(hold) if isl_cc[i] >= 0.95 and coop[h]})
        sep_end = [(a, b) for ai, a in enumerate(hc) for b in hc[ai + 1:] if U[a, b] == -1 and U[b, a] == -1]
        r['first_sep'] = int(first_sep); r['n_sep_end'] = len(sep_end)
        r['sep_end_pair'] = (G(sep_end[0][0]), G(sep_end[0][1])) if sep_end else None
        if first_sep >= 0:
            a, b = int(root[sep_a]), int(root[sep_b])
            br = [bool(coop[h] and U[h, a] == 0 and U[a, h] == 0 and U[h, b] == 0 and U[b, h] == 0) for h in hold]
            r['first_sep_pair'] = (G(sep_a), G(sep_b))
            r['bridge_share_end'] = float(np.mean(br))
            r['sep_share_end'] = [float(np.mean(hold == a)), float(np.mean(hold == b))]
        r['holders'] = Counter(G(h) for h in hold).most_common(6)
    if (pair is not None and mN > 0 and st in (3, 4) and int((htag == 1).sum()) > 0 and int((htag == 2).sum()) > 0) or \
            (exp == 'nat' and r.get('n_sep_end', 0) > 0):
        r['end_counts'] = {G(x_): counts[:, x_].tolist() for x_ in np.nonzero(glob)[0]}
        r['end_tag'] = {G(x_): int(tag[x_]) for x_ in np.nonzero(glob)[0]}
    if I <= 64:
        r['isl'] = dict(t_est=t_est.tolist(), hloc=[round(float(v), 3) for v in e_hloc], htag_end=htag.tolist(),
                        etag=[int(tag[h]) if h >= 0 else -1 for h in e_hold], loc_end=loc_end.astype(int).tolist())
    r['time_s'] = time.time() - t0
    return r


# ------------------------------------------------------------------ cells
def cells(exp):
    """(exp, N, I, mN, k, reps, pair, preset)."""
    out = []
    if exp == 'cal':
        for N in (100, 200, 400):
            out.append(('cal', N, 16, 0.0, 1, 120, None, 'iid'))
            out.append(('cal', N, 64, 0.0, 1, 40, None, 'iid'))
        return out
    if exp == 'time':
        return out
    B = boundary()
    if exp == 'path':
        for N in (100, 200, 400):
            for I in (16, 64):
                for p in (2, 0):
                    out.append(('path', N, I, B[N], 1, 40, p, 'AB'))
    elif exp == 'pathq':
        for N in (100, 200, 400):
            for I in (16, 64):
                out.append(('pathq', N, I, B[N], 1, 120 if I == 16 else 40, None, 'iid'))
    elif exp == 'nat':
        for N in (100, 200):
            for I in (64, 256):
                out.append(('nat', N, I, B[N], 1, 100 if (N, I) == (200, 256) else 300, None, 'iid'))
    elif exp == 'prop':        # k = 1 cells are the path cells at I = 16 (same seeds), not rerun
        for N, ks in ((200, (10, 30)), (400, (10, 30, 60))):
            for k in ks:
                for p in (2, 0):
                    out.append(('prop', N, 16, B[N], k, 40, p, 'AB'))
    elif exp == 'propq':
        for N, ks in ((200, (10, 30)), (400, (10, 30, 60))):
            for k in ks:
                out.append(('propq', N, 16, B[N], k, 120, None, 'iid'))
    elif exp == 'bridge':
        for mN in (0.1, 1.0):
            for preset in ('ABbridge', 'bridge', 'AAbridge'):
                out.append(('bridge', 100, 16, mN, 1, 40, 0, preset))
    return out


def rows_path(exp):
    return os.path.join(RUNS, 'island-path-rows-%s.json.gz' % exp)


def load(exp):
    p = rows_path(exp)
    return json.load(gzip.open(p, 'rt')) if os.path.exists(p) else []


def save(exp, rows):
    json.dump(rows, gzip.open(rows_path(exp), 'wt'))


def ckey(r):
    return (r['exp'], r['N'], r['I'], r['mN'], r['k'], r['pair'], r['preset'])


def warm():
    R.cls(9)
    job(('time', 20, 4, 1.0, 1, 0, 50, 0, 'AB'))
    job(('time', 20, 4, 1.0, 3, 0, 50, 0, 'AB'))


def run_main(a):
    exp = a.exp
    rows = load(exp)
    done = Counter(ckey(r) for r in rows)
    jobs = []
    for c in cells(exp):
        e, N, I, mN, k, reps, pair, preset = c
        key = (e, N, I, mN, k, pair, preset)
        for rep in range(done[key], reps):
            jobs.append((e, N, I, mN, k, rep, a.gens, pair, preset))
    jobs.sort(key=lambda j: -j[1] * j[2] * (1 + j[3]))
    print('%d jobs' % len(jobs), flush=True)
    t0 = time.time(); cell_t = Counter()
    with Pool(a.procs, initializer=warm) as pool:
        for r in pool.imap_unordered(job, jobs):
            rows.append(r); cell_t[ckey(r)] += r['time_s']
            print('%s N=%d I=%d mN=%g k=%d pair=%s %s rep %d: %s gen %d pcc %.3f held %s loss %s (%.1fs; %.0fs total)' % (
                r['exp'], r['N'], r['I'], r['mN'], r['k'], r['pair'], r['preset'], r['rep'], r['status'], r['stop_gen'],
                r['pcc'], r['held_final'], r.get('loss_t'), r['time_s'], time.time() - t0), flush=True)
            if len(rows) % 50 == 0:
                save(exp, rows)
    save(exp, rows)
    for kk, v in sorted(cell_t.items(), key=str):
        print('cell %s: %.0f worker-seconds' % (kk, v))


# ------------------------------------------------------------------ calibration
def calib_main(a):
    rows = load('cal')
    out = dict(T_nuc={}, dist={}, p={}, mN_boundary={}, n_nuc={})
    for N in (100, 200, 400):
        rs = [r for r in rows if r['N'] == N and r['I'] == 16]
        ts = np.array([t for r in rs for t in r['isl']['t_est'] if t >= 0], float)
        nis = sum(r['n_bg'] for r in rs)
        T = float(np.median(ts))
        out['T_nuc'][str(N)] = T
        out['n_nuc'][str(N)] = [int(len(ts)), int(nis)]
        out['p'][str(N)] = float(len(ts) / nis)
        out['dist'][str(N)] = {str(q): float(np.percentile(ts, q)) for q in (5, 10, 25, 50, 75, 90, 95)}
        out['mN_boundary'][str(N)] = round(0.3 * N / T, 3)
        # bootstrap over runs for the median
        rng = np.random.default_rng(1)
        per = [np.array([t for t in r['isl']['t_est'] if t >= 0]) for r in rs]
        bs = []
        for _ in range(2000):
            idx = rng.integers(0, len(per), len(per))
            v = np.concatenate([per[i] for i in idx])
            if len(v): bs.append(np.median(v))
        out['dist'][str(N)]['median_ci'] = [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))]
    xs = np.log([100, 200, 400]); ys = np.log([out['T_nuc'][str(N)] for N in (100, 200, 400)])
    out['T_nuc_exponent'] = float(np.polyfit(xs, ys, 1)[0])
    json.dump(out, open(CALIB, 'w'), indent=1)
    print(json.dumps(out, indent=1))


# ------------------------------------------------------------------ statics
@njit(cache=True)
def _moran2(N, k, w, uqq, uqa, uaq, uaa, reps, seed):
    """Two-type Moran birth-death with the kernel's law: parent ~ count * exp(w * mean payoff, self excluded),
    victim uniform.  Returns the number of runs in which k invaders q fix against resident a."""
    np.random.seed(seed)
    fix = 0
    for r in range(reps):
        j = k
        while 0 < j < N:
            fq = ((j - 1) * uqq + (N - j) * uqa) / (N - 1)
            fa = (j * uaq + (N - j - 1) * uaa) / (N - 1)
            m = max(fq, fa)
            wq = j * np.exp(w * (fq - m)); wa = (N - j) * np.exp(w * (fa - m))
            par_q = np.random.random() * (wq + wa) < wq
            vic_q = np.random.random() * N < j
            if par_q and not vic_q: j += 1
            elif vic_q and not par_q: j -= 1
        if j == N: fix += 1
    return fix


def static_main(a):
    d = R.cls(9); V = d['V']; ix = d['idx']; P = R.PDP
    A = ix[R.PAIRS[0][0]]; B1 = ix[R.PAIRS[0][1]]; B3 = ix[R.PAIRS[2][1]]; X = ix[BRIDGE]
    names = {'A': A, 'B1': B1, 'B3': B3, 'bridge': X}
    def pay(x, y): return float(P[V[x, y], V[y, x]])
    dirs = [('A', 'B1'), ('B1', 'A'), ('A', 'B3'), ('B3', 'A'), ('bridge', 'A'), ('A', 'bridge'), ('bridge', 'B1'), ('B1', 'bridge'),
            ('bridge', 'B3'), ('B3', 'bridge')]
    out = dict(classes={k: d['names'][v] for k, v in names.items()},
               payoffs={'%s|%s' % (x, y): pay(names[x], names[y]) for x in names for y in names}, cells=[])
    reps = a.reps
    jobs = []
    for N in (100, 200, 400):
        for (q, r_) in dirs:
            for k in (1, 10, 30, 60):
                jobs.append((N, q, r_, k))
    for N, q, r_, k in jobs:
        x, y = names[q], names[r_]
        uqq, uqa, uaq, uaa = pay(x, x), pay(x, y), pay(y, x), pay(y, y)
        ex = R.fix_k(N, W, k, uqq, uqa, uaq, uaa)
        t0 = time.time()
        f = int(_moran2(N, k, W, uqq, uqa, uaq, uaa, reps, 1000 * N + 7 * k + 31 * dirs.index((q, r_))))
        from rival_islands_report import wilson
        lo, hi = wilson(f, reps)
        out['cells'].append(dict(N=N, invader=q, resident=r_, k=k, exact=ex, sim=f, reps=reps, ci=[lo, hi],
                                 inside=bool(lo <= ex <= hi) or (f == 0 and ex < 3.0 / reps), time_s=time.time() - t0))
        print('N=%d %s into %s k=%d: exact %.3g sim %d/%d [%.3g, %.3g] (%.1fs)' % (N, q, r_, k, ex, f, reps, lo, hi, time.time() - t0), flush=True)
    json.dump(out, open(os.path.join(RUNS, 'island-path-static.json'), 'w'), indent=1)


# ------------------------------------------------------------------ unskipped reference (propagule batch path)
@njit(cache=True)
def _ref(U, coopmask, tag, init, N, w, m, kprop, gens, seed, preest):
    """Plain simulation, no skipping, no lumping: every birth drawn; stops at global outcome-freezing as the kernel does.  Propagule events with probability m/kprop per
    birth.  Returns end counts, establishment times (checks every 5 generations), local share of the holder at
    establishment, and the first generation at which tags 1 / 2 hold no island."""
    np.random.seed(seed)
    I, K = init.shape
    counts = init.copy(); loc = init.copy()
    est = preest.copy(); t_est = -np.ones(I, np.int64); hloc = -np.ones(I)
    for i in range(I):
        if preest[i] == 1:
            t_est[i] = 0; hloc[i] = 1.0
    held_zero = -np.ones(4, np.int64)
    mp = m / kprop
    rem = np.zeros(K, np.int64); vic = np.zeros(K, np.int64)
    fit = np.zeros(K)
    for g in range(1, gens + 1):
        for b in range(I * N):
            i = np.random.randint(I)
            if I > 1 and np.random.random() < mp:
                src = np.random.randint(I - 1)
                if src >= i: src += 1
                for x in range(K):
                    if counts[src, x] > 0:
                        f = 0.0
                        for y in range(K): f += counts[src, y] * U[x, y]
                        fit[x] = np.exp(w * (f - U[x, x]) / (N - 1))
                    rem[x] = counts[src, x]; vic[x] = 0
                ch = np.zeros(K, np.int64)
                for z in range(kprop):
                    tot = 0.0
                    for x in range(K): tot += rem[x] * fit[x]
                    u = np.random.random() * tot; acc = 0.0; c = -1
                    for x in range(K):
                        if rem[x] > 0: c = x
                    for x in range(K):
                        acc += rem[x] * fit[x]
                        if u <= acc and rem[x] > 0:
                            c = x; break
                    rem[c] -= 1; ch[c] += 1
                nleft = N
                for z in range(kprop):
                    u2 = np.random.randint(nleft); acc2 = 0; v = -1
                    for x in range(K):
                        acc2 += counts[i, x] - vic[x]
                        if u2 < acc2:
                            v = x; break
                    vic[v] += 1; nleft -= 1
                for x in range(K):
                    for z in range(vic[x]):
                        if est[i] == 0 and np.random.random() * (counts[i, x] - z) < loc[i, x]:
                            loc[i, x] -= 1
                    counts[i, x] -= vic[x]
                for x in range(K):
                    counts[i, x] += ch[x]
            else:
                tot = 0.0
                for x in range(K):
                    if counts[i, x] > 0:
                        f = 0.0
                        for y in range(K): f += counts[i, y] * U[x, y]
                        fit[x] = np.exp(w * (f - U[x, x]) / (N - 1))
                        tot += counts[i, x] * fit[x]
                u = np.random.random() * tot; acc = 0.0; c = -1
                for x in range(K):
                    if counts[i, x] > 0:
                        c = x
                        acc += counts[i, x] * fit[x]
                        if u <= acc: break
                u2 = np.random.randint(N); acc2 = 0; v = -1
                for x in range(K):
                    acc2 += counts[i, x]
                    if u2 < acc2:
                        v = x; break
                if est[i] == 0:
                    cl = 1 if np.random.random() * counts[i, c] < loc[i, c] else 0
                    vl = 1 if np.random.random() * counts[i, v] < loc[i, v] else 0
                    loc[i, v] -= vl; loc[i, c] += cl
                counts[i, v] -= 1; counts[i, c] += 1
        if g % 5 == 0:
            held = np.zeros(4, np.int64)
            for i in range(I):
                big = 0
                for x in range(K):
                    if counts[i, x] > counts[i, big]: big = x
                held[tag[big]] += 1
                if est[i] == 0:
                    lo = 1e300; hi = -1e300; allco = True
                    for x in range(K):
                        if counts[i, x] == 0: continue
                        if not coopmask[x]: allco = False
                        for y in range(K):
                            if counts[i, y] == 0: continue
                            if U[x, y] < lo: lo = U[x, y]
                            if U[x, y] > hi: hi = U[x, y]
                    if hi - lo < 1e-12 and allco:
                        est[i] = 1; t_est[i] = g; hloc[i] = loc[i, big] / counts[i, big]
            for t in range(1, 3):
                if held[t] == 0 and held_zero[t] < 0: held_zero[t] = g
            # the kernel's stopping rule: globally outcome-frozen (every present class pairwise payoff-identical)
            lo = 1e300; hi = -1e300
            for x in range(K):
                if counts[:, x].sum() == 0: continue
                for y in range(K):
                    if counts[:, y].sum() == 0: continue
                    if U[x, y] < lo: lo = U[x, y]
                    if U[x, y] > hi: hi = U[x, y]
            if hi - lo < 1e-12:
                break
    return counts, t_est, hloc, held_zero


def _vjob(j):
    impl, preset, pair, N, I, mN, k, rep, gens = j
    d = R.cls(9)
    rng = np.random.default_rng([SALT, 77, N, I, rep, 9 if pair is None else pair, PRESETS.index(preset)])
    init, pre, A, B = build_init(d, N, I, pair, preset, rng)
    sup, U, PCC, coop, tag = R.restrict(d, init, A, B)
    li = np.ascontiguousarray(init[:, sup]); K = len(sup)
    seed = 50021 * rep + 7 * k + int(mN * 100) + (0 if impl == 'ref' else 1)
    if impl == 'ref':
        counts, t_est, hloc, hz = _ref(U, coop, tag, li, N, W, mN / N, k, gens, seed, pre)
    else:
        rr = np.random.default_rng(seed); r1 = rr.random(K); r2 = rr.random(K)
        iDl = int(np.searchsorted(sup, d['iD'])) if d['iD'] in set(sup.tolist()) else -1
        o = R._kern(U, PCC, coop, tag, li, N, W, mN / N, seed, R.checks_schedule(gens), True, iDl, r1, r2, pre, k)
        counts, t_est, hloc, hz = o[2], o[9], o[15], o[7]
    hold = np.array([R.holder(counts[i]) for i in range(I)])
    ht = tag[hold]
    cc = 0.0
    for i in range(I):
        c = counts[i].astype(float)
        cc += (c @ PCC @ c - (np.diag(PCC) * c).sum()) / (N * (N - 1))
    gB = int(counts[:, tag == 2].sum()); gcoop = int(counts[:, coop].sum())
    return dict(impl=impl, preset=preset, pair=pair, k=k, mN=mN, rep=rep, gens=gens, gB=gB, gcoop=gcoop,
                heldA=int((ht == 1).sum()), heldB=int((ht == 2).sum()),
                both=bool((ht == 1).any() and (ht == 2).any()), n_est=int((t_est >= 0).sum()), n_loc=int(((t_est >= 0) & (hloc >= 0.5)).sum()),
                pcc=cc / I, t_first=int(t_est[t_est >= 0].min()) if (t_est >= 0).any() else -1,
                lossB=int(hz[2]) if hz[2] >= 0 else -1)


def _sjob(j):
    """Default-kernel regression against seeds_in_n._run (the rival run's validation cells)."""
    impl, N, I, mN, rep, gens = j
    import seeds_in_n as SN
    d = R.cls(9)
    rng = np.random.default_rng([SALT, 99, N, I, rep])
    init, pre, A, B = R.build_init(d, N, I, None, 'iid', rng)
    sup, U, PCC, coop, tag = R.restrict(d, init, None, None)
    li = np.ascontiguousarray(init[:, sup]); K = len(sup)
    seed = 7919 * rep + N + I + (0 if impl == 'sn' else 3)
    iCl = int(np.searchsorted(sup, d['iC'])) if d['iC'] in set(sup.tolist()) else -1
    if impl == 'sn':
        o = SN._run(U, PCC, li, N, W, mN / N, gens, 20, seed, iCl, coop, np.zeros(K, np.bool_), 0)
        isl_cc = o[3]
    else:
        rr = np.random.default_rng(seed); r1 = rr.random(K); r2 = rr.random(K)
        iDl = int(np.searchsorted(sup, d['iD'])) if d['iD'] in set(sup.tolist()) else -1
        o = R._kern(U, PCC, coop, tag, li, N, W, mN / N, seed, R.checks_schedule(gens), True, iDl, r1, r2, pre, 1)
        isl_cc = o[3]
    return dict(impl=impl, N=N, I=I, mN=mN, rep=rep, eff=bool(isl_cc.mean() >= 0.95), isl_eff=int((isl_cc >= 0.95).sum()))


def validate_main(a):
    out = {}
    jobs = []
    VC = [(preset, pair, k, mN, gens) for preset, pair in (('AB', 2), ('AB', 0), ('iid', None)) for k in (1, 5, 10)
          for mN, gens in ((1.0, 1000), (3.0, 100))]
    for preset, pair, k, mN, gens in VC:
        for rep in range(a.vreps):
            for impl in ('ref', 'kern'):
                jobs.append((impl, preset, pair, 50, 4, mN, k, rep, gens))
    sjobs = []
    for N, I, mN, reps in ((100, 4, 1.0, 600), (100, 16, 0.1, 300)):
        for rep in range(reps):
            for impl in ('sn', 'kern'):
                sjobs.append((impl, N, I, mN, rep, 20000))
    t0 = time.time()
    with Pool(a.procs) as pool:
        rows = list(pool.imap_unordered(_vjob, jobs, chunksize=4))
        print('propagule validation done %.0fs' % (time.time() - t0), flush=True)
        srows = list(pool.imap_unordered(_sjob, sjobs, chunksize=8))
    print('default regression done %.0fs' % (time.time() - t0), flush=True)
    res = []
    for preset, pair, k, mN, gens in VC:
        if True:
            cell = {}
            for impl in ('ref', 'kern'):
                rs = [r for r in rows if r['impl'] == impl and r['preset'] == preset and r['pair'] == pair and r['k'] == k
                      and r['mN'] == mN and r['gens'] == gens]
                cell[impl] = dict(n=len(rs), both=float(np.mean([r['both'] for r in rs])), heldA=float(np.mean([r['heldA'] for r in rs])),
                                  heldB=float(np.mean([r['heldB'] for r in rs])), n_est=float(np.mean([r['n_est'] for r in rs])),
                                  n_loc=float(np.mean([r['n_loc'] for r in rs])), pcc=float(np.mean([r['pcc'] for r in rs])),
                                  lossB=float(np.mean([r['lossB'] >= 0 for r in rs])),
                                  gB=float(np.mean([r['gB'] for r in rs])), gcoop=float(np.mean([r['gcoop'] for r in rs])),
                                  sd=dict(heldA=float(np.std([r['heldA'] for r in rs])), n_est=float(np.std([r['n_est'] for r in rs])),
                                          gB=float(np.std([r['gB'] for r in rs])), gcoop=float(np.std([r['gcoop'] for r in rs])),
                                          n_loc=float(np.std([r['n_loc'] for r in rs])), pcc=float(np.std([r['pcc'] for r in rs]))))
            z = {}
            n1, n2 = cell['ref']['n'], cell['kern']['n']
            for s in ('heldA', 'n_est', 'n_loc', 'pcc', 'gB', 'gcoop'):
                se = math.sqrt(cell['ref']['sd'][s] ** 2 / n1 + cell['kern']['sd'][s] ** 2 / n2)
                z[s] = (cell['kern'][s] - cell['ref'][s]) / se if se > 0 else 0.0
            for s in ('both', 'lossB'):
                p1, p2 = cell['ref'][s], cell['kern'][s]; pp = (p1 * n1 + p2 * n2) / (n1 + n2)
                se = math.sqrt(pp * (1 - pp) * (1 / n1 + 1 / n2))
                z[s] = (p2 - p1) / se if se > 0 else 0.0
            res.append(dict(preset=preset, pair=pair, k=k, mN=mN, gens=gens, ref=cell['ref'], kern=cell['kern'], z=z))
            print(preset, pair, k, mN, gens, {s: round(v, 2) for s, v in z.items()},
                  'both %.3f/%.3f n_loc %.3f/%.3f pcc %.3f/%.3f' % (cell['ref']['both'], cell['kern']['both'], cell['ref']['n_loc'],
                                                                   cell['kern']['n_loc'], cell['ref']['pcc'], cell['kern']['pcc']))
    out['propagule'] = res
    sres = []
    for N, I, mN, reps in ((100, 4, 1.0, 600), (100, 16, 0.1, 300)):
        c = {}
        for impl in ('sn', 'kern'):
            rs = [r for r in srows if r['impl'] == impl and r['I'] == I]
            c[impl] = dict(n=len(rs), eff=float(np.mean([r['eff'] for r in rs])), isl=float(np.mean([r['isl_eff'] for r in rs])) / I)
        sres.append(dict(N=N, I=I, mN=mN, **c))
        print('default kernel vs seeds_in_n (%d, %d, mN %g): eff %.3f vs %.3f; island eff %.3f vs %.3f' % (
            N, I, mN, c['sn']['eff'], c['kern']['eff'], c['sn']['isl'], c['kern']['isl']))
    out['default'] = sres
    json.dump(out, open(os.path.join(RUNS, 'island-path-validate.json'), 'w'), indent=1)


# ------------------------------------------------------------------ merge test
def merge_main(a):
    src = []
    for e in ('path', 'prop'):
        src += [r for r in load(e) if 'end_counts' in r and r['N'] == 200]
    print('%d both-present N = 200 end states to merge' % len(src), flush=True)
    out = []
    with Pool(a.procs) as pool:
        for m in pool.imap_unordered(R.merge_one, src):
            out.append(m)
            print('%s I=%d mN=%g pair %s rep %d: clean %s share %.3f -> %s' % (m['exp'], m['I'], m['mN'], m['pair'], m['rep'],
                  m['clean'], m['share_larger'], 'larger won' if m['larger_won'] else ('MINORITY WON' if m['minority_won'] else 'mixed')), flush=True)
    json.dump(out, gzip.open(os.path.join(RUNS, 'island-path-merge.json.gz'), 'wt'))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('what', choices=['static', 'validate', 'run', 'calib', 'merge', 'report', 'timing'])
    ap.add_argument('--exp', default='cal')
    ap.add_argument('--procs', type=int, default=3)
    ap.add_argument('--gens', type=int, default=GENS)
    ap.add_argument('--reps', type=int, default=10000)
    ap.add_argument('--vreps', type=int, default=300)
    a = ap.parse_args()
    if a.what == 'static': static_main(a)
    elif a.what == 'validate': validate_main(a)
    elif a.what == 'run': run_main(a)
    elif a.what == 'calib': calib_main(a)
    elif a.what == 'merge': merge_main(a)
    elif a.what == 'report':
        import island_path_report as IR
        IR.main()
