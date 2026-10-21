"""Driver for the core-rediscovery run (spec specs/2026-10-21-core-rediscovery.md).

    python3 src/core_auction_run.py statics                       # Part A: pure Nash equilibria, core checks, Vickrey-nearest baselines
    python3 src/core_auction_run.py list                          # the cell registry
    python3 src/core_auction_run.py cells --cells NAME ... [--runs 40] [--workers 1] [--chunk 5]   # island cells (names or group prefixes)
Outputs go to runs/core_auction/: cell_<name>.json (summary and sampled series), rows_<name>.csv.gz (per-island end states).
"""
import argparse, gzip, json, os, sys, time, csv, zlib
from multiprocessing import Pool
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import core_auction as C

OUT = C.OUT
os.makedirs(OUT, exist_ok=True)
SPACES = ('unrestricted', 'no-overbid')
INSTS = C.SPEC_INSTANCES


def log(*a):
    print(*a, flush=True)


# ------------------------------------------------------------------ statics
def statics(insts=None, fname='statics.json'):
    insts = insts or C.SPEC_INSTANCES
    res = dict(instances={i: C.INSTANCES[i] for i in insts}, nash={}, baselines={}, hand={})
    for inst in insts:
        v = C.INSTANCES[inst]
        res['hand'][inst] = dict(v=v, min_revenue=C.min_revenue(v), wstar=C.wstar(v),
                                 core_bounds={''.join(C.ROLES[i] for i in S): b for S, b in C.core_inequalities(v).items()},
                                 vcg=C.vcg_payments(v), vickrey_nearest=C.vickrey_nearest(v))
        for space in SPACES:
            rep = C.nash_report(inst, space)
            summ = C.summarize_nash(rep)
            tally = {}
            rows_out = []
            for r in rep['rows']:
                viol = C.core_violations(v, r['u'], r['rev'])
                for x in viol:
                    tally[x] = tally.get(x, 0) + 1
                rows_out.append([*r['bids'], *[round(x, 3) for x in r['u']], round(r['rev'], 3), round(r['eff'], 3), round(r['core'], 3),
                                 int(r['mean_core']), ' '.join(viol)])
            summ['violation_tally'] = tally
            vn = C.vickrey_nearest(v)
            if 'A' in vn:
                near = 0; edge = 0
                for r in rep['rows']:
                    if r['eff'] > 1 - 1e-9 and r['mean_core'] and r['rev'] <= C.min_revenue(v) + 1 + 1e-9:
                        edge += 1
                        pa = v[1] - r['u'][1]; pb = v[2] - r['u'][2]
                        if abs(pa - vn['A']) <= 1 + 1e-9 and abs(pb - vn['B']) <= 1 + 1e-9:
                            near += 1
                summ['edge_equilibria_in_core'] = edge; summ['edge_equilibria_within_one_tick_of_VN'] = near
            res['nash']['%s/%s' % (inst, space)] = summ
            with gzip.open(os.path.join(OUT, 'nash_%s_%s.csv.gz' % (inst, space)), 'wt') as f:
                w = csv.writer(f)
                w.writerow(['bP', 'bA', 'bB', 'uP', 'uA', 'uB', 'rev', 'eff', 'core_realized', 'core_mean', 'violations'])
                w.writerows(rows_out)
            log(inst, space, {k: summ[k] for k in ('n_nash', 'n_efficient', 'n_in_core_mean', 'revenue_min', 'revenue_max',
                                                    'n_efficient_below_core', 'n_efficient_above_min_plus2')})
        for space in SPACES:
            b = C.edge_baseline(inst, space)
            b.pop('edge', None)
            res['baselines']['%s/%s' % (inst, space)] = b
    json.dump(res, open(os.path.join(OUT, fname), 'w'), indent=1, default=str)
    return res


# ------------------------------------------------------------------ the cell registry
CELLS = {}


def reg(name, inst, space, m_pru=0.0, kind='zero', A=0.0, gens=5000, N=100, I=64, m=0.0, order=(0, 1, 2), inject=False, group='', runs=None):
    CELLS[name] = dict(name=name, inst=inst, space=space, m_pru=m_pru, kind=kind, A=A, gens=gens, N=N, I=I, m=m, order=order, inject=inject, group=group, runs=runs)


def build_registry():
    for inst in INSTS:                                        # Stage 1a: constants, eps = 0, both bid spaces
        for sp in SPACES:
            reg('1a_%s_%s' % (inst, sp), inst, sp, inject=(inst != 'collusion'), group='1a')
    for inst in ('threshold', 'asymmetric'):                  # Stage 1b: the responder, no-overbid space
        for mp, tag in ((0.05, 'm05'), (0.2, 'm20')):
            reg('1b_%s_%s' % (inst, tag), inst, 'no-overbid', m_pru=mp, group='1b')
        reg('1b_%s_m20_rev' % inst, inst, 'no-overbid', m_pru=0.2, order=(2, 1, 0), group='1b_order')
    for inst in INSTS:                                        # re-injection arms on constants
        for sp in SPACES:
            pri = (inst == 'threshold')
            for A, tag in ((1.0, 'ann1'), (3.0, 'ann3')):
                reg('%s_%s_%s' % (tag, inst, sp), inst, sp, kind='ann', A=A, group='reinj' if pri else 'reinj_extra')
            reg('rain_%s_%s' % (inst, sp), inst, sp, kind='rain', gens=20000, group='reinj' if pri else 'reinj_extra')
    for inst in ('threshold', 'asymmetric'):                  # the responder under re-injection (extra, no prediction)
        reg('ann3_%s_m20' % inst, inst, 'no-overbid', m_pru=0.2, kind='ann', A=3.0, group='reinj_pru')
        reg('rain_%s_m20' % inst, inst, 'no-overbid', m_pru=0.2, kind='rain', gens=20000, group='reinj_pru')
    for inst in ('threshold', 'asymmetric', 'collusion'):     # per-role migration, mN = 1
        for sp in SPACES:
            reg('mig_%s_%s' % (inst, sp), inst, sp, m=0.01, group='mig')
    reg('mig_threshold_m20', 'threshold', 'no-overbid', m_pru=0.2, m=0.01, group='mig')
    for sp in SPACES:                                          # N sweep (threshold, constants, eps = 0); N = 100 is the primary cell
        for N in (50, 200):
            reg('nsw_threshold_%s_N%d' % (sp, N), 'threshold', sp, N=N, group='nsw')


    # post-hoc extras (not in the spec): ten times the runs of the primary constant cells (more edge islands for the split statistic), and the skew control
    for inst in ('threshold', 'asymmetric'):
        for sp in SPACES:
            reg('1a_%s_%s_x10' % (inst, sp), inst, sp, group='x10', runs=400)
    for sp in SPACES:
        reg('1a_skew_%s' % sp, 'skew', sp, group='skew')
        reg('mig_skew_%s' % sp, 'skew', sp, m=0.01, group='skew')
    reg('rain_skew_no-overbid', 'skew', 'no-overbid', kind='rain', gens=20000, group='skew')
    reg('1b_skew_m20', 'skew', 'no-overbid', m_pru=0.2, group='skew')


build_registry()


def _founder_seed(cell, run):
    key = '%s|%s|%s|%d' % (cell['inst'], cell['space'], cell['m_pru'], cell['N'])
    return [zlib.crc32(key.encode()), run, cell['I']]


def _dyn_seed(cell, run):
    return (zlib.crc32(cell['name'].encode()) + 7919 * run) % (2 ** 31 - 1)


_TENS = {}


def tensors(cell):
    key = (cell['inst'], cell['space'], cell['m_pru'] > 0, tuple(cell['order']))
    if key not in _TENS:
        _TENS[key] = C.build_tensor(cell['inst'], cell['space'], cell['m_pru'] > 0, cell['order'])
    return _TENS[key]


def losing_roles(inst):
    return (0,) if inst in ('threshold', 'asymmetric') else (1, 2)


def run_one(cell, run):
    """one run (64 islands) of a cell; returns the per-sample aggregate series and the per-island end table (and the injection control)."""
    inst, space, N, I = cell['inst'], cell['space'], cell['N'], cell['I']
    v = C.INSTANCES[inst]; mr = C.min_revenue(v)
    U, X = tensors(cell)
    pr = C.prior(inst, space, cell['m_pru'])
    rng = np.random.default_rng(_founder_seed(cell, run))
    init = C.seed_counts(pr, I, N, rng)
    sched = C.eps_schedule(cell['kind'], N, A=cell['A'], gens=cell['gens'])
    smp = C.sample_times(cell['gens'])
    t0 = time.time()
    counts, samp, first_erode, stop_g, pay = C.sim(U, X, init, N, C.W, cell['m'], cell['gens'], _dyn_seed(cell, run), sched, C.cdf_of(pr), smp, mr)
    dt = time.time() - t0
    F = C.flags(inst, samp)                                   # each (nsamp, I)
    lr = losing_roles(inst)
    ser = dict(
        eroded=F['eroded'].mean(axis=1), core=F['core'].mean(axis=1), edge=F['edge'].mean(axis=1), at_vn=F['at_vn'].mean(axis=1),
        rev=samp[:, :, 3].mean(axis=1), eff=samp[:, :, 4].mean(axis=1),
        lose_max=np.mean([samp[:, :, 9 + r] for r in lr], axis=(0, 2)), lose_med=np.mean([samp[:, :, 12 + r] for r in lr], axis=(0, 2)),
        pru_lose=np.mean([samp[:, :, 15 + r] for r in lr], axis=(0, 2)))
    ever_win = (samp[:, :, 7] > 1e-12).any(axis=0)
    ever_pru = np.array([(init[i, :, C.NC:].sum() > 0) for i in range(I)]) if init.shape[2] > C.NC else np.zeros(I, bool)
    fin = samp[-1]
    Ff = {k: f[-1] for k, f in F.items()}
    # fixation of every role and the final loser bid (modal program's mean bid is the median here)
    npres = (counts > 0).sum(axis=2)
    fixed = (npres == 1).all(axis=1)
    rows = []
    for i in range(I):
        rows.append([run, i, *[round(float(x), 5) for x in fin[i]], int(Ff['eroded'][i]), int(Ff['core'][i]), int(Ff['edge'][i]), int(Ff['at_vn'][i]),
                     int(first_erode[i]), int(ever_win[i]), int(ever_pru[i]), int(fixed[i]),
                     int(init[i, 0, :C.NC].nonzero()[0].min()) if init[i, 0, :C.NC].any() else -1, int(init[i, 0, :C.NC].nonzero()[0].max()) if init[i, 0, :C.NC].any() else -1,
                     int(init[i, 1, :C.NC].nonzero()[0].min()) if init[i, 1, :C.NC].any() else -1, int(init[i, 1, :C.NC].nonzero()[0].max()) if init[i, 1, :C.NC].any() else -1,
                     int(init[i, 2, :C.NC].nonzero()[0].min()) if init[i, 2, :C.NC].any() else -1, int(init[i, 2, :C.NC].nonzero()[0].max()) if init[i, 2, :C.NC].any() else -1])
    out = dict(run=run, seconds=dt, stop=int(stop_g), ser={k: [float(x) for x in a] for k, a in ser.items()}, rows=rows, samples=[int(x) for x in smp])
    if cell['inject'] and cell['kind'] == 'zero' and cell['m'] == 0.0 and cell['m_pru'] == 0.0:
        out['inject'] = injection(cell, U, X, counts, Ff, run)
    return out


def injection(cell, U, X, counts, Ff, run):
    """the outbidder-injection control: into eroded end states inject 5 copies of the profitable outbidder (P bidding the winners' total plus one)
    and continue 5,000 generations at eps = 0; the same islands continued without injection are the control."""
    inst, space, N, I = cell['inst'], cell['space'], cell['N'], cell['I']
    v = C.INSTANCES[inst]; mr = C.min_revenue(v)
    cap = 40 if space == 'unrestricted' else v[0]
    rng = np.random.default_rng([zlib.crc32(cell['name'].encode()), run, 77])
    init2 = counts.copy()
    eroded = np.nonzero(Ff['eroded'])[0]
    kinj = {}
    for i in eroded:
        kA = int(np.argmax(counts[i, 1])); kB = int(np.argmax(counts[i, 2]))
        k = min(kA + kB + 1, cap)
        kinj[int(i)] = k
        take = rng.multivariate_hypergeometric(counts[i, 0], 5)
        init2[i, 0] -= take
        init2[i, 0, k] += 5
    pr = C.prior(inst, space, 0.0)
    smp = C.sample_times(5000)
    sched = C.eps_schedule('zero', N)
    res = {}
    for tag, st in (('inj', init2), ('ctl', counts)):
        c2, samp, fe, stop, pay = C.sim(U, X, st, N, C.W, 0.0, 5000, _dyn_seed(cell, run) + (99991 if tag == 'inj' else 77773), sched, C.cdf_of(pr), smp, mr)
        F2 = C.flags(inst, samp[-1])
        rows = []
        for i in eroded:
            i = int(i)
            share = float(c2[i, 0, kinj[i]]) / N
            rows.append(dict(island=i, kinj=kinj[i], share=share, rev=float(samp[-1, i, 3]), core=bool(F2['core'][i]), eroded=bool(F2['eroded'][i]),
                             eff=float(samp[-1, i, 4]), start_share=5 / N))
        res[tag] = rows
    return dict(n_eroded=int(len(eroded)), **res)


HEAD = ['run', 'island', 'uP', 'uA', 'uB', 'rev', 'eff', 'ir', 'core_enc', 'pruwin', 'cyc', 'bmaxP', 'bmaxA', 'bmaxB', 'bmedP', 'bmedA', 'bmedB', 'pruP', 'pruA', 'pruB',
        'eroded', 'core', 'edge', 'at_vn', 'first_erode', 'ever_pru_win', 'ever_pru_present', 'fixed',
        'founder_loP', 'founder_hiP', 'founder_loA', 'founder_hiA', 'founder_loB', 'founder_hiB']


def _task(args):
    cell, runs = args
    return [run_one(cell, r) for r in runs]


def summarize_cell(cell, results):
    results = sorted(results, key=lambda r: r['run'])
    keys = list(results[0]['ser'].keys())
    ser = {k: np.mean([r['ser'][k] for r in results], axis=0).tolist() for k in keys}
    ser_sd = {k: np.std([r['ser'][k] for r in results], axis=0).tolist() for k in keys}
    rows = [row for r in results for row in r['rows']]
    summary = dict(cell=cell, n_runs=len(results), samples=results[0]['samples'], series_mean=ser, series_sd_across_runs=ser_sd,
                   seconds_total=float(sum(r['seconds'] for r in results)), stops=[r['stop'] for r in results])
    inj = [r['inject'] for r in results if 'inject' in r]
    if inj:
        summary['inject'] = inj
    with gzip.open(os.path.join(OUT, 'rows_%s.csv.gz' % cell['name']), 'wt') as f:
        w = csv.writer(f); w.writerow(HEAD); w.writerows(rows)
    json.dump(summary, open(os.path.join(OUT, 'cell_%s.json' % cell['name']), 'w'))
    return summary


def order_static():
    """Static order diagnostic for the responder: for every (instance, order pair) the share of program triples whose resolved bids differ between the
    orders P,A,B and B,A,P and the cycling share, by the number of PRU roles in the triple; mean payoffs of each role by the number of PRU roles."""
    res = {}
    for inst in ('threshold', 'asymmetric'):
        v = C.INSTANCES[inst]
        NC = C.NC
        U1, X1 = C.build_tensor(inst, 'no-overbid', True, (0, 1, 2))
        U2, X2 = C.build_tensor(inst, 'no-overbid', True, (2, 1, 0))

        def idxs(cap):
            return list(range(cap + 1)) + [NC + c for c in range(cap + 1)]
        iP, iA, iB = idxs(v[0]), idxs(v[1]), idxs(v[2])
        ix = np.ix_(iP, iA, iB)
        diff = (X1[C.XBP][ix] != X2[C.XBP][ix]) | (X1[C.XBA][ix] != X2[C.XBA][ix]) | (X1[C.XBB][ix] != X2[C.XBB][ix])
        npru = (np.array(iP)[:, None, None] >= NC).astype(int) + (np.array(iA)[None, :, None] >= NC) + (np.array(iB)[None, None, :] >= NC)
        d = {}
        for n in range(4):
            m = npru == n
            d[str(n)] = dict(triples=int(m.sum()), differ_between_orders=float(diff[m].mean()), cycling_PAB=float(X1[C.XCYC][ix][m].mean()),
                             cycling_BAP=float(X2[C.XCYC][ix][m].mean()))
            for tag, U, X in (('PAB', U1, X1), ('BAP', U2, X2)):
                d[str(n)]['eff_' + tag] = float(X[C.XEFF][ix][m].mean())
                d[str(n)]['rev_' + tag] = float(X[C.XREV][ix][m].mean())
                d[str(n)]['payoff_roles_' + tag] = [float(U[r][ix][m].mean()) for r in range(3)]
        res[inst] = d
    json.dump(res, open(os.path.join(OUT, 'order_static.json'), 'w'), indent=1)
    return res


def pick(names):
    out = []
    for n in names:
        if n in CELLS:
            out.append(n)
        else:
            m = [k for k, c in CELLS.items() if c['group'] == n or k.startswith(n)]
            if not m:
                raise SystemExit('no cell or group %s' % n)
            out.extend(m)
    return list(dict.fromkeys(out))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd')
    ap.add_argument('--cells', nargs='*', default=[])
    ap.add_argument('--runs', type=int, default=40)
    ap.add_argument('--workers', type=int, default=1)
    ap.add_argument('--chunk', type=int, default=5)
    ap.add_argument('--force', action='store_true')
    a = ap.parse_args()
    if a.cmd == 'statics':
        statics()
    elif a.cmd == 'statics_skew':
        statics(('skew',), 'statics_skew.json')
    elif a.cmd == 'order':
        order_static()
    elif a.cmd == 'list':
        for k, c in CELLS.items():
            log(k, c['group'], c['inst'], c['space'], c['m_pru'], c['kind'], c['A'], c['gens'], c['N'], c['m'], c['order'], c['inject'])
    elif a.cmd == 'cells':
        names = pick(a.cells)
        todo = [n for n in names if a.force or not os.path.exists(os.path.join(OUT, 'cell_%s.json' % n))]
        log('cells', todo)
        for n in todo:
            cell = CELLS[n]
            t0 = time.time()
            nr = cell.get('runs') or a.runs
            chunks = [list(range(s, min(s + a.chunk, nr))) for s in range(0, nr, a.chunk)]
            tasks = [(cell, ch) for ch in chunks]
            if a.workers > 1:
                with Pool(a.workers, maxtasksperchild=1) as pool:
                    res = [x for part in pool.imap_unordered(_task, tasks) for x in part]
            else:
                res = [x for t in tasks for x in _task(t)]
            s = summarize_cell(cell, res)
            sm = s['series_mean']
            log('%s done %.0fs  end: eroded %.3f core %.3f edge %.3f rev %.2f eff %.3f' % (n, time.time() - t0, sm['eroded'][-1], sm['core'][-1], sm['edge'][-1], sm['rev'][-1], sm['eff'][-1]))
