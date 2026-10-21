"""Cells of the Part B ecology (spec specs/2026-10-21-coalition-proof-auctions.md).

    python3 src/auction_islands_run.py static                  # payoff tensors, Nash equilibria, tremble control, constant-bid invasion
    python3 src/auction_islands_run.py cells --set primary|nopol|nsweep|mig [--runs 40]
    python3 src/auction_islands_run.py guard                   # timing

One process; each run is one call.  Outputs: runs/auctions/partB_static.json, runs/auctions/cells/<key>.json (cell summaries; no per-island arrays).
"""
import argparse, json, math, os, sys, time
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
from collections import Counter
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import auction_islands as B

OUT = B.OUT
CELLS = os.path.join(OUT, 'cells')
I_DEF = 64
GENS = 2000
GENS_MIG = 4000
EVERY = 5
PRIORS = ('U', 'S', 'M')
INST_IDX = {'collusion': 0, 'threshold': 1}
RULE_IDX = {'vcg': 0, 'surcharge': 1, 'fp': 2}


def _json(o):
    if isinstance(o, dict): return {str(k): _json(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [_json(v) for v in o]
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, (np.floating,)): return float(o)
    if isinstance(o, np.ndarray): return _json(o.tolist())
    if isinstance(o, float) and not math.isfinite(o): return None
    return o


def save(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(_json(obj), open(path, 'w'), indent=1)


def cell_key(rule, inst, prior, audit, N, mN, nopol):
    return '%s_%s_%s%s_%s_N%d_mN%g' % (rule, inst, prior, '-noPOL' if nopol else '', 'audit' if audit else 'open', N, mN)


_TENS = {}


def get_tensor(rule, inst, audit):
    k = (rule, inst, audit)
    if k not in _TENS:
        U, rec, c = B.tensor(rule, inst, audit)
        _TENS[k] = (U, c)
    return _TENS[k]


def run_once(rule, inst, prior, audit, N, mN, nopol, run, I=I_DEF):
    """one run of I islands; returns per-island arrays."""
    U, c = get_tensor(rule, inst, audit)
    seed_key = [20261021, INST_IDX[inst], PRIORS.index(prior), N, run, int(nopol)]      # founders and dynamics paired across rules and the audit
    rng = np.random.default_rng(seed_key)
    pr = B.prior(prior, noPOL=nopol)
    init = B.seed_counts(pr, I, N, rng)
    # founder flags on the unaudited founders
    pol_f = init[:, 2, 1] > 0
    pol_init = init[:, 2, 1].copy(); pairA_init = init[:, 0, 2].copy(); pairB_init = init[:, 1, 2].copy()
    pair_f = (init[:, 0, 2] > 0) & (init[:, 1, 2] > 0)
    pairu_f = (init[:, 0, 3] > 0) & (init[:, 1, 3] > 0)
    if audit:
        init = B.audit_map(init)
    sim_seed = int(rng.integers(1, 2 ** 31 - 1))
    m = mN / N
    gens = GENS if mN == 0 else GENS_MIG
    cnt, fg, fx, pf, te, sg = B.sim3(U, init, N, B.W, m, gens, sim_seed, EVERY, 1, 2, 3, 1)
    rows = []
    for i in range(I):
        st = B.encounter_stats(c, cnt[i], audit)
        k = B.classify_island(st, cnt[i], audit)
        if mN > 0:
            k['policed'] = bool(cnt[i, 2, 1] > 0.5 * N) and not audit
        triple = tuple(int(np.argmax(cnt[i, r])) for r in range(3))
        mono = all((cnt[i, r] > 0).sum() == 1 for r in range(3))
        rows.append(dict(cls=k['cls'], policed=k['policed'], pair_enf=k['pair_enforced'], pair_unenf=k['pair_unenforced'], items_dev=k['items_dev'],
                         fixed=bool(fx[i] >= 0), frozen=bool(fg[i] >= 0), fixed_gen=int(fx[i]), frozen_gen=int(fg[i]), pol_fix=int(pf[i]),
                         tested=int(te[i]), pol_init=int(pol_init[i]), pairA_init=int(pairA_init[i]), pairB_init=int(pairB_init[i]), pol_founded=bool(pol_f[i]), pair_founded=bool(pair_f[i]), pairu_founded=bool(pairu_f[i]),
                         joint=float(st['joint']), eff=float(st['eff']), rev=float(st['rev']), uA=float(st['uA']), uB=float(st['uB']), uP=float(st['uP']),
                         triple='%s|%s|%s' % (B.ITEM[triple[0]], B.ITEM[triple[1]], B.PROG_P[triple[2]]) if mono else 'mixed',
                         items_label_dev=bool(mono and (B.ITEM[triple[0]] in ('SH', 'PAIR', 'PAIRU') or B.ITEM[triple[1]] in ('SH', 'PAIR', 'PAIRU')))))
    return rows, int(sg)


def summarize_cell(key, params, runs_rows, stops):
    allr = [r for rows in runs_rows for r in rows]
    n = len(allr)
    fx = [r for r in allr if r['fixed']]
    fz = [r for r in allr if r['frozen']]
    # without migration the end state is monomorphic islands (censored = not fixed); with migration the run ends at global payoff-freezing
    # (censored = not payoff-frozen); both shares are reported
    cens = (1 - len(fx) / n) if params['mN'] == 0 else (1 - len(fz) / n)
    out = dict(key=key, params=params, n_runs=len(runs_rows), n_islands=n, n_fixed=len(fx), n_frozen=len(fz), frozen_share=len(fz) / n, fixed_share=len(fx) / n,
               censored_share=cens, stop_gen_median=float(np.median(stops)))
    cls = Counter(r['cls'] for r in allr)
    out['class_share'] = {k: cls.get(k, 0) / n for k in ('pair', 'items_dev', 'p_dev', 'truthful', 'mixed')}
    out['class_share_fixed_only'] = {k: sum(1 for r in fx if r['cls'] == k) / max(1, len(fx)) for k in ('pair', 'items_dev', 'p_dev', 'truthful', 'mixed')}
    out['pair_enforced_share'] = sum(r['pair_enf'] for r in allr) / n
    out['pair_unenforced_share'] = sum(r['pair_unenf'] for r in allr) / n
    out['policed_share'] = sum(r['policed'] for r in allr) / n
    out['policed_and_pair'] = sum(r['policed'] and r['cls'] == 'pair' for r in allr) / n
    out['items_dev_behaviour_share'] = sum(r['items_dev'] for r in allr) / n
    out['items_label_dev_share'] = sum(r['items_label_dev'] for r in allr) / n
    pol = [r for r in allr if r['policed']]
    out['n_policed'] = len(pol)
    out['policed_tested_after_fix'] = (sum(r['tested'] for r in pol) / len(pol)) if pol else None
    out['policed_never_tested'] = (1 - out['policed_tested_after_fix']) if pol else None
    founded = [r for r in allr if r['pol_founded'] and (r['pair_founded'] or r['pairu_founded'])]
    out['n_pol_and_pair_founded'] = len(founded)
    out['founding_exposure_share'] = len(founded) / n
    out['pair_driven_out_share'] = (sum(r['cls'] != 'pair' for r in founded) / len(founded)) if founded else None
    bins = [(0, 0.1), (0.1, 0.2), (0.2, 0.3), (0.3, 0.4), (0.4, 1.01)]
    byb = {}
    for lo, hi in bins:
        sub = [r for r in founded if lo <= r['pol_init'] / params['N'] < hi]
        byb['%.1f-%.1f' % (lo, min(hi, 1.0))] = dict(n=len(sub), driven_out=(sum(r['cls'] != 'pair' for r in sub) / len(sub)) if sub else None,
                                                     policed=(sum(r['policed'] for r in sub) / len(sub)) if sub else None)
    out['driven_out_by_pol_init_share'] = byb
    out['pair_joint_zero_share'] = (sum(r['joint'] < 1e-12 for r in founded) / len(founded)) if founded else None
    out['mean_eff'] = float(np.mean([r['eff'] for r in allr])); out['mean_rev'] = float(np.mean([r['rev'] for r in allr]))
    out['mean_uA'] = float(np.mean([r['uA'] for r in allr])); out['mean_uB'] = float(np.mean([r['uB'] for r in allr])); out['mean_uP'] = float(np.mean([r['uP'] for r in allr]))
    out['mean_rev_by_class'] = {k: float(np.mean([r['rev'] for r in allr if r['cls'] == k])) for k in cls}
    out['fixed_gen_quantiles'] = [float(np.quantile([r['fixed_gen'] for r in fx], q)) for q in (0.1, 0.5, 0.9)] if fx else None
    out['frozen_gen_median'] = float(np.median([r['frozen_gen'] for r in allr if r['frozen']])) if any(r['frozen'] for r in allr) else None
    tr = Counter(r['triple'] for r in allr)
    out['triples'] = dict(tr.most_common(40))
    out['pol_in_P_share'] = None
    # run-level spread of the main shares
    out['run_sd'] = {'pair': float(np.std([np.mean([r['cls'] == 'pair' for r in rows]) for rows in runs_rows])),
                     'policed': float(np.std([np.mean([r['policed'] for r in rows]) for rows in runs_rows])),
                     'items_dev': float(np.std([np.mean([r['items_dev'] for r in rows]) for rows in runs_rows]))}
    out['run_pair_shares'] = [float(np.mean([r['cls'] == 'pair' for r in rows])) for rows in runs_rows]
    out['run_rev_means'] = [float(np.mean([r['rev'] for r in rows])) for rows in runs_rows]
    return out


def run_cell(rule, inst, prior, audit, N, mN, nopol, runs, force=False):
    key = cell_key(rule, inst, prior, audit, N, mN, nopol)
    path = os.path.join(CELLS, key + '.json')
    if os.path.exists(path) and not force:
        return key, json.load(open(path))
    t0 = time.time()
    rows_all = []; stops = []
    for run in range(runs):
        rows, sg = run_once(rule, inst, prior, audit, N, mN, nopol, run)
        rows_all.append(rows); stops.append(sg)
    params = dict(rule=rule, inst=inst, prior=prior, audit=audit, N=N, mN=mN, noPOL=nopol, runs=runs, I=I_DEF, w=B.W, gens=GENS if mN == 0 else GENS_MIG)
    out = summarize_cell(key, params, rows_all, stops)
    out['seconds'] = time.time() - t0
    save(path, out)
    return key, out


def cell_list(which):
    cells = []
    if which == 'primary':
        for prior in PRIORS:
            for inst in ('collusion', 'threshold'):
                for rule in ('vcg', 'surcharge', 'fp'):
                    for audit in (False, True):
                        cells.append((rule, inst, prior, audit, 100, 0, False))
    elif which == 'nopol':
        for inst in ('collusion', 'threshold'):
            for rule in ('vcg', 'surcharge', 'fp'):
                cells.append((rule, inst, 'U', False, 100, 0, True))
    elif which == 'nsweep':
        for N in (50, 200):
            for rule, inst in (('vcg', 'collusion'), ('vcg', 'threshold'), ('surcharge', 'threshold')):
                cells.append((rule, inst, 'U', False, N, 0, False))
        for N in (50, 200):
            cells.append(('vcg', 'collusion', 'U', False, N, 0, True))
    elif which == 'mig':
        for rule in ('vcg', 'surcharge', 'fp'):
            for inst in ('collusion', 'threshold'):
                cells.append((rule, inst, 'U', False, 100, 1, False))
        cells.append(('vcg', 'collusion', 'U', False, 100, 1, True))
    return cells


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd')
    ap.add_argument('--set', default='primary')
    ap.add_argument('--runs', type=int, default=40)
    ap.add_argument('--force', action='store_true')
    a = ap.parse_args()
    if a.cmd == 'static':
        res = B.static_report()
        save(os.path.join(OUT, 'partB_static.json'), res)
        print('static done')
    elif a.cmd == 'guard':
        t = time.time(); run_once('vcg', 'collusion', 'U', False, 100, 0, False, 0); print('one run %.1fs' % (time.time() - t))
        t = time.time(); run_once('vcg', 'collusion', 'U', False, 100, 1, False, 0); print('one migration run %.1fs' % (time.time() - t))
    elif a.cmd == 'cells':
        cl = cell_list(a.set)
        for i, (rule, inst, prior, audit, N, mN, nopol) in enumerate(cl):
            t = time.time()
            key, out = run_cell(rule, inst, prior, audit, N, mN, nopol, a.runs, a.force)
            print('%d/%d %s  pair %.3f policed %.3f items_dev %.3f truthful %.3f cens %.3f  %.0fs' % (
                i + 1, len(cl), key, out['class_share']['pair'], out['policed_share'], out['items_dev_behaviour_share'], out['class_share']['truthful'],
                out['censored_share'], time.time() - t), flush=True)


if __name__ == '__main__':
    main()
