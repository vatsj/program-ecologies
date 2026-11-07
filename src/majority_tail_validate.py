"""Validations V1-V6 of the majority-division experiment (spec specs/2026-11-07-majority-current-object.md).

    python3 src/majority_tail_validate.py [v1 v2 v3 v4 v5 v6] [--workers K]

Results go to runs/majority_tail/validation.json (one entry per gate).  Importable without side effects.
"""
import json, os, sys, time
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy.stats import chi2 as C2
import dollar3 as D
import stable_sets as SS
import migration_window as MW
import churn_primary as CP
import majority_tail as MT
import majority_tail_kern as MK

ROOT = SS.ROOT
OUT = os.path.join(ROOT, 'runs', 'majority_tail')
T = MT.T
CACHE = os.environ.get('MT_CACHE', os.path.join(ROOT, 'runs', '_cache'))


# ====================================================================== V1
def _v1_one(args):
    spec, r, mN = args
    cat = CP.get_cat(spec, CACHE)
    base = CP.founder_base(spec)
    prep = CP.prepare(cat, base, r)
    H = 10000
    N = prep['N']
    ref = CP.kernel(prep, mN, H)
    z = np.zeros(0, np.int64)
    out = MK.kern_mt(prep['J'], prep['PAY'], prep['VEC'], T.ISMEM, T.TOT, prep['loc'], N, MT.W, mN / N, prep['seed'], H, 10,
                     np.array([0, 1000, 2000, 5000, 10000], np.int64), z, z, z, np.zeros(0), z, 10, 10)
    status, stop, counts, modal, majo = out[0], out[1], out[2], out[3], out[4]
    same_modal = bool((modal.astype(np.int64) == ref['modal'].astype(np.int64)).all()) and int(status) == ref['status'] \
        and int(stop) == ref['stop'] and bool((counts == ref['counts']).all()) and int(out[-1]) == ref['nmig']
    fl = CP.flips(modal.astype(np.int64))
    fc = CP.flip_counts(fl, modal.astype(np.int64), int(stop))
    mg = modal[H]
    nm = len({int(x) for x in mg if int(x) in set(MW.V)}); F = int(CP.ISFAIR[mg].sum()); cons = int((mg == mg[0]).all())
    stored = json.load(open(os.path.join(ROOT, 'runs', 'churn_primary', '%s__c0=0.json' % spec)))
    key = '%g' % mN if mN not in (0,) else '0'
    key = {0: '0', 0.1: '0.1', 1: '1'}[mN]
    row = [x for x in stored[key] if x['run'] == r][0]
    same_row = (row['stop'] == int(stop) and row['status'] == int(status) and row['nm'] == nm and row['F'] == F and
                row['cons'] == cons and row['mm'] == fc['mm'] and row['mo'] == fc['mo'] and row['om'] == fc['om'] and
                row['oo'] == fc['oo'] and row['expo'] == fc['expo'])
    return dict(spec=spec, run=r, mN=mN, same_kern_mw=same_modal, same_stored=bool(same_row))


def v1(workers=4):
    from concurrent.futures import ProcessPoolExecutor
    jobs = [(spec, r, mN) for spec in ('B6m', 'T-main') for mN in (0, 0.1, 1) for r in range(40)]
    with ProcessPoolExecutor(workers) as ex:
        res = list(ex.map(_v1_one, jobs, chunksize=1))
    ok = all(x['same_kern_mw'] and x['same_stored'] for x in res)
    by = {}
    for x in res:
        k = '%s|mN=%g' % (x['spec'], x['mN'])
        by.setdefault(k, [0, 0, 0])
        by[k][0] += 1; by[k][1] += x['same_kern_mw']; by[k][2] += x['same_stored']
    return dict(gate='V1', passed=bool(ok), n=len(res), by_cell={k: dict(n=v[0], same_kern_mw=v[1], same_stored=v[2]) for k, v in by.items()},
                fails=[x for x in res if not (x['same_kern_mw'] and x['same_stored'])][:20])


# ====================================================================== V2
def v2():
    out = {}
    ok = True
    for arm in ('M', 'T'):
        laws = MT.base_laws(arm)
        ks = []
        for r in range(40):
            s = MT.make_schedule(100, r, 64)
            ks.append(MT.map_programs(s, laws, 100)[4])
            if sum(len(k) for k in ks) >= 100000:
                break
        k = np.concatenate(ks)
        p = laws[0] / laws[0].sum()
        cnt = np.bincount(k, minlength=len(p)).astype(float)
        top = [x for x in np.argsort(-p)[:20] if p[x] * len(k) >= 5]
        obs = np.array([cnt[x] for x in top] + [len(k) - cnt[top].sum()])
        pe = np.array([p[x] for x in top] + [1 - p[top].sum()]) * len(k)
        chi = float(((obs - pe) ** 2 / pe).sum()); pv = float(C2.sf(chi, len(pe) - 1))
        out[arm] = dict(n=int(len(k)), chi2=chi, dof=int(len(pe) - 1), p=pv, classes_in_test=len(top))
        ok &= pv > 0.01
    # per-slot law of arrivals: same law in each slot; checked via the slot counts
    counts = {}
    for N in (100, 200, 400):
        geo = MT.geometry(N)
        analytic = 100.0 * (1 - 1 / (1 + (geo['gend'] - geo['g0']) / geo['t0']))
        gs, mean = MT.tail_mean(N, geo['g0'], geo['t0'], geo['gend'], 100.0)
        integral = float(mean.sum())
        tot = 0; n_isl = 0; late = 0; tot_all = 0
        for r in range(40 if N < 400 else 20):
            s = MT.make_schedule(N, r, 64)
            tot += len(s['g']); n_isl += 64
            late += int((s['g'] > 15 * N).sum())
        per = tot / n_isl
        counts['N%d' % N] = dict(per_island_mean=per, analytic=analytic, integral_of_schedule=integral,
                                 rel_err=per / analytic - 1, late_share_after_15N=late / max(tot, 1))
        ok &= abs(per / analytic - 1) < 0.02 and abs(integral - analytic) < 1e-9 * 100
    # Lambda = 10 by thinning
    s = MT.make_schedule(100, 0, 64)
    n10 = [(MT.map_programs(MT.make_schedule(100, r, 64), MT.base_laws('M'), 10)[0].shape[0]) / 64 for r in range(40)]
    geo = MT.geometry(100)
    an10 = 10.0 * (1 - 1 / (1 + (geo['gend'] - geo['g0']) / geo['t0']))
    counts['lam10_N100'] = dict(per_island_mean=float(np.mean(n10)), analytic=an10, rel_err=float(np.mean(n10)) / an10 - 1)
    ok &= abs(np.mean(n10) / an10 - 1) < 0.02
    return dict(gate='V2', passed=bool(ok), law=out, counts=counts)


# ====================================================================== V3
def v3():
    cat = CP.get_cat('B6m'); S = cat.S
    rng = np.random.default_rng(3)
    mism = 0; ntr = 0
    # (a) per-run universes contain every arrival and founder at the three sizes
    cover = {}
    allcover = True
    for N in (100, 200, 400):
        nruns = 6
        for r in range(nruns):
            prep = MT.prepare('M', 'main', N, r)
            for lam in (10, 100):
                MT.local_arrivals(prep, lam)         # asserts every arrival is in the universe
            if r == 0:
                cover['N%d' % N] = dict(K=[len(u) for u in prep['U']], J_dtype=str(prep['J'].dtype))
            # (b) the int16 table equals the reference int32 table on random triples of the universe
            U = prep['U']
            Kmax = prep['J'].shape[0]
            for _ in range(3000):
                a, b, c = (int(rng.integers(0, len(U[s]))) for s in range(3))
                ref = SS._joint_table(cat.armi, S.nat, S.atL, S.atJ, S.atA, S.tab, D.PARTNER, U[0][a:a + 1], U[1][b:b + 1], U[2][c:c + 1])[0, 0, 0]
                ntr += 1
                mism += int(prep['J'][a, b, c] != ref)
    # (c) coverage of the full catalogue: any program of positive prior mass can be tabulated against any pair
    full_mism = 0; nfull = 0
    pos = [np.nonzero(MT.base_laws('M')[s] > 0)[0] for s in range(3)]
    for _ in range(10000):
        x = [int(rng.choice(pos[s])) for s in range(3)]
        a = SS._joint_table(cat.armi, S.nat, S.atL, S.atJ, S.atA, S.tab, D.PARTNER, np.array([x[0]]), np.array([x[1]]), np.array([x[2]]))[0, 0, 0]
        b = MT._joint16(cat.armi, S.nat, S.atL, S.atJ, S.atA, S.tab, D.PARTNER, np.array([x[0]]), np.array([x[1]]), np.array([x[2]]))[0, 0, 0]
        nfull += 1; full_mism += int(a != b)
    # arm T: the table is the full 27^3 table
    J, PAY, VEC, ISMEM, TOT = MT.build_tables('T', None)
    ok = (mism == 0 and full_mism == 0 and J.shape == (27, 27, 27))
    return dict(gate='V3', passed=bool(ok), per_run_table_vs_reference=dict(n=ntr, mismatches=mism), full_catalogue_lazy_vs_reference=dict(n=nfull, mismatches=full_mism),
                universes=cover, T_table_shape=list(J.shape),
                note='per-run universe = founders + all scheduled arrivals (Lambda = 100 schedule), so every program an arrival can bring has an entry against every pair that can be present; migrants copy residents')


# ====================================================================== V4
def v4():
    import many_islands_t as MIT
    tabs = MT._tabs(CACHE)
    J, PAY, VEC, ISMEM, TOT = MT.t_charged_tables(tabs, MT.PFAIL)
    net = tabs.payoff(MT.PFAIL, MT.PFAIL)
    d = np.abs(PAY[J] - net).max()
    vecok = bool((VEC[J] == tabs.OUT).all())
    # independent recomputation of random triples through the counted evaluator
    rng = np.random.default_rng(5)
    bad = 0
    n = 300
    cat = tabs.cat
    with MIT.counting():
        for _ in range(n):
            a, b, c = (int(x) for x in rng.integers(0, 27, 3))
            # payoff of slot 0 from (a; next=b, prev=c), slot 1 from (b; next=c, prev=a), slot 2 from (c; next=a, prev=b)
            res = [MIT.f_eval_counted(cat, a, b, c), MIT.f_eval_counted(cat, b, c, a), MIT.f_eval_counted(cat, c, a, b)]
            codes = [r_[0] for r_ in res]
            c0, c1, c2 = codes
            pi, dd = c1 // 3, c1 % 3
            l1 = 3 * (1 - pi) + dd if pi < 2 else c1
            code = c0 * 81 + l1 * 9 + c2
            pay = MIT.PAY[code] - MT.PFAIL * np.array([r_[2] for r_ in res]) - MT.PFAIL * np.array([r_[3] for r_ in res])
            bad += int(np.abs(pay - net[a, b, c]).max() > 1e-9)
    ok = d < 1e-9 and vecok and bad == 0
    return dict(gate='V4', passed=bool(ok), max_abs_diff_vs_Tabs_payoff=float(d), outcomes_equal=vecok, independent_recomputation=dict(n=n, mismatches=bad),
                P_fail=MT.PFAIL, n_types=int(len(PAY)),
                note='the table is built from many_islands_t.Tabs (the queue-69 table); no stored per-triple table exists to compare with, so it is checked against Tabs.payoff and against an independent counted re-evaluation')


# ====================================================================== V5
def v5(trials=10000):
    cat = CP.get_cat('B6m'); S = cat.S
    ci = SS.const_index(S.fs)                  # local action -> class
    lo = D.local_of
    N = 100
    c_h = ci[lo(0, 1, 2)]          # slot 0 names slot 1 at 2/3
    c_l = ci[lo(1, 0, 0)]          # slot 1 names slot 0 at 1/3
    c_e = ci[lo(2, D.ALL, 2)]      # slot 2 resident: ALL at 2/3 (forms nothing)
    c_op = ci[lo(2, 1, 1)]         # slot 2 opener: names slot 1 at 1/2 (not reciprocated by the resident slot 1)
    c_sw = ci[lo(1, 2, 1)]         # slot 1 switch: names slot 2 at 1/2
    U = [np.array(sorted({c_h})), np.array(sorted({c_l, c_sw})), np.array(sorted({c_e, c_op}))]
    Kmax = max(len(u) for u in U)
    Up = [np.concatenate([u, np.full(Kmax - len(u), u[0])]).astype(np.int64) for u in U]
    J = MT._joint16(cat.armi, S.nat, S.atL, S.atJ, S.atA, S.tab, D.PARTNER, Up[0], Up[1], Up[2])
    z = np.zeros(0, np.int64)

    def counts_init(s2_counts, s1_counts):
        loc = np.zeros((1, 3, Kmax), np.int64)
        loc[0, 0, 0] = N
        loc[0, 1, :len(U[1])] = s1_counts
        loc[0, 2, :len(U[2])] = s2_counts
        return loc

    li = {c: t for t, c in enumerate(U[1])}; le = {c: t for t, c in enumerate(U[2])}
    res = {}
    rng = np.random.default_rng(11)
    for label, kk, via in (('opener_k1_arrival', 1, True), ('opener_k10', 10, False), ('opener_kN2', N // 2, False)):
        fix = 0
        for t in range(trials):
            seed = int(rng.integers(1, 2 ** 31 - 1))
            s2 = np.zeros(len(U[2]), np.int64); s1 = np.zeros(len(U[1]), np.int64)
            s1[li[c_l]] = N
            if via:
                s2[le[c_e]] = N
                loc = counts_init(s2, s1)
                out = MK.kern_mt(J, T.PAY, T.VEC, T.ISMEM, T.TOT, loc, N, MT.W, 0.0, seed, 4000, 10 ** 9, np.array([4000], np.int64),
                                 np.array([1], np.int64), np.array([0], np.int64), np.array([2], np.int64), np.array([0.5]),
                                 np.array([le[c_op]], np.int64), 10, 10)
            else:
                s2[le[c_op]] = kk; s2[le[c_e]] = N - kk
                loc = counts_init(s2, s1)
                out = MK.kern_mt(J, T.PAY, T.VEC, T.ISMEM, T.TOT, loc, N, MT.W, 0.0, seed, 4000, 10 ** 9, np.array([4000], np.int64),
                                 z, z, z, np.zeros(0), z, 10, 10)
            fin = out[2]
            fix += int(fin[0, 2, le[c_op]] == N)
        p = kk / N
        se = np.sqrt(p * (1 - p) / trials)
        res[label] = dict(k=kk, trials=trials, fixation=fix / trials, neutral=p, se=float(se), z=float((fix / trials - p) / se),
                          within3se=bool(abs(fix / trials - p) <= 3 * se))
    # the underpaid member's switch (slot 1 -> names slot 2 at 1/2) in an island where slot 2 is all openers
    fix = 0
    sw_trials = trials
    for t in range(sw_trials):
        seed = int(rng.integers(1, 2 ** 31 - 1))
        s2 = np.zeros(len(U[2]), np.int64); s2[le[c_op]] = N
        s1 = np.zeros(len(U[1]), np.int64); s1[li[c_l]] = N - 1; s1[li[c_sw]] = 1
        loc = counts_init(s2, s1)
        out = MK.kern_mt(J, T.PAY, T.VEC, T.ISMEM, T.TOT, loc, N, MT.W, 0.0, seed, 4000, 10 ** 9, np.array([4000], np.int64),
                         z, z, z, np.zeros(0), z, 10, 10)
        fix += int(out[2][0, 1, li[c_sw]] == N)
    res['switch_after_opener'] = dict(trials=sw_trials, fixation=fix / sw_trials, three_over_N=3.0 / N, selected=bool(fix / sw_trials > 3.0 / N))
    ok = all(res[k]['within3se'] for k in ('opener_k1_arrival', 'opener_k10', 'opener_kN2')) and res['switch_after_opener']['selected']
    return dict(gate='V5', passed=bool(ok), N=N, results=res,
                triple='slot 0: (1,2/3) constant, slot 1: (0,1/3) constant, slot 2 resident (ALL,2/3); opener (1,1/2); switch (2,1/2)')


# ====================================================================== V6
def v6():
    out = {}
    cat = CP.get_cat('B6m'); S = cat.S
    rot = [1, 2, 0]
    perm = S.permute(rot)
    law = MT.base_laws('M')
    lawok = all(np.allclose(law[rot[s]][perm[s]], law[s]) for s in range(3))
    fam, vic, bul = MT.dsl_family_data(S)
    famok = all((fam[rot[s]][perm[s]] == fam[s]).all() and (vic[rot[s]][perm[s]] == vic[s]).all() and (bul[rot[s]][perm[s]] == bul[s]).all() for s in range(3))
    # joint tables: payoff of slot s of x equals the payoff of slot rot[s] of the image triple (10^4 random triples)
    rng = np.random.default_rng(6)
    bad = 0
    for _ in range(10000):
        x = rng.integers(0, S.K, 3)
        a = SS._joint_table(cat.armi, S.nat, S.atL, S.atJ, S.atA, S.tab, D.PARTNER, x[:1], x[1:2], x[2:3])[0, 0, 0]
        z = np.zeros(3, np.int64)
        for s in range(3):
            z[rot[s]] = perm[s][x[s]]
        b = SS._joint_table(cat.armi, S.nat, S.atL, S.atJ, S.atA, S.tab, D.PARTNER, z[:1], z[1:2], z[2:3])[0, 0, 0]
        for s in range(3):
            bad += int(abs(T.PAY[a, s] - T.PAY[b, rot[s]]) > 1e-12)
    out['M'] = dict(law_equivariant=bool(lawok), families_equivariant=bool(famok), table_mismatches=bad, triples=10000)
    # T exhaustive: net[a,b,c,s] == net[c,a,b,(s+1)%3]
    tabs = MT._tabs(CACHE)
    net = tabs.payoff(MT.PFAIL, MT.PFAIL)
    bad = 0
    for a in range(27):
        for b in range(27):
            for c in range(27):
                for s in range(3):
                    bad += int(abs(net[a, b, c, s] - net[c, a, b, (s + 1) % 3]) > 1e-12)
    cat_t = CP.get_cat('T-main', CACHE)
    lawT = MT.base_laws('T')
    out['T'] = dict(law_identical_across_slots=bool(all(np.allclose(lawT[s], lawT[0]) for s in range(3))), table_mismatches=bad, triples=27 ** 3)
    # tie-break: ties in the encounter distribution of random configurations, and rotation of the modal outcome when untied
    ties = 0; unt = 0; rotbad = 0
    # outcome id rotation map: outcome of image triple vs outcome of x: compare modal class and fair-pair index under rotation
    out['modal_tie_break'] = dict(note='argmax breaks exact ties by the lowest outcome id, which is not rotation equivariant; the frequency of ties at the recorded snapshots is reported per cell in the rows (snap[..].ties)')
    ok = lawok and famok and out['M']['table_mismatches'] == 0 and out['T']['table_mismatches'] == 0 and out['T']['law_identical_across_slots']
    return dict(gate='V6', passed=bool(ok), **out)


def main():
    gates = [a for a in sys.argv[1:] if a in ('v1', 'v2', 'v3', 'v4', 'v5', 'v6')] or ['v1', 'v2', 'v3', 'v4', 'v5', 'v6']
    workers = 4
    if '--workers' in sys.argv:
        workers = int(sys.argv[sys.argv.index('--workers') + 1])
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, 'validation.json')
    if '--vout' in sys.argv:
        path = os.path.join(ROOT, sys.argv[sys.argv.index('--vout') + 1])
        os.makedirs(os.path.dirname(path), exist_ok=True)
    res = json.load(open(path)) if os.path.exists(path) else {}
    for gname in gates:
        t = time.time()
        r = {'v1': lambda: v1(workers), 'v2': v2, 'v3': v3, 'v4': v4, 'v5': v5, 'v6': v6}[gname]()
        r['wall'] = round(time.time() - t, 1)
        res[r['gate']] = r
        print(r['gate'], 'PASS' if r['passed'] else 'FAIL', r['wall'], 's', flush=True)
        json.dump(res, open(path, 'w'), indent=1, default=float)


if __name__ == '__main__':
    main()
