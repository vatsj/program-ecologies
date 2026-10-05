"""Driver for the union game's agent-based runs (I = 1) and spatial selection on
bosses (I = 16).  Finite eps N: approach rates, not pi.

    python3 src/union_abm_run.py abm --c 0.5 --start low --seed 0 --gens 100000
    python3 src/union_abm_run.py islands --c 0.5 --wg 0 10 0 --seed 0 --gens 20000
Writes runs/union/abm_*.json / islands_*.json.
"""
import argparse, json, os, sys, time
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import union as U
import union_abm as A
from union_run import load, OUT

PH = U.SUMM + ['mixed']


def setup(arm='quorum'):
    d, C, nmw, nmb = load(arm)
    Km = max(C['KcB'], C['KcW'])
    cdfs = np.ones((3, Km))
    for s in range(3):
        m = C['massB'] if s == 0 else C['massW']
        cd = np.cumsum(m) / m.sum()
        cdfs[s, :len(cd)] = cd
    return d, C, nmw, nmb, cdfs


def phases(C, dom):
    """dom (nrec, 3) -> phase index per record (summary of the majority triple, or 7 = mixed)."""
    out = np.full(len(dom), 7, np.int64)
    for r, (b, x, y) in enumerate(dom):
        if b >= 0 and x >= 0 and y >= 0:
            out[r] = U.summary(int(C['Jc'][b, x, y]), int(C['tagc'][x]), int(C['tagc'][y]))
    return out


def runs_of(ph, every):
    """Maximal runs of equal phase: list of (phase, length in generations)."""
    out = []; start = 0
    for k in range(1, len(ph) + 1):
        if k == len(ph) or ph[k] != ph[start]:
            out.append((int(ph[start]), (k - start) * every)); start = k
    return out


def main(a):
    d, C, nmw, nmb, cdfs = setup()
    SUMM, WAGE, WHK = A.tables()
    PAY = U.payoff_table(a.c)
    starts = dict(low=(nmb['(0,none)'], nmw['scab'], nmw['scab']), fair=(nmb['(1/2,none)'], nmw['union'], nmw['union']))
    I = 1 if a.what == 'abm' else a.I
    init = np.array([starts[a.start]] * I, np.int64)
    wg = np.array(a.wg if a.what == 'islands' else [0.0, 0.0, 0.0], float)
    eps = a.epsN / a.N
    t = time.time()
    r_sum, r_sw, r_pay, r_dom, overflow = A.run(C['Jc'], C['tagc'].astype(np.int64), PAY, SUMM, WAGE, WHK, cdfs, init, I, a.N, a.w, eps,
                                                a.mN, wg, a.gens, a.every, a.seed)
    el = time.time() - t
    res = dict(what=a.what, c=a.c, start=a.start, seed=a.seed, N=a.N, I=I, epsN=a.epsN, mN=a.mN, wg=wg.tolist(), w=a.w, gens=a.gens,
               every=a.every, time_s=el, overflow=int(overflow))
    res['summary_mean'] = dict(zip(U.SUMM, r_sum.mean(axis=(0, 1)).tolist()))
    h = r_sum.shape[0] // 2
    res['summary_2nd_half'] = dict(zip(U.SUMM, r_sum[h:].mean(axis=(0, 1)).tolist()))
    sw = r_sw.mean(axis=(0, 1))
    res['wage_whack_mean'] = {'s=%s,%s' % (U.WNAME[k // 3], U.HNAME[k % 3]): float(sw[k]) for k in range(9)}
    res['pay_mean'] = dict(zip(['boss', 'W1', 'W2'], r_pay.mean(axis=(0, 1)).tolist()))
    res['efficiency'] = float(r_pay.sum(2).mean())
    # phases per island
    ph_all = []; first_fair = []; dw = {p: [] for p in PH}
    for i in range(I):
        ph = phases(C, r_dom[:, i])
        ph_all.append(ph)
        ff = np.nonzero(ph == 0)[0]
        first_fair.append(int((ff[0] + 1) * a.every) if len(ff) else None)
        for p, L in runs_of(ph, a.every)[:-1]:          # drop the censored last run
            dw[PH[p]].append(L)
    ph_all = np.array(ph_all)
    res['phase_share'] = {PH[p]: float((ph_all == p).mean()) for p in range(8)}
    res['first_fair_gen'] = first_fair
    res['dwell_gens'] = {p: dict(n=len(v), mean=float(np.mean(v)), median=float(np.median(v))) for p, v in dw.items() if v}
    if I == 1:
        # coarse time series: summary shares per 1,000 generations
        k = max(1, 1000 // a.every)
        ts = r_sum[:, 0].reshape(-1, k, 7).mean(1)
        res['series_per_1000'] = np.round(ts, 3).tolist()
        res['phase_series'] = ''.join('FIZSKRQm'[p] for p in ph_all[0][::k])
        # dominant classes visited (most frequent majority triples)
        from collections import Counter
        cnt = Counter(tuple(x) for x in r_dom[:, 0].tolist())
        res['top_majority_triples'] = [dict(frac=n / len(r_dom), state=('%s | %s | %s' % (
            d['P'].src_b(C['repB'][t_[0]]) if t_[0] >= 0 else '-', d['P'].src_w(C['repW'][t_[1]]) if t_[1] >= 0 else '-',
            d['P'].src_w(C['repW'][t_[2]]) if t_[2] >= 0 else '-'))) for t_, n in cnt.most_common(8)]
    else:
        res['island_summary_mean'] = np.round(r_sum[h:].mean(0), 3).tolist()
        res['island_wage_whack_2nd_half'] = np.round(r_sw[h:].mean(0), 3).tolist()
        k = max(1, r_sum.shape[0] // 50)
        res['series'] = np.round(r_sum.mean(1)[: (r_sum.shape[0] // k) * k].reshape(-1, k, 7).mean(1), 3).tolist()
    tag = '%s_c%g_%s_s%d' % (a.what, a.c, a.start, a.seed)
    if a.what == 'islands':
        tag += '_wg%s' % '-'.join('%g' % v for v in wg)
    json.dump(res, open(os.path.join(OUT, tag + '.json'), 'w'), indent=1, default=float)
    print(tag, 'time %.0fs' % el, {k: round(v, 3) for k, v in res['summary_mean'].items()}, flush=True)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('what', choices=['abm', 'islands'])
    ap.add_argument('--c', type=float, default=0.5)
    ap.add_argument('--start', default='low', choices=['low', 'fair'])
    ap.add_argument('--seed', type=int, default=0)
    ap.add_argument('--N', type=int, default=100)
    ap.add_argument('--I', type=int, default=16)
    ap.add_argument('--epsN', type=float, default=0.1)
    ap.add_argument('--mN', type=float, default=1.0)
    ap.add_argument('--wg', type=float, nargs=3, default=[0.0, 0.0, 0.0])
    ap.add_argument('--w', type=float, default=0.3)
    ap.add_argument('--gens', type=int, default=100000)
    ap.add_argument('--every', type=int, default=10)
    main(ap.parse_args())
