"""eps = 0 island absorption lottery vs island count (iid program seeding).

    python3 src/islands_count.py
Writes runs/islands_count.md/json.
"""
import argparse, json, os, sys
import numpy as np
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(__file__))
from islands import run_one, _load, ROOT


def family(r):
    if r['frozen_at'] >= 0:
        if r['pcc_final'] > 1 - 1e-9: return 'coop'
        if r['pcc_final'] < 1e-9 and abs(r['pay_final'] + 1) < 1e-9: return 'defect'
        return 'other'
    # live: classify by final global state
    if r['pcc_final'] > 0.9: return 'live-coop'
    if r['pcc_final'] < 0.1 and r['pay_final'] < -0.9: return 'live-defect'
    return 'live-other'


def main(a):
    reps = dict(zip(a.Is, a.reps))
    jobs = [('pd', False, 'complete', mN, 'iid', r, I, a.N, a.w, a.gens, 20) for I in a.Is for mN in a.mN for r in range(reps[I])]
    jobs.sort(key=lambda j: -j[6])
    _load('pd', False)
    rows = []
    with Pool(a.procs) as pool:
        for r in pool.imap_unordered(run_one, jobs):
            for k in ('trace_pay', 'trace_R', 'trace_C', 'trans', 'spread_pay_pairs', 'dom_time', 'isl_cc_hist', 'isl_dwl_hist', 'trace_cc'):
                r.pop(k, None)
            r['family'] = family(r)
            rows.append(r)
            print('I=%d mN=%g rep %d: %s frozen %d P(C,C) %.3f (%.0fs)' % (r['I'], r['mN'], r['rep'], r['family'], r['frozen_at'], r['pcc_final'], r['time_s']), flush=True)
    json.dump(rows, open(os.path.join(ROOT, 'runs', 'islands_count.json'), 'w'), indent=1)
    fams = ['coop', 'defect', 'other', 'live-coop', 'live-defect', 'live-other']
    L = ['# eps = 0 islands vs island count (PD, complete graph, N = %d, w = %g, iid program seeding, horizon %d generations)' % (a.N, a.w, a.gens), '',
         '| I | mN | runs | ' + ' | '.join(fams) + ' | median freeze gen | mean final P(C,C) |', '|' + '---|' * (len(fams) + 5)]
    for I in a.Is:
        for mN in a.mN:
            s = [r for r in rows if r['I'] == I and r['mN'] == mN]
            fr = [r['frozen_at'] for r in s if r['frozen_at'] >= 0]
            L.append('| %d | %g | %d | %s | %s | %.3f |' % (I, mN, len(s), ' | '.join('%.2f' % (sum(r['family'] == f for r in s) / len(s)) for f in fams),
                     '%d' % np.median(fr) if fr else '-', np.mean([r['pcc_final'] for r in s])))
    open(os.path.join(ROOT, 'runs', 'islands_count.md'), 'w').write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--Is', type=int, nargs='+', default=[16, 64, 256, 1024])
    ap.add_argument('--reps', type=int, nargs='+', default=[100, 100, 40, 10])
    ap.add_argument('--mN', type=float, nargs='+', default=[0.1, 1.0])
    ap.add_argument('--N', type=int, default=100)
    ap.add_argument('--w', type=float, default=0.3)
    ap.add_argument('--gens', type=int, default=20000)
    ap.add_argument('--procs', type=int, default=9)
    main(ap.parse_args())
