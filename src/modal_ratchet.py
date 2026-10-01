"""E2: ratchet test.  Full modal arm, n = 8, w = 0.3, eps->0 chain at large N,
with eager_poly=False (verified to reproduce the finished n = 8 cells exactly)
and a theta-sensitivity repeat at theta = 1e-7.

    python3 src/modal_ratchet.py
Writes runs/modal_ratchet.md/json (finished n = 8 cells from runs/modal_limN.json included for context).
"""
import json, os, sys
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(__file__))
import modal as M
from modal_limN import cell, ROOT


def _job(j):
    N, theta = j
    return cell(8, N, 0.3, M.build(8), eager_poly=False, theta=theta)


def main():
    jobs = [(N, th) for N in (100000, 300000) for th in (1e-6, 1e-7)]
    with Pool(4) as pool:
        rows = pool.map(_job, jobs)
    json.dump(rows, open(os.path.join(ROOT, 'runs', 'modal_ratchet.json'), 'w'), indent=1, default=str)
    old = [r for r in json.load(open(os.path.join(ROOT, 'runs', 'modal_limN.json'))) if r['n'] == 8 and r['w'] == 0.3]
    L = ['# E2 ratchet: full modal arm n = 8, w = 0.3, eps->0 chain', '',
         '| N | theta | P(C,C) | π(all-D) | π(FairBot) | π(PrudentBot) | π(PB)/π(FB) | cut flow | time (s) |', '|---|---|---|---|---|---|---|---|---|']
    for r in sorted(old, key=lambda r: r['N']) + sorted(rows, key=lambda r: (r['N'], -r['chain_kw'].get('theta', 1e-6))):
        L.append('| %d | %s | %.4f | %.4f | %.4f | %.5f | %.4f | %.1e | %.0f |' % (r['N'], r.get('chain_kw', {}).get('theta', '1e-06 (earlier run)'), r['pcc'], r['pi_D'], r['pi_FB'], r['pi_PB'], r['pi_PB'] / r['pi_FB'], r['cut_flow'], r['time_s']))
    open(os.path.join(ROOT, 'runs', 'modal_ratchet.md'), 'w').write('\n'.join(L) + '\n'); print('\n'.join(L))


if __name__ == '__main__':
    main()
