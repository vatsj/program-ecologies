"""Cells of the fixed-role chicken experiment (spec specs/2026-10-11-fixed-role-chicken.md; notes
notes/fixed-role-chicken.md; predictions predictions/2026-10-11-fixed-role-chicken.md).

    python3 src/fixed_role_chicken_run.py static
    python3 src/fixed_role_chicken_run.py chain [--procs 3]
    python3 src/fixed_role_chicken_run.py onepop [--procs 3]
    python3 src/fixed_role_chicken_run.py lottery --set main|small|controls|forced|swap|onepop [--procs 3] [--runs 40]
    python3 src/fixed_role_chicken_run.py guard          # scale guard: one run per kind, timed

Outputs under runs/fixed_role_chicken/ (JSON; the catalogue caches are gitignored .npz).
"""
import argparse, json, math, os, sys, time
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
from collections import Counter, defaultdict
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fixed_role_chicken as F

OUT = F.OUT
I_DEF = 64
EVERY = 10


def _json(o):
    if isinstance(o, dict): return {str(k): _json(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [_json(v) for v in o]
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, (np.floating,)): return float(o)
    if isinstance(o, np.ndarray): return _json(o.tolist())
    if isinstance(o, float) and not math.isfinite(o): return None
    return o


def save(name, obj):
    os.makedirs(OUT, exist_ok=True)
    json.dump(_json(obj), open(os.path.join(OUT, name), 'w'), indent=1)


def worker_budget():
    import subprocess
    try:
        out = subprocess.run(['ps', '-eo', 'command'], capture_output=True, text=True).stdout
        n = sum(1 for l in out.splitlines() if 'sog_realizable_run' in l or 'identity_tags_run' in l)
    except Exception:
        n = 0
    return max(1, min(3, 10 - n))


# ------------------------------------------------------------------ static
def cmd_static(a):
    res = dict(catalogues={}, static={})
    for arm in F.ARMS:
        d = F.catalogue(arm)
        res['catalogues'][arm] = dict(K=d['K'], n_programs=d['n_programs'], div=float(d.get('div', 0.0)),
                                      classes=[dict(name=F.display_name(d, k), mu=float(d['mu'][k]), size=int(d['sizes'][k]), tag=str(d['tags'][k]),
                                                    vs_Straight=float(d['S'][k, d['iSt']]), vs_Swerve=float(d['S'][k, d['iSw']]), self=float(d['S'][k, k]))
                                               for k in range(d['K'])])
        for g in F.GAME_NAMES:
            res['static']['%s/%s' % (arm, g)] = F.static(arm, g)
    # payoff classes coincide with play classes (per game)
    chk = {}
    for arm in F.ARMS:
        d = F.catalogue(arm)
        for g in F.GAME_NAMES:
            U = np.round(F.payoff(d['S'], g), 9)
            sig = {(U[k].tobytes(), U[:, k].tobytes()) for k in range(d['K'])}
            chk['%s/%s' % (arm, g)] = len(sig) == d['K']
    res['payoff_classes_equal_play_classes'] = chk
    # W0 vs M0 program-level play difference
    dw, dm = F.catalogue('W0'), F.catalogue('M0')
    Sw = dw['S'][np.ix_(dw['prog_cls'], dw['prog_cls'])]
    Sm = dm['S'][np.ix_(dw['prog_cls_M0'], dw['prog_cls_M0'])]
    diff = np.abs(Sw - Sm) > 1e-9
    tw = dw['tags'][dw['prog_cls']]
    kinds = Counter()
    for i, j in zip(*np.nonzero(diff)):
        kinds['%s vs %s' % (tw[i], tw[j])] += 1
    res['matched_play_difference'] = dict(pairs=int(diff.sum()), of=int(diff.size), share=float(diff.mean()), by_tag=dict(kinds))
    save('static.json', res)
    print(json.dumps({k: v for k, v in res.items() if k != 'catalogues' and k != 'static'}, indent=1))
    for k, s in res['static'].items():
        print(k, 'closed', s['n_closed'], s['closed_with_convention'], 'bridges', len(s['bridges']))


# ------------------------------------------------------------------ chains
def chain_job(job):
    arm, game, N = job
    d = F.catalogue(arm)
    U = F.payoff(d['S'], game)
    t = time.time()
    ch = F.two_pop_chain(U, d['mu'], N)
    s = F.chain_summary(d, game, N, ch)
    s['time_s'] = time.time() - t
    # independent solver check on the small catalogues and at N = 100 everywhere
    if d['K'] <= 12 or N == 100:
        lp = F.two_pop_chain_logcheck(U, d['mu'], N)
        s['check_tv_vs_log_gth'] = float(0.5 * np.abs(np.exp(lp) - np.exp(ch['lpi'])).sum())
    return s


def cmd_chain(a):
    jobs = [(arm, g, N) for arm in F.ARMS for g in F.GAME_NAMES for N in (100, 1000, 10000)]
    for arm in F.ARMS:
        F.catalogue(arm)
    from multiprocessing import Pool
    procs = min(a.procs, worker_budget())
    rows = []
    with Pool(procs) as pool:
        for r in pool.imap_unordered(chain_job, jobs):
            rows.append(r)
            print('%s %s N=%d: %s exit*N %.3e bridge share %.3f cut %.1e check %s (%.1fs)' % (
                r['arm'], r['game'], r['N'], {k: round(v, 4) for k, v in r['pi_by_class'].items()}, r['N_exit_R1'],
                r['exit_R1_share_bridge_winner'], r['cut'], r.get('check_tv_vs_log_gth'), r['time_s']), flush=True)
    rows.sort(key=lambda r: (F.ARMS.index(r['arm']), F.GAME_NAMES.index(r['game']), r['N']))
    save('chain.json', rows)


def onepop_job(job):
    arm, game, N, lt, twins = job
    t = time.time()
    r = F.onepop_chain(arm, game, N, log_theta=math.log(lt), twins=twins)
    r['time_s'] = time.time() - t
    r['theta'] = lt
    return r


def cmd_onepop(a):
    jobs = [('modal', g, N, 1e-14, True) for g in F.GAME_NAMES for N in (100, 1000, 10000)]
    jobs += [('modal', g, 10000, lt, True) for g in F.GAME_NAMES for lt in (1e-12, 1e-16)]
    jobs += [('modal', g, N, 1e-14, False) for g in F.GAME_NAMES for N in (100, 1000, 10000)]
    from multiprocessing import Pool
    procs = min(a.procs, worker_budget())
    rows = []
    with Pool(procs) as pool:
        for r in pool.imap_unordered(onepop_job, jobs):
            rows.append(r)
            print('onepop %s %s N=%d theta %.0e twins %s: %s pay %.3f eff %.3f StSt %.3f SwSw %.3f cut %s states %d (%.0fs)' % (
                r['arm'], r['game'], r['N'], r['theta'], r['twins'], {k: round(v, 4) for k, v in r['pi_by_class'].items()}, r['pay_per_player'],
                r['efficiency'], r['StSt'], r['SwSw'], r['log10_cut'], r['n_states'], r['time_s']), flush=True)
            save('onepop_chain.json', rows)
    rows.sort(key=lambda r: (F.GAME_NAMES.index(r['game']), r['twins'], r['theta'], r['N']))
    save('onepop_chain.json', rows)


# ------------------------------------------------------------------ lottery
GAMES_IDX = {g: i for i, g in enumerate(F.GAME_NAMES)}
ARM_IDX = {a: i for i, a in enumerate(F.ARMS)}


def analyse_two_pop(d, game, snap, N, mN, gens, stop_g, marks):
    """statistics of one run (notes 1.6-1.7) at each horizon mark."""
    K = d['K']; S = d['S']
    U = F.payoff(S, game); Jp = F.joint(S)
    lab_pair = F.classify(Jp)
    br = (d['tags'] == 'bridge')
    ns = snap.shape[0]
    X = snap[:, :, 0, :].astype(np.float64) / N
    Y = snap[:, :, 1, :].astype(np.float64) / N
    I = X.shape[1]
    Jisl = np.zeros((ns, I, 4))
    Xf = X.reshape(ns * I, K); Yf = Y.reshape(ns * I, K)
    for k in range(4):
        Jisl[:, :, k] = ((Xf @ Jp[:, :, k]) * Yf).sum(1).reshape(ns, I)
    lab = F.classify(Jisl)
    fs = F.fstar(game)
    res = dict(N=N, mN=mN, gens=gens, stop_gen=int(stop_g))
    # flips (whole run)
    flips = []
    for i in range(I):
        last_conv = None; last_s = None
        for s in range(ns):
            l = lab[s, i]
            if l in (F.R1, F.R2):
                if last_conv is not None and l != last_conv:
                    w = 0 if last_conv == F.R1 else 1           # winner population before the flip
                    wx = X[last_s, i] if w == 0 else Y[last_s, i]
                    lx = Y[last_s, i] if w == 0 else X[last_s, i]
                    bshare = float(wx[br].sum())
                    # loser fitness vs winner comp; best straight-playing pool class
                    f_l = U @ wx                                   # fitness of every class in the loser seat
                    mean_l = float(lx @ f_l)
                    if mN > 0:
                        pool = (snap[last_s, :, 1 - w, :].sum(0) > 0)
                    else:
                        pool = lx > 0
                    st_play = (1 - S) @ wx >= 0.5
                    cand = pool & st_play
                    favour = bool(cand.any() and f_l[cand].max() > mean_l + 1e-9)
                    flips.append(dict(island=i, gen_before=(last_s + 1) * EVERY, gen_after=(s + 1) * EVERY, frm=F.LABELS[last_conv], to=F.LABELS[l],
                                      winner_bridge_share=bshare, reader_mediated=bool(bshare >= fs), selection_favoured=favour,
                                      winner_top=F.display_name(d, int(np.argmax(wx))), loser_top=F.display_name(d, int(np.argmax(lx)))))
                last_conv = l; last_s = s
    res['flips'] = flips
    res['marks'] = {}
    for mk in marks:
        s_end = mk // EVERY - 1
        if s_end >= ns:
            continue
        w0 = s_end - max(1, (mk // 10) // EVERY) + 1           # last tenth of the horizon
        win = lab[w0:s_end + 1]
        stable = (win == win[-1:]).all(0)
        L = lab[s_end]
        est = stable & ((L == F.R1) | (L == F.R2))
        # establishment generation: first sample after which the class never changes up to the mark
        egen = []
        for i in range(I):
            if not est[i]:
                continue
            s0 = s_end
            while s0 > 0 and lab[s0 - 1, i] == L[i]:
                s0 -= 1
            egen.append((s0 + 1) * EVERY)
        cnt = {F.LABELS[c]: int((L == c).sum()) for c in range(5)}
        n1, n2 = int((L == F.R1).sum()), int((L == F.R2).sum())
        h = s_end // 2
        Xm, Ym = X[s_end], Y[s_end]
        M = Xm @ (U + U.T) @ Ym.T                                    # payoff sum, role-1 of A vs role-2 of B
        off = ~np.eye(I, dtype=bool)
        Cr = Xm @ Jp[:, :, 0] @ Ym.T
        Dv = Xm @ Jp[:, :, 3] @ Ym.T
        # patchwork history up to the mark
        pw = ((lab[:s_end + 1] == F.R1).any(1) & (lab[:s_end + 1] == F.R2).any(1))
        resolved = bool(pw.any() and not pw[-1])
        res_gen = None
        if resolved:
            last_pw = int(np.nonzero(pw)[0].max())
            res_gen = (last_pw + 2) * EVERY
        # E3 at the mark (and the first E3-resolved checked sample, every 100 generations)
        e3_first = None
        checks = list(range(9, s_end + 1, 10))
        if not checks or checks[-1] != s_end:
            checks.append(s_end)
        e3_last = None
        for s in checks:
            if mN > 0:
                pool0 = snap[s, :, 0, :].sum(0) > 0; pool1 = snap[s, :, 1, :].sum(0) > 0
            ok = True; labs = []
            for i in range(I):
                c0 = snap[s, i, 0].astype(np.int64); c1 = snap[s, i, 1].astype(np.int64)
                p0 = pool0 if mN > 0 else c0 > 0
                p1 = pool1 if mN > 0 else c1 > 0
                o = F.e3_island(c0, c1, p0, p1, U, U, lab_pair, K)
                labs.append(int(o))
                if o < 0:
                    ok = False
            if ok and e3_first is None:
                e3_first = (s + 1) * EVERY
            e3_last = labs
        e3c = Counter(F.LABELS[o] if o >= 0 else 'unresolved' for o in e3_last)
        npres = (snap[s_end] > 0).sum(2)
        res['marks'][str(mk)] = dict(
            counts=cnt, established=int(est.sum()), est_frac=float(est.mean()),
            est_R1=int((est & (L == F.R1)).sum()), est_R2=int((est & (L == F.R2)).sum()),
            est_gen_median=float(np.median(egen)) if egen else None,
            patchwork=bool(n1 > 0 and n2 > 0), single_convention=bool((n1 == I) or (n2 == I)), ever_patchwork=bool(pw.any()),
            resolved=resolved, resolution_gen=res_gen,
            crash_on_2nd=float(Jisl[h:s_end + 1, :, 0].mean()), dove_on_2nd=float(Jisl[h:s_end + 1, :, 3].mean()),
            crash_on_end=float(Jisl[s_end, :, 0].mean()), dove_on_end=float(Jisl[s_end, :, 3].mean()),
            pay_on=float(np.mean(np.diag(M))), pay_cross=float(M[off].mean()),
            loss_on=float(F.benchmark(game) - np.mean(np.diag(M))), loss_cross=float(F.benchmark(game) - M[off].mean()),
            crash_cross=float(Cr[off].mean()), dove_cross=float(Dv[off].mean()),
            e3=dict(e3c), e3_resolved_gen=e3_first,
            npres_mean=[float(npres[:, 0].mean()), float(npres[:, 1].mean())], polymorphic=float((npres.max(1) > 1).mean()),
            bridge_share=[float(Xm[:, br].sum(1).mean()), float(Ym[:, br].sum(1).mean())],
            top_classes=[[(F.display_name(d, int(k)), int(v)) for k, v in sorted(enumerate(snap[s_end, :, p, :].sum(0)), key=lambda kv: -kv[1])[:5] if v > 0]
                         for p in range(2)])
    return res


def lottery_job(job):
    kind, arm, game, N, mN, rep, gens, swap = job[:8]
    extra = job[8] if len(job) > 8 else {}
    I = extra.get('I', I_DEF)
    d = F.catalogue(arm)
    U = np.ascontiguousarray(F.payoff(d['S'], game))
    seed_key = [20261011, GAMES_IDX[game], ARM_IDX.get(arm, 9), N, int(10 * mN), rep, ['natural', 'paired', 'forced', 'onepop', 'swap'].index(kind)]
    if kind == 'paired':
        seed_key[2] = 77          # identical seeds for W0 and M0
    if kind == 'forced':
        seed_key.append(int(extra.get('bridges', True)))
    rng = np.random.default_rng(seed_key)
    sim_seed = int(rng.integers(2 ** 31 - 1))
    t = time.time()
    if kind == 'onepop':
        init = F.seed_counts(d['mu'], I, N, rng, npop=1)
        snap, ns, stop_g = F.sim_one_pop(U, init, N, F.W, mN / N, gens, EVERY, sim_seed, 1)
        res = analyse_one_pop(d, game, snap, N, mN, gens, stop_g, [gens] if mN == 0 else [2000, gens])
    else:
        if kind == 'paired':
            dw, dm = F.catalogue('W0'), F.catalogue('M0')
            a_, b_ = F.paired_seed_counts(dw, dm, I, N, rng)
            init = a_ if arm == 'W0' else b_
        elif kind == 'forced':
            init = F.forced_counts(d, I, N, extra.get('beta', 0.1), rng, bridges=extra.get('bridges', True))
        else:
            init = F.seed_counts(d['mu'], I, N, rng)
        sw = 1 if kind == 'swap' else 0
        if sw:
            init = init[:, ::-1, :].copy()       # populations exchanged: the run's role-r draws act on population 1 - r
        snap, ns, stop_g = F.sim_two_pop(U, U, init, N, F.W, mN / N, gens, EVERY, sim_seed, sw, 1)
        if sw:
            snap = snap[:, :, ::-1, :].copy()    # report in role order (role 1 = the population role-1 draws act on)
        res = analyse_two_pop(d, game, snap, N, mN, gens, stop_g, [gens] if mN == 0 else [2000, gens])
    res.update(kind=kind, arm=arm, game=game, rep=rep, swap=int(kind == 'swap'), I=I, time_s=time.time() - t,
               **({'bridges': extra.get('bridges', True), 'beta': extra.get('beta', 0.1)} if kind == 'forced' else {}))
    return res


def analyse_one_pop(d, game, snap, N, mN, gens, stop_g, marks):
    K = d['K']; S = d['S']; U = F.payoff(S, game); Jp = F.joint(S)
    ns, I, _ = snap.shape
    X = snap.astype(np.float64) / N
    Xf = X.reshape(ns * I, K)
    Jisl = np.zeros((ns, I, 4))
    for k in range(4):
        Jisl[:, :, k] = ((Xf @ Jp[:, :, k]) * Xf).sum(1).reshape(ns, I)
    res = dict(N=N, mN=mN, gens=gens, stop_gen=int(stop_g), marks={})
    for mk in marks:
        s_end = mk // EVERY - 1
        if s_end >= ns:
            continue
        cls = F.classify_onepop(Jisl[s_end])
        pay = ((Xf.reshape(ns, I, K)[s_end] @ U) * X[s_end]).sum(1)
        h = s_end // 2
        res['marks'][str(mk)] = dict(counts=dict(Counter(cls.tolist())), asym_max=float((Jisl[s_end, :, 1] + Jisl[s_end, :, 2]).max()),
                                     asym_mean=float((Jisl[s_end, :, 1] + Jisl[s_end, :, 2]).mean()),
                                     crash_end=float(Jisl[s_end, :, 0].mean()), dove_end=float(Jisl[s_end, :, 3].mean()),
                                     crash_2nd=float(Jisl[h:s_end + 1, :, 0].mean()), dove_2nd=float(Jisl[h:s_end + 1, :, 3].mean()),
                                     pay_per_player=float(pay.mean()), efficiency=float(2 * pay.mean() / F.benchmark(game)),
                                     top_classes=[(F.display_name(d, int(k)), int(v)) for k, v in sorted(enumerate(snap[s_end].sum(0)), key=lambda kv: -kv[1])[:6] if v > 0])
    return res


def jobs_for(set_, runs):
    J = []
    if set_ == 'main':            # natural seeds, weak and modal, all games, N = 100, mN in {0, 1}
        for arm in ('weak', 'modal'):
            for g in F.GAME_NAMES:
                for mN in (0, 1):
                    for r in range(runs):
                        J.append(('natural', arm, g, 100, mN, r, 2000 if mN == 0 else 4000, 0))
    elif set_ == 'small':         # small-N panel
        for arm in ('weak', 'modal'):
            for g in F.GAME_NAMES:
                for N in (25, 50):
                    for mN in (0, 1):
                        for r in range(runs):
                            J.append(('natural', arm, g, N, mN, r, 2000 if mN == 0 else 4000, 0))
    elif set_ == 'controls':      # constants-only (all N) and the matched W0/M0 pair
        for g in F.GAME_NAMES:
            for N in (25, 50, 100):
                for mN in (0, 1):
                    for r in range(runs):
                        J.append(('natural', 'const', g, N, mN, r, 2000 if mN == 0 else 4000, 0))
            for arm in ('W0', 'M0'):
                for mN in (0, 1):
                    for r in range(runs):
                        J.append(('paired', arm, g, 100, mN, r, 2000 if mN == 0 else 4000, 0))
    elif set_ == 'forced':
        for arm in ('weak', 'modal'):
            for g in F.GAME_NAMES:
                for br in (True, False):
                    for r in range(runs):
                        J.append(('forced', arm, g, 100, 1, r, 4000, 0, dict(bridges=br, beta=0.1)))
    elif set_ == 'swap':
        for arm in ('weak', 'modal'):
            for g in F.GAME_NAMES:
                for mN in (0, 1):
                    for r in range(runs):
                        J.append(('swap', arm, g, 100, mN, r, 2000 if mN == 0 else 4000, 1))
    elif set_ == 'onepop':
        for g in F.GAME_NAMES:
            for mN in (0, 1):
                for r in range(runs):
                    J.append(('onepop', 'modal', g, 100, mN, r, 2000 if mN == 0 else 4000, 0))
    return J


def cmd_lottery(a):
    jobs = jobs_for(a.set, a.runs)
    for arm in F.ARMS:
        F.catalogue(arm)
    path = os.path.join(OUT, 'lottery_%s.json' % a.set)
    rows = json.load(open(path)) if (a.resume and os.path.exists(path)) else []
    done = {(r['kind'], r['arm'], r['game'], r['N'], r['mN'], r['rep'], r.get('bridges', True)) for r in rows}
    jobs = [j for j in jobs if (j[0], j[1], j[2], j[3], j[4], j[5], (j[8] if len(j) > 8 else {}).get('bridges', True)) not in done]
    procs = min(a.procs, worker_budget())
    print('%d jobs, %d workers' % (len(jobs), procs), flush=True)
    from multiprocessing import Pool
    t0 = time.time()
    with Pool(procs) as pool:
        for n, r in enumerate(pool.imap_unordered(lottery_job, jobs)):
            rows.append(_json(r))
            mk = r['marks'][str(max(int(k) for k in r['marks']))]
            print('[%d/%d %.0fs] %s %s %s N=%d mN=%g rep %d: %s est %.3f stop %d flips %d (%.1fs)' % (
                n + 1, len(jobs), time.time() - t0, r['kind'], r['arm'], r['game'], r['N'], r['mN'], r['rep'], mk.get('counts'),
                mk.get('est_frac', float('nan')), r['stop_gen'], len(r.get('flips', [])), r['time_s']), flush=True)
            if n % 20 == 0:
                save('lottery_%s.json' % a.set, rows)
    save('lottery_%s.json' % a.set, rows)


def cmd_guard(a):
    for job in [('natural', 'weak', 'chicken', 100, 1, 0, 400, 0), ('natural', 'modal', 'hd3', 100, 1, 0, 400, 0),
                ('natural', 'weak', 'hd3', 100, 0, 0, 400, 0), ('onepop', 'modal', 'chicken', 100, 1, 0, 400, 0)]:
        t = time.time()
        r = lottery_job(job)
        print(job, 'time %.1fs for %d generations' % (time.time() - t, job[6]), flush=True)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd')
    ap.add_argument('--set', default='main')
    ap.add_argument('--runs', type=int, default=40)
    ap.add_argument('--procs', type=int, default=3)
    ap.add_argument('--resume', action='store_true')
    a = ap.parse_args()
    {'static': cmd_static, 'chain': cmd_chain, 'onepop': cmd_onepop, 'lottery': cmd_lottery, 'guard': cmd_guard}[a.cmd](a)
